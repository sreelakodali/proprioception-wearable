/*
 * Firmware Code for Proprioception Wearable Device
 * Written by Sreela Kodali (kodali@stanford.edu)
 * 
 * */

#include <Wire.h> //For I2C/SMBus
#include <Servo.h>
#include "SparkFun_Displacement_Sensor_Arduino_Library.h"
#include <SD.h>
#include <SPI.h>
#include<FastMap.h>

// Constants
#define flexCapacitiveSensor_MIN 0//-2000//0
#define flexCapacitiveSensor_MAX 180//8000//11600
#define position_MIN 64//46//46 //139 new
#define position_MAX 139//130 // 47 new

// Pin Names
#define position1_IN A3 // pin to measure position1_Measured
#define position1_OUT 9 // pin to send position1_Command
#define button_IN 4 // pushbutton
#define led_OUT 6 // led indicator
#define CHIP_SELECT 10 // SD card writing

//////////////////////////////////////////////////////////////////////////////////////////
// SET VALUES BEFORE
const bool serialON = true; // sets if device will write data to serial
const int actuatorType = 1; // 1 indicates either the original actuator or Tom's, 2 is the additional one we ordered
const bool fastMapON = false; // set true if reading flex value as a float and doing mapFloat
const bool sdWriteON = !(serialON); // if outputting data via serial, no need to write to SD card
const int WRITE_COUNT = 25;//100; // typically 2000, for every n runtime cycles, write out data
int T_CYCLE = 10; // help sets minimum time length per cycle FIX Why doesn't work with 0
//////////////////////////////////////////////////////////////////////////////////////////

const byte I2C_ADDR = 0x04; // force sensor
int user_position_MIN = position_MIN;  // --- CALIBRATION --- //
int user_position_MAX = position_MAX;
float user_flex_MIN = flexCapacitiveSensor_MIN;
float user_flex_MAX = flexCapacitiveSensor_MAX;

typedef enum { NONE, ZERO_FORCE, FLEX, MAX_PRESSURE, ACTUATOR  
} CALIBRATION_OPTIONS;

int cycleCount = 0; //keeps track of cycle so knows when to send serial data
bool powerOn; // checks if 12V on

Servo actuator1;  // ---- ACTUATOR ----- create servo object to control a servo
int position1_Command = 0;    // variable to store the servo command
int position1_Measured = 0;

ADS capacitiveFlexSensor;// ---- FLEX SENSOR -----
//int16_t flexSensor = 0; 
float flexSensor = 0.0; // variable to store sensor value
FastMap mapper; // mapFloat efficiently

int buttonState = 0; // ---- PUSHBUTTON --- //
int oldButtonState = 0;
int buttonCount = 0;

// SD Card Batching
//const int BUFFER_SIZE = 25; // how many datastrings until sd card write within 512 buffer
//String buf = "";
//int bufferCount = 0;
// Characterizing Actuators
//const int COMMAND_COUNT = 400000; //for slow sweep of actuator position
//int commandCount = 0;

//////////////////////////////////////////////////////////////////////////////////////////

void setup() {
  initializeSystem();
  analogWrite(led_OUT, 30);
  Serial.println("Actuator and flex sensor connected. Entering calibration mode. Close serial monitor and start calibration.py");
  calibration();
  if (fastMapON) mapper.init(0, 180, user_position_MIN, user_position_MAX);
  Serial.println("Calibrated. Entering runtime");
  //while(!risingEdgeButton());
}


void loop() {
  if(buttonCount % 2 == 0) runtime(true);
  else runtime(false);
}


//////////////////////////////////////////////////////////////////////////////////////////
// SUPPORTING FUNCTIONS //
//////////////////////////////////////////////////////////////////////////////////////////
void initializeSystem() {
  Wire.begin(); // join i2c bus
  initializeSerial(); // start serial for output
  initializeSDCard(); // initialize sd card
  initializeActuator(); // initialize actuator and set in min position
  initializeFlexSensor(); // initialize flex sensor
  initializeIO(); // initialize IO pins, i.e. button and led
}


