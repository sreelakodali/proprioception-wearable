/** Testing Actuonix Micro Linear Actuator
    Written by: Sreela Kodali, kodali@stanford.edu
    Last updated: November 9th, 2021 **/

// Set pin names
#define i_sensorInput A0
#define out_actuatorOutput 6
#define in_actuatorPosition A3

int sensorValue = 0;        // value read from the sensor
int actOutputValue = 0;        // value output to the PWM (analog out)
int actuatorPosition = 0; // value from actuator feedback

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {

   // read the analog in value:
//  sensorValue = analogRead(i_sensorInput);
//  actuatorPosition = analogRead(in_actuatorPosition);
  
//  // map it to the range of the analog out:
//  actOutputValue = map(sensorValue, 0, 780, 0, 255);
//  
//  // change the analog out value:
  analogWrite(out_actuatorOutput, 10);
//
//  // print the results to the Serial Monitor:
//  Serial.print("Sensor = ");
//  Serial.print(sensorValue);
//  Serial.print("\t Actuator = ");
//  Serial.print(actOutputValue);
//  Serial.print("\t Position = ");
//  Serial.println(actuatorPosition);

  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
  delay(15);

}
