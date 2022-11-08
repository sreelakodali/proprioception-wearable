/** Testing Actuonix Micro Linear Actuator
    Written by: Sreela Kodali, kodali@stanford.edu
    Last updated: November 12th, 2021 **/

#include <Servo.h>

//Set constants
#define actuator1_LOWER_LIMIT 46
#define actuator1_UPPER_LIMIT 145

// Set pin names
#define sensor_IN A0
#define actuator1Pos_measured_IN A3
#define actuator1_OUT 5

Servo actuator1;  // create servo object to control a servo
int actuator1Pos_target = 0;    // variable to store the servo position
int sensorValue = 0;        // value read from the sensor
int actuator1Pos_measured = 0; // value from actuator feedback
int pos = 0;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  
  // attaches the servo on pin 5 to the servo object
  actuator1.attach(5);  
}

void loop() {

//  // read the analog in value:
//  sensorValue = analogRead(sensor_IN);
////  actuator1Pos_measured = analogRead(actuator1Pos_measured_IN);
//
//  // map it to the range of the analog out:
//  actuator1Pos_target = map(sensorValue, 0, 850, actuator1_LOWER_LIMIT, actuator1_UPPER_LIMIT);
//
//  if (actuator1Pos_target < actuator1_LOWER_LIMIT) {
//    actuator1Pos_target = actuator1_LOWER_LIMIT;
//  }
//
//  if (actuator1Pos_target > actuator1_UPPER_LIMIT) {
//    actuator1Pos_target = actuator1_UPPER_LIMIT;
//  }
//  
//  // tell servo to go to position
//  actuator1.write(actuator1Pos_target);
//
//  // print the results to the Serial Monitor:
//  Serial.print("Sensor = ");
//  Serial.print(sensorValue);
//  Serial.print("\t Actuator Position, Target= ");
//  Serial.println(actuator1Pos_target);
////  Serial.print("\t Actuator Position, Measured = ");
////  Serial.println(actuatorPosition);
//  delay(15);

  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    actuator1.write(pos);              // tell servo to go to position in variable 'pos'
    Serial.print("Position =");
    Serial.println(pos);
    delay(30);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    actuator1.write(pos);              // tell servo to go to position in variable 'pos'
    Serial.print("Position =");
    Serial.println(pos);
    delay(30);                       // waits 15ms for the servo to reach the position
  }
}
