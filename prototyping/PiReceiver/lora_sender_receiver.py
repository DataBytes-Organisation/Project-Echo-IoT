import comms
import paho.mqtt.client as mqtt
import time
import base64
import json
import binascii
import re
import ast

BROKER_ADDRESS = "au1.cloud.thethings.industries"
TOPIC = "v3/project-echo-mqtt@projectecho/devices/#"
PORT = 1883
USERNAME = "project-echo-mqtt@projectecho"
PASSWORD = "NNSXS.L2YSQUKS3DYMNUQRW2SSNKIUAYEOPB6VOOJNZ7A.BEG5Q24ESO2YJAZ7LRAFTF7J4PW4OAGKNYWFYFU7K35L5F253OLQ"

#This application specific information
APPLICATION_ID = "project-echo-mqtt@projectecho"
ACCESS_KEY = "3714DFE1003A4DAE79E2C58E9EEA0613"
DEVICE_ID = "echonode-001"

# MUST publish to the replace queue, else the push queue will fill up
PUBLISH_TOPIC = f"v3/{APPLICATION_ID}/devices/{DEVICE_ID}/down/replace"


class Receiver:

    def __init__(self, database):

        self.server = BROKER_ADDRESS
        self.database = database
        self.non_byte_comp = 16
        self.topic = TOPIC


    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker.")
            client.subscribe(TOPIC)  # Subscribe to the specified topic

        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):

        try:


            payload = msg.payload.decode()
            data = json.loads(payload)

            #Get the port, to ignore any outgoing messages

            downlink_port = data.get("downlink_sent", {}).get("f_port")

            # if downlink port is None i.e. its an uplink message
            if downlink_port is None:


                #Determine sender
                end_device = data.get('end_device_ids', {}).get('device_id')

                #Check if there is a payload, sometimes Nodes will send a blank msg

                uplink_payload = data.get('uplink_message', {}).get('frm_payload')

                if uplink_payload is not None:
                    #Determine message type (with the port value)

                    decoded_string = ""

                    #Split the payload for processing
                    try:
                        message_as_b64 = data.get('uplink_message', {}).get('frm_payload')
                        decoded_bytes = base64.b64decode(message_as_b64)
                        decoded_string = decoded_bytes.decode('utf-8', errors='ignore')


                    except Exception as e:

                        print(e)


                    split_parts = decoded_string.split('|')

                    node_id = int(re.search(r'\d+', end_device).group())

                    if int(split_parts[0]) == 0:

                        print(f"Pulse received from Node {end_device}")
                    # New Header has arrived
                    elif int(split_parts[0]) == 1:

                        image_id = int(split_parts[2])
                        number_of_pieces = int(split_parts[3])
                        filename = split_parts[4]
                        print(f"New Header arrived Node:{node_id} Image:{image_id} Number of Pieces {number_of_pieces}")
                        self.database.insert_header_and_empty_pieces(node_id, number_of_pieces,image_id,filename)

                    # New Heartbeat has arrived (not yet implemented)
                    elif int(split_parts[0]) == 2:
                        print(f"Heartbeat has Arrived: Node {node_id}")

                    # New Piece of image has arrived
                    elif int(split_parts[0]) == 3:

                        # We need to determine the length of the string components, plus 4 for the delim
                        total_length = len(split_parts[0]) + len(split_parts[1]) + len(split_parts[2]) + len(split_parts[3]) + 4

                        image_id = int(split_parts[2])
                        piece_id = int(split_parts[3])

                        print(f"Piece has Arrived: Node {node_id} Image:{image_id} Piece ID {piece_id}")

                        #Because we know the length of the string part of the data, we can simply insert the bytes from the raw bytes part
                        # which resolves any issues with lost data while converting
                        self.database.insert_a_piece(node_id, image_id, piece_id,
                                                     decoded_bytes[total_length:])





        except Exception as e:
            print(f"Error processing message: {e}")


    def check_for_outgoing_messages(self):

        # Here, we run a periodic check to see if there is any need of us to publish a message to mqtt queue
        # these will eventually forward to a Node if required

        #Assuming we've received the Header, and generated the empty space, let's find an empty piece
        empty_piece = self.database.find_empty_piece()

        # empty_piece = node id, image id, peice id,....
        if empty_piece is not None:

            #construct the string
            # which is node_id, image_id, piece_id
            payload_str = f"{int(empty_piece[0])}|{int(empty_piece[1])}|{int(empty_piece[2])}"
            string_bytes = payload_str.encode('utf-8')
            base64_payload = base64.b64encode(string_bytes).decode('utf-8')

            PUBLISH_TOPIC = f"v3/{APPLICATION_ID}/devices/echonode-00{int(empty_piece[0])}/down/replace"

            #construct the payload and send
            downlink_payload = {
                "downlinks": [
                    {
                        "f_port": 42,  # LoRaWAN port for incoming piece request
                        "frm_payload": base64_payload,  # Base64-encoded payload (e.g., "Hello World")
                        "priority": "NORMAL"  # Can be "NORMAL" or "HIGH"
                    }
                ]
            }

            self.client.publish(PUBLISH_TOPIC, json.dumps(downlink_payload))

            print(f"Sending Request to Node {payload_str} ")


    def receiver_thread(self):

        self.database.connect()

        # Initialize MQTT client and connect to the broker
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.username_pw_set(username=USERNAME, password=PASSWORD)

        try:
            self.client.connect(self.server, PORT, 60)
            print(f"Connecting to MQTT broker at {self.server}...")
            self.client.loop_start()  # Start the MQTT loop in a separate thread

            while True:

                self.check_for_outgoing_messages()
                time.sleep(5)  # Keep the thread running

                self.client.loop_stop()  #temporarily while we compile message


                self.database.find_ready_to_compile_image_ids()

                self.client.loop_start()

        except Exception as e:
            print(f"{e}")
            self.client.loop_stop()



