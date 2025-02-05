/*
 * Runtime Mapping Example
 * Using DeepPressureWearableBLE library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 *  NOTE: Actuator indexing starts at 0
 *  Example: for a system with two actuators, first actuator is idx=0. second actuator is idx=1
 * 
 * */

#include <DeepPressureWearableBLE.h>



// create and initialize instance of DeepPressureWearableBLE(INPUT_TYPE input, bool serial, bool c)

const INPUT_TYPE in = IMU_INPUT;// NO_INPUT, FLEX_INPUT, SERIAL_INPUT, IMU_INPUT
const bool serialON = true; // and has serial output
const int calibrateOn = false;


DeepPressureWearableBLE device(in, serialON, calibrateOn);


void setup() {
    Serial.println("Device initialized.");
    device.blinkN(10, 1000);
    //delay(10000);
}

void loop() {
  device.runtime(mapping);
}

// ------------------------------- SUPPORT FUNCTIONS --------------------------------//

// For this mapping function, we're assuming 2 actuators
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
