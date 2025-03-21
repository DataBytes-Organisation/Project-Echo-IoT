# Instructions:
# To run, ensure following libraries are installed (run from RPi terminal):
# sudo apt-get install python3-smbus python3-dev i2c-tools
# sudo pip3 install pi-ina219 **
# ** This should ideally be installed in a virtual environment to not clash with other packages, and may create an
#    error. If so, run sudo pip3 install pi-ina219 --break-system-packages

import time
from ina219 import INA219, DeviceRangeError

# Define constants for the INA219 sensor
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0 

# Battery voltage thresholds
VOLT_FULL = 4.2  # Voltage when the battery is fully charged
VOLT_EMPTY = 3.2  # Voltage when the battery is fully depleted

class Battery:
    def __init__(self, database):
        self.database = database
        self.ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, busnum=1)
        self.ina.configure()
        print("Battery monitoring initialized.")

    def calculate_battery_percentage(self, voltage):
        # Maps the battery voltage to a percentage between 0% and 100%.
        if voltage >= VOLT_FULL:
            return 100.0
        elif voltage <= VOLT_EMPTY:
            return 0.0
        else:
            # Linear interpolation between VOLT_EMPTY and VOLT_FULL
            return ((voltage - VOLT_EMPTY) / (VOLT_FULL - VOLT_EMPTY)) * 100.0

    def read_battery_status(self):
        # Reads the battery voltage and calculates the battery percentage.
        try:
            voltage = self.ina.voltage()  # Read the battery voltage
            percentage = self.calculate_battery_percentage(voltage)
            return {"voltage": voltage, "percentage": percentage}
        except DeviceRangeError as e:
            print(f"Error reading from INA219: {e}")
            return {"voltage": 0, "percentage": 0}

    def do_something(self):
        # Reads the battery status and inserts it into the database.
        battery_status = self.read_battery_status()
        # print(f"Battery Status: Voltage = {battery_status['voltage']:.2f} V, "f"Percentage = {battery_status['percentage']:.2f}%")
        self.database.insert_battery_status(battery_status)
        time.sleep(30)  # Adjust the delay as needed
        # return the battery percentage here

    def battery_thread(self):
        time.sleep(3)  # Allow time for initialization
        print("Battery Monitor Process started.")
        while True:
            self.do_something()
            # use the returned value in a message here?




