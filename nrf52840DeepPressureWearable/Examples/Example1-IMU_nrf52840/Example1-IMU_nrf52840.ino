/*
 * IMU Example
 * Using nrf52840DeepPressureWearable library
 * Written by Aarya Sumuk (asumuk@stanford.edu) and Sreela Kodali (kodali@stanford.edu) 
 * 
 * */

#include <nrf52840DeepPressureWearable.h>



nrf52840DeepPressureWearable device;


void setup() {
  Serial.begin(115200);
  while (!Serial);
  device.initializeIMU();
  device.calibrateSensors();
  //device.blinkN(10, 1000);
  Serial.println("Device initialized.");
    
}

void loop() {
  device.measureRollPitch(1);
}