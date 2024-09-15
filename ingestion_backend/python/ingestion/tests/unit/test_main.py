"""
This module contains pytest unit tests for src.main.py
"""

import os
from unittest import mock

from ingestion.src.main import main

@mock.patch.dict(os.environ, {"DATABASE_URL": "mytemp"}, clear=True)
def test_main():
    """
    Tests main() runs.
    """
    with patch("from ...src.main.MQTTClientBuilder"):
        main()
