"""
This module contains pytest unit tests for ingestion.src.mqtt_client
"""

from typing import Dict
from unittest.mock import patch, Mock

from ingestion.src.mqtt_client import MQTTClientBuilder


###############################################################################################
# MQTTClientBuilder tests
###############################################################################################

def test_mqttclientbuilder_build(app_kwargs: Dict[str, str]):
    """
    Tests MQTTClientBuilder calls the appropriate methods to build the MQTT client.

    Arguments:
        app_kwargs: Dict[str, str]
            Pytest fixture containing application arguments.
    """
    client_mock: Mock = Mock()
    client_mock.connect = Mock()
    client_mock.username_pw_set = Mock()
    with patch("ingestion.src.mqtt_client.mqtt.Client", return_value=client_mock):
        MQTTClientBuilder().get(**app_kwargs)
        client_mock.connect.assert_called()
        client_mock.username_pw_set.assert_called_with(
            username = app_kwargs["user_name"],
            password = app_kwargs["password"]
        )
