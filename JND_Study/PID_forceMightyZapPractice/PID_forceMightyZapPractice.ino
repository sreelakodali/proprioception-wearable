/********************************************************
 * PID Basic Example
 * Reading force sensor input for ttl position output
 ********************************************************/

#include <PID_v2.h>
#include <MightyZap.h>
#include <movingAvg.h>
#include <Wire.h>
#include "skFilter2.h"
#include "skFilter2_terminate.h"


#define ID_NUM 2
#define N_SETPOINTS 3
#define STABLE_MAX 20

// Specify the links and initial tuning parameters
const byte I2C_ADDR = 0x04;
//double Kp = 5.0, Ki = 0.0, Kd = 0.0;
double Kp = 80.0, Ki = 25.0, Kd = 20.0;
const int mightyZapWen_OUT = 12;
const float setPointArr[N_SETPOINTS] = {3.0, 1.5, 5.5};
int setPointidx = 0;

PID_v2 myPID(Kp, Ki, Kd, PID::Direct); // PID::P_On::Measurement
MightyZap m_zap(&Serial4, mightyZapWen_OUT);
movingAvg filter50(25);
short zeroForce;

// skFilter
int test = 1;
short xData[1] = {0};
float yData[1] = {0};

float out = 0;
float setpoint = setPointArr[0];
int td_WriteOut = 100;
int stableCount = 0;

unsigned long myTimeGlobal;
unsigned long startTimeWriteOut;

unsigned long pidParamStartTime;

void setup() {
  Wire.begin(); // join i2c bus (address optional for central)
  Serial.begin(4608000);  
    Serial.flush();
    while (!Serial);

  m_zap.begin(32);
  m_zap.GoalPosition(ID_NUM, 0);
  filter50.begin();

//  // wait until the setpoint is set
//  Serial.println("Please wear and turn on the device. Then please enter your force setpoint in newtons."); 
//  while(Serial.available() <= 0);
//  float forceSetpoint = Serial.parseFloat();
//  Serial.read(); // comment out if python
//  Serial.print(forceSetpoint);
//  Serial.println(" N");
//  setpoint = forceSetpoint;
  
  
  myPID.Start(double( (readDataFromSensor(I2C_ADDR) - 246.0 ) * 45.0/512.0),  // input
              out,                      // current output
              setpoint);                   // setpoint
 myPID.SetOutputLimits(0, 2048);
 myPID.SetSampleTime(25);

  unsigned long startTime2 = millis();
  startTimeWriteOut = millis();
  unsigned long myTime = millis();
    int td_filterItnitialization = 25000;
  
  String dataString = "";
  short filteredData1;

  Serial.println("Waiting...");
  while((myTime-startTime2) < td_filterInitialization) {

      myTime = millis();
      // update counter for writing out and reading data
      if (int(myTime - startTimeWriteOut) > td_WriteOut) {
        short data = readDataFromSensor(I2C_ADDR);
        short filteredData = filter50.reading(data);
        xData[0] = data;
        skFilter2(xData, &test, yData, &test);
        filteredData1 = yData[0];
        float input = (filteredData1 - 255) * 45.0/512.0;
        int measuredPos = 0;//m_zap.presentPosition(ID_NUM);
        dataString += (String(myTime) + "," + String(setpoint) + "," + String(filteredData1));
        Serial.println(dataString);
        startTimeWriteOut = millis();
        dataString = "";
      }
      
    }
    
  zeroForce = filteredData1;
 startTimeWriteOut = millis();
 
}


void loop() {

  pidParamStartTime = millis(); // start time
  Serial.print("START! TIME= " );
  Serial.print(pidParamStartTime/1000.0);
  Serial.print(" SETPOINT= ");
  Serial.print(setpoint); 
  Serial.print(" PID PARAMS= ");
  Serial.print(Kp);
  Serial.print(",");
  Serial.print(Ki);
  Serial.print(",");
  Serial.println(Kd);
  // test out a set of PID parameters
  while (1) {
    String dataString = "";
    short data = readDataFromSensor(I2C_ADDR);
    short filteredData = filter50.reading(data);
    xData[0] = data;
    skFilter2(xData, &test, yData, &test);
    short filteredData1 = yData[0];
  
     myTimeGlobal = millis();
  
    
    float input = (filteredData1 - zeroForce) * 45.0/512.0;
    float gap = abs(setpoint - input);

    
  
    // reached the goal
    // measure the rise time, reset, change pid parameters
    if (gap < 0.2) {

      stableCount = stableCount + 1;


      if (stableCount == STABLE_MAX) { 
        unsigned long endTime = millis();
        unsigned long riseTime = (endTime - pidParamStartTime);
        dataString += ("DONE! TIME=" + String(endTime/1000.0) +  " SETPOINT="  + String(setpoint) + " PIDPARAMS=" + String(Kp) + ", " + String(Ki)+ ", " + String(Kd) + " RISE_TIME=" + String(riseTime/1000.0));
        Serial.println(dataString);
        setPointidx = setPointidx + 1;
        if (setPointidx ==N_SETPOINTS) while (1);
        Serial.println("NEXT SETPOINT: ");
        setpoint = setPointArr[setPointidx];
        myPID.Setpoint(setpoint);
        break;
      } 
     
    } else {

      stableCount = 0;
      out = round(myPID.Run(input));
      m_zap.GoalPosition(ID_NUM, out);
    }
    
        // update counter for writing out and reading data
      if (int(myTimeGlobal - startTimeWriteOut) > td_WriteOut) {
          int measuredPos = 0;//m_zap.presentPosition(ID_NUM);
          //dataString += (String(setpoint) + "," + String(input));
          dataString += (String(myTimeGlobal) + "," + String(setpoint) + "," + String(filteredData1) + "," + String(input) + "," + out + "," + measuredPos);
          Serial.println(dataString);
          startTimeWriteOut = millis();
          dataString = "";
        }
    
    if (Serial.available() > 0) {
          float forceSetpoint = Serial.parseFloat();
          Serial.read(); // comment out if python
          Serial.print("NEW SETPOINT (N): ");
          Serial.println(forceSetpoint);
          setpoint = forceSetpoint;
          myPID.Setpoint(forceSetpoint);
          delay(5000);       
    }
      delay(15);  
  }
}



short readDataFromSensor(short address)
{
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
