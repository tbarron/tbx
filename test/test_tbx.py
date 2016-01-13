"""
Tests for module tbx
"""
import os
import pdb    # pylint: disable=unused-import
import pytest
import shutil


import pytest


import tbx


# -----------------------------------------------------------------------------
def test_chdir_good(tmpdir):
    """
    Trying to chdir to a non existent directory
    """
    orig = os.getcwd()
    with tbx.chdir(tmpdir.strpath):
        assert os.getcwd() == tmpdir.strpath
    assert orig == os.getcwd()


# -----------------------------------------------------------------------------
def test_chdir_nosuchdir(tmpdir):
    """
    Trying to chdir to a non existent directory
    """
    nosuch = tmpdir.join('foo/bar/somewhere')
    with pytest.raises(OSError) as err:
        with tbx.chdir(nosuch.strpath):
            assert os.getcwd() == tmpdir.strpath
    assert 'No such file or directory' in str(err)


# -----------------------------------------------------------------------------
def test_chdir_rug(tmpdir):
    """
    Trying to chdir out af a non existent directory
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
def test_contents_nosuch_default():
    """
    Attempting to get the contents of a non-existent file with a default value
    should return the default
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_contents_nosuch_nodefault():
    """
    Attempting to get the contents of a non-existent file with no default value
    should raise an exception
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_contents_good_str():
    """
    Calling contents on a file that exists as a string
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_contents_good_list():
    """
    Calling contents on a file that exists as a list
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
@pytest.mark.parametrize('level', [0, 1, 2, None])
def test_dirname(level):
    """
    Default level for dirname is 0
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_revnumerate():
    """
    Enumerate a copy of a sequence in reverse as a generator
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_dispatch_help_nosuch():
    """
    Dispatch help on a function that does not exist
    """
    pytest.skip('construction')

# -----------------------------------------------------------------------------
def test_dispatch_help_good():
    """
    Dispatch help on a function that exists
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_dispatch_bad(capsys):
    """
    Calling dispatch with a non-existent function name
    """
    with pytest.raises(SystemExit) as err:
        tbx.dispatch(module=__name__,
                     prefix='dtst',
                     function='bumble',
                     argl=[1,2,3])
    assert 'Module test_tbx has no function dtst_bumble' in str(err)
    out, err = capsys.readouterr()
    assert out == ''


# -----------------------------------------------------------------------------
def test_dispatch_good(capsys):
    """
    Calling dispatch with a good function name
    """
    argl = [7, 8, 9, 17]
    tbx.dispatch(__name__, 'dtst', 'foobar', argl)
    out, err = capsys.readouterr()
    exp = "This is foobar: {0}".format(', '.join([str(_) for _ in argl]))
    assert exp in out


# -----------------------------------------------------------------------------
def dtst_foobar(*args):
    """
    Dispatchable function for test_dispatch_good
    """
    print "This is foobar: {0}".format(", ".join([str(_) for _ in args]))


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
