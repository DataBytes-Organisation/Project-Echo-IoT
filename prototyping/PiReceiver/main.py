import multiprocessing
import time
from PIL import Image

import database, receiver, comms, sender

def wait_while():

    time.sleep(10)


if __name__ == '__main__':

    database = database.Database()
    receiver = receiver.Receiver(database)
    sender = sender.Sender(database)

    sender_process = multiprocessing.Process(target=sender.sender_thread,daemon=True,name="SenderProcess")
    receiver_process = multiprocessing.Process(target=receiver.receiver_thread, daemon=True, name="ReceiverProcess")

    receiver_process.start()

    sender_process.start()

    database.connect()



    while True:
        wait_while()