void initializeIO() {
  pinMode(button_IN, INPUT); // set button and led
  pinMode(led_OUT, OUTPUT);
}


void initializeActuator() {
  actuator1.attach(position1_OUT); // attach servo 
  actuator1.write(position_MIN); //put in minimum position
}

void initializeFlexSensor() {
    if (capacitiveFlexSensor.begin() == false) {
      Serial.println(("No sensor detected. Check wiring. Freezing..."));
      while (1);
  }
  capacitiveFlexSensor.enableStretching(true);
}

void initializeSerial() {
    Serial.begin(4608000);  
    Serial.flush();
    while (!Serial);
}

void initializeSDCard() {
  if (sdWriteON) {
    // See if the card is present and can be initialized:
    if (!SD.begin(CHIP_SELECT)) {
      Serial.println("Card failed, or not present");
      while (1);
    }
    Serial.println("card initialized.");
    // fix test code
    //    SD.remove("raw_data.csv");
    //    Serial.println("Removed old data");
  }
}


void testLed () {
  digitalWrite(led_OUT, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);               // wait for a second
  digitalWrite(led_OUT, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);               // wait for a second
}

void testPushbutton () {
  digitalWrite(led_OUT, LOW);
  if (risingEdgeButton()) {
    if (serialON) Serial.println("Pushed!");
    digitalWrite(led_OUT, HIGH);
    delay(50);
    digitalWrite(led_OUT, LOW);
  }
}

void blink_T (int t_d) {
  digitalWrite(led_OUT, LOW);
  delay(t_d);
  digitalWrite(led_OUT, HIGH);
  delay(t_d);
}

