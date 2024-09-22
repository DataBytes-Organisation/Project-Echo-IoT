@ -0,0 +1,44 @@
const int analogPin = A0;    // Pin to read the voltage
const float R1 = 10000.0;    // Resistor R1 (10kΩ)
const float R2 = 10000.0;    // Resistor R2 (22kΩ)
const float refVoltage = 5; // Reference voltage of Arduino (5V)
float bat_percentage;

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
}


float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void loop() {
  int analogValue = analogRead(analogPin); // Read the analog value
  float voltage = analogValue * (refVoltage / 1023.0); // Convert to voltage
  float batteryVoltage = voltage * ((R1 + R2) / R2); // Calculate the battery voltage
  bat_percentage = mapFloat(batteryVoltage, 3.3, 3.8, 0, 100); 
 
  if (bat_percentage >= 100)
  {
    bat_percentage = 100;
  }
  if (bat_percentage <= 0)
  {
    bat_percentage = 1;
  }
  
  Serial.print("Voltage Divider Circuit Read: ");
  Serial.print(voltage);
  Serial.println(" V");
  
  Serial.print("Calculated Battery Voltage: ");
  Serial.print(batteryVoltage);
  Serial.println(" V");
  
  Serial.print("Battery Percentage: ");
  Serial.print(bat_percentage);
  Serial.println("%");

  delay(5000); // Wait for 30 seconds before taking another reading
}