"""
This module contains code relating to configuring the MQTT client for
"""

from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.client import ConnectFlags
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from .builder import BuilderBase
from .message_processor import MessageProcessor

CLIENT_ID = "python_ingestion_backend1"
CLIENT_TRANSPORT = "websockets"
SESSION_EXPIRY_INTERVAL = 30 * 60

class MQTTClientBuilder(BuilderBase):
    """
    Concrete implementation of builder.
    This builder builds an instance of paho.mqtt.client.Client connected to the
    IOT ingestion backend.
    """
    def build(self, **kwargs) -> None:
        """
        Builds paho.mqtt.client.Client and sets as result.

        Arguments:
            self
            **kwargs
                user_name: str
                password: str
                topic: str
                endpoint: str
        Returns:
            None
        """
        # pylint: disable=unused-argument
        def on_connect(
                client: mqtt.Client,
                userdata: Any,
                flags: ConnectFlags,
                reason_code: ReasonCode,
                properties: Properties
            ) -> None:
            """
            Callback set as on_callback property on Paho MQTT client.
            See https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client
            .Client.on_message:~:text=property-,on_connect,-%3A%20Callable%5B

            Arguments:
                client: mqtt.Client,
                userdata: Any,
                ConnectFlags,
                reason_code: ReasonCode,
                properties: Properties
            Returns:
                None
            """
            if reason_code.is_failure:
                print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
            else:
                # we should always subscribe from on_connect callback to be sure
                # our subscribed is persisted across reconnections.
                client.subscribe(kwargs["topic"])
                print("Connected to broker")

        def on_message(
                client: mqtt.Client,
                userdata: Any,
                msg: mqtt.MQTTMessage
            ) -> None:
            """
            Callback set as on_message property on Paho MQTT client.
            See https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client
            .Client.on_message:~:text=property-,on_message,-%3A%20Callable%5B

            Arguments:
                client: mqtt.Client,
                userdata: Any,
                msg: mqtt.MQTTMessage
            Returns:
                None
            """
            MessageProcessor().process(msg)
        # pylint: enable=unused-argument

        client: mqtt.Client = mqtt.Client(
            client_id=CLIENT_ID,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            transport=CLIENT_TRANSPORT,
            protocol=mqtt.MQTTv5
        )
        client.on_connect = on_connect
        client.on_message = on_message
        client.tls_set()
        client.username_pw_set(
            username=kwargs["user_name"],
            password=kwargs["password"]
        )

        properties: Properties = Properties(PacketTypes.CONNECT)
        properties.SessionExpiryInterval = SESSION_EXPIRY_INTERVAL # in seconds

        client.connect(kwargs["endpoint"],
            port=443,
            clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
            properties=properties,
            keepalive=30
        )
        self.result = client
