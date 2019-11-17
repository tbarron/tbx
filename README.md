# Toolbox library in python

## Functions (see Examples below)

 * abspath(relpath)

    * Returns the absolute path of whatever *relpath* points at. But wait!
      Doesn't os.path.abspath() already exist? Well, yes. My reasons for
      putting it here are: 1) "tbx.abspath" is shorter than
      "os.path.abspath", and 2) related functions dirname() and basename()
      in this package add functionality not available from the os.path
      versions and if I want those, having abspath() here may let me avoid
      having to import os.path.

    * Example

            import tbx

            testpath = "../dtm"
            assert tbx.abspath(testpath)) == "/Users/tbarron/prj/github/dtm"

 * basename(path, segements=1)

    * Returns the last component of *path*. But wait! Doesn't
      os.path.basename() already exist? Well, yes. See above. Also, this
      basename() provides some power the os.path version does not: the
      argument *segments* controls the number of path components returned.

    * Example

        assert tbx.basename(testpath, segments=3) == "prj/github/dtm"
        assert tbx.basename(testpath, 2) == "github/dtm"

 * chdir(path)

    * Context manager that allows directory excursions that
      automagically return to your starting point upon exiting the
      with scope.

 * contents(name, default=None, fmt='str', sep='\n')

    * Return the contents of a file. If the file does not exist, return
      *default*. The *fmt* argument can be 'list' or 'str'. If *fmt* is
      'list', the return value is a list of strings and *sep* is used to
      split the file contents, with its default being newline. If *fmt* is
      'str', the return value is a string and *sep* is ignored. If *fmt*
      is passed as anything other than 'list' or 'str', it will be treated
      as if 'str' had been passed.

 * dirname(path, segments=1)

    * Return the directory parent of *path*. If *segments* is something
      other 1, *segments* path components are removed from the end of path.
      But wait! Doesn't os.path.dirname() already exist? Well, yes. See the
      description of abspath above. Also, this dirname() provides some
      power the os.path version does not: the argument *segments* controls
      the number of path components returned.

 * envset(VARNAME=VALUE, ...)

    * Context manager that sets one or more environment variables,
      returning them to their original values when control leaves the
      context. Note that VARNAME should not be quoted, but VALUE must be.

 * Error(message)

    * The Error class provides a simple exception class for use in the tbx
      library and any packages that import it. If *message* is not
      provided, a suitable default failure message is used.

 * exists(path)

    * Returns True or False to indicate whether *path* exists in the file
      system. But wait! Doesn't os.path.exists() already exist? See the
      discussion of abspath().

 * expand(str)

    * Expand environment variables in *str*, replacing "$<variable>" with
      the contents of the variable. Replace occurrences of '~' in the
      argument with the contents of $HOME. Variable expansion happens first
      so that any occurrences of '~' in the contents of variables get
      expanded as part of user expansion. I tried to implement expansion of
      expressions like '~username', but that turned into a can of worms.

 * fatal(msg)

    * Print *msg* and exit the process. Wait! Why do we need this when we
      already have tbx.Error()? Why not just raise tbx.Error(msg)? Well,
      calling raise tbx.Error() produces a traceback. If what we want is
      just a clean exit message without a lot of ugly traceback, this will
      provide that. Yeah, but so will sys.exit(msg), right? Yes, but if
      we're importing tbx anyway, this may let us avoid importing sys.

 * git_last_tag()

    * Returns the most recently defined tag from a git repo.

 * git_hash(ref=None)

    * Returns a hash of *ref* (or HEAD if *ref* is None).

 * git_current_branch()

    * Return the name of the currently active git branch.

 * git_status()

    * Return 1) a list of staged but uncommitted updates, 2) a list of
      unstaged updates, and 3) a list of untracked files,

 * revnumerate(sequence)

    * Enumerate *sequence* in reverse. The numbers count down from
      len(*sequence*)-1 to 0.

 * run(cmd, input={str|StringIO|fd|file},
            output={str|StringIO|fd|file})

    * If *input* is a str that begins with '<', the path named in the
      argument will be read and its contents will be written to stdin of
      the command. If a str *input* ends with '|' the argument will be run
      as a command and its output will be written to stdin of the payload
      command. If *input* does not contain either of these characters in
      those positions, the contents of the string is passed to stdin of the
      process.

    * If *output* is a str that begins with '> ', the command's output will
      be written to the file named in the remainder of the string. If
      *output* is a str beginning with '| ', the commands's output will be
      piped to stdin of the command named in the remainder of the string.
      Note that run cannot write directly to the string if it does not
      contain redirection characters ('>' or '|' at the beginning).

 * version()

    * Return the version of tbx.

