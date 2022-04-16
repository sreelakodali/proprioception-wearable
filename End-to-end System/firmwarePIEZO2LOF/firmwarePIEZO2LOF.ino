/*
 * Firmware Code for Proprioception Wearable Device
 * Written by Sreela Kodali (kodali@stanford)
 * 
 * */

#include <Wire.h> //For I2C/SMBus
#include <Servo.h>
#include "SparkFun_Displacement_Sensor_Arduino_Library.h"
#include <SD.h>
#include <SPI.h>
//#include<FastMap.h>

// Constants
#define position_MIN 46
#define position_MAX 130
#define flexCapacitiveSensor_MIN -2000
#define flexCapacitiveSensor_MAX 11500

// Pin Names
#define position1_IN A6 // pin to measure position1_Measured
#define position1_OUT 21 // pin to send position1_Command
#define button_IN 4 // pushbutton

bool serialON = true;
bool sdWriteON = false;

const byte I2C_ADDR = 0x04; // force sensor
const int CHIP_SELECT = 10; // SD card writing
const int WRITE_COUNT = 100; // for every n runtime cycles, write out data
int cycleCount = 0;

// Actuator
Servo actuator1;  // create servo object to control a servo
int position1_Command = 0;    // variable to store the servo command
int position1_Measured = 0;

// Flex sensor
int16_t flexSensor = 0;        // value read from the sensor
ADS capacitiveFlexSensor;
//FastMap mapper;

// Push Button
int buttonState = 0;
int oldButtonState = 0;
int buttonCount = 0;

// Calibration
short zeroForce = 0;
int user_position_MIN = position_MIN;
short detectionForce = 0;
int user_position_MAX = position_MAX;
short painForce = 0;

void setup() { 
  Wire.begin(); // join i2c bus

  // start serial for output
  if (serialON) {
    Serial.begin(921600);  
    Serial.flush();
    while (!Serial);
  }

  if (sdWriteON) {
    // See if the card is present and can be initialized:
    if (!SD.begin(CHIP_SELECT)) {
      if (serialON) Serial.println("Card failed, or not present");
      while (1); // No SD card, so don't do anything more - stay stuck here
    }
    if (serialON) Serial.println("card initialized.");
  }
  
  actuator1.attach(position1_OUT); // attach servo
  pinMode(button_IN, INPUT);

  if (capacitiveFlexSensor.begin() == false) {
    if (serialON) Serial.println(("No sensor detected. Check wiring. Freezing..."));
    while (1);
  }
//  calibration();
}


void loop() {
//  if (risingEdgeButton()) Serial.println("bloop!");
  runtime();
//  actuator1.write(65);
}

void runtime() {
    short data;
    unsigned long myTime;
    String dataString = "";

    // time for the beginning of the loop
    myTime = millis();
    
    // Read flex sensor
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    
    // Map angle to actuator command
    position1_Command = map(flexSensor, flexCapacitiveSensor_MIN, flexCapacitiveSensor_MAX, position_MIN, position_MAX);
    //mapper.map(flexSensor);
    
    // Measure force and actuator position
    data = readDataFromSensor(I2C_ADDR);
    position1_Measured = analogRead(position1_IN);

    // Send command to actuator
    actuator1.write(position1_Command);

    cycleCount = cycleCount + 1;
    if (cycleCount == WRITE_COUNT) {
      if (sdWriteON || serialON) {
        dataString += (String(myTime) + "," + String(flexSensor) + "," + String(position1_Command) + "," \
        + String(position1_Measured) + "," + String(data));
        if (sdWriteON) {
          File dataFile = SD.open("raw_data.csv", FILE_WRITE);
          if (dataFile) {
            dataFile.println(dataString);
            dataFile.close();
          } else if (serialON) Serial.println("error opening datalog.txt");
        }
        if (serialON) Serial.println(dataString);
      } 
      cycleCount = 0;
    }
}

void sweep() {
    short data;
    unsigned long myTime;
    int counter = user_position_MIN;
    int extending = 1;
    
    
    while (counter <= user_position_MAX) {
      String dataString = "";
      actuator1.write(counter);
      //if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
      //data = readDataFromSensor(I2C_ADDR);
      position1_Measured = analogRead(position1_IN);
      myTime = millis();

      if (serialON) {
        dataString += (String(myTime) + "," + String(counter) + "," \
        + String(position1_Measured));
        Serial.println(dataString);
      }

      if (extending == 1) {
        if (counter == (user_position_MAX)) {
          counter = counter - 1;
          extending = 0;
        } else counter = counter + 1;
      }
      else if (extending == 0) {
        if (counter == user_position_MIN) {
          counter = counter + 1;
          extending = 1;
        } else counter = counter - 1;
      }
      delay(500);
    }    
}

