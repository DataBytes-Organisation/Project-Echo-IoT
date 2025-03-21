import paho.mqtt.client as mqtt
import time
import base64
import json
import binascii



class Receiver:

    def __init__(self, database, broker_address="au1.cloud.thethings.industries", topic="default/topic"):
        self.client = None
        self.database = database
        self.broker_address = broker_address
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker.")
            client.subscribe("#")  # Subscribe to the specified topic
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:


            payload = msg.payload.decode()
            data = json.loads(payload)

            end_device = data.get('end_device_ids', {}).get('device_id')
            print(f"Message from: {end_device}")

            message_as_b64 = data.get('uplink_message', {}).get('frm_payload')

            decoded_bytes = base64.b64decode(message_as_b64)
            hex_string = binascii.hexlify(decoded_bytes).decode('utf-8')
            print(f"Message: {hex_string}")
            #
            # # NEW HEADER HAS ARRIVED
            # if int(incoming_payload[0]) == 7:
            #     image_id = int(incoming_payload[1])
            #     piece_id = int(incoming_payload[2])
            #     print(f"New Request arrived - image_id:{image_id}, piece_id:{piece_id}")
            #     # self.database.request_piece(image_id, piece_id)

                # Treat this as an Ack for a received Header message
                # self.database.ack_header(image_id)
        except Exception as e:
            print(f"Error processing message: {e}")

    def receiver_thread(self):
        # Initialize MQTT client and connect to the broker
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.username_pw_set(username="project-echo-mqtt@projectecho", password="NNSXS.L2YSQUKS3DYMNUQRW2SSNKIUAYEOPB6VOOJNZ7A.BEG5Q24ESO2YJAZ7LRAFTF7J4PW4OAGKNYWFYFU7K35L5F253OLQ")

        try:
            self.client.connect(self.broker_address, 1883, 60)
            print(f"Connecting to MQTT broker at {self.broker_address}...")
            self.client.loop_start()  # Start the MQTT loop in a separate thread

            while True:
                time.sleep(1)  # Keep the thread running

        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            self.client.loop_stop()

database = "test"
receiver = Receiver(database)
receiver.receiver_thread()