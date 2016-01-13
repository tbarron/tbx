"""
Toolbox
"""
import contextlib
import os
import sys
import types


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def chdir(directory):
    """
    Context-based directory excursion

    When the with statement ends, you're back where you started.
    """
    try:
        origin = os.getcwd()
        os.chdir(directory)
        yield

    finally:
        os.chdir(origin)


# -----------------------------------------------------------------------------
def dispatch(module, prefix, function, argl=None, kwd=None):
    """
    If <module>.<prefix>_<function> exists as a function, call it with *argl*
    """
    arglist = argl or []
    kwargs = kwd or {}
    mod = sys.modules[module]
    try:
        fullname = '_'.join([prefix, function])
        func = getattr(mod, fullname)
        if isinstance(func, types.FunctionType):
            rval = func(*arglist, **kwargs)
    except AttributeError:
        sys.exit('Module {0} has no function {1}'.format(module, fullname))


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
