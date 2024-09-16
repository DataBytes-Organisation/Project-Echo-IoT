"""
This module is the entry point for the python ingestion backend service.
It subscribes to the MQTT broker, listens to a topic and sends data to Echo Store
through Echo API.
"""

import os
import logging

from paho.mqtt.client import Client

from src.app_logging import LogConfigurator
from src.constants import LOGGER_NAME
from src.mqtt_client import MQTTClientBuilder

LOGGER = logging.getLogger(LOGGER_NAME + "." + __name__)
LogConfigurator.configure_logger(LOGGER)

ENDPOINT_ENV_VAR = "IOT_ENDPOINT"
TOPIC_ENV_VAR = "IOT_TOPIC"
USER_ENV_VAR = "IOT_USER"
USER_PASS_ENV_VAR = "IOT_PASSWORD"


class IOTIngestion:
    """
    Main class that runs the app. May appear redundant but creating a class for it
    makes testing easier.

    Arguments:
        self,
        endpoint: str
            MQTT broker endpoint url
        topic: str
            MQTT topic to subscribe to
        user_name: 
            Username used to connect to broker
        password: str
            Password for user to connect to broker
    """
    def __init__(
        self,
        endpoint: str,
        topic: str,
        user_name: str,
        password: str
        ):
        LOGGER.info("Getting MQTT client.")
        self.client: Client = MQTTClientBuilder().get(
            endpoint = endpoint,
            topic = topic,
            user_name = user_name,
            password = password
        )
        LOGGER.info("Gotten MQTT client.")

    def run(self) -> None:
        """

        Arguments
            self
        Returns:
            None
        """
        LOGGER.info("MQTT client looping forever.")
        self.client.loop_forever()


def main() -> None:
    """
    Runs the iot ingestion backend service program.
    Creates a configured Paho MQTT client (its on_message callback processes messages)
    and runs it.

    Arguments:
        None
    Returns:
        None
    """
    LOGGER.info("Initialising IOTIngestion application.")
    app: IOTIngestion = IOTIngestion(
        endpoint = os.environ[ENDPOINT_ENV_VAR],
        topic = os.environ[TOPIC_ENV_VAR],
        user_name = os.environ[USER_ENV_VAR],
        password = os.environ[USER_PASS_ENV_VAR]
    )
    LOGGER.info("Initialised. Running now.")
    app.run()


if __name__ == "__main__":
    LOGGER.info("__name__ is main. Calling main().")
    main()
