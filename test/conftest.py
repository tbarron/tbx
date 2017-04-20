"""
Configure pytest
"""
import os
import pdb
import sys

import pytest


# -----------------------------------------------------------------------------
def pytest_addoption(parser):
    """
    Add options --nolog, --all to the command line
    """
    # pdb.set_trace()
    parser.addoption("--dbg", action="append", default=[],
                     help="start debugger on named test or all")
    parser.addoption("--all", action="store_true", default=False,
                     help="suppress -x, run all tests")
    parser.addoption("--skip", action="append", default=[],
                     help="skip named test(s)")
    sys.path.append(os.getcwd())


# -----------------------------------------------------------------------------
def pytest_configure(config):
    """
    Stuff to do at config time
    """
    if "../tbx" not in sys.path:
        sys.path.append("../tbx")

    # If --all and -x, turn off -x, that is, I like to have -x (fail fast, exit
    # on the first failure) turned on by default. But if I've put --all on the
    # command line, I want to override the -x (config.option.exitfirst) so turn
    # it off.
    if config.getoption("--all"):
        if "exitfirst" in config.option.__dict__:
            config.option.__dict__["exitfirst"] = False
        if "maxfail" in config.option.__dict__:
            config.option.__dict__["maxfail"] = 200


# -----------------------------------------------------------------------------
def pytest_runtest_setup(item):
    """
    Decide whether to skip a test before running it
    """
    dbg_n = '..' + item.name
    dbg_l = item.config.getvalue('dbg')
    skip_l = item.config.getvalue('skip')
    if any([item.name in skip_l,
            any([x in item.name for x in skip_l])]):
        pytest.skip('Skipping at user request')

    if dbg_n in dbg_l or '..all' in dbg_l:
        pdb.set_trace()

    if any([item.name in item.config.getoption('--dbg'),
            any([x in item.name for x in item.config.getoption('--dbg')]),
            'all' in item.config.getoption('--dbg')]):
        pytest.dbgfunc = pdb.set_trace
    else:
        pytest.dbgfunc = lambda: None
