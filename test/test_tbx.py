"""
Tests for module tbx
"""
import os
import re
import shlex
import shutil
import io
import subprocess as subp
import sys
import pytest
import tbx


# -----------------------------------------------------------------------------
def test_zlint():
    """
    Run flake8 on the payload and test code
    """
    pytest.dbgfunc()
    result = subp.Popen(shlex.split("flake8 tbx test"),
                        stdout=subp.PIPE).communicate()[0]
    assert result.decode() == ''


# -----------------------------------------------------------------------------
def test_abspath(tmpdir):
    """
    Verify that tbx.abspath() behaves as expected
    """
    pytest.dbgfunc()
    nib = tmpdir.join("testfile")
    nib.write("This is the test file")
    with tbx.chdir(tmpdir.strpath):
        assert tbx.abspath("./testfile") == nib.strpath


# -----------------------------------------------------------------------------
def test_basename(tmpdir):
    """
    Verify that tbx.abspath() behaves as expected
    """
    pytest.dbgfunc()
    fname = "testfile"
    tf = tmpdir.join(fname)
    tf.write("{} exists".format(fname))
    assert tbx.basename(tf.strpath) == fname
    assert tbx.basename(tf.strpath) == os.path.basename(tf.strpath)


# -----------------------------------------------------------------------------
def test_chdir_good(tmpdir):
    """
    chdir(a.directory.that.exists) should work. After the with statement, we
    should be back where we started.
    """
    pytest.dbgfunc()
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
    pytest.dbgfunc()
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
    pytest.dbgfunc()
    origin = os.getcwd()
    rug = tmpdir.join('foo/bar/nosuch')
    rug.ensure(dir=True)
    with tbx.chdir(rug.strpath):
        shutil.rmtree(rug.dirname)
        with pytest.raises(OSError) as err:
            with tbx.chdir('..'):
                assert os.getcwd() == origin
        assert any(['No such file or directory' in str(err),
                    'Invalid argument' in str(err)])
        with pytest.raises(OSError) as err:
            assert os.getcwd() == rug.strpath
    assert os.getcwd() == origin
    assert any(['No such file or directory' in str(err),
                'Invalid argument' in str(err)])


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
    Calling contents on a file that exists with an invalid separator
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
    pytest.dbgfunc()
    ctest.data.chmod(0000)
    with pytest.raises(tbx.Error) as err:
        _ = tbx.contents(ctest.data.strpath, fmt=str, sep=r'\s')
    assert "Can't read file {0}".format(ctest.data.strpath) in str(err)


# -----------------------------------------------------------------------------
def test_contents_invalid_fmt(ctest):
    """
    Calling contents with an invalid format
    """
    pytest.dbgfunc()
    with pytest.raises(tbx.Error) as err:
        _ = tbx.contents(ctest.data.strpath, fmt='foobar', sep=r'\s')
    assert "Error: Invalid format" in str(err)


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
def dtst_foobar(*args):
    """foobar - print a comma delimited argument list
    """
    print("This is foobar: {0}".format(", ".join([str(_) for _ in args])))


# -----------------------------------------------------------------------------
def xtst_undocumented(*args):
    print("This is undocumented")


# -----------------------------------------------------------------------------
def test_envset_new_none():
    """
    Set a new environment variable to None
    """
    pytest.dbgfunc()
    vname = 'TEST_ENVSET'
    if os.getenv(vname):
        del os.environ[vname]
    with tbx.envset(TEST_ENVSET=None):
        assert os.getenv(vname) is None
    assert os.getenv(vname) is None


# -----------------------------------------------------------------------------
def test_envset_new_1():
    """
    Set a single new environment variable
    """
    pytest.dbgfunc()
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
    pytest.dbgfunc()
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
    pytest.dbgfunc()
    orig = os.getenv('HOME')
    with tbx.envset(HOME='/somewhere/over/the/rainbow'):
        assert os.getenv('HOME') == '/somewhere/over/the/rainbow'
    assert os.getenv('HOME') == orig


