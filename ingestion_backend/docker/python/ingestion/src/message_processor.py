"""
This module contains code relating to the message processor class.
It's purpose is to receive a message from an MQTT topic to process.
"""

import logging

from paho.mqtt.client import MQTTMessage

from .constants import LOGGER_NAME

LOGGER = logging.getLogger(LOGGER_NAME + "." + __name__)

class MessageProcessor:
    """
    This class processes messages from the IOT backend ingestion broker.
    """
    def process(self, message: MQTTMessage) -> None:
        """
        <when implemented properly add description here>
        Currently just logs the message payload.

        Arguments:
            self
            message: MQTTMessage
                This is to payload to be processed
        Returns:
            None
        """
        LOGGER.info(message.topic + " " + str(message.payload))
