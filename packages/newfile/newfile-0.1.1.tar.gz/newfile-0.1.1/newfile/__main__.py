import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from inspect import signature

import yaml
import click

import jinja2
from jinja2 import Environment, FunctionLoader, select_autoescape

from rich.console import Console
from rich.traceback import install
from rich import inspect
console = Console()
install(show_locals=True,suppress=[jinja2,click])
print = console.print

def main():
    newfile()

#PART: util

def findup(dest,dir='.'):
    if type(dest) not in (list,tuple):
        dest = [dest]
    
    p = Path(dir).absolute()
    res = None
    for i in dest:
        r = p.joinpath(i)
        if r.exists():
            res = r.absolute()
            break

    if not res and  str(p) != p.root:
        res = findup(dest,p.parent)

    return res


def show_path(p,mode):
    p = Path(p)
    if p.is_absolute():
        p = str(p)
        cwd = str(Path.cwd()) 
        git = GITDIR 
        home = HOMEDIR
        for k,v in {
            str(Path.cwd()):'.',
            str(GITDIR): '◆',
            str(HOMEDIR): '~'
        }.items():
            if len(p) < len(k):
                continue
            prefix = p[:len(k)]
            if prefix == k:
                p = v+p[len(prefix):]
                break
        
    title = {
            'r':'[blue]load',
            'w':'[yellow]write',
            'x':'[green]create',
            'a':'[green]append',
    }.get(mode,f'[magenta]{mode}')
    print(f'[bold]{title}[/bold]\t{p}')

#PART: init

HOMEDIR = Path.home()
GITDIR =  (findup('.git') or Path('./x').absolute()).parent

template_catch = {}
def load_template(name):
    if not name:
        return ""
    source = ''
    if name in template_catch:
        return template_catch[name]['source']

    p = findup([
        f'newfile_templates/{name}.jinja',
        f'newfile_templates/{name}',
    ])

    if not p:
        for i in [
        f'{GITDIR}/newfile_templates/{name}.jinja',
        f'{GITDIR}/newfile_templates/{name}',
        f'{HOMEDIR}/newfile_templates/{name}.jinja',
        f'{HOMEDIR}/newfile_templates/{name}',
        f'{HOMEDIR}/.vim/bundle/vim-snippets/newfile_templates/{name}.jinja',
        f'{HOMEDIR}/.vim/bundle/vim-snippets/newfile_templates/{name}',
        ]:
            _p = Path(i)
            if _p.exists():
                p = _p
                break
        if not p:
            raise FileNotFoundError(f"Template not found: '{name}'")

    p = str(p)
    show_path(p,'r')
    with open(p) as f:
        source = f.read()

    data = {
        'name':name,
        'path':p,
        'setup':'{}',
        'param':{},
        'source': source
    }
    preprocess_template(data)
    template_catch[name] = data
    return data['source']

tlenv = Environment(
loader = FunctionLoader(load_template),
autoescape = select_autoescape(),
undefined=jinja2.DebugUndefined,
finalize=lambda s: s not in [None,False] and str(s) or ''
)
tlctx = {
    'args':[],
    'opts':{},
    'state':{},
    'env':tlenv,
}

tlenv.globals['_tl_'] = tlctx
tlenv.globals['args'] = tlctx['args']
tlenv.globals['opts'] = tlctx['opts']
tlenv.globals['now'] = datetime.now().ctime()

def tlfilter(func,g=False):
    name = func.__name__
    if len(name) > 2 and name[0:2] == 'tl':
        name = name[2:]
    tlenv.filters[name] = func
    if g:
        tlenv.globals[name] = func
    return func

def tlfunc(func):
    return tlfilter(func,True)


@tlfunc
def set_state(value,name):
    console.print('set_state: ',(name,value))
    tlctx['state'][name] = value
    return ''

@tlfilter
def tlsignature(func):
    try:
        return signature(func)
    except:
        return str(func)

@tlfilter
def tlinspect(obj):
    inspect(obj)
    return ''
tlfilter(str)

#PART: pre/post process

