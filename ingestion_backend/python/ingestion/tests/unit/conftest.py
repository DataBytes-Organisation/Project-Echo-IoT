"""
This is a test configuration file for pytest.

It is used for storing code & config common to all pytest tests for the direction including:

* Fixtures
* Hooks
* Plugins

https://www.geeksforgeeks.org/conftest-in-pytest/

"""

from typing import Dict

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

@pytest.fixture(name="app_kwargs", scope="function")
def get_app_kwargs() -> Dict[str, str]:
    """
    Pytest fixture that provides application testing arguments.

    Returns:
        Dict[str, str]
            Dict with application testing arguments.
    """
    return {
        "endpoint": "https://dummyendpointurl",
        "topic": "dummytopic",
        "user_name": "dummyuser",
        "password": "dummypassword"
    }
