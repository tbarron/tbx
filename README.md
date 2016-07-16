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

 * envset
    * Context manager that sets one or more environment variables,
      returning them to their original values when control leaves the
      context.

 * 