void blinkN (int n, int t_d) {
  for(int i=0; i < n; i++) {
    analogWrite(led_OUT, 10);
    delay(t_d/2);
    analogWrite(led_OUT, 200);
    delay(t_d/2);  
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

//void writeOutDataBatching(unsigned long t, int f, int c, int m, short d, unsigned long t1, unsigned long t2, unsigned long t3, unsigned long t4) {
//  String dataString = "";
//  
//  if (sdWriteON) {
//    buf += (String(t) + "," + String(f) + "," + String(c) + "," \
//    + String(m) + "," + String(d) + "\n");
//    bufferCount = bufferCount + 1;
//    
//    if (bufferCount == BUFFER_SIZE) {
//      File dataFile = SD.open("raw_data.csv", FILE_WRITE);
//      if (dataFile) {
//        dataFile.print(buf);
//        dataFile.close();
//        bufferCount = 0;
//        buf = "";
//      }
//    }
//  } else if (serialON) {
//      dataString = (String(t) + "," + String(f) + "," + String(c) + "," \
//      + String(m) + "," + String(d) + "," + String(t1) + "," + String(t2) + "," + String(t3) + "," + String(t4) + ",");
//      Serial.print(dataString);
//  }
//}

void safety() {
      // Safety withdraw actuator and stop
    if (risingEdgeButton()) {
      actuator1.write(position_MIN);
      if (serialON) Serial.println("Device off. Turn off power.");
      if (sdWriteON) {
        File dataFile = SD.open("raw_data.csv", FILE_WRITE);
        if (dataFile) {
            //dataFile.print(buf);
            dataFile.close();
        }
      }
      while (1);
    }
}

void runtime(bool feedback) {
    short data;
    unsigned long myTime;

    // time for the beginning of the loop
    myTime = millis();
    // Read flex sensor
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    //myTime_1 = micros();
    
     // Map angle to actuator command
    if (fastMapON) position1_Command = mapper.map(flexSensor);
    else position1_Command = map(int(flexSensor), 0, 180, user_position_MIN, user_position_MAX); // FIX: why does fastmap on and off change the outcome. And why does map not work when 0,180 vs user_MIN user MAX
    //FIX WHY does fast map on cause actuator to move to extremes only
    if(position1_Command > position_MAX) position1_Command = position_MAX;
    else if(position1_Command < position_MIN) position1_Command = position_MIN;

    //myTime_2 = micros(); // after computation
    
    // Send command to actuator
    if (feedback) actuator1.write(position1_Command);
    else actuator1.write(position_MIN);

    //myTime_3 = micros(); // after sending to servo
    
    // Measure actuator position
    position1_Measured = analogRead(position1_IN);

    cycleCount = cycleCount + 1;

    //myTime_4 = micros(); // after reading
    
    if ((cycleCount == WRITE_COUNT)) {
      data = readDataFromSensor(I2C_ADDR);
      powerOn = (data >= 150);
      if (powerOn) analogWrite(led_OUT, 255);
      else analogWrite(led_OUT, 30);
      //writeOutDataBatching(myTime, flexSensor, position1_Command, position1_Measured, data, myTime_1, myTime_2, myTime_3, myTime_4);
      writeOutData(myTime, flexSensor, position1_Command, position1_Measured, data);
      cycleCount = 0;
    }


    risingEdgeButton();
    if (T_CYCLE > 0) delay(T_CYCLE);

    //myTime_5 = micros(); // after data write out
}

void runtime_NoFeedback() {
    short data;
    unsigned long myTime;
    
    // time for the beginning of the loop
    myTime = millis();
    
    // Read flex sensor
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    
    // Map angle to actuator command
    if (fastMapON) position1_Command = mapper.map(flexSensor);
    else position1_Command = map(int(flexSensor), 0, 180, user_position_MIN, user_position_MAX); // FIX: why does fastmap on and off change the outcome. And why does map not work when 0,180 vs user_MIN user MAX
    //FIX WHY does fast map on cause actuator to move to extremes only
    if(position1_Command > position_MAX) position1_Command = position_MAX;
    else if(position1_Command < position_MIN) position1_Command = position_MIN;

    // Send command to actuator
    actuator1.write(position_MIN);
    
    // Measure force and actuator position
    position1_Measured = analogRead(position1_IN);

    cycleCount = cycleCount + 1;
    
    if ((cycleCount == WRITE_COUNT)) {
      data = readDataFromSensor(I2C_ADDR);
      powerOn = (data >= 150);
      if (powerOn) analogWrite(led_OUT, 255);
      else analogWrite(led_OUT, 30);
      writeOutData(myTime, flexSensor, position1_Command, position1_Measured, data);
      cycleCount = 0;
    }
    risingEdgeButton();
    if (T_CYCLE > 0) delay(T_CYCLE);
}

// sweeping actuator position, increasing and decreasing. infinite loop.
// t_d is time between actuator steps
int sweep(int t_d) {
    unsigned long myTime;
    int counter = user_position_MIN;
    int extending = 1;
    int minValue = 1000;
    
    
    while (counter <= position_MAX) {
      String dataString = "";
      actuator1.write(counter);
      position1_Measured = analogRead(position1_IN);
      myTime = millis();
      if (position1_Measured < minValue) minValue = position1_Measured;

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
          break; // comment if I want infinite sweeping
        } else counter = counter - 1;
      }
      delay(t_d);
    }
    return minValue;    
}


// Measuring Actuator Position. Slow ladder step
//void sweep2() {
//    unsigned long myTime_1;
//    unsigned long myTime_2;
//    short data;
//    int c = user_position_MIN;
//
//    while (c <= user_position_MAX) {
//      String dataString = "";
//
//      commandCount = commandCount + 1;
//      cycleCount = cycleCount + 1;
//
//      myTime_1 = micros();
//
//      //if (risingEdgeButton()) {
//      if (commandCount == COMMAND_COUNT) {
//        if (actuatorType == 1) {
//          actuator1.write(c);  
//        } else {
//          actuator1.write(180-c);
//        }
//        c = c + 1;
//        commandCount = 0;
//      }
//
//      myTime_2 = micros();
//
//      if (cycleCount == WRITE_COUNT) {
//        position1_Measured = analogRead(position1_IN);
//        data = readDataFromSensor(I2C_ADDR);
//        if (serialON) {
//          dataString = (String(myTime_1) + "," + String(myTime_2) + "," + String(c) + "," + String(data) + "," + String(position1_Measured) + ",");
//          Serial.println(dataString);
//        }
//        cycleCount = 0;
//      }
//
//    }
//}

