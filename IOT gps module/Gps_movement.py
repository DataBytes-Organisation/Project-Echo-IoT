import serial
import time
import pynmea2
import math

# Haversine formula to calculate distance in meters
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in meters

def read_gps_with_movement(threshold=2.0):
    try:
        port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
        print("GPS Module connected. Detecting movement...")

        prev_lat = None
        prev_lon = None

        while True:
            line = port.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                try:
                    msg = pynmea2.parse(line)
                    if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                        lat = msg.latitude
                        lon = msg.longitude
                        print(f"[INFO] Time: {msg.timestamp}, Lat: {lat}, Lon: {lon}")

                        if prev_lat is not None and prev_lon is not None:
                            distance = haversine(prev_lat, prev_lon, lat, lon)
                            if distance >= threshold:
                                print(f"🚶 Movement detected! Moved ~{distance:.2f} meters.")
                            else:
                                print("🟩 No significant movement.")
                        prev_lat = lat
                        prev_lon = lon
                except pynmea2.ParseError:
                    continue
            time.sleep(1.5)
    except KeyboardInterrupt:
        print("Program terminated.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    read_gps_with_movement()