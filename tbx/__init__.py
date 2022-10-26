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
from py.path import local
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
    Returns the absolute path of *relpath*. This has the same functionality as
    os.path.abspath, but a shorter name, and it corresponds to basename() and
    dirname() so that when no other os.path functionality is required, tbx can
    replace it.
    """
    return osp.abspath(relpath)


# -----------------------------------------------------------------------------
def basename(path, segments=None):
    """
    Returns the basename of *path*. With only the first argument, this provides
    the same functionality as os.path.basename. However, its overall name is
    shorter and it corresponds to abspath() and dirname(), allowing tbx to
    replace os.path if no other os.path functionality is required.
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
    Return the name of the calling function of the function from which this
    routine is called. That is, this function returns the name of its
    grand-caller.
    """
    return inspect.stack()[2].function


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def chdir(directory):
    """
    Provides a context-based directory excursion. For example, given the
    following code:

        with chdir(somedir):
            foo(baz)

    The call to foo() with argument baz will take place with somedir being the
    current directory. Once the with scope completes, the directory context
    returns to where it was before the with scope began.
    """
    origin = os.getcwd()
    try:
        os.chdir(directory)
        yield

    finally:
        os.chdir(origin)


# -----------------------------------------------------------------------------
def cmkdir(path):
    """
    If *path* exists, do nothing, returning local(path). Otherwise, call
    os.makedirs() to create *path*, including any missing intermediate
    segments, and return local(path) if the operation is successful. If the
    directory creation fails, return None.
    """
    rv = local(path)
    if not os.path.isdir(rv.strpath):
        rv.ensure(dir=True)
    return rv


# -----------------------------------------------------------------------------
def conditional_debug(**kw):
    """
    If kw['d'] is True, start the debugger after the call to
    conditional_debug()
    """
    if kw['d']:
        pdb.set_trace()


# -----------------------------------------------------------------------------
def contents(name=None, default=None, fmt='str', sep=None):
    """
    Return the contents of file named *name*. If the file does not exist,
    return the value in *default*. If the file is not accessible for some other
    reason, raise an exception.

    The *fmt* argument determines the format of the return value. It can be
    'str', str, 'list', or list. If it is 'str' or str, the contents of the
    file is returned as a string.

    If it is 'list' or list, the contents of the file will be split on the
    value of *sep* and the resulting list will be returned.

    The *sep* argument can be a regex in a string or a list of regexes. If
    *fmt* is 'list' or list and *sep* is not specified, the file content will
    be split on '\\n'.
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
        if isinstance(sep, str):
            rsep = sep
        elif isinstance(sep, list):
            rsep = "|".join(sep)
        rval = re.split(rsep, data)
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
    Remove *segments* tails from path and return what's left. If segments is
    not specified, it defaults to 1. Argument *level* is DEPRECATED but will
    continue to be honored as a synomym for *segements* for a few releases for
    backward compatibility.
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
    excursion.

    To unset a variable temporarily, pass its value as None.

    Example:
        with tbx.envset(PATH='whatever'):
            ... do stuff ...
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
    Return True if *path* exists, else False. This mirrors os.path.exists().
    """
    return osp.exists(path)


# -----------------------------------------------------------------------------
def expand(path):
    """
    Return path with any '~' expressions or env vars expanded.
    """
    return _expanduser(osp.expandvars(path))


# -----------------------------------------------------------------------------
def _expanduser(instr):
    """
    Expand '~' to the value of $HOME
    """
    hval = os.getenv("HOME") or ""
    rval = re.sub("~", hval, instr)
    return rval


# -----------------------------------------------------------------------------
def fatal(msg='Fatal error with no reason specified'):
    """
    Display *msg* before exiting the current process
    """
    sys.exit(msg)


# -----------------------------------------------------------------------------
def git_last_tag():
    """
    If we're in a git repo, return the most recently defined tag.
    """
    result = run("git --no-pager tag")
    tag_l = result.strip().split("\n")
    rval = tag_l[-1] if 0 < len(tag_l) else ""
    return rval


# -----------------------------------------------------------------------------
def git_hash(ref=None):
    """
    If we're in a git repo, return a hash of *ref*. If *ref* is None (i.e.,
    unspecified), return a hash of HEAD.
    """
    cmd = "git --no-pager log -1 --format=format:\"%H\""
    if ref:
        cmd += " {}".format(ref)
    result = run(cmd)
    return result


# -----------------------------------------------------------------------------
def git_current_branch():
    """
    If we're in a git repo, return the name of the currently active branch.
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
def isnum_str(inp):
    """
    Return True if the string input *inp* contains only whitespace and digits
    """
    if not isinstance(inp, str):
        return False
    elif re.match(r"^\s*\d+\s*$", inp):
        return True
    else:
        return False


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
def collect_missing_docs(treeroot, ignore_l=None):
    """
    Find all python files in a directory tree and report any functions/methods
    that have no doc string or an undefined one.
    """
    ignore_l = ignore_l or []
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
                if name in ignore_l:
                    continue
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
    The doc string is considered missing if there is no __doc__ element or if
    *obj*.__doc__ is None. Note that a blank or empty doc string ("", " ") is
    not considered missing.
    """
    if not hasattr(obj, '__doc__') or obj.__doc__ is None:
        return True
    else:
        return False


# -----------------------------------------------------------------------------
def my_name():
    """
    Return the name of the caller.

    Example:
        me = tbx.my_name()
        print("{} says 'hello!'", me)
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

    If *input* is an io.StringIO, its contents will be used as stdin for the
    child process.

    If *input* is a str beginning with '<', the following text will be treated
    as a file name and that file will be opened and read as the child's stdin.

    If *input* is a str ending with '|', the preceding text will be treated as
    a command and the child's stdin will come from the command's stdout.

    If *input* is an int (file descriptor) or a file, it will be used as stdin
    for the child process.

    If *output* is a str beginning with '>', the following text will be treated
    as a file name and that file will be opened to receive child's stdout.

    If *output* is a str beginning with '|', the following text will be treated
    as a command and child's stdout will be connected to the command's stdin.

    If *output* is a file descriptor (int) or file, it will be used to receive
    child's stdout.
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
    Returns the current tbx project version
    """
    return verinfo._v


# -----------------------------------------------------------------------------
class Error(Exception):
    """
    Errors raised in this file
    """
    pass
