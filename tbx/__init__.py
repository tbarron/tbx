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
from tbx import verinfo


# -----------------------------------------------------------------------------
def abspath(relpath):
    """
    Returns the absolute path of *relpath*
    """
    return os.path.abspath(relpath)


# -----------------------------------------------------------------------------
def basename(path):
    """
    Returns the basename of *path*
    """
    return os.path.basename(path)


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
    return os.path.exists(path)


# -----------------------------------------------------------------------------
def expand(path):
    """
    Return path with any '~' or env vars expanded.
    """
    return _expanduser(os.path.expandvars(path))


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
    result = run("git branch")
    for candy in result.split("\n"):
        if "*" in candy:
            curb = candy.split()[1]
            break
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