def preprocess_template(data): 
    s = data['source']
    if re.match(r'\s*===+\n',s):
        s = re.split('\n===+\n',s.lstrip(" =\t\r\n"),1)
        data['source'] = s[1]
        head = {
            'param':[],
            'setup':[],
        }
        last = 'param'
        for i in s[0].split('\n'):
            if i and i[0] == ' ':
                head[last].append(i)
            elif i and i[0] == '-':
                head['param'].append(i)
                last = 'param'
            else:
                head['setup'].append(i)
                last = 'setup'
                
        data['setup'] = '\n'.join(head['setup'])
        param = head['param']
        param = '\n'.join(param)
        param = inline_render(param)
        param = yaml.load(param)
        if type(param) == dict:
            for l,r in param.items():
                preprocess_param (l,r,data)


param_defined = set()
def preprocess_param(left,right,data):
    args = []
    kwargs = argparse.Namespace()

    for i in left.split(','):
        i = i.strip()
        if len(i) == 0:
            continue
        if i[0] == '-':
            args.append(i)
            param_defined.add(i)
        else:
            kwargs.help = i
    t = type(right)
    if t in [int,float]:
        k.type = int
    elif t == list:
        kwargs.type = str
        kwargs.action = 'append'

    elif right == False:
        kwargs.action = 'store_true'
    elif right == True:
        kwargs.action = 'store_false'
    else:
        kwargs.type = str
    
    kwargs.default = right

    if kwargs.default == None:
        kwargs.default = ''

    try:
        tlctx['parser'].add_argument(*args,**vars(kwargs))
    except argparse.ArgumentError as e:
        pass

def post_args(args,opts):
    param = []
    for arg in args:
        if arg and arg[0] == '-':
            a = arg.split('=',1)
            k = a[0].lstrip('-').replace('-','_')
            if len(a) == 2:
                opts[k] = a[1]
            else:
                opts[k] = True
        else:
            param.append(arg)
    
    return param


def pull_args():
    parser :argparse.ArgumentParser = tlctx['parser']
    (opts,args) = parser.parse_known_args(tlctx['argv'])
    opts = vars(opts)
    params = post_args(args,opts)
    tlctx['args'] = params
    tlctx['opts'] = opts
    tlenv.globals['args'] = params
    for i in tlctx['opts']:
        s = tlctx['opts'][i]
        tlenv.globals[i] = tlctx['opts'][i]


def inline_render(text):
    if type(text) == str:
        tl = tlenv.from_string(text)
        return tl.render()
    elif type(text) == dict:
        for i in text:
            text[i] = inline_render(text[i])
    elif type(text) == list:
        for i in range(len(text)):
            text[i] = inline_render(text[i])
    
    return text


#PART: entry

tlargparser = argparse.ArgumentParser(
    add_help=False,
    allow_abbrev=False
)

def entry(template,args,output=None):
    tlctx['parser'] = tlargparser
    tlctx['argv'] = args
    
    load_template(template)
    setup = template_catch[template]['setup']

    @tlfunc
    def tlsetup(v,k=None):
        if k:
            setup[k] = v
            return ''
        return setup[k]

    tlhandle = tlenv.get_template(template)

    tlargparser.parse_known_args(args)

    # pre-process
    pull_args()
    tlhandle.render()
    try:
      tlargparser.add_argument(
        '--help',
        *{'-h'}-param_defined,'-?',
        action='store_true',
        default=False,
        help='display help of template'
      )
      tlargparser.add_argument(
        '--force',
        *{'-f'}-param_defined,
        action='store_true',
        default=False,
        help='force overwrite output file'
      )
    except argparse.ArgumentError:
        pass

    pull_args()

    setup = inline_render(setup)
    setup = yaml.load(setup)
    if type(setup) != dict:
        setup = {}

    opts = tlctx['opts']
    if opts['help']:
        tlargparser.print_help()
        return
    
    output = output or setup.get('output',template)

    rendered = tlhandle.render(
        FILENAME=output,
    )

    mode = setup.get('force',opts['force']) and 'w' or 'x'
    with open(output,mode) as f:
        f.write(rendered)
        show_path(output,mode)

    for i,o in setup.get('relate',{}).items():
        entry(i,args,o)

@click.command(context_settings={
#'ignore_unknown_options':True,
'allow_interspersed_args':False,
'allow_extra_args':True
})
@click.argument('template')
@click.argument('args',nargs=-1)
def newfile(template,args,**opts):
    entry(template,args)
    
    


if '__main__' == __name__:
    try:
        main()
    except FileNotFoundError as e:  
        print(e)
        sys.exit(1)
    except FileExistsError as e:
        print(e)
        print('Hint: overwrite file with flag --force')
        sys.exit(1)