void calibrationActuatorFeedback() {
  int ACTUATOR_FEEDBACK_MAX = 500;
  int ACTUATOR_FEEDBACK_MIN = 500;
  
  // Calibration: Sweep and record the actuator position feedback positions
  actuator1.write(position_MIN);
  
//  Serial.println("-------------------------------------------");
//  Serial.println("CALIBRATION: ACTUATOR");
//  Serial.println("-------------------------------------------");
//  Serial.println("Instructions: For this calibration stage, please don't wear the actuator. Make sure power is on and press the button when ready.");
//  while(!risingEdgeButton());
  
  delay(500);
  ACTUATOR_FEEDBACK_MAX = analogRead(position1_IN);
  ACTUATOR_FEEDBACK_MIN = sweep(300);
  Serial.println(ACTUATOR_FEEDBACK_MAX);
  Serial.println(ACTUATOR_FEEDBACK_MIN);
//  Serial.println("Calibration stage complete. Press button to move on.");
//  while(!risingEdgeButton());
}

void calibrationZeroForce() {
  short zeroForce = 0;
  
  // Calibration Stage: Get the zero force of the device
  actuator1.write(position_MIN);
//  Serial.println("-------------------------------------------");
//  Serial.println("CALIBRATION: ZERO FORCE");
//  Serial.println("-------------------------------------------");  
//  Serial.println("Instructions: Please wear the device and keep your arm relaxed, no need to do anything. Make sure power is on.");
//  Serial.println("Press button once when you're ready to begin.");
//  while(!(risingEdgeButton()));
  
  zeroForce = readDataFromSensor(I2C_ADDR);
//  Serial.println("Calibration stage complete. Zero Force = ");
  Serial.println((zeroForce - 255) * (45.0)/512);
//  Serial.println("Researcher will record values and will let you know when to click button to move on.");
//  while(!risingEdgeButton());
}

void calibrationFlexSensor() {
  unsigned long startTime;
  unsigned long endTime;
  unsigned long TIME_LENGTH = 30000;

  actuator1.write(position_MIN);
//  Serial.println("-------------------------------------------");
//  Serial.println("CALIBRATION: FLEX SENSOR");
//  Serial.println("-------------------------------------------");
//  
//  Serial.println("Instructions: Please wear the device.");
//  Serial.println("Raise your right arm with your palm facing the ceiling until it is parallel with the table.");
//  Serial.println("Keeping your upper arm parallel still, bend your elbow towards yourself and then back to the original position.");
//  Serial.println("Please repeat this motion until researcher tells you to stop.");
//  Serial.println("Press button once when you're ready to begin.");
//  while(!(risingEdgeButton()));
//  Serial.println("Begin flex sensor calibration");

    // use the initial value as baseline. otherwise user_flex is set at 0 180 default
    if (capacitiveFlexSensor.available() == true) user_flex_MIN = capacitiveFlexSensor.getX();
    user_flex_MAX = user_flex_MIN;
    Serial.println(user_flex_MIN);
    delay(2*T_CYCLE);
 
  // record flex values for x seconds
  startTime = millis();
  endTime = millis();

  while((endTime - startTime) < TIME_LENGTH) {
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    if (flexSensor < user_flex_MIN) user_flex_MIN = flexSensor;
    else if (flexSensor > user_flex_MAX) user_flex_MAX = flexSensor;
    Serial.println(flexSensor);
    endTime = millis();
    delay(2*T_CYCLE);
  }

  startTime = millis();
  endTime = millis();
  while((endTime - startTime) < TIME_LENGTH) {
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    Serial.println(flexSensor);
    endTime = millis();
    delay(2*T_CYCLE);
  }
//  Serial.println(user_flex_MIN);
//  Serial.println(user_flex_MAX);
  
  
  // send signal fix
  
  // Serial.println("Calibration stage complete. Researcher will record values and will let you know when to press the button to move on.");
  //while(!risingEdgeButton());
}

