/*
 * Firmware Code for Proprioception Wearable Device
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */
#include <MightyZap.h>
#include "SparkFun_Displacement_Sensor_Arduino_Library.h"
#include <MightyZap.h>
#include <Servo.h>
#include <Wire.h>
#include <SD.h>
#include <SPI.h>
#include <movingAvg.h>
#include "IntervalTimerEx.h"
#include "skFilter.h"
#include "skFilter_terminate.h"

# define N_ACT 2
# define T_SAMPLING 1000000
#define WINDOW_SIZE 50


// MightyZap actuator limits
typedef enum {
  POSITION_MIN = 0, 
  POSITION_MAX = 4095
} ACTUATOR_LIMITS;

//MightyZap* m_zap;
movingAvg filter(WINDOW_SIZE);

int  user_position_MIN = POSITION_MIN;
int  user_position_MAX = 1000;
const bool serialON = true;
//float  user_flex_MIN;
//float  user_flex_MAX;
int  buttonCount; // button count. global!

int position_CommandArr[N_ACT];
short forceData[N_ACT];
int position_MeasuredArrGlobal[N_ACT];

const  byte I2C_ADDRArr[4] = {0x06, 0x08, 0x0A, 0x0C};
const bool actuatorType = 1; // NEW. 0 = actuonix and 1 = MightyZap. CHANGE THIS for new actuator!
const int mightyZapWen_OUT = 12; // FIX THIS: temporary write enable output signal for buffer


MightyZap m_zap(&Serial4, mightyZapWen_OUT);

int WRITE_COUNT = 8;
int T_CYCLE = 15; // minimum delay to ensure not sampling at too high a rate for sensors
short zeroForceArr[N_ACT]; // should this be local?

//  IntervalTimerEx ForceSampleSerialWriteTimer;
   
//const  int position_INArr[4] = {21, 20, 22, 23}; // analog adc pins
//const  int position_OUTArr[4] = {7, 6, 8, 9}; // pwm output
const int  button_IN = 4;
const int  led_OUT = 5;
  
 // flex sensor and angle
ADS  capacitiveFlexSensor;
//float  flexSensor; // could be local(?)

// Pushbutton & LED
int  buttonState; // button state
int  oldButtonState; // old button state
  



void setup() {
    initializeSystem(0);
    Serial.println("Device initialized.");
    if (CrashReport) {
    /* print info (hope Serial Monitor windows is open) */
    Serial.print(CrashReport);
  }

}

void loop() {
  sweep(1000,1);
}


// -------------------- SUPPORT FUNCTIONS --------------------//
void writeActuator(int idx, int pos) {
  if (actuatorType) m_zap.GoalPosition(idx+1,pos); // mightyZap
  //else actuatorArr[idx].write(pos); // actuonix
}

int readFeedback(int idx) {
  int value = -1;
  if (actuatorType) value = m_zap.presentPosition(idx+1); // if mightyZap
  else {
    //value = analogRead(position_INArr[idx]); // if actuonix
  }
  return value;
}

// sweeping actuator position, increasing and decreasing. infinite loop.
// t_d is time between actuator steps. idx is which actuator
int sweep(int t_d, int idx) {
    unsigned long myTime;
    short data;
    short filteredData;
    bool retracting = false;
    int position_Measured = 0;
    int counter = user_position_MIN-1;
    int inc = 50;
    int minValue = 1000;
    //bool localWriteOut;
    unsigned long startTimeCmd = millis();
    unsigned long startTimeWriteOut = millis();
    String dataString;
    int td_WriteOut = 100;

    while(1) {

      
      myTime = millis();

      // update counter for new position commands for sweep
      if (int(myTime - startTimeCmd) > t_d) {
        counter = counter + inc;
        //bound the command
        if(counter > user_position_MAX) counter = user_position_MAX;
        else if(counter < user_position_MIN) counter = user_position_MIN;
        //Serial.println(counter);
        writeActuator(idx, counter);
        startTimeCmd = millis();
      }

      // update counter for writing out and reading data
      if (int(myTime - startTimeWriteOut) > td_WriteOut) {
        data = readDataFromSensor(I2C_ADDRArr[idx]);
        //filteredData = filter.reading(data);
        position_Measured = readFeedback(idx); // this adds 152 ms
        dataString += (String(myTime) + "," + String(counter) + "," + String(position_Measured) + "," + data);
        if (serialON) Serial.println(dataString);
        startTimeWriteOut = millis();
        dataString = "";
      }


//      noInterrupts();
//      localWriteOut = writeOut;
//      // read force data and write out data. writeOut is activated by IntervalTimer, interrupt based
//    
//      if (localWriteOut) {
//        dataString = "";
//        data = forceData[n];
//        position_Measured = position_MeasuredArrGlobal[n];
//        if (position_Measured < minValue) minValue = position_Measured;
//        dataString += (String(myTime) + "," + String(counter) + "," + String(position_Measured) + "," + data);
//        if (serialON) Serial.println(dataString);
//        //writeOutData(N_ACTUATORS, myTime, flexSensor, position_CommandArr, position_MeasuredArr, data);
//        writeOut = false;
//      }
//      interrupts(); 

      if (counter >= user_position_MAX) {
        inc = -1 * inc;
        retracting = true;
      }
      else if (counter <= (user_position_MIN) && retracting) break;

    }
    return minValue;    
}


