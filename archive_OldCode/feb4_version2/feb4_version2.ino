/*
 * Full System, Version 2.0
 * Written: February 4th, 2022 by Sreela Kodali (kodali@stanford)
 * 
 * */

#include <Wire.h> //For I2C/SMBus
#include <Servo.h>

// Constants
#define position_MIN 46
#define position_MAX 145
//#define flexResistiveSensor_MIN 0
//#define flexResistiveSensor_MAX 665

// Pin Names
#define flexSensor_IN A0
#define position1_IN A1 // pin to measure position1_Measured
#define position1_OUT 5 // pin to send position1_Command

Servo actuator1;  // create servo object to control a servo
int position1_Command = 0;    // variable to store the servo command
int position1_Measured = 0;   // variable to store the measured servo position
//int flexSensor = 0;        // value read from the sensor
int user_position_MAX = position_MAX;

byte i2cAddress = 0x04;
float force = 0.0;

void setup()
{
  short data;
  int counter;
  unsigned long myTime;
  bool debug = false;
  
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

  // attaches the servo on pin to the servo object
  actuator1.attach(position1_OUT);
  Serial.println("Attach servo.");
  Serial.println("----------------------------------------");

   // Calibraton Mode
  Serial.println("----------------------------------------");  
  Serial.println("Calibration Mode");
  Serial.println("Click the button when device makes contact with your skin and when device is applying max pressure without pain.");
  Serial.println("----------------------------------------");  
     
  counter = position_MIN;
  user_position_MAX = position_MAX;
  while (counter <= position_MAX) {
      position1_Command = counter;
      data = readDataFromSensor(i2cAddress);
      position1_Measured = analogRead(position1_IN);
      position1_Measured = map(position1_Measured, 9, 606, 20, 0);
      //if (position1_Command >= position_MAX) break;
      force = (data - 256) * (45.0)/511;
      myTime = millis();
      actuator1.write(position1_Command);
      Serial.print(myTime);
      Serial.print("     Actuator Pos Command: ");
      Serial.print(position1_Command);
      Serial.print("     Actuator Pos Measured: ");
      Serial.print(position1_Measured);
      Serial.print("     Force:    ");
      
      if (force <= 45.0) {
          Serial.print(force);    
          Serial.print(" N \n");
      }
      // if force at max
      else  {
        Serial.print(force);    
        Serial.print(" N  >45N \n");
        user_position_MAX = position1_Command-1;
        delay(500);
        break;
      }
      
      // if button pressed
      if () {
        user_position_MAX = position1_Command-1;
        break;
      }
      delay(500);
      counter = counter + 1;
  }
}

void loop()
{
    //byte i2cAddress;
    short data;
    //float force;
    int counter;
    //int user_position_MAX;
    unsigned long myTime;
    bool debug = false;

  /* Note: No sensor should be addressed with default 0x04 value */ 
    // Reading data from sensor 1
    if (debug) Serial.println("Reading data from sensor 1");  
    i2cAddress = 0x04;

//    //read flex sensor
//    flexSensor = analogRead(flexSensor_IN);
//      // map it to the range of the analog out:
//  position1_Command = map(flexSensor, flexResistiveSensor_MIN, flexResistiveSensor_MAX, position_MIN, position_MAX);
//  if (flexSensor <= 290) actuator1Pos_target = actuator_MIN;
//  if (position1_Command < position_MIN) position1_Command = position_MIN;
//  if (position1_Command > position_MAX) position1_Command = position_MAX;

  //  data = readDataFromSensor(i2cAddress);
    //position1_Measured = analogRead(position1_IN);

    // data collection
    while (counter <= user_position_MAX) {
      position1_Command = counter;
      data = readDataFromSensor(i2cAddress);
      position1_Measured = analogRead(position1_IN);
      position1_Measured = map(position1_Measured, 9, 606, 20, 0);
      //if (position1_Command >= position_MAX) break;
      force = (data - 256) * (45.0)/511;
      myTime = millis();
      actuator1.write(position1_Command);
      Serial.print(myTime);
      Serial.print("     Actuator Pos Command: ");
      Serial.print(position1_Command);
      Serial.print("     Actuator Pos Measured: ");
      Serial.print(position1_Measured);
      Serial.print("     Force:    ");
      
      Serial.print(force);    
      Serial.print(" N \n");
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