int calibrationMaxDeepPressure() {
   int counter = position_MIN;
   int x;
   //short data;
   short maxForce = 0;
   short zeroForce = 0;

//   Serial.println("-------------------------------------------");
//   Serial.println("CALIBRATION: MAX PRESSURE ");
//   Serial.println("-------------------------------------------");
//   Serial.println("Instructions: Please wear the device. Make sure power is on. The actuator will extend into your arm and apply a deep pressure.");
//   Serial.println("During this stage, please click the button once to indicate when it is too uncomfortable.");
//   Serial.println("When you're ready to begin calibration stage, press the button.");
//
//   while(!(risingEdgeButton()));

//   Serial.println("Calibration Stage beginning...");

   actuator1.write(counter);
   blinkN(5,1000);
   zeroForce = readDataFromSensor(I2C_ADDR);
   // Calibration Stage: Get the detection and pain thresholds
    while (counter <= position_MAX) {
       // Measure force and actuator position
      //data = readDataFromSensor(I2C_ADDR);
      position1_Measured = analogRead(position1_IN);
      // Send command to actuator
      actuator1.write(counter);
      //if (serialON) Serial.println((data - 255) * (45.0)/512);
      if (Serial.available() > 0) x = (Serial.read() - '0');
//      Serial.println(x);
      if (risingEdgeButton() || (x == 5)) {

          user_position_MAX = counter - 2;
          maxForce = readDataFromSensor(I2C_ADDR);
          actuator1.write(position_MIN);
          break; 
      }
      delay(250);
      counter = counter + 1;
  }
  actuator1.write(position_MIN);

//Serial.println("ZERO FORCE:");
  Serial.println(zeroForce);
//Serial.println("UPPER LIMIT FORCE:");
  Serial.println(maxForce);
//  Serial.println("Calibration stage complete. Max actuator positions is:");
  Serial.println(user_position_MAX);
//  Serial.println("Make sure to researcher records these values and press button to proceed.");
//  while(!risingEdgeButton());
  return user_position_MAX;
}

/* Calibration */
void calibration() {
  CALIBRATION_OPTIONS mode;
  bool calibrationComplete = false;
  int nMaxPressure = 0;
  int sum = 0;
  int user_position_MAX_arr[10];
  
  // Reset position of actuator
  if (actuatorType == 1) actuator1.write(position_MIN);  
  else actuator1.write(180-position_MIN);

  while(!(calibrationComplete)){
    if (Serial.available() > 0) {
      mode = CALIBRATION_OPTIONS(Serial.read() - '0');
      switch (mode) {
        case FLEX:
          calibrationFlexSensor();
          break;
        case MAX_PRESSURE:
          user_position_MAX_arr[nMaxPressure] = calibrationMaxDeepPressure();
          nMaxPressure = nMaxPressure + 1;
          for (int i = 0; i< nMaxPressure; i++) {
            sum = sum + user_position_MAX_arr[i];
          }
          user_position_MAX = sum/nMaxPressure;
          break;
        case ACTUATOR:
          calibrationActuatorFeedback();
          break;
        case NONE:
          calibrationComplete = true;
        default:
          break;
      }
      delay(50); 
    }
  }
}

bool risingEdgeButton() {
  buttonState = digitalRead(button_IN);
  //Serial.println(buttonState);
  if (buttonState != oldButtonState) {
    if (buttonState == HIGH) {
      buttonCount = buttonCount + 1;
      oldButtonState = buttonState;
      delay(300);
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
