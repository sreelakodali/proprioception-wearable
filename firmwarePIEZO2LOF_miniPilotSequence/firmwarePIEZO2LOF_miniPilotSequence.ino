/*
 * Firmware Code for Proprioception Wearable Device
 * Using DeepPressureWearable library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */

#include <DeepPressureWearableArr.h>

// create and initialize instance of DeepPressureWearable(INPUT_TYPE input, bool serial, bool c)

const INPUT_TYPE in = NO_INPUT; // NO_INPUT, FLEX_INPUT, KEYBOARD_INPUT
const bool serialON = true; // and has serial output
const int calibrateOn = true;

DeepPressureWearableArr device(in, serialON, calibrateOn);


void setup() {
    Serial.println("Device initialized.");
    device.beginTimer();
//    Serial.println("Patterns in sequence");
    //device.miniPilot_patternsSequence(10000);
    Serial.println("Patterns by command");
}

void loop() {
  //device.sweep(100);
  // pressing button can turn feedback on and off
  device.sweep(500, 0);
  //device.miniPilot_patternsCommandbyLetter();
  //Serial.println("Sweep");
  //device.miniPilot_sweep(50);
  //device.miniPilot_sweepKeyboard();
}
