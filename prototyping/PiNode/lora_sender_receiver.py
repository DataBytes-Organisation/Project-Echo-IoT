
import time
import serial
import re

PORT = "/dev/serial0"
BAUD_RATE = 115200
TIMEOUT = 1

# REGEX Defs for incoming messages

TX_DONE = r"\+EVT:TX_DONE"
TX_LOCKED = r"AT_BUSY_ERROR"
TX_RECEIVED = r"\+EVT:RX_"

class LoraSenderReceiver():

    def __init__(self, database):

        self.server = None
        self.uart = None
        self.database = database



    def send_message(self, payload, type):

        #Construct the full payload
        port = 2
        if type == "HEADER":
            port = 1
        if type == "PIECE":
            port = 3

        hex_payload = payload.hex().upper()
        at_command = f"AT+SEND={port}:{hex_payload}\r\n"

        try:
            print(f"Sending cmd: {at_command}")

            self.uart.write(at_command.encode('utf-8'))


            # Read response until 5 blank lines are encountered
            blank_line_count = 0
            response = []

            while blank_line_count < 5:
                line = self.uart.read_until(b'\r\n').decode('utf-8').strip()

                if line:  # Non-blank line
                    #print(f"Response Line: {line}")
                    response.append(line)
                    blank_line_count = 0  # Reset blank line count
                else:  # Blank line
                    blank_line_count += 1

            # Combine the response into a single string
            full_response = "\n".join(response)
            # print(f"Full Response:\n{full_response}")

            return full_response
        except Exception as e:
            print(f"Error communicating with device: {e}")
            return None

    def send_long_message(self, payload, type):

        #Construct the full payload
        port = 2
        if type == "HEADER":
            port = 1
        if type == "PIECE":
            port = 3

        hex_payload = payload.hex().upper()
        at_command = f"AT+LPSEND={port}:0:{hex_payload}\r\n"

        try:
            print(f"Sending cmd: {at_command}")

            self.uart.write(at_command.encode('utf-8'))


            # Read response until 5 blank lines are encountered
            blank_line_count = 0
            response = []

            while blank_line_count < 5:
                line = self.uart.read_until(b'\r\n').decode('utf-8').strip()

                if line:  # Non-blank line
                    #print(f"Response Line: {line}")
                    response.append(line)
                    blank_line_count = 0  # Reset blank line count
                else:  # Blank line
                    blank_line_count += 1

            # Combine the response into a single string
            full_response = "\n".join(response)
            # print(f"Full Response:\n{full_response}")

            return full_response
        except Exception as e:
            print(f"Error communicating with device: {e}")
            return None
    def lora_thread(self):

        time.sleep(3)

        #Initiate connection to lora radio via serial port

        try:

            self.uart = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
            self.uart.reset_input_buffer()
            self.uart.reset_output_buffer()

        except serial.serialutil.SerialException as e:
            print(f"Error opening port {PORT}: {e}")
            exit()

        # Enter the infinite loop
        # flag to send a blank message to check for new messages
        send_event = False
        while True:

            # Do stuff here for each iteration, and send stuff when needed

            #After sending, you'll get a list of responses, store those for processing
            list_of_responses = None

            if send_event:
                #We need to send a blank message, this is actioned when we have a loop of nothing
                list_of_responses = re.split(r'\r\n|\r|\n', self.send_message(str.encode("00"), "HEADER"))

                #mark it as False, so we only retrigger the empty send when it's actually needed
                send_event = False

            #Only action genuine checks if we haven't got responses from the last send process
            if list_of_responses is None:

                # Get all unsent Headers, if there are any
                header = self.database.get_unsent_header()

                if header is not None:

                    # HEADER TYPE   |  Image id | Number of pieces | filename
                    node_id = 1
                    # payload type =1 which is a header for a file
                    payload = '1'+'|'+ str(node_id) +'|'+str(header[0])+'|'+str(header[1])+'|'+str(header[4])
                    list_of_responses = re.split(r'\r\n|\r|\n', self.send_message(str.encode(payload), "HEADER"))


                #Else, check for unsent pieces
                else:
                    requested = self.database.get_unsent_request()

                    if requested is not None:
                        node_id = 1
                        print(requested)
                        str_data = '3' + '|' + str(node_id) + '|' + str(requested[0]) + '|' + str(requested[1]) + '|'
                        bytes_data = str_data.encode('utf-8')
                        # payload = '3' + '|' + str(node_id) + '|' + str(requested[0]) + '|' + str(requested[1]) + '|' + requested[2]
                        payload = bytes_data + requested[2]
                        list_of_responses = re.split(r'\r\n|\r|\n', self.send_message(payload, "PIECE"))

                        # now that we sent it, you can mark it as request fulfilled
                        self.database.reset_request(str(requested[0]), str(requested[1]))

            #process any responses from the last send

            if list_of_responses is not None:

                for response in list_of_responses:
                    print(f"Response: {response}")
                    if re.search(TX_DONE, response):

                        print("Transmission Completed to Gateway")

                    elif re.search(TX_LOCKED, response):

                        print("Radio in use, waiting")

                    elif re.search(TX_RECEIVED, response):

                        payload_segment = response.split(':')[-1]
                        decoded_string = bytes.fromhex(payload_segment).decode('utf-8')
                        print("Decoded String from Gateway:", decoded_string)
                        split_decoded_string = decoded_string.split('|')

                        # Ack the header, if the request is for a piece
                        self.database.ack_header(int(split_decoded_string[1]))

                        # Set the piece as being 'requested'
                        self.database.request_piece(int(split_decoded_string[1]), int(split_decoded_string[2]))

                        # and that's all the gateway does right now, but more functions could be added


            else:
                #if we have no responses yet, prompt radio to send a TX to action a new RX
                # next loop, trigger a send before anything else
                send_event = True




            time.sleep(.2)





