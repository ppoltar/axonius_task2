from setuptools import setup

setup(
    name="pytest-suite-timeout",
    version="0.1",
    py_modules=["pytest_suite_timeout"],
    entry_points={
        "pytest11": [
            "suite_timeout = pytest_suite_timeout",
        ],
    },
)