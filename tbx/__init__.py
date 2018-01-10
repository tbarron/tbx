"""
Toolbox
"""
import contextlib
import os
import re
import shlex
try:
    import StringIO as io
except ImportError:
    import io
    file = io.TextIOWrapper
import subprocess as sproc
import sys


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def chdir(directory):
    """
    Context-based directory excursion

    When the with statement ends, you're back where you started.
    """
    origin = os.getcwd()
    try:
        os.chdir(directory)
        yield

    finally:
        os.chdir(origin)


# -----------------------------------------------------------------------------
def contents(name=None, default=None, fmt='str', sep=None):
    """
    Return the contents
    """
    try:
        rbl = open(name, 'r')
        data = rbl.read()
    except IOError as err:
        if 'Permission denied' in str(err):
            raise Error("Can't read file {0}".format(name))
        elif 'No such file' in str(err) and default:
            data = default
        else:
            raise
    if fmt == 'list' or fmt == list:
        sep = sep or '\n'
        rval = re.split(sep, data)
    elif fmt == 'str' or fmt == str:
        if sep:
            raise Error('Non-default separator is only valid for list format')
        rval = data
    else:
        raise Error('Invalid format')
    return rval


# -----------------------------------------------------------------------------
def dirname(path, level=None):
    """
    Peel off *level* tails from path
    """
    if level is None:
        level = 1
    rval = path
    for _ in range(0, level):
        rval = os.path.dirname(rval)
    return rval


# -----------------------------------------------------------------------------
def dispatch(mname='__main__', prefix=None, args=None):
    """
    Call a subfunction from module *mname* based on *prefix* and *args*
    """
    if prefix is None:
        sys.exit('*prefix* is required')
    args = args or ('',)
    try:
        subcmd = args[0]
    except IndexError:
        dispatch_help(mname, prefix, args)
        return

    if subcmd in ['help', '-h', '--help']:
        dispatch_help(mname, prefix, args)
        return

    try:
        func_name = "_".join([prefix, subcmd])
        func = getattr(sys.modules[mname], func_name)
        func(*tuple(args[1:]))
    except AttributeError:
        fatal("Module {0} has no function {1}".format(mname, func_name))


# -----------------------------------------------------------------------------
def dispatch_help(mname='__main__', prefix=None, args=None):
    """
    Standard help function for dispatch-based tool programs
    """
    if prefix is None:
        sys.exit('*prefix* is required')
    try:
        mod = sys.modules[mname]
    except KeyError:
        sys.exit('Module {0} is not in sys.modules'.format(mname))

    args = args or []
    if len(args) < 1:
        prefix += '_'
        print("help - show a list of available commands")
        for item in dir(mod):
            if item.startswith(prefix):
                func = getattr(mod, item)
                docsum = func.__doc__.split('\n')[0]
                print(docsum)
    else:
        while 0 < len(args):
            topic = args.pop(0)
            if topic == 'help':
                print("\n".join(["help - show a list of available commands",
                                 "",
                                 "   With no arguments, show a list of "
                                 "commands",
                                 "   With a command as argument, show help"
                                 " for that command",
                                 ""
                                 ]))
            else:
                funcname = '_'.join([prefix, topic])
                try:
                    func = getattr(mod, funcname)
                except AttributeError:
                    sys.exit('Module {0} has no attribute {1}'
                             ''.format(mname, funcname))
                if func.__doc__:
                    print(func.__doc__)
                else:
                    sys.exit('Function {0} is missing a __doc__ string'
                             ''.format(funcname))


@contextlib.contextmanager
# -----------------------------------------------------------------------------
def envset(**kwargs):
    """
    Set environment variables that will last for the duration of the with
    statement.

    To unset a variable temporarily, pass its value as None.
    """
    prev = {}
    try:
        # record the original values
        for name in kwargs:
            prev[name] = os.getenv(name)

        # set the new values
        for name in kwargs:
            if kwargs[name] is None:
                if name in os.environ:
                    del os.environ[name]
            else:
                os.environ[name] = kwargs[name]

        yield

    finally:
        for name in kwargs:
            if prev[name] is not None:
                os.environ[name] = prev[name]
            elif os.getenv(name) is not None:
                del os.environ[name]


# -----------------------------------------------------------------------------
def expand(path):
    """
    Return path with any '~' or env vars expanded.
    """
    return expanduser(os.path.expandvars(path))


# -----------------------------------------------------------------------------
def expanduser(instr):
    """
    Expand '~' to the contents of $HOME
    """
    hval = os.getenv("HOME") or ""
    rval = re.sub("~", hval, instr)
    return rval


# -----------------------------------------------------------------------------
def fatal(msg='Fatal error with no reason specified'):
    """
    The default value is okay because strings in python are immutable
    """
    sys.exit(msg)


# -----------------------------------------------------------------------------
def revnumerate(sequence):
    """
    Enumerate *sequence* in reverse
    """
    idx = len(sequence) - 1
    for item in reversed(sequence):
        yield idx, item
        idx -= 1


# -----------------------------------------------------------------------------
def run(cmd, input=None, output=None):
    """
    Run *cmd* in a separate process. Return stdout + stderr.
    """
    posarg = shlex.split(str(cmd))
    kwa = {'stdin': sproc.PIPE,
           'stdout': sproc.PIPE,
           'stderr': sproc.STDOUT}

    if isinstance(input, io.StringIO):
        input = input.getvalue()
    elif isinstance(input, str):
        if input.strip().startswith('<'):
            kwa['stdin'] = open(input.strip()[1:].strip())
            input = None
        elif input.strip().endswith('|'):
            scmd = input.strip()[:-1].strip()
            input = run(scmd)
    elif isinstance(input, int):
        kwa['stdin'] = input
        input = None
    elif isinstance(input, file):
        kwa['stdin'] = input
        input = None

    if isinstance(output, str):
        if output.strip().startswith('>'):
            kwa['stdout'] = open(output.strip()[1:].strip(), 'w')
        elif output.strip().startswith('|'):
            pass
        else:
            raise Error('| or > required for string output')
    elif isinstance(output, file):
        kwa['stdout'] = output
    elif isinstance(output, int):
        kwa['stdout'] = output

    child = sproc.Popen(posarg, **kwa)
    if isinstance(input, bytes):
        (out, _) = child.communicate(input)
    elif isinstance(input, str):
        (out, _) = child.communicate(bytes(input, 'utf8'))
    else:
        (out, _) = child.communicate()

    if isinstance(output, io.StringIO):
        output.write(str(out))
        out = None
    elif isinstance(output, file):
        out = None
    elif isinstance(output, int):
        out = None
    elif isinstance(output, str) and output.strip().startswith('|'):
        cmd = output.strip()[1:].strip()
        out = run(cmd, input=out)

    return out


# -----------------------------------------------------------------------------
class Error(Exception):
    """
    Errors raised in this file
    """
    pass
