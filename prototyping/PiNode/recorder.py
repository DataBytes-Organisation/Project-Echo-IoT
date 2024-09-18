
import time


class Recorder:

    def __init__(self, database):

        self.server = None

        self.database = database


    def do_something(self):

        #Do something, record data etc
        # But, if we're not doing anything, sleep, otherwise this is an infinitely fast infinite loop!!
        print(f"Recording Data...")
        time.sleep(20)

    def recorder_thread(self):

        # Give time for database accessor to initialise in the main thread
        time.sleep(3)

        print(f"Recorder Process started")

        while True:
            self.do_something()



