import multiprocessing
import time
import glob, os, shutil


#Project imports
import battery, recorder
import database, lora_sender_receiver, comms

#number of bytes per chunk, needs to adhere to lora guidelines
FILE_CHUNK_SIZE = 100

def wait_while(database):
    # This is the parent process, which currently doesn't do much, except wait while other processes are running
    # If we don't let it sleep, it'll max out CPU while running very fast for no reason.

    # check for new files
    filename = check_for_file("")
    if filename:
        file_id = os.path.splitext(os.path.basename(filename))[0]
        split_and_insert(FILE_CHUNK_SIZE, database, filename, int(file_id))

    time.sleep(10)


def check_for_file(directory_path):

    jpg_files = glob.glob(os.path.join(directory_path, "*.jpg"))

    if jpg_files:
        print(f"New detection found: {jpg_files[0]}")
        return jpg_files[0]
    else:
        return False


def move_file(filename):
    destination_directory = 'processed'
    file_name = os.path.basename(filename)
    destination_file_path = os.path.join(destination_directory, file_name)

    shutil.move(file_name, destination_file_path)

def split_image(image_path, size_of_chunks):
    with open(image_path, 'rb') as file:
        data = file.read()
    chunks = [data[i:i+size_of_chunks] for i in range(0, len(data), size_of_chunks)]
    return chunks

def split_and_insert(size_pieces, database, image_path, image_id):


    #get chunks from the file
    chunks = split_image(image_path, size_pieces)

    for i,chunk in enumerate(chunks):
        database.insert_piece(chunk, i, image_id)

    #We know the number of pieces, so build our header, which is automatically sent to the Gateway
    header = (image_id, i, image_path)
    database.insert_header(header)

    #Move file to processed directory
    move_file(image_path)



if __name__ == '__main__':

    # Initialise all the individual process classes
    database = database.Database()

    lora = lora_sender_receiver.LoraSenderReceiver(database)

    # Add the recorder class and the battery class as placeholders
    recorder = recorder.Recorder(database)
    battery_monitor = battery.Battery(database)

    lora_process = multiprocessing.Process(target=lora.lora_thread,daemon=True,name="SenderProcess")

    # Spawn placeholder sub processes
    recorder_process = multiprocessing.Process(target=recorder.recorder_thread, daemon=True, name="RecorderProcess")
    battery_monitor_process = multiprocessing.Process(target=battery_monitor.battery_thread, daemon=True, name="BatteryProcess")


    #Start the processes (Before opening connection to database)

    lora_process.start()
    recorder_process.start()
    battery_monitor_process.start()

    #Now we can connect to database
    database.connect()



    while True:
        wait_while(database)
