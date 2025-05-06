#  Axonius task2 - pytest-suite-timeout

## Features

- ⏱ Add a `--suite-timeout <seconds>` command-line option to define a maximum allowed runtime for your test suite.
- ❌ Automatically fails the test session with a clear error message if it exceeds the timeout.
- 🔌 Installable as a local pytest plugin using `pip install .` or in editable mode with `pip install -e .`.
- 🚫 No external dependencies required — built using Python standard library only.

---

## Installation

### Install locally (one-time usage):

```bash
pip install .
```

### Install in editable/development mode:
```bash
pip install -e .
```
🔁 Use -e (editable mode) if you plan to modify the plugin source code and want changes to reflect immediately.



### Usage
Run your pytest suite with the --suite-timeout option:

```bash
pytest --suite-timeout 600
```
This will abort the entire test suite if it runs longer than 600 seconds (10 minutes).

The default timeout is 900 seconds (15 minutes) if no value is provided.


### Example

```bash
pytest --suite-timeout 1200 tests/
```

Output when exceeding timeout:

❌ Test suite exceeded the timeout limit. Aborting all remaining tests in suite.


### Requirements
This plugin was implemented to satisfy the following constraints:

✅ Add a command-line option (--suite-timeout <seconds>) to define a per-suite timeout.
(e.g. a suite with many tests cannot run longer than 15 minutes)

✅ Fail all tests in the test suite when the timeout is exceeded, with a clear error.

✅ Installable locally via pip using a standard setup.py file.

✅ No third-party packages are used — built entirely with Python’s standard library.


### Platform Compatibility
✅ Works on Unix/Linux/macOS using signal.alarm().

⚠️ Not supported on Windows, since the signal.SIGALRM mechanism is not available on that platform.