### Examples

  * abspath(relpath)

        import tbx

        testpath = "../dtm"
        assert tbx.abspath(testpath)) == "/Users/tbarron/prj/github/dtm"

  * basename(path, segments=1)

        assert tbx.basename(testpath, segments=3) == "prj/github/dtm"
        assert tbx.basename(testpath, 2) == "github/dtm"

  * chdir(PATH)

        orig = getcwd()
        with tbx.chdir("/other/directory"):
            assert "/other/directory" == getcwd()
            ... do work in "/other/directory"
        assert orig == getcwd()


 * contents(FILENAME, default=None, fmt={'str'|'list'}, sep='\n')

        from py.path import local

        example = local("testdata")
        example.write("one\ntwo\nthree\nfour\n")

        # default operation
        info = tbx.contents("testdata")
        assert info == "one\ntwo\nthree\nfour\n"

        # return a list rather than a string
        info = tbx.contents("testdata", fmt='list')
        assert info == ["one", "two", "three", "four"]

        # return default if file does not exist
        info = tbx.contents("nosuchfile", default="the file does not exist")
        assert info == "the file does not exist"

        # but if the file is empty, return an empty string
        info = tbx.contents("/dev/null", default="the file is empty")
        assert info == ""

        # alternate separator
        info = tbx.contents("testdata", fmt='list', sep="t")
        assert info == ["one\n", "wo\n", "hree\nfour"]

        # alternate separator is a string, not a character class
        info = tbx.contents("testdata", fmt='list', sep="\nt")
        assert info == ["one", "wo", "hree\nfour"]


 * dirname(PATH, level=1)

        assert tbx.dirname("/a/b/c/d/e/f") == "/a/b/c/d/e"
        assert tbx.dirname("/a/b/c/d/e/f", 2) == "/a/b/c/d"
        assert tbx.dirname("foobar") == "."
        assert tbx.dirname("/a/b/c/d/e/f", 25) == "/"


  * envset(VARNAME=VALUE, ...)

        orig = getenv("PATH")
        with tbx.envset(PATH='/somewhere/else'):
            assert "/somewhere/else" == getenv("PATH")
            ... do stuff with alternate $PATH ...
        assert orig == getenv("PATH")


  * raise Error('this is the error message')

        Traceback (most recent call last):
          File "<string>", line 1, in <module>
        tbx.Error: this is the error message


  * exists(path)

        assert tbx.exists(tbx.expand("$HOME")) == True
        assert tbx.exists("/no/such/file/on/this/system") == False


  * expand("HOME = $HOME = ~")

        "HOME = /usr/home/username = /usr/home/username"


  * fatal(MSG)

        tbx.fatal("The process ends now")


  * git_last_tag()

        assert tbx.git_last_tag() == '1.1.5'


  * git_hash(ref=None)

        assert tbx.git_hash() == '7cc775ddc...'
        assert tbx.git_hash('1.1.5') == '7cc775ddc...'
        assert tbx.git_hash('1.1.3') == '423543dd9...'


  * git_current_branch()

        assert tbx.git_current_branch() == 'edit-readme'


  * git_status()

        assert tbx.git_status() == (['CHANGELOG.md'], # staged, uncommitted
                                    ['README.md'],    # updated, unstaged
                                    ['.startup'])     # untracked, not in git


  * revnumerate(SEQUENCE)

        import string

        last = None
        count_up = 0
        for idx, item in revnumerate(string.ascii_uppercase):
            if last:
                assert idx = last - 1
            assert item == string.ascii_uppercase[idx]
            assert idx == len(string.ascii_uppercase) - count_up
            count_up += 1
            last = idx

  * run(CMD, input={str|StringIO|fd|file}, output={str|StringIO|fd|file})

        # By default, no input expected, output goes to return value
        result = run("echo This is a message")
        assert "This is a message\n" == result

        # output=<str>, redirect to a file
        result = run("echo This is a message", output="> myfile")
        # "This is a message" written to file myfile

        # output=<str>, redirect to a command
        result = run("echo This is a message", output="| cut -c1-14")
        assert "This is a mess\n" == result

        # output=<StringIO>
        StringIO abc
        run("echo This is a message", output=abc)
        assert abc.getvalue() == "This is a message\n"

        # output=<file descriptor>
        outfile = open("outfile", 'w')
        run("echo This is a message", output=outfile.fileno())
        # "This is a message\n" written to file outfile

        # output=<file object>
        outfile = open("outfile", 'w')
        run("echo This is a message", output=outfile)
        # "This is a message\n" written to file outfile

        # input=<str>, use content of string
        result = run("cat", input="This is a message\n")
        assert "This is a message\n" == result

        # input=<str>, read a file
        infile = local("infile")
        infile.write("This is a message\n")
        result = run("cat", input="< {}".format(infile.strpath))
        assert "This is a message\n" == result

        # input=<str>, input piped from a command
        result = run("cat", input="echo This is a message |")
        assert "This is a message\n" == result

        StringIO abc("This is a message\n")
        result = run("cat", input=abc)
        assert "This is a message\n" == result

        # input=<file-descriptor>
        infile = local("infile")
        infile.write("This is a message\n")
        f = open(infile.strpath, 'r')
        result = run("cat", input=f.fileno())
        assert "This is a message\n" == result

        # input=<file-object>
        result = run("cat", input=open(infile.strpath, 'r'))
        assert "This is a message\n" == result


## Running tests

        $ py.test

With a coverage report (must have coverage and pytest-cov installed):

        $ py.test --cov

With a coverage report showing the lines not tested

        $ py.test --cov --cov-report term-missing

## Notes

 * Notice that there is an assymetry between `run(<cmd>, input=<str>, ...)`
   and `run(<cmd>, ..., output=<str>)`.

    * Specifically, `input=<str>` can use the string directly as input, or
      use it as a redirection expression (`<cmd> |` or `> <path>`).

    * However, in the case of `output=<str>`, the called run function can't
      assign into the string named as the output argument. The output
      argument can use the string as a redirection expression, but that's all.