# -----------------------------------------------------------------------------
def test_envset_old_2():
    """
    Set multiple new environment variables
    """
    pytest.dbgfunc()
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
    pytest.dbgfunc()
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
    pytest.dbgfunc()
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
def test_envset_child():
    """
    If we set an env var with envset, then spawn a process, the new setting
    should show up in the child process.
    """
    pytest.dbgfunc()
    result = tbx.run("env")
    assert "TBX_TEST=gargantuan" not in result
    with tbx.envset(TBX_TEST="gargantuan"):
        result = tbx.run("env")
        assert "TBX_TEST=gargantuan" in result
    result = tbx.run("env")
    assert "TBX_TEST=gargantuan" not in result


# -----------------------------------------------------------------------------
def test_exists(tmpdir):
    """
    Verify that tbx.exists() behaves as expected
    """
    pytest.dbgfunc()
    exfile = tmpdir.join("exists")
    exfile.write("This file exists")
    nsfile = tmpdir.join("nosuch")
    assert tbx.exists(exfile)
    assert tbx.exists(nsfile) is False


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [   # noqa
    ('$FOO', 'my home dir = /home/dir'),
    ('do nothing', 'do nothing'),
    ('$HOME', '/home/dir'),
    ('~', '/home/dir'),
    ('EVAR', 'EVAR'),
    ('EVAR/~', 'EVAR//home/dir'),
    ('$EVAR', 'value'),
    ('~/$EVAR', '/home/dir/value'),
    ])
def test_expand(inp, exp):
    """
    Expand all environment variables, then expand '~' into $HOME.

    Note: os.path.expanduser() only expands '~' if it's at the beginning of the
    string (not what I want)
    """
    pytest.dbgfunc()
    with tbx.envset(HOME='/home/dir', FOO='my home dir = ~', EVAR='value'):
        assert tbx.expand(inp) == exp


# -----------------------------------------------------------------------------
def test_fatal_empty():
    """
    fatal(empty message) should throw a SystemExit with some non-empty message
    """
    pytest.dbgfunc()
    exp = 'Fatal error with no reason specified'
    with pytest.raises(SystemExit) as err:
        tbx.fatal()
    assert exp in str(err)


# -----------------------------------------------------------------------------
def test_fatal_msg():
    """
    fatal(non-empty message) should throw a SystemExit with the message
    """
    pytest.dbgfunc()
    msg = 'This is a fatal error message'
    with pytest.raises(SystemExit) as err:
        tbx.fatal(msg)
    assert msg in str(err)


# -----------------------------------------------------------------------------
def test_fatal_number():
    """
    fatal(non-string) should throw a SystemExit with str(message)
    """
    pytest.dbgfunc()
    msg = 32.198
    with pytest.raises(SystemExit) as err:
        tbx.fatal(msg)
    assert str(msg) in str(err)


# -----------------------------------------------------------------------------
def test_revnumerate():
    """
    Enumerate a copy of a sequence in reverse as a generator
    """
    pytest.dbgfunc()
    data = ['john', 'mary', 'bill', 'sally', 'pfhisllig']
    pidx = None
    for idx, item in tbx.revnumerate(data):
        if pidx:
            assert idx < pidx
            assert item == data[idx]
        pidx = idx


# -----------------------------------------------------------------------------
def test_run_noargs():
    """
    Without arguments, tbx.run() should throw a TypeError exception
    """
    pytest.dbgfunc()
    with pytest.raises(TypeError) as err:
        tbx.run()
    assert 'run() takes' in str(err) or 'run() missing' in str(err)
    assert 'argument' in str(err)


# -----------------------------------------------------------------------------
def test_run_cmd(rdata):
    """
    With just a command (*cmd*), tbx.run() should run the command and return
    its stdout + stderr
    """
    pytest.dbgfunc()
    result = tbx.run("python -c 'import this'")
    assert isinstance(result, str)
    for item in rdata.exp:
        check_in(item, result)


