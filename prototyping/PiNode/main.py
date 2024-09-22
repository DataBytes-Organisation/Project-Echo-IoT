import multiprocessing
import time
from PIL import Image


#Project imports
import battery, recorder
import database, receiver, comms, sender

def wait_while():
    # This is the parent process, which currently doesn't do much, except wait while other processes are running
    # If we don't let it sleep, it'll max out CPU while running very fast for no reason.
    time.sleep(10)

# Temp assignment of image id
image_id = 1

def split_and_insert(image_bytes, database):

    size_pieces = 200
    for i in range(len(image_bytes) // size_pieces):
        piece = image_bytes[i * size_pieces:(i * size_pieces) + size_pieces]
        # print(f"{i} piece is {len(piece)} bytes:  {i * size_pieces} to {(i * size_pieces) + size_pieces}")

        database.insert_piece(piece, i, image_id)

    # Still need the last partial chunk
    i += 1
    piece = image_bytes[i * size_pieces:-1]
    # print(f"{i} piece is {len(piece)} bytes:  {i * size_pieces} to {len(image_bytes)}")
    database.insert_piece(piece, i, image_id)

    #We know the number of pieces, so build our header, which is automatically sent to the Gateway
    header = (image_id, i)
    database.insert_header(header)


if __name__ == '__main__':

    # Initialise all the individual process classes
    database = database.Database()
    receiver = receiver.Receiver(database)
    sender = sender.Sender(database)

    # Add the recorder class and the battery class as placeholders
    recorder = recorder.Recorder(database)
    battery_monitor = battery.Battery(database)

    sender_process = multiprocessing.Process(target=sender.sender_thread,daemon=True,name="SenderProcess")
    receiver_process = multiprocessing.Process(target=receiver.receiver_thread, daemon=True, name="ReceiverProcess")

    # Spawn placeholder sub processes
    recorder_process = multiprocessing.Process(target=recorder.recorder_thread, daemon=True, name="RecorderProcess")
    battery_monitor_process = multiprocessing.Process(target=battery_monitor.battery_thread, daemon=True, name="BatteryProcess")


    #Start the processes (Before opening connection to database)
    receiver_process.start()
    sender_process.start()
    recorder_process.start()
    battery_monitor_process.start()

    #Now we can connect to database
    database.connect()

    # Testing splitting and joining large files
    #Generate a large split file from an image

    image_bytes = Image.open('image.jpg').tobytes()

    #split into pieces and generate header
    split_and_insert(image_bytes, database)



    while True:
        wait_while()
