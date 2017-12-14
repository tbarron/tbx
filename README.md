# Toolbox library in python

## Functions

 * chdir(path)
    * Context manager that allows directory excursions that
      automagically return to your starting point upon exiting the
      with scope.

 * contents(name, default=None, fmt='str', sep='\n')
    * Return the contents of a file. If the file does not exist,
      return *default*. If *fmt* is 'list', the return value is a list
      of strings. If *fmt* is 'str', the return value is a string. If
      *sep* is not specified and *fmt* is 'list', the file content
      will be split on newlines ('\n')

 * dirname(path, level=1)
    * Return the directory parent of *path*. If *level* is something
      other 1, *level* path components are removed from the path.

 * dispatch(mname, prefix, args)
    * Introspect module *mname* for a callable named *prefix*_*args[0]*. If
      found, call it with arguments *args[1:]*

 * dispatch_help(mname, prefix, args)
    * Introspect module *mname* and print help info from __doc__
      strings for callables with names [*prefix*_foo for foo in args].
      If *args* is empty, print the first line of each __doc__ for all
      the callables in the module whose name begins with *prefix*

 * envset(VARNAME=VALUE, ...)
    * Context manager that sets one or more environment variables,
      returning them to their original values when control leaves the
      context.

          orig = getenv("PATH")
          with tbx.envset(PATH='/somewhere/else'):
              assert "/somewhere/else" == getenv("PATH")
              ... do stuff with alternate $PATH ...
          assert orig == getenv("PATH")

 * fatal(msg)
    * Print *msg* and exit the process

 * revnumerate(sequence)
    * Enumerate *sequence* in reverse. The numbers count down from
      len(*sequence*)-1 to 0

 * run(cmd, input={str|StringIO|fd|file},
            output={str|StringIO|fd|file})
    * If *input* (or *output*) is a str that begins with '<', the path
      named in the argument will be read and its contents will be
      written to stdin of the command. If a str *input* ends with '|'
      the argument will be run as a command and its output will be
      written to stdin of the payload command.

### Examples

  * chdir(PATH)

      orig = getcwd()
      with tbx.chdir("/other/directory"):
          assert "/other/directory" == getcwd()
          ... do work in "/other/directory"
      assert orig == getcwd()

## Running tests

        $ py.test

With a coverage report (must have coverage and pytest-cov installed):

        $ py.test --cov

With a coverage report showing the lines not tested

        $ py.test --cov --cov-report term-missing
