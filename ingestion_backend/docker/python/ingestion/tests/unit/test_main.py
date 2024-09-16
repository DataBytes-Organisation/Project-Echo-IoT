"""
This module contains pytest unit tests for src.main.py
"""

import os
from typing import Dict
from unittest.mock import patch, Mock

from ingestion.src.main import main, IOTIngestion, ENDPOINT_ENV_VAR, TOPIC_ENV_VAR, USER_ENV_VAR,\
    USER_PASS_ENV_VAR


###############################################################################################
# IOTIngestion tests
###############################################################################################

def test_iotingestion_run(app_kwargs: Dict[str, str]):
    """
    Tests IOTIngestion runs and creates client with the correctly passed variables.

    Arguments:
        app_kwargs: Dict[str, str]
            Pytest fixture containing application arguments.
    """
    mock_builder: Mock = Mock()
    mock_client: Mock = Mock()
    mock_client.username_pw_set = Mock()
    mock_builder.get = Mock(return_value=mock_client)

    with patch("ingestion.src.main.MQTTClientBuilder", return_value=mock_builder):
        app: IOTIngestion = IOTIngestion(
            **app_kwargs
        )
        app.run()

        # assert builder called with correct vars
        mock_builder.get.assert_called_with(
            **app_kwargs
        )
        # asssert loop forever called
        # pylint: disable-next=no-member
        app.client.loop_forever.assert_called()


###############################################################################################
# main (function) tests
###############################################################################################

@patch.dict(
        os.environ,
        {
            ENDPOINT_ENV_VAR: "https://dummyendpoint.com",
            TOPIC_ENV_VAR: "dummytopic",
            USER_ENV_VAR: "dummyuser",
            USER_PASS_ENV_VAR: "dummypassword"
        },
        clear=True
)
def test_main():
    """
    Tests main() calls IOTIngestion with expected values and also calls IOTIngestion.run()
    to start application
    """
    mock_iotingestion: Mock = Mock()
    mock_iotingestion.run = Mock()
    with patch(
        "ingestion.src.main.IOTIngestion",
        return_value = mock_iotingestion
    ) as iotingestion_call:
        main()
        iotingestion_call.assert_called_with(
            endpoint = os.environ[ENDPOINT_ENV_VAR],
            topic = os.environ[TOPIC_ENV_VAR],
            user_name = os.environ[USER_ENV_VAR],
            password = os.environ[USER_PASS_ENV_VAR]
        )
        mock_iotingestion.run.assert_called()
