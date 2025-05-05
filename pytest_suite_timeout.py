import pytest
import signal
from time import time

def pytest_addoption(parser):
    parser.addoption(
        "--suite-timeout",
        action="store",
        type=int,
        default=10,
        help="Set a timeout (in seconds) for the entire test suite"
    )

def _timeout_handler(signum, frame):
    pytest.exit("❌ Test suite exceeded the timeout limit. Aborting all remaining tests.")

def pytest_sessionstart(session):
    timeout = session.config.getoption("--suite-timeout")
    session.start_time = time()
    if timeout:
        session.suite_timeout = timeout
        # Set signal alarm to abort the entire process after timeout (Unix only)
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout)
    else:
        session.suite_timeout = None

def pytest_sessionfinish(session, exitstatus):
    # Cancel the alarm if still active
    signal.alarm(0)