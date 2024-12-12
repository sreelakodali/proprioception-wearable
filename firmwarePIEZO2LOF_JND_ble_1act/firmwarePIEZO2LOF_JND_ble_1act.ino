/*
 * Firmware Code for Proprioception Wearable Device 
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */
#include <Arduino.h>
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_UART.h"
//
//#include "BluefruitConfig.h"
 
#include <MightyZap.h>
#include "SparkFun_Displacement_Sensor_Arduino_Library.h"
#include <Servo.h>
#include <Wire.h>
#include "skFilter2.h"
#include "skFilter2_terminate.h"

//#include <Arduino.h>
//#include "Adafruit_BLE.h"
//#include "Adafruit_BluefruitLE_UART.h"
//#include "BluefruitConfig.h"

//#include "IntervalTimerEx.h"

# define N_ACT 1
#define ID_NUM 1

// BLE UART 
#define BUFSIZE                        128   // Size of the read buffer for incoming data
#define VERBOSE_MODE                   false  // If set to 'true' enables debug output
#define BLUEFRUIT_HWSERIAL_NAME      Serial2
#define BLUEFRUIT_UART_MODE_PIN        11    // Set to -1 if unused
#define FORCE_MIN 0.0 
#define FORCE_MAX 20.0//4095

typedef enum {
  POSITION_MIN = 0, 
  POSITION_MAX = 2000//4095
} ACTUATOR_LIMITS;


// Calibration states
typedef enum { NONE, LOADMINMAX, MAX_PRESSURE, FILTER 
} CALIBRATION_OPTIONS;

// System wide variables
double tScale = 3.34;
int  buttonCount = 0; // button count. global!
//float  user_flex_MIN;
//float  user_flex_MAX;
//  IntervalTimerEx ForceSampleSerialWriteTimer;
const bool bleON = true;
const bool serialON = false;

const bool calibratepidON = false;
const  byte I2C_ADDR = 0x04;
const  byte I2C_ADDRArr[4] = {0x04, 0x08, 0x0A, 0x0C};
const bool actuatorType = 1; // NEW. 0 = actuonix and 1 = MightyZap. CHANGE THIS for new actuator!
const int mightyZapWen_OUT = 12; // write enable output signal for buffer
const int t_setup = 15000; // set up time for filter values to stabilize
const int T_CYCLE = 15*tScale; // minimum delay to ensure not sampling at too high a rate for sensors
const int td_WriteOut = 100; // write out rate


// MightyZap actuator
MightyZap m_zap(&Serial5, mightyZapWen_OUT);
int  user_position_MIN = POSITION_MIN;
int  user_position_MAX = POSITION_MAX;
float user_force_MIN = FORCE_MIN;
float user_force_MAX = FORCE_MAX-3;
int measuredPos;
short zeroForceGlobal = 255;

// skFilter
int test = 1;
short xData[1] = {0};
float yData[1] = {0};

// I/O and additional peripherals
const int  button_IN = 4;
const int  led_OUT = 5;
const int  ledPower_OUT = 13;
//int buttonCount = 0;
int  buttonState; // button state
int  oldButtonState; // old button state  
ADS  capacitiveFlexSensor;  // flex sensor and angle
//float  flexSensor; // could be local(?)

// BLE UART
Adafruit_BluefruitLE_UART ble(BLUEFRUIT_HWSERIAL_NAME, BLUEFRUIT_UART_MODE_PIN);
int idx_BLERx = 0;
char* strBuf = "";
char detectionChar = 'x';

// PID

//// ACTUATOR 2
//double scaleF = 0.25;
////double tScale = 3.34;
//double KpConst = 60*scaleF;//130.00;
//double KiConst = 310*scaleF;//0.031;
//double KdConst = 25;//50*scaleF;//30.0;
//double setPointTest = 2.0;
//double td = 0.02*tScale;

// ACTUATOR 1
double scaleF = 2;
double KpConst = 10*scaleF;//130.00;
double KiConst = 32*scaleF;//0.031;
double KdConst = 15;//50*scaleF;//30.0;
double setPointTest = 0.0;
double td = 0.02*tScale;

