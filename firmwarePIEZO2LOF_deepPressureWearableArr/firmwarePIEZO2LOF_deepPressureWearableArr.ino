/*
 * Firmware Code for Proprioception Wearable Device
 * Using DeepPressureWearableArr library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */

#include <DeepPressureWearableArr.h>

// create and initialize instance of DeepPressureWearable(INPUT_TYPE input, bool serial, bool c)

const INPUT_TYPE in = NO_INPUT;//FLEX_INPUT; // NO_INPUT, FLEX_INPUT, KEYBOARD_INPUT
const bool serialON = true; // and has serial output
const int calibrateOn = false;

DeepPressureWearableArr device(in, serialON, calibrateOn);


void setup() {
    Serial.println("Device initialized.");
    device.blinkN(10, 1000);
    //delay(10000);
}

void loop() {
  // pressing button can turn feedback on and off
  device.miniPilot_patternsCommandbyLetter();
  //device.runtime(mapping);
  //device.sweep(50, 0);
  //device.testLed();
}

void mapping(int angle) {
  int x;
  int midpoint = 60;

  // set device1.position1_Command and device1.position2_Command with angle
   
//  x = map(angle, int(device.user_flex_MIN), int(device.user_flex_MAX), device.user_position_MIN, device.user_position_MAX);
//  device.position1_Command = x;
//  device.position2_Command = x;
  
  if (angle < midpoint) {
    x = map(angle, int(device.user_flex_MIN), midpoint, device.user_position_MIN, device.user_position_MAX);
    //x=x-20;
    device.position_CommandArr[0] = x;
    device.position_CommandArr[1] = device.user_position_MIN;
  }
  else {
    x = map(angle, midpoint, int(device.user_flex_MAX), device.user_position_MIN, device.user_position_MAX);
    //x=x-20;
    device.position_CommandArr[0] = device.user_position_MIN;
    device.position_CommandArr[1] = x;
  }
}
