import serial
import paho.mqtt.client as mqtt

import Adafruit_BBIO.UART as UART

# Libraries required for Power Monitoring
from ina219 import INA219, DeviceRangeError
import time

# UART configuration change as needed
uart_device = '/dev/ttyO1'
uart_baudrate = 9600

# MQTT configuration if configured on local machine
mqtt_broker = 'localhost'
mqtt_port = 1883
mqtt_topic = 'SIT764/projectEcho'

# Connect to the MQTT broker
client = mqtt.Client("Client")

client.username_pw_set("username", "password")

def on_connect(client, userdata, flags, rc):
    print('Connected to broker')

def on_publish(client, userdata, mid):
    print('Message published')

client.on_connect = on_connect
client.on_publish = on_publish

client.connect(mqtt_broker)
client.loop_start()

# Connect the UART device on UART1
UART.setup("UART1")

# Initialise INA219 sensor
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0
BATTERY_CAPACITY_MAH = 20000.0
IDLE_CONSUMPTION_MA = 500.0
BATTERY_PERCENTAGE = 100.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, busnum=1)
ina.configure()

# Script to calculate battery percentage
def update_battery_percentage(current_mA, elapsed_time_s):
    global BATTERY_PERCENTAGE
    energy_consumed_mAh = (IDLE_CONSUMPTION_MA * (elapsed_time_s / 3600.0))
    energy_recharged_mAh = (current_mA * (elapsed_time_s / 3600.0))
    BATTERY_PERCENTAGE -= (energy_consumed_mAh / BATTERY_CAPACITY_MAH) * 100.0
    BATTERY_PERCENTAGE += (energy_recharged_mAh / BATTERY_CAPACITY_MAH) * 100.0
    BATTERY_PERCENTAGE = max(0.0, min(100.0, BATTERY_PERCENTAGE))
    return BATTERY_PERCENTAGE


uart = serial.Serial(port=uart_device,baudrate=uart_baudrate)
uart.close()
uart.open()


try:
    start_time = time.time()
    while True:
        # Read INA219 sensor data
        current_mA = ina.current()
        power_mW = ina.power()
        bus_voltage = ina.voltage()
        elapsed_time_s = time.time() - start_time
        start_time = time.time()
        battery_percentage = update_battery_percentage(current_mA, elapsed_time_s)
        
        # Prepare and send data via MQTT
        ina219_data = f"Bus Voltage: {bus_voltage:.2f} V, Current: {current_mA:.2f} mA, Power: {power_mW:.2f} mW, Battery: {battery_percentage:.2f}%"
        
        # Wait until you have some text waiting on the serial line
        # when you have a line, read it and publish it to MQTT
        # Then loop again
        if uart.in_waiting>0:
            uart_data = uart.readline().decode('utf-8').strip()
            # Combine UART data with INA219 data
            combined_data = f"{uart_data}, {ina219_data}"            
            client.publish(mqtt_topic, uart_data)

except:
    print("Error")

finally:
    client.loop_stop()
    client.disconnect()
    uart.close()
