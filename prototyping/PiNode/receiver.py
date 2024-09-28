import comms
import time

class Receiver:

    def __init__(self,database):

        self.server = None
        self.database = database


    def receive_message(self):


        payload = comms.receive_message(self.server)


        # Do something when you receive a message
        # Check Byte
        incoming_payload = payload.decode().split('|')

        # NEW HEADER HAS ARRIVED
        if int(incoming_payload[0]) == 7:



            image_id = int(incoming_payload[1])
            piece_id = int(incoming_payload[2])
            print(f"New Request arrived  - image_id:{image_id} piece_id:{piece_id}")
            self.database.request_piece(image_id, piece_id)

            # We also treat this as an Ack for a received Header message

            self.database.ack_header(image_id)



    def receiver_thread(self):
        time.sleep(1)
        self.server = comms.receive_connect(bind = "udp://*:61666")

        while True:

            self.receive_message()