// PID
// create struct of PID_sk type called myPID
struct PID_sk {
  double Kp; //how quickly system responds
  double Ki; // changes the steady-state error. cap term because of integral windup
  double Kd; // dampens out oscillations, but can slow down response time
  double setpoint;
  double pErr;
  double Iterm;
  int actuatorCommand;
  short zeroForce;
  unsigned long pTime;
  unsigned long tLastWriteout;
} myPID;


void setup() {
    initializeSystem();
    if (ID_NUM ==2 ) {
          // ACTUATOR 2
        scaleF = 0.25;
        KpConst = 60*scaleF;//130.00;
        KiConst = 310*scaleF;//0.031;
        KdConst = 25;//50*scaleF;//30.0;
        setPointTest = 0.0;
        td = 0.02*tScale;
        
        detectionChar = 'y';
    }
    if (serialON) Serial.println("Device initialized.");
//    if (bleON) ble.println("Device initialized.");
    blinkN(5, 500);

    // initialize PID
    initializePID(&myPID, KpConst, KiConst, KdConst, setPointTest);
    
    // CALIBRATION
    zeroForceGlobal = initializeFilter();
    myPID.zeroForce = zeroForceGlobal;

    blinkN(5, 500);
    //ble.println("in calibration");
    calibration();
    //FIX: INSERT MIN MAX PRESSURE CALIBRATION
    blinkN(5, 500);
     //Serial.println(ble.isConnected());

}

void loop() {

 unsigned long myTimeLoop = millis();
 short data = readDataFromSensor(I2C_ADDR); // 1) read input
 double filteredData1 = filterData(data, 1);
 double error = computeError(&myPID, filteredData1); // 3) compute error between input and setpoint 
 
 myPID.actuatorCommand = PIDcompute(&myPID, error);
 m_zap.GoalPosition(ID_NUM, myPID.actuatorCommand);

 if ((myTimeLoop - myPID.tLastWriteout) > td_WriteOut) { // writeout data
  String dataString = "";
  //dataString += (String(myTimeLoop));
  
  // dataString += (String(myPID.setpoint) + "," + String(filteredData1)+ "," + String(myPID.setpoint - error));
  dataString += (String(myTimeLoop) + "," + String(myPID.setpoint) + "," + String(myPID.setpoint - error) + "," + String(filteredData1)+ "," + String(myPID.actuatorCommand) + "," + String(measuredPos));
  if (calibratepidON) dataString =  (String(myPID.setpoint)+ "," + String(myPID.setpoint - error));
  if (serialON) Serial.println(dataString);
  if (bleON) ble.println(dataString);
  //myPID.tLastWriteout = millis();
 }

 if (bleON) directActuatorControlForce();
 if (serialON) serialActuatorControlForce();
 measuredPos = m_zap.presentPosition(ID_NUM);
 
//if (T_CYCLE > 0) delay(T_CYCLE);  
//  sweep(2000,ID_NUM-1);
 
}


// -------------------- SUPPORT FUNCTIONS --------------------//


// Calibration functions

// FIX: FYI won't need this
void calibrationActuatorFeedback() {
  int i;
  int ACTUATOR_FEEDBACK_MAX = 500;
  int ACTUATOR_FEEDBACK_MIN = 500;

  // Calibration: Sweep and record the actuator position feedback positions
  writeActuator(ID_NUM-1, POSITION_MIN);

  
  delay(500);
  ACTUATOR_FEEDBACK_MIN = readFeedback(ID_NUM);
  ACTUATOR_FEEDBACK_MAX = sweep(300, ID_NUM);
  if (serialON) Serial.println(ACTUATOR_FEEDBACK_MAX);
  if (serialON) Serial.println(ACTUATOR_FEEDBACK_MIN);
  if (bleON) ble.println(ACTUATOR_FEEDBACK_MAX);
  if (bleON) ble.println(ACTUATOR_FEEDBACK_MIN);
}


