/*
 * Firmware Code for Proprioception Wearable Device
 * Using DeepPressureWearable library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */

#include <DeepPressureWearable.h>

// create and initialize instance of DeepPressureWearable(INPUT_TYPE input, bool serial, bool c)

const INPUT_TYPE in = NO_INPUT; // NO_INPUT, FLEX_INPUT, KEYBOARD_INPUT
const bool serialON = true; // and has serial output
const int calibrateOn = false;

DeepPressureWearable device(in, serialON, calibrateOn);


void setup() {
    Serial.println("Device initialized.");
}

void loop() {
  // pressing button can turn feedback on and off
  //device.runtime(mapping);
  //device.sweep(50);
  device.miniPilot_sweep(50);

}

void mapping(int angle) {
  int x;

  // set device1.position1_Command and device1.position2_Command with angle
   
//  x = map(angle, int(device.user_flex_MIN), int(device.user_flex_MAX), device.user_position_MIN, device.user_position_MAX);
//  device.position1_Command = x;
//  device.position2_Command = x;
  
  if (angle < 110) {
    x = map(angle, int(device.user_flex_MIN), 110, device.user_position_MIN, device.user_position_MAX);
    device.position1_Command = x;
    device.position2_Command = device.user_position_MIN;
  }
  else {
    x = map(angle, 110, int(device.user_flex_MAX), device.user_position_MIN, device.user_position_MAX);
    device.position1_Command = device.user_position_MIN;
    device.position2_Command = x;
  }
}
