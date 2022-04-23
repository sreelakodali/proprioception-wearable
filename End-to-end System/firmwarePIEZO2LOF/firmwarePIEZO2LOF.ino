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
#include<FastMap.h>

// Constants
#define flexCapacitiveSensor_MIN 0
#define flexCapacitiveSensor_MAX 11400
#define position_MIN 46
#define position_MAX 130
#define sreela_MAX 90 //dorsal forearm, maxforce without reaching max current

// Pin Names
#define position1_IN A6 // pin to measure position1_Measured
#define position1_OUT 21 // pin to send position1_Command
#define button_IN 4 // pushbutton

typedef enum { NONE, ZERO_FORCE, FLEX, MAX_PRESSURE, ACTUATOR  
} CALIBRATION_OPTIONS;

const bool serialON = true;
const CALIBRATION_OPTIONS calibrationMode = FLEX;
const bool fastMapON = false;
const bool sdWriteON = !(serialON);
int user_position_MIN = position_MIN;
int user_position_MAX = 60;

const int WRITE_COUNT = 100; // for every n runtime cycles, write out data
const byte I2C_ADDR = 0x04; // force sensor
const int CHIP_SELECT = 10; // SD card writing
const int BUFFER_SIZE = 25; // how many datastrings until sd card write within 512 buffer
int cycleCount = 0;
int bufferCount = 0;
String buf = "";
//bool powerOn;

// Actuator
Servo actuator1;  // create servo object to control a servo
int position1_Command = 0;    // variable to store the servo command
int position1_Measured = 0;

// Flex sensor
int16_t flexSensor = 0; // variable to store sensor value
ADS capacitiveFlexSensor;

// floating point
float flexSensorFloat = 0;
FastMap mapper;

// Push Button
int buttonState = 0;
int oldButtonState = 0;
int buttonCount = 0;

// Calibration
short zeroForce = 0;

short detectionForce = 0;
short painForce = 0;

void setup() { 
  Wire.begin(); // join i2c bus

  // start serial for output
  if (serialON) {
    Serial.begin(4608000);  
    Serial.flush();
    while (!Serial);
  }

  if (sdWriteON) {
    // See if the card is present and can be initialized:
    if (!SD.begin(CHIP_SELECT)) {
      if (serialON) Serial.println("Card failed, or not present");
      while (1);
    }
    if (serialON) Serial.println("card initialized.");
    // fix test code
    //    SD.remove("raw_data.csv");
    //    if (serialON) Serial.println("Removed old data");
  }
  if (fastMapON) mapper.init(175, 40, position_MIN, position_MAX);

  // attach servo
  actuator1.attach(position1_OUT); 
  actuator1.write(position_MIN);

  pinMode(button_IN, INPUT);

  if (capacitiveFlexSensor.begin() == false) {
    if (serialON) Serial.println(("No sensor detected. Check wiring. Freezing..."));
    while (1);
  }
  calibration(calibrationMode);
}

void loop() {
  if(buttonCount % 2 == 1) {
    runtime();  
  }
  else {
    runtime_NoFeedback();
  }
}

void writeOutData(unsigned long t, int f, int c, int m, short d) {
  String dataString = "";
  if (sdWriteON || serialON) {
    dataString += (String(t) + "," + String(f) + "," + String(c) + "," \
    + String(m) + "," + String(d));
    if (sdWriteON) {
      File dataFile = SD.open("raw_data.csv", FILE_WRITE);
      if (dataFile) {
        dataFile.println(dataString);
        dataFile.close();
      } else if (serialON) Serial.println("error opening datalog");
    }
        if (serialON) Serial.println(dataString);
  }  
}

void writeOutDataBatching(unsigned long t, int f, int c, int m, short d) {
  String dataString = "";
  
  if (sdWriteON) {
    buf += (String(t) + "," + String(f) + "," + String(c) + "," \
    + String(m) + "," + String(d) + "\n");
    bufferCount = bufferCount + 1;
    
    if (bufferCount == BUFFER_SIZE) {
      File dataFile = SD.open("raw_data.csv", FILE_WRITE);
      if (dataFile) {
        dataFile.print(buf);
        dataFile.close();
        bufferCount = 0;
        buf = "";
      }
    }
  } else if (serialON) {
      dataString = (String(t) + "," + String(f) + "," + String(c) + "," \
      + String(m) + "," + String(d));
      Serial.println(dataString);
  }
}

