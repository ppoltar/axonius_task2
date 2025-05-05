import pytest
from time import time

def pytest_addoption(parser):
    parser.addoption(
        "--suite-timeout",
        action="store",
        type=int,
        default=900,
        help="Set a timeout (in seconds) for the entire test suite"
    )

def pytest_sessionstart(session):
    timeout = session.config.getoption("--suite-timeout")
    if timeout:
        session.start_time = time()
        session.suite_timeout = timeout
    else:
        session.start_time = None
        session.suite_timeout = None

def pytest_collection_modifyitems(session, config, items):
    if session.suite_timeout is not None:
        session.exceeded_timeout = False

def pytest_runtest_setup(item):
    session = item.session
    if hasattr(session, "suite_timeout") and session.suite_timeout is not None:
        elapsed = time() - session.start_time
        if elapsed > session.suite_timeout:
            pytest.exit("Test suite exceeded timeout limit. Aborting test run.")

def pytest_runtest_call(item):
    if getattr(item.session, "exceeded_timeout", False):
        pytest.fail("Test suite exceeded timeout limit. All remaining tests are failed.")

