"""
Tests for module tbx
"""
import os
import re
import shutil

import pytest
import pexpect

import tbx

# -----------------------------------------------------------------------------
def test_chdir_good(tmpdir):
    """
    chdir(a.directory.that.exists) should work. After the with statement, we
    should be back where we started.
    """
    orig = os.getcwd()
    with tbx.chdir(tmpdir.strpath):
        assert os.getcwd() == tmpdir.strpath
    assert orig == os.getcwd()

# -----------------------------------------------------------------------------
def test_chdir_nosuchdir(tmpdir):
    """
    chdir(a.directory.that.does.not.exist) should throw an OSError with the
    message 'No such file or directory'.
    """
    nosuch = tmpdir.join('foo/bar/somewhere')
    with pytest.raises(OSError) as err:
        with tbx.chdir(nosuch.strpath):
            assert os.getcwd() == tmpdir.strpath
    assert 'No such file or directory' in str(err)

# -----------------------------------------------------------------------------
def test_chdir_rug(tmpdir):
    """
    Trying to chdir out af a non existent directory (i.e., one that was removed
    after we chdir'd into it)
    """
    origin = os.getcwd()
    rug = tmpdir.join('foo/bar/nosuch')
    rug.ensure(dir=True)
    with tbx.chdir(rug.strpath):
        shutil.rmtree(rug.dirname)
        with pytest.raises(OSError) as err:
            with os.chdir('..'):
                assert os.getcwd() == origin
        assert 'No such file or directory' in str(err)
        with pytest.raises(OSError) as err:
            assert os.getcwd() == rug.strpath
    assert os.getcwd() == origin
    assert 'No such file or directory' in str(err)

# -----------------------------------------------------------------------------
# pylint: disable=redefined-outer-name
@pytest.fixture
def ctest(tmpdir):
    """
    Set up for contents tests
    """
    ctest.data = tmpdir.join('ctest_data')
    ctest.exp = '\n'.join(['this is the test data',
                           'this is the second line',
                           'frumple'])
    ctest.data.write(ctest.exp)
    return ctest

# -----------------------------------------------------------------------------
def test_contents_nosuch_default(ctest):
    """
    Attempting to get the contents of a non-existent file with a default value
    should return the default
    """
    pytest.dbgfunc()
    filename = ctest.data.strpath + 'xxx'
    result = tbx.contents(filename,
                          default='foobar')
    assert result == 'foobar'

# -----------------------------------------------------------------------------
def test_contents_nosuch_nodefault(ctest):
    """
    Attempting to get the contents of a non-existent file with no default value
    should raise an exception
    """
    pytest.dbgfunc()
    filename = ctest.data.strpath + 'xxx'
    with pytest.raises(IOError) as err:
        _ = tbx.contents(filename)
    assert "No such file or directory" in str(err)
    assert filename in str(err)

# -----------------------------------------------------------------------------
def test_contents_good_str(ctest):
    """
    Calling contents on a file that exists as a string
    """
    pytest.dbgfunc()
    result = tbx.contents(ctest.data.strpath)
    assert result == ctest.exp

# -----------------------------------------------------------------------------
def test_contents_good_list(ctest):
    """
    Calling contents on a file that exists as a list
    """
    pytest.dbgfunc()
    result = tbx.contents(ctest.data.strpath, fmt='list')
    assert result == ctest.exp.split('\n')

# -----------------------------------------------------------------------------
def test_contents_good_altsep(ctest):
    """
    Calling contents on a file that exists as a list
    """
    pytest.dbgfunc()
    result = tbx.contents(ctest.data.strpath, fmt='list', sep=r'\s')
    assert len(result) == len(re.split(r'\s', ctest.exp))
    assert result == re.split(r'\s', ctest.exp)

# -----------------------------------------------------------------------------
def test_contents_badfmt(ctest):
    """
    Calling contents on a file that exists as a list
    """
    pytest.dbgfunc()
    with pytest.raises(tbx.Error) as err:
        _ = tbx.contents(ctest.data.strpath, fmt='str', sep=r'\s')
    assert 'Non-default separator is only valid for list format' in str(err)

# -----------------------------------------------------------------------------
def test_contents_badperm(ctest):
    """
    Calling contents on a file that is not readable with throw an exception
    """
    # pytest.skip('construction')
    ctest.data.chmod(0000)
    with pytest.raises(tbx.Error) as err:
        _ = tbx.contents(ctest.data.strpath, fmt=str, sep=r'\s')
    assert "Can't read file {0}".format(ctest.data.strpath) in str(err)

