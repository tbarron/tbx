"""
Toolbox

This is free and unencumbered software released into the public domain.
For more information, please refer to <http://unlicense.org/>
"""
import contextlib
import glob
from importlib import import_module
import inspect
import os
import os.path as osp
import pdb
import random
import re
import shlex
try:
    import StringIO as io
except ImportError:
    import io
    file = io.TextIOWrapper
import subprocess as sproc
import sys
from tbx import verinfo


# -----------------------------------------------------------------------------
def abspath(relpath):
    """
    Returns the absolute path of *relpath*
    """
    return osp.abspath(relpath)


# -----------------------------------------------------------------------------
def basename(path, segments=None):
    """
    Returns the basename of *path*
    """
    if segments is None:
        segs = 1
    else:
        segs = segments
    pcomps = [_ for _ in path.split('/') if _ != '']
    if 0 == segs:
        rval = ''
    elif 1 < len(pcomps):
        rval = osp.join(*pcomps[-segs:])
    elif 1 == len(pcomps):
        rval = pcomps[0]
    else:
        rval = ''
    return rval


# -----------------------------------------------------------------------------
def caller_name():
    """
    Return the name of the caller of the caller
    """
    return inspect.stack()[2].function


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
def conditional_debug(**kw):
    """
    If kw['d'] is True, start the debugger
    """
    if kw['d']:
        pdb.set_trace()


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
def dirname(path, segments=None, level=None):
    """
    Peel off *segments* tails from path. Argument level is DEPRECATED but will
    continue to be supported for a few releases for backward compatibility.
    """
    if segments is None and level is None:
        segs = 1
    elif segments is None and level is not None:
        segs = level
    elif segments is not None:
        segs = segments

    rval = path
    for _ in range(0, segs):
        rval = osp.dirname(rval)
    return rval


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
def exists(path):
    """
    Return True if *path* exists, else False
    """
    return osp.exists(path)


# -----------------------------------------------------------------------------
def expand(path):
    """
    Return path with any '~' or env vars expanded.
    """
    return _expanduser(osp.expandvars(path))


# -----------------------------------------------------------------------------
def _expanduser(instr):
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
def git_last_tag():
    """
    Return the most recently defined tag
    """
    result = run("git --no-pager tag")
    tag_l = result.strip().split("\n")
    rval = tag_l[-1] if 0 < len(tag_l) else ""
    return rval


# -----------------------------------------------------------------------------
def git_hash(ref=None):
    """
    Return a hash -- of HEAD if *ref* == None, of whatever *ref* points to if
    specified
    """
    cmd = "git --no-pager log -1 --format=format:\"%H\""
    if ref:
        cmd += " {}".format(ref)
    result = run(cmd)
    return result


# -----------------------------------------------------------------------------
def git_current_branch():
    """
    Run 'git branch' and return the one marked with a '*'
    """
    curb = run("git symbolic-ref --short HEAD")
    curb = curb.strip()
    return curb


# -----------------------------------------------------------------------------
def git_status():
    """
    Run 'git status --porc' and return: 1) a list of untracked files, 2) a list
    of unstaged updates, and 3) a list of staged but uncommitted updates.
    """
    subx = r"^[AM? ][AM? ]\s"
    mstgx = r"^[AM].\s"
    mchgx = r"^.[AM]\s"
    utrkx = r"^\?\?"
    result = run("git status --porc").rstrip()
    staged = [re.sub(subx, "", x) for x in result.split("\n")
              if re.match(mstgx, x)]
    unstaged = [re.sub(subx, "", x) for x in result.split("\n")
                if re.match(mchgx, x)]
    untracked = [re.sub(subx, "", x) for x in result.split("\n")
                 if re.match(utrkx, x)]
    return(staged, unstaged, untracked)


# -----------------------------------------------------------------------------
def lglob(*args, dupl_allowed=False):
    """
    glob a list of paths and return the results in a single list
    """
    rval = []
    [rval.extend(y) for y in [glob.glob(x) for x in args]]
    if not dupl_allowed:
        rval = list(set(rval))
    return rval


# -----------------------------------------------------------------------------
def collect_missing_docs(treeroot):
    """
    In a tree, find all python files and scan each for functions/methods with
    no doc string
    """
    importables = []
    prefix = treeroot + "/"
    for dp, dl, fl in os.walk(treeroot):
        del_these = []
        for dname in dl:
            if any([dname.startswith('venv'),
                    dname.startswith('.'),
                    dname == '__pycache__',
                    'egg-info' in dname]):
                del_these.append(dname)
        for item in del_these:
            dl.remove(item)
        for fname in fl:
            if fname.endswith(".py"):
                iname = fname.replace(".py", "")
                if iname == "__init__":
                    importables.append(dp.replace(prefix, ""))
                elif iname == "setup":
                    continue
                elif dp == '.':
                    importables.append(iname)
                else:
                    importables.append("{}.{}".format(dp.replace(prefix, ""),
                                                      iname))

    missing_doc = []
    for mname in importables:
        try:
            # print("import_module({})".format(mname))
            mod = import_module(mname)

            for name, obj in inspect.getmembers(mod, inspect.isclass):
                if doc_missing(obj) and name not in missing_doc:
                    missing_doc.append(name)

                for mthname, mthobj in inspect.getmembers(obj,
                                                          inspect.isfunction):
                    if doc_missing(mthobj) and mthname not in missing_doc:
                        missing_doc.append("{}.{}".format(name, mthname))

            for name, obj in inspect.getmembers(mod, inspect.isfunction):
                if doc_missing(obj) and name not in missing_doc:
                    missing_doc.append("{}.{}".format(mname, name))

        except SystemExit:
            print("SystemExit: failed importing {}".format(mname))
        except ImportError:
            print("ImportError: failed importing {}".format(mname))

    if missing_doc:
        return missing_doc


# -----------------------------------------------------------------------------
def doc_missing(obj):
    """
    Check *obj* for a non-empty __doc__ element
    """
    if not hasattr(obj, '__doc__') or obj.__doc__ is None:
        return True
    else:
        return False


# -----------------------------------------------------------------------------
def my_name():
    """
    Return the name of the caller
    """
    return inspect.stack()[1].function


# -----------------------------------------------------------------------------
def randomize(ref=None, direction=None, window=None):
    """
    Return a random integer value based on REF, DIRECTION, and WINDOW.

    DIRECTION should be +1, -1, or 0 to indicate whether the random value
    should be above, below, or centered on REF.

    WINDOW indicates how far away from REF generated random values can fall.
    """
    ref = int(ref + 0.5) or 0
    direction = int(direction) or 0
    window = int(window) or 100
    if 0 < direction:
        high = ref + window
        low = ref
    elif direction < 0:
        high = ref
        low = ref - window
    else:
        high = ref + (window / 2)
        low = ref - (window / 2)
    return random.randint(low, high)


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

    if isinstance(out, bytes):
        return out.decode()
    elif isinstance(out, str):
        return out


# -----------------------------------------------------------------------------
def version():
    """
    Returns the current project version
    """
    return verinfo._v


# -----------------------------------------------------------------------------
class Error(Exception):
    """
    Errors raised in this file
    """
    pass
