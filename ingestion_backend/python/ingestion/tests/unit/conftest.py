"""
This is a test configuration file for pytest.

It is used for storing code & config common to all pytest tests for the direction including:

* Fixtures
* Hooks
* Plugins

https://www.geeksforgeeks.org/conftest-in-pytest/

"""
from typing import Callable

import pytest

@pytest.fixture(name="hello_world", scope="function")
def hello_world() -> str:
    """
    Pytest fixture that returns hello world

    Parameters:
        None
    Returns:
        str
            Provides a function scoped pytest fixture "hello_world" that contains the string
            hello world.
    """
    return "hello world"
