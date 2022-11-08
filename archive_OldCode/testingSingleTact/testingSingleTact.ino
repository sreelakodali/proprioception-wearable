/** Testing SingleTact sensor
    Written by: Sreela Kodali, kodali@stanford.edu
    Last updated: November 21st, 2021 **/

#include <Wire.h>
#include <Timer1.h> //For timestamp

// Constants
const byte I2C_TO_SENSOR_BUFFER_LENGTH = 32;

// Data structures
byte outgoingI2CBuffer[I2C_TO_SENSOR_BUFFER_LENGTH];
unsigned long timeStamp_;

//Zero a buffer
void BlankBuffer(byte* buffer, byte length)
{
  for(int i = 0; i < length; i++)
  {
    buffer[i] = 0;
  }
}

void setup() {
  // join i2c bus
  Wire.begin(); 
  Serial.begin(9600);
  BlankBuffer(outgoingI2CBuffer, I2C_TO_SENSOR_BUFFER_LENGTH);

  timeStamp_ = 0;
  startTimer1(100); //Timer for timestamp
}

int sensorData = 0;

void loop() {

  // Step 1: Transmit Calibration Data to interface board
  // transmit to device 0x04 (00000010). i2c addressing uses high 7 bits so it's 2
  Wire.beginTransmission(2); 


  // Step 2: set address to pointed to read sensor data
  Wire.write(byte(0x132)); 
  Wire.endTransmission(); // stop transmitting

  delay(1000);
  Wire.requestFrom(2,2); // request 2 bytes from sensor #2

  if (2 <= Wire.available()) {
    Serial.print("hi!");
    sensorData = Wire.read(); // reads high byte
    sensorData = sensorData << 8; // move to MSB
    sensorData |= Wire.read(); // read lower byte
    Serial.print("Force = ");
    Serial.println(sensorData);
  }
  
}