/* Calibration: Use a pushbutton to let the device know when it's making contact with
 *  skin (min) and when at threshold for pain (max). Run this for each user */
void calibration() {
  int counter = position_MIN;
  short data;
  unsigned long myTime;

  // Reset position of actuator
  actuator1.write(counter);
      
  // Caliration Stage 1: Get the zero force of the device not worn
  delay(5000);
  zeroForce = readDataFromSensor(I2C_ADDR);

  // Delay between Stage 1 and Stage 2 to wear the device. Click button for next stage
  while(!(risingEdgeButton() && (buttonCount == 0)));

  // Calibration Stage 2: Get the detection and pain thresholds
  while (counter <= position_MAX) {
    
      // time for the beginning of the loop
      myTime = millis();

       // Measure force and actuator position
      data = readDataFromSensor(I2C_ADDR);
      position1_Measured = analogRead(position1_IN);

      // Send command to actuator
      actuator1.write(counter);

      // Calibration Stage 2a
      // Click button if you detect the tactor. Detection Threshold stored
      if (risingEdgeButton() && (buttonCount == 1)) {
        user_position_MIN = counter;
        detectionForce = readDataFromSensor(I2C_ADDR);
      }
      
      // Calibration Stage 2b
      // Click button if feeling pain from tactor. Pain threshold stored
      if (risingEdgeButton() && (buttonCount == 2)) {
        user_position_MAX = counter - 1;
        painForce = readDataFromSensor(I2C_ADDR);
        break;
      }
      delay(500);
      counter = counter + 1;
  }
}

bool risingEdgeButton() {
  buttonState = digitalRead(button_IN);
  //Serial.println(buttonState);
  if (buttonState != oldButtonState) {
    if (buttonState == HIGH) {
      buttonCount = buttonCount + 1;
      oldButtonState = buttonState;
      delay(50);
      return true;
    }
  }
  oldButtonState = buttonState; 
  delay(50);
  return false;
}

float mapFloat(int x, int in_min, int in_max, float out_min, float out_max)
{
 return (float) ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min);
}


void pulse(Servo &myServo, int retraction, int extension, int t_delay) {
  myServo.write(extension);
  delay(t_delay);
  myServo.write(retraction);
}


short readDataFromSensor(short address)
{
  byte i2cPacketLength = 6;//i2c packet length. Just need 6 bytes from each slave
  byte outgoingI2CBuffer[3];//outgoing array buffer
  byte incomingI2CBuffer[6];//incoming array buffer
  bool debug;

  debug = false;

  outgoingI2CBuffer[0] = 0x01;//I2c read command
  outgoingI2CBuffer[1] = 128;//Slave data offset
  outgoingI2CBuffer[2] = i2cPacketLength;//require 6 bytes

  if (debug) Serial.println("Transmit address");  
  Wire.beginTransmission(address); // transmit to device 
  Wire.write(outgoingI2CBuffer, 3);// send out command
  if (debug) Serial.println("Check sensor status");
  byte error = Wire.endTransmission(); // stop transmitting and check slave status
  if (debug) Serial.println("bloop");
  if (error != 0) return -1; //if slave not exists or has error, return -1
  Wire.requestFrom((uint8_t)address, i2cPacketLength);//require 6 bytes from slave
  if (debug) Serial.println("Request bytes from sensor");
  
  byte incomeCount = 0;
  while (incomeCount < i2cPacketLength)    // slave may send less than requested
  {
    if (Wire.available())
    {
      incomingI2CBuffer[incomeCount] = Wire.read(); // receive a byte as character
      incomeCount++;
      if (debug) Serial.println("Read byte from sensor");
    }
    else
    {
      delayMicroseconds(10); //Wait 10us 
      if (debug) Serial.println("Waiting from sensor");
    }
  }

  short rawData = (incomingI2CBuffer[4] << 8) + incomingI2CBuffer[5]; //get the raw data

  return rawData;
}
