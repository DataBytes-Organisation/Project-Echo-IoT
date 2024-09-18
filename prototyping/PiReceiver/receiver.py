import comms

class Receiver:

    def __init__(self, database):

        self.server = None
        self.database = database


    def receive_message(self):


        payload = comms.receive_message(self.server)


        # Do something when you receive a message
        # Check Byte
        incoming_payload = payload.decode().split('|')

        # NEW HEADER HAS ARRIVED
        if int(incoming_payload[0]) == 1:
            print("New Header arrived")
            node_id = int(incoming_payload[1])
            image_id = int(incoming_payload[2])
            number_of_pieces = int(incoming_payload[3])
            print(node_id, image_id, number_of_pieces)
            self.database.insert_empty_pieces(node_id, number_of_pieces,image_id)


        if int(incoming_payload[0]) == 3:
            print("New Piece arrived")
            node_id = int(incoming_payload[1])
            image_id = int(incoming_payload[2])
            piece_id = int(incoming_payload[3])
            piece = bytes(incoming_payload[4], encoding='utf8')

            print(node_id, image_id, piece_id, piece)
            self.database.insert_a_piece(node_id, image_id, piece_id, piece)
    def receiver_thread(self):

        self.server = comms.receive_connect(bind = "udp://*:61667")

        while True:

            self.receive_message()