# -----------------------------------------------------------------------------
@pytest.mark.parametrize('level', [0, 1, 2, None])
def test_dirname(level):
    """
    Default level for dirname is 0
    """
    pytest.dbgfunc()
    inp = '/a/b/c/d/e'
    exp = inp[:]
    if level is None:
        exp = os.path.dirname(exp)
    else:
        for _ in range(level):
            exp = os.path.dirname(exp)
    result = tbx.dirname(inp, level=level)
    assert result == exp

# -----------------------------------------------------------------------------
def test_revnumerate():
    """
    Enumerate a copy of a sequence in reverse as a generator
    """
    pytest.skip('construction')

# -----------------------------------------------------------------------------
def test_dispatch_help_good(capsys):
    """
    Dispatch help on a function that exists and has a doc string
    """
    pytest.dbgfunc()
    exp = 'foobar - print a comma delimited argument list'
    tbx.dispatch_help(__name__, 'dtst', ['foobar'])
    out, _ = capsys.readouterr()
    assert exp in out

# -----------------------------------------------------------------------------
def test_dispatch_help_help(capsys):
    """
    Dispatch help on help
    """
    pytest.dbgfunc()
    exp = ['help - show a list of available commands',
           'With no arguments',
           'With a command as argument']
    tbx.dispatch_help(__name__, 'dtst', ['help'])
    out, _ = capsys.readouterr()
    assert all([_ in out for _ in exp])

# -----------------------------------------------------------------------------
def test_dispatch_help_multiple(capsys):
    """
    Dispatch help for multiple topics
    """
    pytest.dbgfunc()
    exp = ['help - show a list of available commands',
           'With no arguments',
           'With a command as argument',
           'foobar - print a comma delimited argument list']
    tbx.dispatch_help(__name__, 'dtst', ['foobar', 'help'])
    out, _ = capsys.readouterr()
    assert all([_ in out for _ in exp])

# -----------------------------------------------------------------------------
def test_dispatch_help_noargs(capsys):
    """
    Dispatch help with no arguments -- should list available dispatchables
    """
    pytest.dbgfunc()
    exp = ['help - show a list of available commands',
           'foobar - print a comma delimited argument list']
    tbx.dispatch_help(__name__, 'dtst')
    out, _ = capsys.readouterr()
    assert all([_ in out for _ in exp])

# -----------------------------------------------------------------------------
def test_dispatch_help_nodoc():
    """
    Dispatch help on a function that has no doc string
    """
    pytest.dbgfunc()
    exp = 'Function xtst_undocumented is missing a __doc__ string'
    with pytest.raises(SystemExit) as err:
        tbx.dispatch_help(__name__, 'xtst', ['undocumented'])
    assert exp in str(err)

# -----------------------------------------------------------------------------
def test_dispatch_help_nomodule():
    """
    Dispatch help on a non-existent module
    """
    pytest.dbgfunc()
    exp = 'Module xtest.test_tbx is not in sys.modules'
    with pytest.raises(SystemExit) as err:
        tbx.dispatch('x' + __name__, 'foo', ['help', 'nosuch'])
    assert exp in str(err)

# -----------------------------------------------------------------------------
def test_dispatch_help_nopfx():
    """
    Dispatch help with no prefix
    """
    pytest.dbgfunc()
    exp = '*prefix* is required'
    with pytest.raises(SystemExit) as err:
        tbx.dispatch(__name__, args=['help', 'nosuch'])
    assert exp in str(err)

# -----------------------------------------------------------------------------
def test_dispatch_help_nosuch():
    """
    Dispatch help on a function that does not exist
    """
    pytest.dbgfunc()
    exp = 'Module test.test_tbx has no attribute foo_nosuch'
    with pytest.raises(SystemExit) as err:
        tbx.dispatch(__name__, 'foo', ['help', 'nosuch'])
    assert exp in str(err)

# -----------------------------------------------------------------------------
def test_dispatch_bad(capsys):
    """
    Calling dispatch with a non-existent function name
    """
    with pytest.raises(SystemExit) as err:
        tbx.dispatch(mname=__name__,
                     prefix='dtst',
                     args=['bumble', 1, 2, 3])
    assert 'Module test.test_tbx has no function dtst_bumble' in str(err)
    out, err = capsys.readouterr()
    assert out == ''

# -----------------------------------------------------------------------------
def test_dispatch_good(capsys):
    """
    Calling dispatch with a good function name
    """
    pytest.dbgfunc()
    argl = ['foobar', 7, 8, 9, 17]
    tbx.dispatch(__name__, 'dtst', argl)
    out, _ = capsys.readouterr()
    exp = "This is foobar: {0}".format(', '.join([str(_) for _ in argl[1:]]))
    assert exp in out

