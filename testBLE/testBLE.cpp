
#include "testBLE.h"

testBLE::testBLE() {
	LSM6DS3 myIMU(I2C_MODE, 0x6A);
	previousTime = micros();
	initializeSystem();
}


void testBLE::measureRollPitch(bool p) {	
}

void testBLE::initializeIMU() {
	if (myIMU.begin() != 0) Serial.println("IMU error");
}
void testBLE::calibrateSensors() {
	float sumAccelX = 0, sumAccelY = 0, sumAccelZ = 0;
  float sumGyroX = 0, sumGyroY = 0, sumGyroZ = 0;

  for (int i = 0; i < calibrationSamples; i++) {
    sumAccelX += (myIMU).readFloatAccelX();
    sumAccelY += (myIMU).readFloatAccelY();
    sumAccelZ += (myIMU).readFloatAccelZ();
    sumGyroX += (myIMU).readFloatGyroX();
    sumGyroY += (myIMU).readFloatGyroY();
    sumGyroZ += (myIMU).readFloatGyroZ();
    delayMicroseconds(100);
  }

  accelXBias = sumAccelX / calibrationSamples;
  accelYBias = sumAccelY / calibrationSamples;
  accelZBias = sumAccelZ / calibrationSamples - 1.0;
  gyroXBias = sumGyroX / calibrationSamples;
  gyroYBias = sumGyroY / calibrationSamples;
  gyroZBias = sumGyroZ / calibrationSamples;
}

// void testBLE::initializeSystem() {
// 	//Wire.begin();
//   Serial.begin(115200);
//   while (!Serial);
//   initializeIMU();
//   calibrateSensors();
// }

void testBLE::readAllAccelGyro() {
	accelX = myIMU.readFloatAccelX() - accelXBias;
  accelY = myIMU.readFloatAccelY() - accelYBias;
  accelZ = myIMU.readFloatAccelZ() - accelZBias;
  gyroX = myIMU.readFloatGyroX() - gyroXBias;
  gyroY = myIMU.readFloatGyroY() - gyroYBias;
  gyroZ = myIMU.readFloatGyroZ() - gyroZBias;
}

float testBLE::computeRoll() {
	return atan2(accelY, accelZ) * 180.0 / M_PI;
}
float testBLE::computePitch() {
  return atan2(-accelX, sqrt(accelY * accelY + accelZ * accelZ)) * 180.0 / M_PI;
}
float testBLE::complementaryFilter(float v, float dt, bool isRoll) {
  float complementaryValue;

  if (isRoll) complementaryValue = alpha * (complementaryRoll + gyroX * dt) + (1 - alpha) * v;
  else complementaryValue = alpha * (complementaryPitch + gyroY * dt) + (1 - alpha) * v;

  return complementaryValue;
}

void testBLE::measureRollPitch(bool p) {
	  unsigned long currentTime = micros();
  float deltaTime = (currentTime - previousTime) / 1000000.0;
  previousTime = currentTime;

  readAllAccelGyro();
  roll = computeRoll();
  pitch = computePitch();
  complementaryRoll = complementaryFilter(roll, deltaTime, 1);
  complementaryPitch = complementaryFilter(pitch, deltaTime, 0);

  if (p) {
    Serial.print(complementaryRoll, 2);
    Serial.print(",");
    Serial.println(complementaryPitch, 2);
  }
  delay(15);
}