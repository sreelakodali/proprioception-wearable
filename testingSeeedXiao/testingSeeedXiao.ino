/*
 * Building up DeepPressureWearableBLE  
 * 
 * */

#include <Servo.h>
#include <Wire.h>
#include "LSM6DS3.h"
#include <math.h>
#include <DeepPressureWearableBLE.h>



struct deepPressureWearable {
  LSM6DS3 myIMU;
  float accelX, accelY, accelZ;
  float gyroX, gyroY, gyroZ;
  float roll, pitch;
  float complementaryRoll, complementaryPitch;

  float accelXBias, accelYBias, accelZBias;
  float gyroXBias, gyroYBias, gyroZBias;

  unsigned long previousTime;
  const float alpha = 0.98;  // Complementary filter coefficient
  const int calibrationSamples = 1000;

  deepPressureWearable() {
    LSM6DS3 myIMU(I2C_MODE, 0x6A);
    //myIMU = &myIMUObj;
    previousTime = micros();
  }
} myWearable;




void setup() {
  initializeSystem();
  Serial.println("initialized");
}

void loop() {
  //LSM6DS3* test = myWearable.myIMU;
  Serial.println(myWearable.myIMU.readFloatAccelX());
  //measureRollPitch(1);
}


void initializeIMU() {  
  //LSM6DS3* test = myWearable.myIMU;
  if ((myWearable.myIMU).begin() != 0) Serial.println("IMU error");
  //if (myWearable.myIMU).begin() != 0) Serial.println("IMU error")
}

void calibrateSensors() {
  float sumAccelX = 0, sumAccelY = 0, sumAccelZ = 0;
  float sumGyroX = 0, sumGyroY = 0, sumGyroZ = 0;

  //LSM6DS3* test = myWearable.myIMU;
  for (int i = 0; i < myWearable.calibrationSamples; i++) {
    sumAccelX += (myWearable.myIMU).readFloatAccelX();
    sumAccelY += (myWearable.myIMU).readFloatAccelY();
    sumAccelZ += (myWearable.myIMU).readFloatAccelZ();
    sumGyroX += (myWearable.myIMU).readFloatGyroX();
    sumGyroY += (myWearable.myIMU).readFloatGyroY();
    sumGyroZ += (myWearable.myIMU).readFloatGyroZ();
    delayMicroseconds(100);
  }

  myWearable.accelXBias = sumAccelX / myWearable.calibrationSamples;
  myWearable.accelYBias = sumAccelY / myWearable.calibrationSamples;
  myWearable.accelZBias = sumAccelZ / myWearable.calibrationSamples - 1.0;
  myWearable.gyroXBias = sumGyroX / myWearable.calibrationSamples;
  myWearable.gyroYBias = sumGyroY / myWearable.calibrationSamples;
  myWearable.gyroZBias = sumGyroZ / myWearable.calibrationSamples;
}

void initializeSystem() {
  //Wire.begin();
  Serial.begin(115200);
  while (!Serial);
  initializeIMU();
  //calibrateSensors();
}

void readAllAccelGyro() {
  //LSM6DS3* test = myWearable.myIMU;
  myWearable.accelX = myWearable.myIMU.readFloatAccelX() - myWearable.accelXBias;
  myWearable.accelY = myWearable.myIMU.readFloatAccelY() - myWearable.accelYBias;
  myWearable.accelZ = myWearable.myIMU.readFloatAccelZ() - myWearable.accelZBias;
  myWearable.gyroX = myWearable.myIMU.readFloatGyroX() - myWearable.gyroXBias;
  myWearable.gyroY = myWearable.myIMU.readFloatGyroY() - myWearable.gyroYBias;
  myWearable.gyroZ = myWearable.myIMU.readFloatGyroZ() - myWearable.gyroZBias;
}

float computeRoll() {
  return atan2(myWearable.accelY, myWearable.accelZ) * 180.0 / M_PI;
}

float computePitch() {
  return atan2(-myWearable.accelX, sqrt(myWearable.accelY * myWearable.accelY + myWearable.accelZ * myWearable.accelZ)) * 180.0 / M_PI;
}

float complementaryFilter(float v, float dt, bool isRoll) {
  float complementaryValue;

  if (isRoll) complementaryValue = myWearable.alpha * (myWearable.complementaryRoll + myWearable.gyroX * dt) + (1 - myWearable.alpha) * v;
  else complementaryValue = myWearable.alpha * (myWearable.complementaryPitch + myWearable.gyroY * dt) + (1 - myWearable.alpha) * v;

  return complementaryValue;
}

void measureRollPitch(bool p) {
  unsigned long currentTime = micros();
  float deltaTime = (currentTime - myWearable.previousTime) / 1000000.0;
  myWearable.previousTime = currentTime;

  readAllAccelGyro();
  myWearable.roll = computeRoll();
  myWearable.pitch = computePitch();
  myWearable.complementaryRoll = complementaryFilter(myWearable.roll, deltaTime, 1);
  myWearable.complementaryPitch = complementaryFilter(myWearable.pitch, deltaTime, 0);

  if (p) {
    Serial.print(myWearable.complementaryRoll, 2);
    Serial.print(",");
    Serial.println(myWearable.complementaryPitch, 2);
  }
  delay(15);
}
