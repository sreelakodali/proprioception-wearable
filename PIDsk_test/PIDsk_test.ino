/********************************************************
 * PID - from Scratch
 * Written by Sreela Kodali kodali@stanford.edu
 * Reading force sensor input for ttl position output
 ********************************************************/

#include <MightyZap.h>
#include <Wire.h>
#include "skFilter2.h"
#include "skFilter2_terminate.h"

#define ID_NUM 1

// MightyZap actuator limits
typedef enum {
  POSITION_MIN = 0, 
  POSITION_MAX = 2000//4095
} ACTUATOR_LIMITS;

/********************************************************
 *  PID PARAMETERS AND SETPOINT TO CHANGE  
 ********************************************************/
 // 50, 600, 30
 // 75, 600, 35
 // 150, 600, 35
 //132 750 30
 // 100 750
 // 50 400
 //70 275
 //85 250
 //100 260
 // 45 400
 // 55 400 7

// for 2N 54 400 6
//for 4 N 53 400 4
//for 6N  53 400 15
// 53 380
//55 379 42
// 0.7 55 379 no scale 15
// 0.7 55 320 no scale 13
// 0.5 55 350
// 0.6 55 350
// 0.6 60 350
//0.6 60 310
//0.6 60 310 15*scaleF
//double scaleF = 2.0;
//double KpConst = 60*scaleF;//130.00;
//double KiConst = 30;//;310*scaleF;//0.031;
//double KdConst = 0;//15*scaleF;//30.0;
//double setPointTest = 2.5;
//double td = 0.104;


//double scaleF = 1;
//double tScale = 3.34;
//double KpConst = 55*scaleF;//130.00;
//double KiConst = 120*scaleF;//0.031;
//double KdConst = 10;//50*scaleF;//30.0;
//double setPointTest = 2.5;
//double td = 0.02*tScale;

////ACTUATOR 2
//double scaleF = 0.25;
//double tScale = 3.34;
//double KpConst = 60*scaleF;//130.00;
//double KiConst = 310*scaleF;//0.031;
//double KdConst = 25;//50*scaleF;//30.0;
//double setPointTest = 6.0;
//double td = 0.02*tScale;

// ACTUATOR 1
double scaleF = 0.11;
double tScale = 3.34;
double KpConst = 60*scaleF;//130.00;
double KiConst = 310*scaleF;//0.031;
double KdConst = 0;//50*scaleF;//30.0;
double setPointTest = 6.0;
double td = 0.02*tScale;

int measuredPos = 0;
// ------------------------------------------------------------------------------------------------------
const byte I2C_ADDR = 0x04;
const double IMax = 100000; // capping integral term
const int mightyZapWen_OUT = 12;
const int t_setup = 15000; // set up time for filter values to stabilize
const int T_CYCLE = 15*tScale; // minimum delay to ensure not sampling at too high a rate for sensors
const int td_WriteOut = 100; // write out rate

int test = 1; // skFilter
short xData[1] = {0}; // skFilter
float yData[1] = {0};// skFilter
MightyZap m_zap(&Serial4, mightyZapWen_OUT);

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
  double filteredData1;

  // initialize i2c and serial  
    Wire.begin(); // join i2c bus
    Serial.begin(4608000);  
    Serial.flush();
    while (!Serial);

    // initialize filter and acutator
    m_zap.begin(32);
    m_zap.GoalPosition(ID_NUM, POSITION_MIN);


    // give the filters some time to begin
  unsigned long setupTime = millis();
  //tLastWriteout = millis();
  unsigned long myTimeSetup = millis();
  
  while ( (myTimeSetup - setupTime) < t_setup) {

    // every td_WriteOut seconds, read, filter and writeout data
    if ((myTimeSetup - myPID.tLastWriteout) > td_WriteOut)  {
      
      short data = readDataFromSensor(I2C_ADDR);
      filteredData1 = filterData(data, 1);
      
      
      String dataString = ""; // writeout       //dataString += (String(filteredData)+ "," + String(filteredData1) + "," + String(filteredData2));
      dataString += (String(0.0)+ "," + String(4.0));
      Serial.println(dataString);
      myPID.tLastWriteout = millis();
    }
    myTimeSetup = millis();
  }
    // initialize PID
  initializePID(&myPID, KpConst, KiConst, KdConst, setPointTest);
  myPID.zeroForce = filteredData1;
  //Serial.println(myPID.zeroForce);
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
  dataString +=  (String(myPID.setpoint)+ "," + String(myPID.setpoint - error));
  //dataString += (String(myTimeLoop) + "," + String(myPID.setpoint) + "," + String(myPID.setpoint - error) + "," + String(filteredData1)+ "," + String(myPID.actuatorCommand) + "," + String(measuredPos));
  Serial.println(dataString);
  myPID.tLastWriteout = millis();
 }

 if (Serial.available() > 0) { // update setpoint via serial 
    String test = Serial.readString();
    test.trim();
    Serial.println(test);
    if (test == "set") serialChangeSetpoint();
    else if (test == "param") serialChangeParams();
  }
  measuredPos = m_zap.presentPosition(ID_NUM);
  //if (T_CYCLE > 0) delay(T_CYCLE);  
}

// -------------------- SUPPORT FUNCTIONS --------------------//



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
  if (out < POSITION_MIN) out = POSITION_MIN;
  if (out > POSITION_MAX) out = POSITION_MAX;
 
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



short readDataFromSensor(short address) {
  byte i2cPacketLength = 6;//i2c packet length. Just need 6 bytes from each peripheral
  byte outgoingI2CBuffer[3];//outgoing array buffer
  byte incomingI2CBuffer[6];//incoming array buffer

  outgoingI2CBuffer[0] = 0x01;//I2c read command
  outgoingI2CBuffer[1] = 128;//peripheral data offset
  outgoingI2CBuffer[2] = i2cPacketLength;//require 6 bytes

  Wire.beginTransmission(address); // transmit to device 
  Wire.write(outgoingI2CBuffer, 3);// send out command
  byte error = Wire.endTransmission(); // stop transmitting and check peripheral status
  if (error != 0) return -1; //if peripheral not exists or has error, return -1
  Wire.requestFrom(address, i2cPacketLength);//require 6 bytes from peripheral

  byte incomeCount = 0;
  while (incomeCount < i2cPacketLength)    // peripheral may send less than requested
  {
    if (Wire.available())
    {
      incomingI2CBuffer[incomeCount] = Wire.read(); // receive a byte as character
      incomeCount++;
    }
    else
    {
      delayMicroseconds(10); //Wait 10us 
    }
  }

  short rawData = (incomingI2CBuffer[4] << 8) + incomingI2CBuffer[5]; //get the raw data

  return rawData;
}
