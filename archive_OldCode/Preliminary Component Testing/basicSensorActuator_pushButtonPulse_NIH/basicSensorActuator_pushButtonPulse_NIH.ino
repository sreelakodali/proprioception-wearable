/** Testing Actuonix Micro Linear Actuator
    Written by: Sreela Kodali, kodali@stanford.edu
    Last updated: November 12th, 2021 **/

#include <Servo.h>

//Set constants
#define actuator_MIN 46
#define actuator_MAX 145

// Set pin names
#define sensor_IN A0
#define actuator1Pos_measured_IN A3
#define actuator1_OUT 5
#define button_IN 2

Servo actuator1;  // create servo object to control a servo
int actuator1Pos_target = 0;    // variable to store the servo position
int sensorValue = 0;        // value read from the sensor
int actuator1Pos_measured = 0; // value from actuator feedback
int buttonState = 0;
int oldButtonState = 0;
int restState = actuator_MIN;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);

  // attaches the servo on pin 5 to the servo object
  actuator1.attach(5);
}

void pulse (Servo &myServo, int retraction, int extension, int t_delay) {
  myServo.write(extension);
  delay(t_delay);
  myServo.write(retraction);
}

void loop() {

  // read the analog in values:
  sensorValue = analogRead(sensor_IN);
//  actuator1Pos_measured = analogRead(actuator1Pos_measured_IN);
//  buttonState = digitalRead(button_IN); // read the pushbutton input pin:
  
  // map it to the range of the analog out:
  actuator1Pos_target = map(sensorValue, 0, 780, actuator_MIN, actuator_MAX);
  if (actuator1Pos_target < actuator_MIN) actuator1Pos_target = actuator_MIN;
  if (actuator1Pos_target > actuator_MAX) actuator1Pos_target = actuator_MAX;

//  if (actuator1Pos_target == actuator_MIN) {
//      // rising edge detection: if pushbutton pressed, do a pulse
//    if (buttonState != oldButtonState) {
//      if (buttonState == HIGH) {
//        Serial.println("ON!");
//        pulse (actuator1, restState, actuator_MAX, 1000);
//      }
//    }
//    oldButtonState = buttonState;
//    actuator1.write(restState);
//  }
  
  // tell servo to go to position
  actuator1.write(actuator1Pos_target);


  // print the results to the Serial Monitor:
  Serial.print("Sensor = ");
  Serial.print(sensorValue);
  Serial.print("\t Actuator Position, Target= ");
  Serial.print(actuator1Pos_target);
  Serial.print("\t Actuator Position, Measured = ");
  Serial.println(actuator1Pos_measured);
  delay(15);
}
