/*
 * Firmware Code for Proprioception Wearable Device
 * Using DeepPressureWearable library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */

#include <DeepPressureWearable.h>

// create and initialize instance of DeepPressureWearable(INPUT_TYPE input, bool serial, bool c)

const INPUT_TYPE in = FLEX_INPUT; // NO_INPUT, FLEX_INPUT, KEYBOARD_INPUT
const bool serialON = true; // and has serial output
const int calibrateOn = true;

DeepPressureWearable device1(in, serialON, calibrateOn);


void setup() {
    Serial.println("Device initialized.");
}

void loop() {
  // pressing button can turn feedback on and off
  device1.runtime();
}
