import time


class Battery:

    def __init__(self, database):
        self.server = None

        self.database = database

    def read_battery_status(self):

        # Do something to read the battery status for external device
        battery_status = 1  # TEMP!!! Change this to be Voltage level

        return battery_status

    def do_something(self):
        # Do something, Take reading of battery and insert it into the database

        time.sleep(5)

        self.database.insert_battery_status(self.read_battery_status())



    def battery_thread(self):
        # Give time for database accessor to initialise in the main thread
        time.sleep(3)

        print(f"Battery Monitor Process started")

        while True:
            self.do_something()



