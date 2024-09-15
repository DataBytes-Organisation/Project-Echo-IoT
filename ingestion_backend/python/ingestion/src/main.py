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
    mqtt_client: Client = MQTTClientBuilder().get(
        endpoint = ENDPOINT,
        topic = TOPIC,
        user_name = os.environ["IOT_USER"],
        password = os.environ["IOT_PASSWORD"]
    )
    mqtt_client.loop_forever()

if __name__ == "__main__":
    main()
