/*
 * Full System, Version 1.0
 * Written: January 20th, 2022 by Sreela Kodali (kodali@stanford)
 * 
 * Using resistive flex sensor to change linear actuator
 * while measuring applied force with single tact
 * */

#include <Wire.h> //For I2C/SMBus
#include <Servo.h>

// Constants
#define actuatorPosition_MIN 46
#define actuatorPosition_MAX 145
//#define sensor_MIN 0
//#define sensor_MAX 665

// Pin Names
#define flexSensor_IN A0
#define actuator1Pos_IN
#define actuator1Pos_OUT 5

Servo actuator1;  // create servo object to control a servo
int actuator1Pos_target = 0;    // variable to store the servo position
//int flexSensor = 0;        // value read from the sensor


void setup()
{
  Wire.begin(); // join i2c bus (address optional for master)
  //TWBR = 12; //Increase i2c speed if you have Arduino MEGA2560, not suitable for Arduino UNO
  Serial.begin(57600);  // start serial for output
  Serial.flush();
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("PPS UK: SingleTact multiple sensor value in PSI.");
  Serial.println("Refer manual for any other calculation.");
  Serial.println("----------------------------------------");  

  // attaches the servo on pin 5 to the servo object
  actuator1.attach(actuator1Pos_OUT);
  Serial.println("Attach servo.");
  Serial.println("----------------------------------------");  
}

void loop()
{
    byte i2cAddress;
    short data;
    float force;
    int counter = actuatorPosition_MIN;
    bool debug = false;

  /* Note: No sensor should be addressed with default 0x04 value */ 
    // Reading data from sensor 1
    if (debug) Serial.println("Reading data from sensor 1");  
    i2cAddress = 0x04;
    data = readDataFromSensor(i2cAddress);

//    //read flex sensor
//    sensorValue = analogRead(sensor_IN);
//      // map it to the range of the analog out:
//  actuator1Pos_target = map(sensorValue, sensor_MIN, sensor_MAX, actuator_MIN, actuator_MAX);
//  if (sensorValue <= 290) actuator1Pos_target = actuator_MIN;
//  if (actuator1Pos_target < actuator_MIN) actuator1Pos_target = actuator_MIN;
//  if (actuator1Pos_target > actuator_MAX) actuator1Pos_target = actuator_MAX;

  while (counter <= actuatorPosition_MAX) {
    data = readDataFromSensor(i2cAddress);
    actuator1Pos_target = counter;
    if (actuator1Pos_target >= actuatorPosition_MAX) break;
    
    actuator1.write(actuator1Pos_target);
    Serial.print("     Actuator = ");
    Serial.print(actuator1Pos_target);
    Serial.print("     Force:    ");
    if (data <=312) {
        force = (data - 256) * (45.0)/511;
        Serial.print(force);    
        Serial.print(" N \n");
    }

    // if reach max force break
    
    else  { //if (data >767) {    ``
        Serial.println("Force > 5N");
        break;
    }
    delay(100); // Change this if you are getting values too quickly
    counter = counter + 1;
  }

//    // tell servo to go to position
//    actuator1.write(actuator1Pos_target);
//      Serial.print("Sensor = ");
//      Serial.print(sensorValue);
//      Serial.print("     Actuator = ");
//      Serial.print(actuator1Pos_target);
//
//    Serial.print("     Force:    ");
//    
////    bitWrite(data,0,1);
////    Serial.println(data, BIN);
//    if (data <=767) {
//      force = (data - 256) * (45.0)/511;
//      Serial.print(force);    
//      Serial.print(" N \n");
//    }
//    else if (data >767) {
//      Serial.println("Force > 45N");
//    }
//    
//    
//    delay(100); // Change this if you are getting values too quickly

//    // Reading data from sensor 2
//    i2cAddress = 0x08;
//    data = readDataFromSensor(i2cAddress);
//    Serial.print("I2C Sensor 2  Data:");
//    Serial.print(data);    
//    Serial.print("\n");
//    delay(100); // Change this if you are getting values too quickly
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
