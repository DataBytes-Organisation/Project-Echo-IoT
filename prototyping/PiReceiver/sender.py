import comms
import time
from PIL import Image
import io

class Sender:

    def __init__(self, database):

        self.server = None
        self.database = database


    def send_message(self, payload):

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

                print(self.database.get_unique_image_ids())

                for each in self.database.get_unique_image_ids():
                    if self.database.image_complete(each):

                        image_bytes = b''
                        pieces = self.database.get_all_pieces(1,each)

                        for piece in pieces:
                            image_bytes += piece[3]

                        filename = str(each) + '_output.jpg'
                        print(f"Attempting to reconstruct completed file {filename}")
                        bin_file = open(filename, 'wb')
                        bin_file.write(image_bytes)
                        bin_file.close()


                        #Remove the component peices from database

                        self.database.delete_image(each)

                time.sleep(10)
            time.sleep(.1)