# -----------------------------------------------------------------------------
def test_run_cmd_istr(rdata):
    """
    tbx.run(cmd, input=str)
    """
    pytest.dbgfunc()
    result = tbx.run('python', input='import this\n')
    assert isinstance(result, str)
    for item in rdata.exp:
        check_in(item, rdata.exp)


# -----------------------------------------------------------------------------
def test_run_cmd_istrio(rdata):
    """
    tbx.run(cmd, input=StringIO)
    """
    pytest.dbgfunc()
    result = tbx.run('python', input=io.StringIO('import this\n'))
    assert isinstance(result, str)
    for item in rdata.exp:
        check_in(item, result)


# -----------------------------------------------------------------------------
def test_run_cmd_ipath(rdata, tmpdir):
    """
    tbx.run(cmd, input='< path')
    """
    pytest.dbgfunc()
    input_file = tmpdir.join('script')
    input_file.write('import this\n')
    result = tbx.run('python', input='< {0}'.format(input_file))
    assert isinstance(result, str)
    for item in rdata.exp:
        check_in(item, result)


# -----------------------------------------------------------------------------
def test_run_cmd_icmd(rdata):
    """
    tbx.run(cmd, input='cmd |')
    """
    pytest.dbgfunc()
    icmd = "echo 'import this' |"
    result = tbx.run('python', input=icmd)
    assert isinstance(result, str)
    for item in rdata.exp:
        check_in(item, result)


# -----------------------------------------------------------------------------
def test_run_cmd_ifd(rdata, tmpdir):
    """
    tbx.run(cmd, input=fd)
    """
    pytest.dbgfunc()
    infile = tmpdir.join('infile')
    infile.write('import this\n')
    fobj = infile.open(mode='r')
    fnum = fobj.fileno()
    result = tbx.run('python', input=fnum)
    assert isinstance(result, str)
    for item in rdata.exp:
        check_in(item, result)


# -----------------------------------------------------------------------------
def test_run_cmd_ifobj(rdata, tmpdir):
    """
    tbx.run(cmd, input=open(filename, 'r'))
    """
    pytest.dbgfunc()
    infile = tmpdir.join('infile')
    infile.write('import this\n')
    fobj = infile.open(mode='r')
    result = tbx.run('python', input=fobj)
    assert isinstance(result, str)
    for item in rdata.exp:
        check_in(item, rdata.exp)


# -----------------------------------------------------------------------------
def test_run_cmd_ostr():
    """
    tbx.run(cmd, output='foobar')
        should raise error -- '>' or '|' required
    """
    pytest.dbgfunc()
    with pytest.raises(tbx.Error) as err:
        tbx.run('python -c "import this"', output='foobar')
    assert '| or > required for string output' in str(err)


# -----------------------------------------------------------------------------
def test_run_cmd_ostr_redir(rdata, tmpdir):
    """
    tbx.run(cmd, output='> foobar')
        should write data to foobar
    """
    pytest.dbgfunc()
    outfile = tmpdir.join('outfile')
    target = '> ' + outfile.strpath
    tbx.run('python -c "import this"', output=target)
    result = outfile.read()
    for item in rdata.exp:
        assert item in result


# -----------------------------------------------------------------------------
def test_run_cmd_ostrio(rdata):
    """
    tbx.run(cmd, output=StringIO)
        output should wind up in the StringIO object
    """
    pytest.dbgfunc()
    outstr = io.StringIO()
    rval = tbx.run('python -c "import this"', output=outstr)
    assert rval is None
    result = outstr.getvalue()
    for item in rdata.exp:
        assert item in result


# -----------------------------------------------------------------------------
def test_run_cmd_opath(rdata, tmpdir):
    """
    tbx.run(cmd,
            input={str, StringIO, '< path', '| cmd', fd, fileobj},
            output={str, StringIO, '> path', 'cmd |', fd, fileobj})
    """
    pytest.dbgfunc()
    outfile = tmpdir.join('outfile')
    rval = tbx.run('python -c "import this"',
                   output="> {0}".format(outfile.strpath))
    assert rval is None
    result = outfile.read()
    for item in rdata.exp:
        assert item in result


