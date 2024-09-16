"""
"""

from typing import Dict
from unittest.mock import patch, Mock

from ingestion.src.mqtt_client import MQTTClientBuilder, OnConnectCallbackBuilder,\
    OnMessageCallbackBuilder

###############################################################################################
# MQTTClientBuilder tests
###############################################################################################

def test_mqttclientbuilder_build(app_kwargs: Dict[str, str]):
    """
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