void safety() {
      // Safety withdraw actuator and stop
    if (risingEdgeButton()) {
      actuator1.write(position_MIN);
      if (serialON) Serial.println("Device off. Turn off power.");
      if (sdWriteON) {
        File dataFile = SD.open("raw_data.csv", FILE_WRITE);
        if (dataFile) {
            dataFile.print(buf);
            dataFile.close();
        }
      }
      while (1);
    }
}

void runtime() {
    short data;
    unsigned long myTime;
    
    // time for the beginning of the loop
    myTime = millis();
    
    // Read flex sensor
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    
    // Map angle to actuator command
    if (fastMapON) position1_Command = mapper.map(flexSensorFloat);
    else position1_Command = map(flexSensor, flexCapacitiveSensor_MIN, flexCapacitiveSensor_MAX, position_MIN, position_MAX);
    if(position1_Command > position_MAX) position1_Command = position_MAX;
    if(position1_Command < position_MIN) position1_Command = position_MIN;
    
    // Measure force and actuator position
    data = readDataFromSensor(I2C_ADDR);
    position1_Measured = analogRead(position1_IN);

    // Send command to actuator
    actuator1.write(position1_Command);

    cycleCount = cycleCount + 1;
    // fix test code
    //powerOn = (data >= 150);
    //Serial.println((cycleCount == WRITE_COUNT) && powerOn);
    //Serial.println(powerOn);
    if ((cycleCount == WRITE_COUNT)) {
      writeOutData(myTime, flexSensor, position1_Command, position1_Measured, data);
      cycleCount = 0;
    }
    risingEdgeButton();
}

void runtime_NoFeedback() {
    short data;
    unsigned long myTime;
    String dataString = "";
    
    // time for the beginning of the loop
    myTime = millis();
    
    // Read flex sensor
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    
    // Map angle to actuator command
    if (fastMapON) position1_Command = mapper.map(flexSensor);
    else position1_Command = map(flexSensor, flexCapacitiveSensor_MIN, flexCapacitiveSensor_MAX, position_MIN, position_MAX);
    if(position1_Command > position_MAX) position1_Command = position_MAX;
    if(position1_Command < position_MIN) position1_Command = position_MIN;
    
    // Measure force and actuator position
    data = readDataFromSensor(I2C_ADDR);
    position1_Measured = analogRead(position1_IN);

    // Send command to actuator
    actuator1.write(position_MIN);

    cycleCount = cycleCount + 1;
    //powerOn = (data >= 150);
    //Serial.println((cycleCount == WRITE_COUNT) && powerOn);
    //Serial.println(powerOn);
    if ((cycleCount == WRITE_COUNT)) {
      writeOutData(myTime, flexSensor, position1_Command, position1_Measured, data);
      cycleCount = 0;
    }
    risingEdgeButton();
}

void sweep() {
    unsigned long myTime;
    int counter = user_position_MIN;
    int extending = 1;
    
    
    while (counter <= position_MAX) {
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
        if (counter == (position_MAX)) {
          counter = counter - 1;
          extending = 0;
        } else counter = counter + 1;
      }
      else if (extending == 0) {
        if (counter == position_MIN) {
          counter = counter + 1;
          extending = 1;
          break;
        } else counter = counter - 1;
      }
      delay(500);
    }    
}

void calibrationActuatorFeedback() {
     // Calibration: Sweep and record the actuator position feedback positions
  actuator1.write(position_MIN);
  if (serialON) Serial.println("Calibration: Actuator");
  if (serialON) Serial.println("Instructions: For this calibration stage, please don't wear the actuator. Make sure power is on and press the button when ready.");
  while(!risingEdgeButton());
  sweep();
  if (serialON) Serial.println("Calibration stage complete. Researcher will record values and will let you know when to begin next stage.");
}

void calibrationZeroForce() {
  // Calibration Stage: Get the zero force of the device
  actuator1.write(position_MIN);
  if (serialON) Serial.println("Calibration: Zero Force");
  if (serialON) Serial.println("Instructions: Please wear the device and keep your arm relaxed, no need to do anything. Make sure power is on.");
  if (serialON) Serial.println("Press button once when you're ready to begin.");
  
  while(!(risingEdgeButton()));
  zeroForce = readDataFromSensor(I2C_ADDR);
  if (serialON) Serial.println("Calibration stage complete. Zero Force = ");
  if (serialON) Serial.println((zeroForce - 249) * (45.0)/511);
  if (serialON) Serial.println("Researcher will record values and will let you know when to begin next stage.");
}