int serialMinMaxCalibration() {
  if (Serial.available()) {
  int mode = (Serial.read() - '0');
  Serial.read();
    return mode;
  }
  return -1;
}
// Calibration Stage: Get the detection and pain thresholds
int calibrationMaxDeepPressure() {
   int counter = POSITION_MIN;
   int x = 0;
   short data;
   int position_Measured;
   String dataString;
   int nClicks = 0;

   writeActuator(ID_NUM-1, POSITION_MIN);
   blinkN(5,1000);

    while (counter <= POSITION_MAX) {
       // Measure force and actuator position
      dataString = "";
      data = readDataFromSensor(I2C_ADDRArr[0]);
      position_Measured = 0;//readFeedback(ID_NUM);
      // Send command to actuator
//      writeActuator(ID_NUM-1, counter);
//      dataString += (String(counter) + "," + String((data - zeroForceGlobal) * (45.0)/512));
//      if (serialON) Serial.println(dataString);
//      if (bleON) ble.println(dataString);

      if (serialON)  x = serialMinMaxCalibration();
      if (bleON)  x = bleMinMaxCalibration();
      //ble.println(x);
      //if (Serial.available() > 0) x = (Serial.read() - '0');
      // FIX: if I get signal from user. how to detect calibration click
//      Serial.println(x);
      if (x == 5) {
        nClicks = nClicks + 1;
        x = 0;
      }
      if (nClicks == 1) {
          //Serial.println("min detected!");
          user_position_MIN = counter;
          delay(3000);
          user_force_MIN = (readDataFromSensor(I2C_ADDRArr[0]) - zeroForceGlobal) * (45.0)/512;
          //nClicks = nClicks + 1;
          dataString = ("MINIMUM FOUND: " + String(user_position_MIN) + String(user_force_MIN));
          if (bleON) ble.println(dataString);
          if (bleON) ble.println(dataString);
      }
      if (nClicks == 2) { // NOTE: nClicks = 3 is deliebrate. rising edge of click
          user_position_MAX = counter - 5; // NOTE: the -5 is arbitrary
          user_force_MAX = (readDataFromSensor(I2C_ADDRArr[0]) - zeroForceGlobal) * (45.0)/512;
          delay(3000);
          writeActuator(ID_NUM-1, POSITION_MIN);
          dataString = ("MAXIMUM FOUND: " + String(user_force_MIN) + "," + String(user_force_MAX) + "," + String(user_position_MIN) + "," + String(user_position_MAX));
          if (serialON) Serial.println(dataString);
          if (bleON) ble.println(dataString);
          break;
      }
      delay(20);
      counter = counter + 1;
  }

  writeActuator(ID_NUM-1, POSITION_MIN);
  
    dataString = ("CALIBRATION FOUND: " + String(user_force_MIN) + "," + String(user_force_MAX) + "," + String(user_position_MIN) + "," + String(user_position_MAX));
  if (serialON) Serial.println(dataString);
  if (bleON) ble.println(dataString);

  return user_position_MAX;;
}

int calibrationIncrementActuator(int counter) {
   //int x = 0;
   //int position_Measured;
   short data;
   String dataString;

//      if (serialON)  x = serialMinMaxCalibration();
//      if (bleON)  x = bleMinMaxCalibration();
   counter = counter + 5;
   if (counter > POSITION_MAX) counter = POSITION_MAX;
   if (counter < POSITION_MIN) counter = POSITION_MIN;
   dataString = "";
   data = readDataFromSensor(I2C_ADDRArr[0]);   
   writeActuator(ID_NUM-1, counter);
   dataString += (String(counter) + "," + String((data - zeroForceGlobal) * (45.0)/512));
   if (serialON) Serial.println(dataString);
   if (bleON) ble.println(dataString);

  return counter;
}

int calibrationDecrementActuator(int counter) {
   //int x = 0;
   //int position_Measured;
   short data;
   String dataString;

//      if (serialON)  x = serialMinMaxCalibration();
//      if (bleON)  x = bleMinMaxCalibration();
   counter = counter -5;
   if (counter > POSITION_MAX) counter = POSITION_MAX;
   if (counter < POSITION_MIN) counter = POSITION_MIN;
   dataString = "";
   data = readDataFromSensor(I2C_ADDRArr[0]);   
   writeActuator(ID_NUM-1, counter);
   dataString += (String(counter) + "," + String((data - zeroForceGlobal) * (45.0)/512));
   if (serialON) Serial.println(dataString);
   if (bleON) ble.println(dataString);

  return counter;
}

