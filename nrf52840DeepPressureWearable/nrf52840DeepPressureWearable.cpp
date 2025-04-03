// nrf52840DeepPressureWearable.cpp
// Written by: Sreela Kodali, kodali@stanford.edu
#include "nrf52840DeepPressureWearable.h"

nrf52840DeepPressureWearable::nrf52840DeepPressureWearable() {
	LSM6DS3 myIMU(I2C_MODE, 0x6A);
	previousTime = micros();
	//initializeSystem();
}

void nrf52840DeepPressureWearable::initializeIMU() {
	if (myIMU.begin() != 0) Serial.println("IMU error");
}
void nrf52840DeepPressureWearable::calibrateSensors() {
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

void nrf52840DeepPressureWearable::readAllAccelGyro() {
	accelX = myIMU.readFloatAccelX() - accelXBias;
  accelY = myIMU.readFloatAccelY() - accelYBias;
  accelZ = myIMU.readFloatAccelZ() - accelZBias;
  gyroX = myIMU.readFloatGyroX() - gyroXBias;
  gyroY = myIMU.readFloatGyroY() - gyroYBias;
  gyroZ = myIMU.readFloatGyroZ() - gyroZBias;
}

float nrf52840DeepPressureWearable::computeRoll() {
	return atan2(accelY, accelZ) * 180.0 / M_PI;
}
float nrf52840DeepPressureWearable::computePitch() {
  return atan2(-accelX, sqrt(accelY * accelY + accelZ * accelZ)) * 180.0 / M_PI;
}
float nrf52840DeepPressureWearable::complementaryFilter(float v, float dt, bool isRoll) {
  float complementaryValue;

  if (isRoll) complementaryValue = alpha * (complementaryRoll + gyroX * dt) + (1 - alpha) * v;
  else complementaryValue = alpha * (complementaryPitch + gyroY * dt) + (1 - alpha) * v;

  return complementaryValue;
}

void nrf52840DeepPressureWearable::measureRollPitch(bool p) {
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