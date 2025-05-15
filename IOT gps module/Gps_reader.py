import serial
import time
import pynmea2

def read_gps():
    try:
        # Open serial port
        port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
        print("GPS Module connected. Reading data...")

        while True:
            line = port.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                try:
                    msg = pynmea2.parse(line)
                    if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                        print(f"Time: {msg.timestamp}, Latitude: {msg.latitude}, Longitude: {msg.longitude}")
                except pynmea2.ParseError:
                    continue
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program terminated.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    read_gps()