import comms

class Receiver:

    def __init__(self, database):

        self.server = None
        self.database = database
        self.non_byte_comp = 16

    def receive_message(self):


        payload = comms.receive_message(self.server)


        # Do something when you receive a message
        # Check Byte

        incoming_payload = payload[:self.non_byte_comp].decode().split('|')

        # NEW HEADER HAS ARRIVED
        if int(incoming_payload[0]) == 1:

            node_id = int(incoming_payload[1])
            image_id = int(incoming_payload[2])
            number_of_pieces = int(incoming_payload[3])
            print(f"New Header arrived Node:{node_id} Image:{image_id} NUmber of Pieces {number_of_pieces}")
            self.database.insert_empty_pieces(node_id, number_of_pieces,image_id)


        if int(incoming_payload[0]) == 3:

            length_of_not_byte_component = 16

            further_decoded = payload[:self.non_byte_comp].decode().split('|')

            node_id = int(further_decoded[1])
            image_id = int(further_decoded[2])
            piece_id = int(further_decoded[3])
            piece = payload[self.non_byte_comp:]
            print(f"New Piece arrived Node:{node_id} Image:{image_id} Piece{piece_id}")

            self.database.insert_a_piece(node_id, image_id, piece_id, piece)
    def receiver_thread(self):

        self.server = comms.receive_connect(bind = "udp://*:61667")

        while True:

            self.receive_message()