/* Calibration: Interfaces with python gui */
void calibration() {
  int x;
  bool calibrationComplete = false;
  int nClicks = 0;
  String dataString = "";
  int counter = POSITION_MIN;
  unsigned long clickTime = 0;
  unsigned long previousClickTime = 0;
          
  // Reset position of actuator
  writeActuator(ID_NUM-1, POSITION_MIN);
  
  while(!(calibrationComplete)){

      if (serialON) x = serialMinMaxCalibration();
      if (bleON) x = bleMinMaxCalibration();
      //if (x >= 0) ble.println(x);
      switch (x) {

        case 2:
          // alternate version sweep:
          // calibrationMaxDeepPressure();
          // increment forward
          counter = calibrationIncrementActuator(counter);
          //
          break;
        case 3:
          //zeroForceGlobal = initializeFilter();
          counter = calibrationDecrementActuator(counter);
          break;
        case 4:
             writeActuator(ID_NUM-1, POSITION_MIN); // max retract
              counter = POSITION_MIN;
          break;
          
        case 5:
          // LIMIT DETECTED
          previousClickTime = clickTime;
          clickTime = millis();
          //if ((clickTime - previousClickTime) > 500) {
            nClicks = nClicks + 1;
            float f = (readDataFromSensor(I2C_ADDRArr[0]) - zeroForceGlobal) * (45.0)/512;
            dataString = "LIMIT =" + String(counter) + "," + String(f);
            if (bleON) ble.println(dataString);
          break;
        case 0:
          writeActuator(ID_NUM-1, POSITION_MIN);
          calibrationComplete = true;
          //if (bleON) ble.println("DONE!");
          break;
        default:
          break;
      }
      delay(25); 
  }
  //writeActuator(ID_NUM-1, POSITION_MIN);
}



// NEW FUNCTIONS

void directActuatorControlForce() { 

  while ( ble.available() ) {
    char c = (char) ble.read();
    
    strBuf[idx_BLERx] = c;
    idx_BLERx = idx_BLERx + 1;
    
    if (c == '\n') {
      if (strBuf[0] == detectionChar) {
        char* strBuf2 = &strBuf[1];
        float setpoint = atof(strBuf2);
        if (serialON) Serial.print("NEW SETPOINT=");
        if (serialON) Serial.println(setpoint);
        if (bleON) ble.print("NEW SETPOINT=");
        if (bleON) ble.println(setpoint);
        blinkN(5, 200);
        changeSetpoint(&myPID, setpoint);
      }
      idx_BLERx = 0;
      strBuf = "";
    }

  }
}

int bleMinMaxCalibration() { 

  while ( ble.available() ) {
    char c = (char) ble.read();
    //ble.println(c);
    strBuf[idx_BLERx] = c;
    idx_BLERx = idx_BLERx + 1;
    
    if (c == '\n') {
      if (strBuf[0] == 'c') {
        idx_BLERx = 0;
        strBuf = "";
        return 2;
      } else if (strBuf[0] == 'z') {
        idx_BLERx = 0;
      strBuf = "";
        return 5; // click
      } else if (strBuf[0] == 'd') {
        idx_BLERx = 0;
      strBuf = "";
        return 0; // complete calibration
      } else if (strBuf[0] == 'w') {
        idx_BLERx = 0;
        strBuf = "";
        return 3; // complete calibration

      } else if (strBuf[0] == 'v') {
        idx_BLERx = 0;
        strBuf = "";
        return 4; // complete calibration
      }
      idx_BLERx = 0;
      strBuf = "";
    }
  }
  return -1;
}

void serialActuatorControlForce() {
  if (Serial.available() ) {

    float setpoint = Serial.parseFloat();
    Serial.read(); // for the carriage return

    if (setpoint > 20) {
      serialChangeParams();
    } else {
      if (serialON) Serial.print("NEW SETPOINT=");
      if (serialON) Serial.println(setpoint);
      blinkN(5, 200);
      changeSetpoint(&myPID, setpoint);
    } 
  }
}


// PID FUNCTIONS

