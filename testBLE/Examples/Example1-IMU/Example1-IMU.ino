/*
 * IMU Example
 * Using DeepPressureWearableBLE library
 * Written by Aarya Sumuk (asumuk@stanford.edu) and Sreela Kodali (kodali@stanford.edu) 
 * 
 * */

#include <testBLE.h>



testBLE device;


void setup() {
  Serial.begin(115200);
  while (!Serial);
  device.initializeIMU();
  device.calibrateSensors();
  device.blinkN(10, 1000);
  Serial.println("Device initialized.");
    
}

void loop() {
  device.measureRollPitch(1);
}

// ------------------------------- SUPPORT FUNCTIONS --------------------------------//