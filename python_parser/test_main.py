import sys

def test_python_version():
    assert sys.version_info >= (3, 0), "Python 3 or higher is required"

test_python_version()