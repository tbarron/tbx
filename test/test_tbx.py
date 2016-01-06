"""
Tests for module tbx
"""
import os
import pdb    # pylint: disable=unused-import
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