# -----------------------------------------------------------------------------
def test_run_cmd_ocmd(rdata):
    """
    tbx.run(cmd1, '| cmd2')
        should pipe the output of cmd1 to cmd2
    """
    pytest.dbgfunc()
    cmd1 = "python -c 'import this'"
    cmd2 = "grep better"
    result = tbx.run(cmd1, output='| {0}'.format(cmd2))
    assert isinstance(result, str)
    for item in [_ for _ in rdata.exp if 'better' in _]:
        check_in(item, result)
    for item in [_ for _ in rdata.exp if 'better' not in _]:
        check_in(item, result, negate=True)


# -----------------------------------------------------------------------------
def test_run_cmd_ofd(rdata, tmpdir):
    """
    tbx.run(cmd, output=fd)
        should write output into file open on fd
    """
    pytest.dbgfunc()
    outfile = tmpdir.join('outfile')
    fobj = open(outfile.strpath, 'w')
    fnum = fobj.fileno()
    rval = tbx.run('python -c "import this"', output=fnum)
    assert rval is None
    result = outfile.read()
    for item in rdata.exp:
        assert item in result


# -----------------------------------------------------------------------------
def test_run_cmd_ofobj(rdata, tmpdir):
    """
    tbx.run(cmd, output=fileobj)
        should write output into fileobj
    """
    pytest.dbgfunc()
    outfile = tmpdir.join('outfile')
    rval = tbx.run('python -c "import this"',
                   output=open(outfile.strpath, 'w'))
    assert rval is None
    result = outfile.read()
    for item in rdata.exp:
        assert item in result


# -----------------------------------------------------------------------------
def test_version():
    """
    Verify that tbx.version() returns a valid version string
    """
    pytest.dbgfunc()
    assert re.match(r"\d\.\d\.\d", tbx.version())
    assert tbx.version() == tbx.verinfo._v


# -----------------------------------------------------------------------------
def test_deployable():
    """
    Check that 1) no untracked files are hanging out, 2) no staged but
    uncommitted updates are outstanding, 3) no unstaged, uncommitted changes
    are outstanding, 4) the most recent git tag matches HEAD, and 5) the most
    recent git tag matches the current version.
    """
    pytest.dbgfunc()
    staged, changed, untracked = tbx.git_status()
    assert untracked == [], "You have untracked files"
    assert changed == [], "You have unstaged updates"
    assert staged == [], "You have updates staged but not committed"

    if tbx.git_current_branch() != 'master':
        return True

    last_tag = tbx.git_last_tag()
    msg = "Version ({}) does not match tag ({})".format(tbx.version(),
                                                        last_tag)
    assert tbx.version() == last_tag, msg
    assert tbx.git_hash() == tbx.git_hash(last_tag), "Tag != HEAD"


# -----------------------------------------------------------------------------
def check_in(a, b, negate=False):
    """
    Assert that a is in b and fail otherwise
    """
    if type(a) == type(b):
        if negate:
            assert a not in b
        else:
            assert a in b
    elif isinstance(a, str) and isinstance(b, bytes):
        if negate:
            assert bytes(a, 'utf8') not in b
        else:
            assert bytes(a, 'utf8') in b


# -----------------------------------------------------------------------------
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
def get_this():
    """
    return The Zen of Python as a string
    """
    while True:
        try:
            rval = get_this.zen
            return rval
        except AttributeError:
            buf = io.StringIO('w')
            orig = sys.stdout
            sys.stdout = buf
            import this    # noqa
            sys.stdout = orig
            get_this.zen = buf.getvalue()


# -----------------------------------------------------------------------------
@pytest.fixture
def rdata():
    """
    Set up for run tests
    """
    zen = get_this()
    rdata.exp = [_ for _ in zen.split('\n') if _ != '']
    return rdata


# -----------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def fx_calls_debug(request):
    """
    Fails if the target test function does not call pytest.dbgfunc()
    """
    if 'dbgfunc' not in request.function.__code__.co_names:
        pytest.fail("Test '{}' does not call pytest.dbgfunc"
                    "".format(request.function.__code__.co_name))
