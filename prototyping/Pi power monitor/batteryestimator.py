# -*- coding: utf-8 -*-

# Instructions:
# To run, ensure following libraries are installed (run from RPi terminal):
# sudo apt-get install python3-smbus python3-dev i2c-tools
# sudo pip3 install pi-ina219 **
# ** This should ideally be installed in a virtual environment to not clash with other packages, and may create an
#    error. If so, run sudo pip3 install pi-ina219 --break-system-packages

from ina219 import INA219, DeviceRangeError
import time

# Define constants
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0  # Adjust according to your INA219 settings

# Battery information
BATTERY_CAPACITY_MAH = 20000.0  # Battery capacity in mAh
IDLE_CONSUMPTION_MA = 500.0  # Average current draw of the Raspberry Pi at idle in mA
BATTERY_PERCENTAGE = 100.0  # Starting with a fully charged battery

# Time interval between updates (in seconds)
UPDATE_INTERVAL = 30

# Initialize the INA219 sensor
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, busnum=1)
ina.configure()

# Function to update the battery percentage
def update_battery_percentage(current_mA, elapsed_time_s):
    global BATTERY_PERCENTAGE

    # Calculate energy consumed by Raspberry Pi in mAh (mA * hours)
    energy_consumed_mAh = (IDLE_CONSUMPTION_MA * (elapsed_time_s / 3600.0))

    # Calculate energy recharged in mAh (mA * hours)
    energy_recharged_mAh = (current_mA * (elapsed_time_s / 3600.0))

    # Update battery percentage
    BATTERY_PERCENTAGE -= (energy_consumed_mAh / BATTERY_CAPACITY_MAH) * 100.0
    BATTERY_PERCENTAGE += (energy_recharged_mAh / BATTERY_CAPACITY_MAH) * 100.0

    # Constrain battery percentage between 0 and 100
    BATTERY_PERCENTAGE = max(0.0, min(100.0, BATTERY_PERCENTAGE))

    return BATTERY_PERCENTAGE

# Main loop
print("Monitoring voltage, current, power, and battery percentage with INA219 ...")
start_time = time.time()

while True:
    try:
        # Read sensor values
        bus_voltage = ina.voltage()            # Bus voltage in volts
        shunt_voltage = ina.shunt_voltage()    # Shunt voltage in mV
        current_mA = ina.current()             # Current in mA
        power_mW = ina.power()                 # Power in mW

        # Calculate elapsed time
        current_time = time.time()
        elapsed_time_s = current_time - start_time
        start_time = current_time

        # Update battery percentage
        battery_percentage = update_battery_percentage(current_mA, elapsed_time_s)

        # Print the results
        print(f"Bus Voltage:    {bus_voltage:.3f} V")
        print(f"Current:        {current_mA:.3f} mA")
        print(f"Power:          {power_mW:.3f} mW")
        print(f"Battery:        {battery_percentage:.2f} %")
        print("")

        # Wait before the next reading
        time.sleep(UPDATE_INTERVAL)

    except DeviceRangeError as e:
        print("Error: ", e)
        time.sleep(UPDATE_INTERVAL)