short initializeFilter() {
    double filteredData1;
     // give the filters some time to begin
  unsigned long setupTime = millis();
  //tLastWriteout = millis();
  unsigned long myTimeSetup = millis();

  writeActuator(ID_NUM-1, POSITION_MIN);
  while ( (myTimeSetup - setupTime) < t_setup) {

    // every td_WriteOut seconds, read, filter and writeout data
    if ((myTimeSetup - myPID.tLastWriteout) > td_WriteOut)  {
      
      short data = readDataFromSensor(I2C_ADDR);
      filteredData1 = filterData(data, 1);
      
      
      String dataString = ""; // writeout       //dataString += (String(filteredData)+ "," + String(filteredData1) + "," + String(filteredData2));
      dataString += (String(data)+ "," + String(filteredData1));
      if (calibratepidON) dataString = "0.0, 4.0";
      if (serialON) Serial.println(dataString);
      if (bleON) ble.println(dataString);
      
      myPID.tLastWriteout = millis();
    }
    myTimeSetup = millis();
  }

  return filteredData1;
}

// initialze PID
void initializePID(PID_sk* pid, double p, double i, double d, double s) {
  (*pid).Kp = p;
  (*pid).Ki = i;
  (*pid).Kd = d;
  (*pid).setpoint = s;
  (*pid).pErr = 0.0;
  (*pid).Iterm = 0.0;
  (*pid).actuatorCommand = 0;
  (*pid).zeroForce = 0;
  (*pid).pTime = millis();
  (*pid).tLastWriteout = millis();
}

// change setpoint
void changeSetpoint(PID_sk* pid, float s) {

  if (s < user_force_MIN) s = user_force_MIN;
  if (s > user_force_MAX) s = user_force_MAX;
  (*pid).setpoint = s;
  (*pid).Iterm = 0.0;
  (*pid).pTime = millis();
}

// change parameters
void changePIDparam(PID_sk* pid, float p, float i, float d) {
  (*pid).Kp = p;
  (*pid).Ki = i;
  (*pid).Kd = d;
  (*pid).Iterm = 0.0;
  (*pid).setpoint = 0.0;
  (*pid).pTime = millis();
}

// compute error difference
double computeError(PID_sk* pid, double input) {
  double inputForce = (input - (*pid).zeroForce) * (45.0/512.0);
  double err = (*pid).setpoint - inputForce; //compute error between input and desired output/setpoint
  return err;
}

// compute
int PIDcompute(PID_sk* pid, double err) {
  // String dataString = "";
  // compute the PID terms
  unsigned long myTime = millis();
  double Pcomponent = (*pid).Kp * err;
  double Icomponent = (*pid).Ki * err * td;//(myTime - (*pid).pTime);
  (*pid).Iterm += Icomponent;
  //if ((*pid).Iterm > IMax) (*pid).Iterm = IMax;// cap on Iterm to avoid integral windup
  double Dcomponent = (*pid).Kd * ( err - (*pid).pErr) / td; 
  double outF = Pcomponent + (*pid).Iterm + Dcomponent; // use that error to adjust the signal going to the system
  int out = int(outF);
  //dataString +=  (String((*pid).setpoint)+ "," + String((*pid).setpoint - err));//+ "," + String(out)
    
  // bound output and make sure out is an integer
  if (out < user_position_MIN) out = user_position_MIN;
  if (out > user_position_MAX) out = user_position_MAX;
 
//  //dataString += (myTimeLoop + "," + String(myPID.setpoint) + "," + String(myPID.setpoint - error) + "," + String(filteredData1) + "," + String(myPID.actuatorCommand) );
  //Serial.println(dataString);
  
  (*pid).pErr = err;
  (*pid).pTime = myTime;
  return out;
}

double filterData(short d, bool filterType) {
  double fd;
  
  if (!(filterType)) {
    fd = 0.0;
    //fd = double(filter50.reading(d));   // 2) filter input
  }
  else {
    xData[0] = d;
    skFilter2(xData, &test, yData, &test);
   fd = yData[0];
  }
  return fd;
}

void serialChangeSetpoint() {
      Serial.println("Write the new setpoint.");
      while ( !(Serial.available() > 0));
      double forceSetpoint = Serial.parseFloat();
      Serial.read(); // comment out if python
      changeSetpoint(&myPID, forceSetpoint);
      Serial.print("NEW SETPOINT=");
      Serial.println(forceSetpoint);
      delay(5000); 
}