// FIX: need to add multiple filters
void directActuatorControl(int n) {
    short data[n];
    int position_Measured[n];
    unsigned long myTime;
    int i;
    bool localWriteOut;
    unsigned long startTime = millis();
    int td_writeOut = 500;
    
    while(1) {
      
      myTime = millis(); // time for beginning of the loop
      if (int(myTime - startTime) > td_writeOut) {
        for (i=0; i < n; ++i) data[i] = readDataFromSensor(I2C_ADDRArr[i]);
        for (i=0; i < n; ++i) position_Measured[i] = readFeedback(i);
        writeOutData(n, myTime, position_CommandArr, position_Measured, data);
        startTime = millis();
      }
      
    // parse serial input for command value
      if (Serial.available() > 0) {
        position_CommandArr[0] = Serial.parseInt();
        Serial.read(); // comment out if python
        Serial.println(position_CommandArr[0]);
        //bound the command
        if(position_CommandArr[0] > user_position_MAX) position_CommandArr[0] = user_position_MAX;
        else if(position_CommandArr[0] < user_position_MIN) position_CommandArr[0] = user_position_MIN;

        // pass the command to other actuators
        if (n > 1) {
            for (i=1; i < n; ++i) position_CommandArr[i] = position_CommandArr[0];
        }
      }

    // Send command to actuator and measure actuator position
    if (!(buttonCount % 2)) for (i=0; i < n; ++i) writeActuator(i, position_CommandArr[i]);
    else for (i=0; i < n; ++i) writeActuator(i, POSITION_MIN);

//    noInterrupts();
//    localWriteOut = writeOut;
//    // read force data and write out data at lower frequency. writeOut is activated by IntervalTimer, interrupt based
//    
//    if (localWriteOut) {
//      for (i=0; i < N_ACTUATORS; ++i) data[i] = forceData[i];
//      writeOutData(N_ACTUATORS, myTime, flexSensor, position_CommandArr, position_Measured, data);
//      writeOut = false;
//    }
//    interrupts(); 

    risingEdgeButton();
    if (T_CYCLE > 0) delay(T_CYCLE);  
  }  
}

void writeOutData(int l, unsigned long t, int *c, int *m, short *d) {
  int i;
  String dataString = "";
  if (serialON) {
    dataString += (String(t));

    for (i=0; i < l; ++i) {
      dataString += ( "," + String(c[i]) + "," + String(m[i]) + "," + String(d[i]));
    }
    if (serialON) Serial.println(dataString);
  }  
}

void safety() {
      // Safety withdraw actuator and stop
    if (risingEdgeButton()) {
      int i;
      for (int i=0; i < N_ACT; ++i) writeActuator(i, POSITION_MIN);

      if (serialON) Serial.println("Device off. Turn off power.");
      while (1);
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

void blinkN (int n, int t_d) {
  //noInterrupts();
  for(int i=0; i < n; i++) {
    analogWrite(led_OUT, 10);
    delay(t_d/2);
    analogWrite(led_OUT, 200);
    delay(t_d/2);
  }
  //interrupts();
}

void initializeSystem(bool c) {
  Wire.begin(); // join i2c bus
  initializeSerial(); // start serial for output
  initializeMightyZap();
  filter.begin();
  for (int i=0; i < N_ACT; ++i) writeActuator(i, POSITION_MIN); // initialize actuator and set in min position
  //flexSensor = 180; 
  initializeIO(); // initialize IO pins, i.e. button and led
  analogWrite(led_OUT, 10);
//  if (c) {
//    Serial.println("Entering calibration...");
//    calibration();
//  }
}

void initializeMightyZap(){
//    MightyZap m_zapObj(&Serial4, mightyZapWen_OUT);
//    m_zap = &m_zapObj;
    m_zap.begin(32);
    
}
bool initializeSerial() {
    Serial.begin(4608000);  
    Serial.flush();
    while (!Serial);
    return (true); 
}

bool initializeIO() {
  pinMode(button_IN, INPUT); // set button and led
  pinMode(led_OUT, OUTPUT);
  return (true); 
}


short readDataFromSensor(short address) {
  byte i2cPacketLength = 6;//i2c packet length. Just need 6 bytes from each peripheral
  byte outgoingI2CBuffer[3];//outgoing array buffer
  byte incomingI2CBuffer[6];//incoming array buffer
  bool debug;

  debug = false;

  outgoingI2CBuffer[0] = 0x01;//I2c read command
  outgoingI2CBuffer[1] = 128;//peripheral data offset
  outgoingI2CBuffer[2] = i2cPacketLength;//require 6 bytes

  if (debug) Serial.println("Transmit address");  
  Wire.beginTransmission(address); // transmit to device 
  Wire.write(outgoingI2CBuffer, 3);// send out command
  if (debug) Serial.println("Check sensor status");
  byte error = Wire.endTransmission(); // stop transmitting and check peripheral status
  if (debug) Serial.println("bloop");
  if (error != 0) return -1; //if peripheral not exists or has error, return -1
  Wire.requestFrom((uint8_t)address, i2cPacketLength);//require 6 bytes from peripheral
  if (debug) Serial.println("Request bytes from sensor");
  
  byte incomeCount = 0;
  while (incomeCount < i2cPacketLength)    // peripheral may send less than requested
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
