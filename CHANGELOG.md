## 1.1.8 ...

 * User facing
    * Add payload and test for randomize, lglob, collect_missing_docs,
      caller_name, my_name, isnum_str, cmkdir
    * Add tests for git_hash, git_last_tag, git_current_branch, git_status
    * Support list value in sep arg to tbx.contents()

 * Internal
    * Test coverage tracking and reporting
    * Simplify git_current_branch()
    * Test for git_hash that does not depend on a specific hash value
    * .gitignore TAGS, .tbx-cov, etc.
    * Update version string


## 1.1.7 ... 2020-01-26 08:31:27

 * User Facing
    * Applying the unlicense: "This is free and unencumbered software released
      into the public domain. For more information, please refer to
      <http://unlicense.org/>" (LICENSE, README.md, setup.py, tbx/__init__.py,
      tbx/verinfo.py, test/conftest.py, test/test_tbx.py)

 * Internal
    * .gitignore egg-info directories and file .project (.gitignore)
    * Upgraded pip, install . editably for development (requirements.txt)
    * Set minimum python version, deliver data files, set the license (setup.py)
    * Drop Pipfile, Pipfile.lock

## 1.1.6 ... 2019-11-17 09:25:15

 * Test both Python 3.6 and 3.8 in continuous integration (on travis)
 * Add tests and payload for segments argument in tbx.basename() and
   tbx.dirname()
 * Argument 'level' in tbx.dirname() is deprecated in favor of 'segments'.
   Argument 'level' will be removed in release 1.2.0.
 * Document missing functions in README.md, moving examples up close to
   their respective function descriptions
 * Add list of projects that depend on this one to the bottom of README.md


## 1.1.5 ... 2019-10-13 16:54:24

 * Avoid "import this" to get the Zen of Python -- just hardcode it
   internally.
 * Remove obsolete imports.
 * Update .travis.yml to drop support for Python 2.7.

## 1.1.4 ... 2019-10-13 15:00:47

 * Don't build for Python 2.6.
 * Fix call to io.StringIO in test_tbx.get_this() to not attempt to
   initialize the StringIO object -- Python 2.7 was complaining about this.
 * Stringify the arguments to tbx.exists() to keep Python 2.7 happy.

## 1.1.3 ... 2019-10-13 14:37:28

 * Update .travis.yml to only build tagged versions and branch 'travis'.

## 1.1.2 ... 2019-10-13 10:17:10

 * Back in 2018, I wrote random_path() to generate random relative paths
   for testing tbx.abspath(), tbx.exists(), and tbx.basename(). This was
   fine on my machine where I own all the files. It was not such a good
   idea on, say, Travis' (the CI service) machines where my code has no
   business peeking over into the directories of other processes. I have
   rewritten those tests to behave more responsibly and predictably.

## 1.1.1 ... 2019-10-13 09:52:00

 * On Travis, only build branches 'master' and 'travis'

## 1.1.0 ... 2019-10-13 09:34:56

 * Remove fx_deprecated, the tests that used it, and the old tbx.dispatch()
   functionality the tests covered
 * Tweaks to keep flake happy with the code quality
    * Remove an unused module (warnings)
    * Prefix strings containing escapes with 'r'

## 1.0.9 ... 2019-10-12 09:57:08

 * Remove version.py from top level directory

## 1.0.8 ... 2019.1012 09:51:00

 * Update setup.py, tbx/__init__.py, and tests to import verinfo from tbx

## 1.0.7 ... 2018.0215 06:54:41

 * Add tests and support for tbx.abspath(), tbx.basename(), and
   tbx.exists(). (Requires function random_path for testing.)
 * Ensure all tests are debuggable with --dbg
 * Deprecate dispatch(), dispatch_help() and update tests to verify the
   deprecation warnings.
 * Bug in git_status due to loss of meaningful leading whitespace in 'git
   status --porc' output.

## 1.0.6 ... 2018.0212 16:00:08

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