void serialChangeParams() {
  m_zap.GoalPosition(ID_NUM, POSITION_MIN);
      String outputStr = "";
      Serial.print("Write the new PID parameters. Current parameters are=");
      outputStr += (String(myPID.Kp) + ", " + String(myPID.Ki) + ", " + String(myPID.Kd));
      Serial.println(outputStr);
      double arr[3];
      for(int i = 0; i < 3; ++i) {
        while ( !(Serial.available() > 0));
        double parameter = Serial.parseFloat();
        //if (i == 1) parameter = parameter/100.0;
        Serial.read();// comment out if python
        arr[i] = parameter;
        Serial.println(arr[i]);
      }
      changePIDparam(&myPID, arr[0], arr[1], arr[2]);
      Serial.print("NEW PARAMETERS=");
      outputStr = "";
      outputStr += ("P=" + String(arr[0]) + " I=" + String(arr[1]) + " D=" + String(arr[2]));
      Serial.println(outputStr);
      delay(5000); 
}


void writeActuator(int idx, int pos) {
  if (actuatorType) m_zap.GoalPosition(idx+1,pos); // mightyZap
  //else actuatorArr[idx].write(pos); // actuonix
}

int readFeedback(int idx) {
  int value = -1;
  if (actuatorType) value = m_zap.presentPosition(idx+1); // if mightyZap
//  else {
//    //value = analogRead(position_INArr[idx]); // if actuonix
//  }
  return value;
}

// sweeping actuator position, increasing and decreasing. infinite loop.
// t_d is ti me between actuator steps. idx is which actuator
int sweep(int t_d, int idx) {
    short data;
    bool retracting = false;
    int position_Measured = 0;
    int counter = user_position_MIN-1;
    int inc = 10;
    int maxValue = 0;
    //bool localWriteOut;
    unsigned long startTimeCmd;
    unsigned long startTimeWriteOut = millis();
    unsigned long myTime = millis();
    String dataString;
    //int td_filterInitialization = 25000;
    int td_WriteOut = 150;
    int i;
    
    startTimeCmd = millis();

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
        //filteredData = filter50.reading(data);
        xData[0] = data;
        skFilter2(xData, &test, yData, &test);
        short filteredData1 = yData[0];
        position_Measured = readFeedback(idx); // this adds 152 ms
        if (position_Measured > maxValue) maxValue = position_Measured;
        dataString += (String(myTime) + "," + String(counter) + "," + String(position_Measured) + "," + data + "," + filteredData1);
        if (serialON) Serial.println(dataString);
        if (bleON) ble.println(dataString);
        startTimeWriteOut = millis();
        dataString = "";
      }

      if (counter >= user_position_MAX) {
        inc = -1 * inc;
        retracting = true;
      }
      else if (counter <= (user_position_MIN) && retracting) break;
    }
    return maxValue;    
}


void directActuatorControl(int n) {
    short data[n];
    int position_Measured[n];
    int position_CommandArr[n];
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

void initializeSystem() {
 // analogWrite(led_OUT, 10);
  Wire.begin(); // join i2c bus
  analogWrite(ledPower_OUT, 255);
  blinkN(2,2000);
  analogWrite(led_OUT, 10);
  initializeSerial(); // start serial for output
  initializeMightyZap();
  if (bleON) initializeBLE();
  //flexSensor = 180; 
  initializeIO(); // initialize IO pins, i.e. button and led
  
//  if (c) {
//    Serial.println("Entering calibration...");
//    calibration();
//  }
}

void initializeBLE() {
  ble.begin(VERBOSE_MODE);
  ble.factoryReset();  
  ble.echo(false);
  while (! ble.isConnected()) {
    delay(500);   /* Wait for connection */
    m_zap.GoalPosition(ID_NUM, POSITION_MIN);
  }
  ble.setMode(BLUEFRUIT_MODE_DATA);
}

void initializeMightyZap(){
//    MightyZap m_zapObj(&Serial4, mightyZapWen_OUT);
//    m_zap = &m_zapObj;
    
    m_zap.begin(32);
    //m_zap.ledOn(0,RED);
    m_zap.GoalPosition(ID_NUM, POSITION_MIN);
    
}
bool initializeSerial() {
     if (serialON) Serial.begin(4608000);  
    Serial.flush();
     if (serialON) while (!Serial);
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
