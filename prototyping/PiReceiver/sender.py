import comms
import time
from PIL import Image

class Sender:

    def __init__(self, database):

        self.server = None
        self.database = database


    def send_message(self, payload):

        print(f"sending {payload}")

        comms.send_message("udp://127.0.0.1:61666", str.encode(payload))


    def sender_thread(self):



        while True:

            # Do stuff here for each iteration, and send stuff when needed
            # Find empty pieces in the database
            empty_piece = self.database.find_empty_piece()

            # empty_piece = node id, image id, peice id,....
            if empty_piece is not None:

                self.send_message('7|' + str(empty_piece[1])+'|'+str(empty_piece[2]))

            else:

                #Try to reconstruct
                image_bytes = ""
                pieces = self.database.get_all_pieces(1,1)

                for piece in pieces:
                    # image_bytes += piece[3]
                    print(piece)
                print(len(image_bytes))
            time.sleep(.1)





