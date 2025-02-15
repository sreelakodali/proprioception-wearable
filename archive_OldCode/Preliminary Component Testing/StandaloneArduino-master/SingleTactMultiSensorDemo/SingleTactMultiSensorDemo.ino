/*-----------------------------------------------------------------------------
 * SingleTact Multisensor I2C Demo
 * 
 * Copyright (c) 2017 Pressure Profile Systems
 * Licensed under the MIT license. This file may not be copied, modified, or
 * distributed except according to those terms.
 * 
 * 
 * Demonstrates sensor input by reading I2C and display value on comm port.
 * 
 * The circuit: as described in the manual for PC interface using Arduino. 
 * 
 * To compile: Sketch --> Verify/Compile
 * To upload: Sketch --> Upload
 * 
 * For comm port monitoring: Click on Tools --> Serial Monitor
 * Remember to set the baud rate at 57600.
 * 
 * March 2017
 * ----------------------------------------------------------------------------- */


#include <Wire.h> //For I2C/SMBus

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
}

void loop()
{
    byte i2cAddress; // Slave address (SingleTact), default 0x04
    short data;
    float force;

    bool debug;

    debug = false;

	/* Note: No sensor should be addressed with default 0x04 value */	
    // Reading data from sensor 1
    if (debug) Serial.println("Reading data from sensor 1");  
    i2cAddress = 0x04;
    data = readDataFromSensor(i2cAddress);
    Serial.print("I2C Sensor 1 Data:    ");
    
//    bitWrite(data,0,1);
//    Serial.println(data, BIN);
    if (data <=767) {
      force = (data - 256) * (45.0)/511;
      Serial.print(force);    
      Serial.print(" N \n");
    }
    else if (data >767) {
      Serial.println("Force > 45N");
    }
    
    
    delay(100); // Change this if you are getting values too quickly

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
