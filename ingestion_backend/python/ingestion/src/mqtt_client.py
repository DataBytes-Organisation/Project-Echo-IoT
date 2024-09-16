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


class OnConnectCallbackBuilder(BuilderBase):
    """
    Builds callback callable used as on_connect callback on Paho MQTT client.
    """
    def build(self, topic: str) -> None:
        """
        Builds callback callable used as on_connect callback on Paho MQTT client.

        Arguments:
            self
            topic: str
                MQTT topic on broker to subscribe to
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
                client.subscribe(topic)
                print("Connected to broker")
        # pylint: enable=unused-argument
        self.result = on_connect


class OnMessageCallbackBuilder(BuilderBase):
    """
    Builds callback callable used as on_message callback on Paho MQTT client.
    """
    def build(self) -> None:
        """
        Builds callback callable used as on_message callback on Paho MQTT client.

        Arguments:
            self
            topic: str
                MQTT topic on broker to subscribe to
        Returns:
            None
        """
        # pylint: disable=unused-argument
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
        self.result = on_message


class MQTTClientBuilder(BuilderBase):
    """
    Concrete implementation of builder.
    This builder builds an instance of paho.mqtt.client.Client connected to the
    IOT ingestion backend.
    """
    def build(
            self,
            user_name: str,
            password: str,
            topic: str,
            endpoint: str
    ) -> None:
        """
        Builds paho.mqtt.client.Client and sets as result.

        Arguments:
            self
            user_name: str
            password: str
            topic: str
            endpoint: str
        Returns:
            None
        """
        client: mqtt.Client = mqtt.Client(
            client_id=CLIENT_ID,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            transport=CLIENT_TRANSPORT,
            protocol=mqtt.MQTTv5
        )

        client.on_connect = OnConnectCallbackBuilder().get(topic=topic)
        client.on_message = OnMessageCallbackBuilder().get()
        client.tls_set()
        client.username_pw_set(
            username=user_name,
            password=password
        )

        properties: Properties = Properties(PacketTypes.CONNECT)
        properties.SessionExpiryInterval = SESSION_EXPIRY_INTERVAL # in seconds

        client.connect(endpoint,
            port=443,
            clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
            properties=properties,
            keepalive=30
        )
        self.result = client