# -----------------------------------------------------------------------------
def dtst_foobar(*args):
    """foobar - print a comma delimited argument list
    """
    print "This is foobar: {0}".format(", ".join([str(_) for _ in args]))

# -----------------------------------------------------------------------------
# pylint: disable=missing-docstring,unused-argument
def xtst_undocumented(*args):
    print "This is undocumented"
# pylint: enable=missing-docstring,unused-argument

# -----------------------------------------------------------------------------
def test_envset_new_1():
    """
    Set a single new environment variable
    """
    if os.getenv('TEST_ENVSET'):
        del os.environ['TEST_ENVSET']
    with tbx.envset(TEST_ENVSET='foobar'):
        assert os.getenv('TEST_ENVSET') == 'foobar'
    assert os.getenv('TEST_ENVSET') is None

# -----------------------------------------------------------------------------
def test_envset_new_2():
    """
    Set multiple new environment variables
    """
    vlist = ['TEST_ENVSET', 'TEST_ENVSET_2']
    for varname in vlist:
        if os.getenv(varname):
            del os.environ[varname]
    with tbx.envset(TEST_ENVSET='foobar',
                    TEST_ENVSET_2='yetanother'):
        assert os.getenv('TEST_ENVSET') == 'foobar'
        assert os.getenv('TEST_ENVSET_2') == 'yetanother'
    assert os.getenv('TEST_ENVSET') is None
    assert os.getenv('TEST_ENVSET_2') is None

# -----------------------------------------------------------------------------
def test_envset_old_1():
    """
    Set a single existing environment variable to a new value
    """
    assert os.getenv('HOME') is not None
    orig = os.getenv('HOME')
    with tbx.envset(HOME='/somewhere/over/the/rainbow'):
        assert os.getenv('HOME') == '/somewhere/over/the/rainbow'
    assert os.getenv('HOME') == orig

# -----------------------------------------------------------------------------
def test_envset_old_2():
    """
    Set multiple new environment variables
    """
    vlist = ['HOME', 'TERM']
    orig = {}
    for varname in vlist:
        orig[varname] = os.getenv(varname)
    with tbx.envset(HOME='new-value',
                    TERM='not-the-old-value'):
        assert os.getenv('HOME') == 'new-value'
        assert os.getenv('TERM') == 'not-the-old-value'
    assert os.getenv('HOME') == orig['HOME']
    assert os.getenv('TERM') == orig['TERM']

# -----------------------------------------------------------------------------
def test_envset_rm():
    """
    Temporarily unset an environment variable
    """
    vname = 'TEST_ENVSET_RM'
    origval = 'original value'
    kwa = {vname: None}
    os.environ[vname] = origval
    with tbx.envset(**kwa):
        assert os.getenv(vname) is None
    assert os.getenv(vname) == origval
    del os.environ[vname]

# -----------------------------------------------------------------------------
def test_envset_rmset():
    """
    Temporarily set one environment variable and unset another one
    """
    keys = ['TEST_ENVSET_RM', 'TEST_ENVSET_SET']
    origval = dict(zip(keys, ['something', 'something else']))
    updval = dict(zip(keys, [None, 'different from the first']))

    for key in keys:
        os.environ[key] = origval[key]
    with tbx.envset(**updval):
        for key in keys:
            assert os.getenv(key) == updval[key]
    for key in keys:
        assert os.getenv(key) == origval[key]
    for key in keys:
        del os.environ[key]

# -----------------------------------------------------------------------------
def test_fatal_empty():
    """
    fatal(empty message) should throw a SystemExit with some non-empty message
    """
    exp = 'Fatal error with no reason specified'
    with pytest.raises(SystemExit) as err:
        tbx.fatal()
    assert exp in str(err)

# -----------------------------------------------------------------------------
def test_fatal_msg():
    """
    fatal(non-empty message) should throw a SystemExit with the message
    """
    msg = 'This is a fatal error message'
    with pytest.raises(SystemExit) as err:
        tbx.fatal(msg)
    assert msg in str(err)

# -----------------------------------------------------------------------------
def test_fatal_number():
    """
    fatal(non-string) should throw a SystemExit with str(message)
    """
    msg = 32.198
    with pytest.raises(SystemExit) as err:
        tbx.fatal(msg)
    assert str(msg) in str(err)

# -----------------------------------------------------------------------------
def test_zlint():
    """
    Run pylint on the payload and test code
    """
    result = pexpect.run('pylint -rn tbx test')
    assert result == ''