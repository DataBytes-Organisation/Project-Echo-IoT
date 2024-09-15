"""
This module contains code relating to the message processor class.
It's purpose is to receive a message from an MQTT topic to process.
"""

from paho.mqtt.client import MQTTMessage

# pylint: disable-next=too-few-public-methods
class MessageProcessor:
    """
    This class processes messages from the IOT backend ingestion broker.
    """
    def process(self, message: MQTTMessage) -> None:
        """
        <when implemented properly add description here>
        Currently just prints the message payload.

        Arguments:
            self
            message: MQTTMessage
                This is to payload to be processed
        Returns:
            None
        """
        print(message.topic +" "+ str(message.payload))
