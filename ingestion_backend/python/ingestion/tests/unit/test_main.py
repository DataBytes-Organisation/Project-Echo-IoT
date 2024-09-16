"""
This module contains pytest unit tests for src.main.py
"""

import os
from unittest.mock import patch, Mock

from ingestion.src.main import main, IOTIngestion, ENDPOINT, TOPIC, USER_ENV_VAR, USER_PASS_ENV_VAR

###############################################################################################
# IOTIngestion tests
###############################################################################################

def test_iotingestion_run():
    """
    Tests IOTIngestion runs and creates client with the correctly passed variables.
    """
    # vars to test with
    test_endpoint: str = "https://dummyendpointurl",
    test_topic: str = "dummytopic",
    test_user: str = "dummyuser"
    test_password: str = "dummypassword"

    mock_builder: Mock = Mock()
    mock_client: Mock = Mock()
    mock_client.username_pw_set = Mock()
    mock_builder.get = Mock(return_value=mock_client)

    with patch("ingestion.src.main.MQTTClientBuilder", return_value=mock_builder):
        app: IOTIngestion = IOTIngestion(
            test_endpoint,
            test_topic,
            test_user,
            test_password
        )
        app.run()

        # assert builder called with correct vars
        mock_builder.get.assert_called_with(
            endpoint = test_endpoint,
            topic = test_topic,
            user_name = test_user,
            password = test_password
        )
        # asssert loop forever called
        app.client.loop_forever.assert_called()

###############################################################################################
# main (function) tests
###############################################################################################

@patch.dict(
        os.environ,
        {USER_ENV_VAR: "dummyuser", USER_PASS_ENV_VAR: "dummypassword"},
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
            endpoint = ENDPOINT,
            topic = TOPIC,
            user_name = os.environ[USER_ENV_VAR],
            password = os.environ[USER_PASS_ENV_VAR]
        )
        mock_iotingestion.run.assert_called()
