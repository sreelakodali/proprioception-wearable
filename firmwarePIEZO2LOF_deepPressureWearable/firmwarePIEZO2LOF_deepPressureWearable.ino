/*
 * Firmware Code for Proprioception Wearable Device
 * Using DeepPressureWearable library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */

#include <DeepPressureWearable.h>

// create and initialize instance of DeepPressureWearable(bool keyboard, bool serial)
const bool keyboardON = false; // interfaces with flex sensor for elbow measurement
const bool serialON = true; // and has serial output

DeepPressureWearable device1(keyboardON, serialON);


void setup() {
    Serial.println("Actuator and flex sensor connected. Entering calibration mode. Close serial monitor and start calibration.py");
    device1.calibration();
    Serial.println("Calibrated. Entering runtime");
}

void loop() {
  // pressing button can turn feedback on and off
  device1.runtime();
}