void calibrationFlexSensor() {
  unsigned long startTime;
  unsigned long endTime;

  actuator1.write(position_MIN);
  if (serialON) Serial.println("Calibration: Flex Sensor");
  if (serialON) Serial.println("Instructions: Please wear the device.");
  if (serialON) Serial.println("Raise your left arm with your palm facing the ceiling until it is parallel with the table.");
  if (serialON) Serial.println("Keeping your upper arm parallel still, bend your elbow towards yourself and then back to the original position.");
  if (serialON) Serial.println("Please repeat this motion until researcher tells you to stop.");
  if (serialON) Serial.println("Press button once when you're ready to begin.");
  while(!(risingEdgeButton()));
  // record flex values for 10 seconds
  startTime = millis();
  endTime = millis();
  while((endTime - startTime) < 10000) {
    runtime_NoFeedback();
    endTime = millis();
  }
  if (serialON) Serial.println("Calibration stage complete. Researcher will record values and will let you know when to press the button for next stage.");
}

void calibrationMaxDeepPressure() {
   int counter = position_MIN;
   short data;

   if (serialON) Serial.println("Calibration: Max Pressure ");
   if (serialON) Serial.println("Instructions: Please wear the device. Make sure power is on. The actuator will extend into your arm and apply a deep pressure.");
   if (serialON) Serial.println("During this stage, please click the button once to indicate when it is too uncomfortable.");
   if (serialON) Serial.println("When you're ready to begin calibration stage, press the button.");

   while(!(risingEdgeButton()));

   if (serialON) Serial.println("Calibration Stage beginning...");
   // Calibration Stage: Get the detection and pain thresholds
    while (counter <= position_MAX) {
       // Measure force and actuator position
      data = readDataFromSensor(I2C_ADDR);
      position1_Measured = analogRead(position1_IN);
      // Send command to actuator
      actuator1.write(counter);
      if (serialON) Serial.println((data - 249) * (45.0)/511);
      if (risingEdgeButton()) {
//        // Calibration Stage 2a
//        // Click button if you detect the tactor. Detection Threshold stored
//        if (buttonCount == 4) {
//          user_position_MIN = counter;
//          detectionForce = readDataFromSensor(I2C_ADDR);
//          if (serialON) {
//            Serial.println("DETECTION THRESHOLD:");
//            Serial.println((detectionForce - 256) * (45.0)/511);
//          }
//        }
        // Calibration Stage 2b
        // Click button if feeling pain from tactor. Pain threshold stored
        //else {
          user_position_MAX = counter - 1;
          painForce = readDataFromSensor(I2C_ADDR);
          if (serialON) {
            Serial.println("DISCOMFORT THRESHOLD:");
            Serial.println((painForce - 249) * (45.0)/511);
          }
          break; 
        //} 
      }
      delay(500);
      counter = counter + 1;
  }
  actuator1.write(position_MIN);
  if (serialON) Serial.println("Calibration stage complete. Min and max actuator positions are:");
  if (serialON) Serial.println(user_position_MIN);
  if (serialON) Serial.println(user_position_MAX);
  if (serialON) Serial.println("Make sure to researcher records these values and updates them in the processing code.");
}

/* Calibration: Use a pushbutton to let the device know when it's making contact with
 *  skin (min) and when at threshold for pain (max). Run this for each user */
void calibration(CALIBRATION_OPTIONS mode) {
  // Reset position of actuator
  actuator1.write(position_MIN);

  for (int i = 0; i < mode; i++) {
      switch (mode - i) {
        case ZERO_FORCE:
          calibrationZeroForce();
          break;
        case FLEX:
          calibrationFlexSensor();
          break;
        case MAX_PRESSURE:
          calibrationMaxDeepPressure();
          break;
        case ACTUATOR:
          calibrationActuatorFeedback();
          break;
        default:
          break;
      }
      delay(2000);
  }
  if (serialON) Serial.println("Calibrated. Please click the button to move on.");
  while(!(risingEdgeButton()));
}

bool risingEdgeButton() {
  buttonState = digitalRead(button_IN);
  //Serial.println(buttonState);
  if (buttonState != oldButtonState) {
    if (buttonState == HIGH) {
      buttonCount = buttonCount + 1;
      oldButtonState = buttonState;
      delay(100);
      return true;
    }
  }
  oldButtonState = buttonState; 
  return false;
}

float mapFloat(int x, int in_min, int in_max, float out_min, float out_max) {
 return (float) ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min);
}

void pulse(Servo &myServo, int retraction, int extension, int t_delay) {
  myServo.write(extension);
  delay(t_delay);
  myServo.write(retraction);
}


short readDataFromSensor(short address) {
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
