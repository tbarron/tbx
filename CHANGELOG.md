## 1.0.6 ... 2018.0212

 * Write git functions and use them in test_deployable()

## 1.0.5 ... 2018.0130 15:52:42

 * Document and add examples for Error() and expand().
 * Rename expanduser() to _expanduser() to indicate that it is intended to
   be internal to the libary.
 * Improve legibility of CHANGELOG.md by separating version and date.

## 1.0.4 ... 2018.0112 13:29:52

 * tbx.run() used to return a byte array, now it always returns a str.
 * Starting to use pipenv (added Pipfile, Pipfile.lock).
 * Added test to verify that processes spawned under tbx.envset() reflect
   the adjusted environment.

## 1.0.3 ... 2018.0110 15:14:54

 - Update tbx.expand() to expand '~' even when it's not at the beginning of
   the input (which is what os.path.expanduser() does).

## 1.0.2 ... 2017.1224 20:19:03

 - Fix for breakage when setting a non-existent env var to None. We were
   attempting to del a key from os.environ that wasn't there.
 - Hold the version in version.py rather than hard-coding it in
   setup.py. In setup.py, make use of version._v.
 - Add test to verify that version._v matches the last git tag.
 - Rearrange the tests: lint first, version last.

## 1.0.1 ... 2017.1215 06:10:39

 * Improving CHANGELOG legibility

## 1.0.0 ... 2017.1215 05:52:20

 * Use coverage with pytest to see how completely the target code is
   tested
 * Test tweaks
 * More .gitignore items: .env, venv, .coverage*, ...
 * Use tox with travis to cover more Python versions
 * Add '--all' option to pytest
 * Add CHANGELOG.md (this file)
 * Wordsmithed README.md, separated function descriptions from examples

## 0.0.3 ... 2016.0723 10:03:32

 * New functions: contents(), dirname(), dispatch(), dispatch_help(),
   fatal(), revnumerate(), run()
 * New tests for contents(), dirname(), dispatch(), dispatch_help(),
   envset(), fatal(), revnumerate(), run()
 * New class: Error
 * Configure pytest: new file conftest.py
 * Use flake8 to assess code quality
 * Add function descriptions in README.md
 * Add Travis config file
 * Ignore emacs work files in .gitignore

## 0.0.2 ... 2016.0106 06:19:51

 * Add version in setup.py
 * Make package directory explicit

## 0.0.1 ... 2016.0106 06:11:05

 * Getting setup, adding .gitignore, etc.

## 0.0.0 ... 2016.0106 05:51:57

 * Repo started
