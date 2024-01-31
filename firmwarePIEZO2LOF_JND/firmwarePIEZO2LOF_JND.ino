/*
 * Firmware Code for Proprioception Wearable Device
 * Using DeepPressureWearableArr library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */

#include <DeepPressureWearableArr.h>

// create and initialize instance of DeepPressureWearable(INPUT_TYPE input, bool serial, bool c)

const INPUT_TYPE in = KEYBOARD_INPUT;//FLEX_INPUT; // NO_INPUT, FLEX_INPUT, KEYBOARD_INPUT
const bool serialON = true; // and has serial output
const int calibrateOn = true;

DeepPressureWearableArr device(in, serialON, calibrateOn);


void setup() {
    Serial.println("Device initialized.");
    device.blinkN(20, 500);
}

void loop() {
  // pressing button can turn feedback on and off
  //device.sweep(500,0); // single actuator control
  device.directActuatorControl(1); // single actuator control
}
