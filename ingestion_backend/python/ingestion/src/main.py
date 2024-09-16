"""
This module is the entry point for the python ingestion backend service.
It subscribes to the MQTT broker, listens to a topic and sends data to Echo Store
through Echo API.
"""

import os

from paho.mqtt.client import Client

from src.mqtt_client import MQTTClientBuilder

ENDPOINT = "iot.databytesprojectecho.com"
TOPIC = "iotdata"

USER_ENV_VAR = "IOT_USER"
USER_PASS_ENV_VAR = "IOT_PASSWORD"


class IOTIngestion:
    """
    Main class that runs the app. May appear redundant but creating a class for it makes testing easier.

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
        self.client: Client = MQTTClientBuilder().get(
            endpoint = endpoint,
            topic = topic,
            user_name = user_name,
            password = password
        )

    def run(self) -> None:
        """

        Arguments
            self
        Returns:
            None
        """
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
    app: IOTIngestion = IOTIngestion(
        endpoint = ENDPOINT,
        topic = TOPIC,
        user_name = os.environ[USER_ENV_VAR],
        password = os.environ[USER_PASS_ENV_VAR]
    )
    app.run()


if __name__ == "__main__":
    main()
