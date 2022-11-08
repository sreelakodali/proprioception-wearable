/*
 * Mapping PWM Servo Command to Actuator Movement
 * Written: February 16th, 2022 by Sreela Kodali (kodali@stanford)
 * 
 * */

#include <Wire.h> //For I2C/SMBus
#include <Servo.h>

// Constants
#define position_MIN 46
#define position_MAX 130

// Pin Names
#define position1_IN A1 // pin to measure position1_Measured
#define position1_OUT 5 // pin to send position1_Command
#define button_IN 2 // pushbutton

// Actuator
Servo actuator1;  // create servo object to control a servo
int position1_Command = 0;    // variable to store the servo command
float position1_Measured = 0.0;   // variable to store the measured servo position

// Push Button
int buttonState = 0;
int oldButtonState = 0;
int pushCount = 0;


void setup()
{  
  Wire.begin(); // join i2c bus (address optional for master)
  //TWBR = 12; //Increase i2c speed if you have Arduino MEGA2560, not suitable for Arduino UNO
  Serial.begin(57600);  // start serial for output
  Serial.flush();
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // attaches the servo on pin to the servo object
  actuator1.attach(position1_OUT);
  Serial.println("Attach servo.");
  Serial.println("----------------------------------------");
  pinMode(button_IN, INPUT);
  pinMode(1, OUTPUT);
  pinMode(0, OUTPUT);
  digitalWrite(0, LOW);
  digitalWrite(1, HIGH);
  position1_Command = position_MAX;
}


void loop()
{
    unsigned long myTime;
    bool debug = false;
    float analogVal;
    
    buttonState = digitalRead(button_IN); // read the pushbutton input pin:
    //      rising edge detection: if pushbutton pressed, do a pulse
    if (buttonState != oldButtonState) {
      if (buttonState == HIGH) {
        Serial.println("ON!");
        position1_Command = position1_Command - 1;
      }
    }
    oldButtonState = buttonState;
    actuator1.write(position1_Command);
    analogVal = analogRead(position1_IN);
    position1_Measured = mapFloat(analogVal, 9, 606, 20.0, 0.0);
    myTime = millis();
      
    Serial.print(myTime);
    Serial.print("     Actuator Pos Command: ");
    Serial.print(position1_Command);
    Serial.print("     Actuator Pos Measured: ");
    Serial.print(analogVal);
    Serial.print("    ");
    Serial.println(position1_Measured);
    delay(500);
}

float mapFloat(int x, int in_min, int in_max, float out_min, float out_max)
{
 return (float) ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min);
}

void pulse (Servo &myServo, int retraction, int extension, int t_delay) {
  myServo.write(extension);
  delay(t_delay);
  myServo.write(retraction);
}
