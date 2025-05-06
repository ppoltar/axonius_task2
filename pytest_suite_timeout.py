import pytest
import signal
from time import time

def pytest_addoption(parser):
    """
    Adds a custom command-line option to set a timeout for the entire test suite.

    Args:
        parser (pytest.Parser): The pytest parser object that manages command-line options.

    Options:
        --suite-timeout (int): Sets the timeout (in seconds) for the entire test suite to complete.
                               The default value is 900 seconds (15 minutes).
    """
    parser.addoption(
        "--suite-timeout",
        action="store",
        type=int,
        default=900,
        help="Set a timeout (in seconds) for the entire test suite"
    )

def _timeout_handler(signum, frame):
    """
    Handler function that is invoked when the test suite exceeds the timeout limit.

    Args:
        signum (int): The signal number.
        frame (frame): The current stack frame.

    Raises:
        SystemExit: Exits the pytest session and aborts all remaining tests with a custom message.
    """
    pytest.exit("❌ Test suite exceeded the timeout limit. Aborting all remaining tests.")

def pytest_sessionstart(session):
    """
     Initializes and sets up the timeout for the test session.

     This function is called before the test session starts. It retrieves the timeout
     value from the command line option `--suite-timeout` and sets up an alarm that
     will terminate the test session if the time limit is exceeded.

     Args:
         session (pytest.Session): The pytest session object representing the test session.

     Initializes the following session attributes:
         - session.start_time (float): Timestamp when the test session starts.
         - session.suite_timeout (int): Timeout value (in seconds) for the test session.
     """
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
    """
    Cleans up after the test session finishes, ensuring the alarm is disabled.

    This function is called after the test session has completed, regardless of success or failure.
    It cancels the signal alarm to prevent any further timeout handling after the session finishes.

    Args:
        session (pytest.Session): The pytest session object representing the test session.
        exitstatus (int): The exit status code of the test session (not used in this function).
    """
    signal.alarm(0)