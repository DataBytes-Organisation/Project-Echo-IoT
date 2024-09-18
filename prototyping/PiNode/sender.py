import comms
import time


class Sender:

    def __init__(self, database):

        self.server = None

        self.database = database



    def send_message(self, payload):

        print(f"sending {payload}")

        comms.send_message("udp://127.0.0.1:61667", str.encode(payload))


    def sender_thread(self):

        time.sleep(3)

        while True:

            # Do stuff here for each iteration, and send stuff when needed

            # Get all unsent Headers
            header = self.database.get_unsent_header()

            if header is not None:

                # HEADER TYPE   |  Image id | Number of pieces
                node_id = 1
                payload = '1'+'|'+ str(node_id) +'|'+str(header[0])+'|'+str(header[1])
                self.send_message(payload)



            requested = self.database.get_unsent_request()

            if requested is not None:

                node_id = 1
                payload = '3'+'|'+ str(node_id) +'|'+str(requested[0])+'|'+str(requested[1]) + '|'+str(requested[2])
                self.send_message(payload)

                #also, now we sent it, you can mark it as request fulfilled
                self.database.reset_request(str(requested[0]), str(requested[1]))

            time.sleep(2)





