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
  calibration();
}


void loop() {
  //if (risingEdgeButton()) Serial.println(buttonCount);
  runtime();
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
    if(position1_Command > position_MAX) position1_Command = position_MAX;
    if(position1_Command < position_MIN) position1_Command = position_MIN;
    
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

  // Reset position of actuator
  actuator1.write(counter);

  if (serialON) Serial.println("---- DEVICE CALIBRATION ----");
  if (serialON) Serial.println("For the first step, please do not wear the actuator. Leave it on the table, and press the button when ready.");

  while(!risingEdgeButton());
  
  // Caliration Stage 1: Get the zero force of the device not worn
  if (serialON) Serial.println("Calibration Stage 1. Please do not wear the actuator and leave it on the table.");
  delay(5000);
  zeroForce = readDataFromSensor(I2C_ADDR);
  
  if (serialON) Serial.println("Calibration Stage 1 complete. Zero Force = ");
  if (serialON) Serial.println((zeroForce - 256) * (45.0)/511);
  
  if (serialON) Serial.println("Calibration Stage 2. Please wear the actuator on your forearm, and press the button when ready.");
  
  // Delay between Stage 1 and Stage 2 to wear the device. Click button for next stage
  while(!(risingEdgeButton()));

  if (serialON) Serial.println("Calibration Stage 2 Instructions");
  if (serialON) Serial.println("The actuator will extend into your arm and apply a deep pressure.");
  if (serialON) Serial.println("During this stage, please click the button once to indicate when you detect the pressure, and click then again when you feel pain.");
  if (serialON) Serial.println("When you're ready to begin calibration stage 2, press the button.");

  while(!(risingEdgeButton()));

  if (serialON) Serial.println("Calibration Stage 2 beginning...");
  // Calibration Stage 2: Get the detection and pain thresholds
  while (counter <= position_MAX) {

       // Measure force and actuator position
      data = readDataFromSensor(I2C_ADDR);
      position1_Measured = analogRead(position1_IN);

      // Send command to actuator
      actuator1.write(counter);

     
      if (risingEdgeButton()) {
        // Calibration Stage 2a
        // Click button if you detect the tactor. Detection Threshold stored
        if (buttonCount == 4) {
          user_position_MIN = counter;
          detectionForce = readDataFromSensor(I2C_ADDR);
          if (serialON) {
            Serial.println("DETECTION THRESHOLD:");
            Serial.println((detectionForce - 256) * (45.0)/511);
          }
        }

        // Calibration Stage 2b
        // Click button if feeling pain from tactor. Pain threshold stored
        else {
          user_position_MAX = counter - 1;
          painForce = readDataFromSensor(I2C_ADDR);
          if (serialON) {
            Serial.println("PAIN THRESHOLD:");
            Serial.println((painForce - 256) * (45.0)/511);
          }
          break; 
        } 
      }
      delay(500);
      counter = counter + 1;
  }

  if (serialON) Serial.println("Calibration Stage 2 complete. Min and max actuator positions are:");
  if (serialON) Serial.println(user_position_MIN);
  if (serialON) Serial.println(user_position_MAX);
  if (serialON) Serial.println("Make sure to researcher records these values and updates them in the processing code.");
  if (serialON) Serial.println("Please click the button once this is complete to conclude device calibration.");
  while(!(risingEdgeButton()));
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
