## 1.0.3 2018.0110

 - Update tbx.expand() to expand '~' even when it's not at the beginning of
   the input (which is what os.path.expanduser() does).

## 1.0.2 2017.1224

 - Fix for breakage when setting a non-existent env var to None. We were
   attempting to del a key from os.environ that wasn't there.
 - Hold the version in version.py rather than hard-coding it in
   setup.py. In setup.py, make use of version._v.
 - Add test to verify that version._v matches the last git tag.
 - Rearrange the tests: lint first, version last.

## 1.0.1 2017.1215

 * Improving CHANGELOG legibility

## 1.0.0 2017.1215

 * Use coverage with pytest to see how completely the target code is
   tested
 * Test tweaks
 * More .gitignore items: .env, venv, .coverage*, ...
 * Use tox with travis to cover more Python versions
 * Add '--all' option to pytest
 * Add CHANGELOG.md (this file)
 * Wordsmithed README.md, separated function descriptions from examples

## 0.0.3 2016.0723

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

## 0.0.2 2016.0106

 * Add version in setup.py
 * Make package directory explicit

## 0.0.1 2016.0106

 * Getting setup, adding .gitignore, etc.

## 0.0.0 2016.0106

 * Repo started
