#include "LSM6DS3.h"
#include "Wire.h"
#include <math.h>

LSM6DS3 myIMU(I2C_MODE, 0x6A);

float accelX, accelY, accelZ;
float gyroX, gyroY, gyroZ;
float roll, pitch;
float complementaryRoll, complementaryPitch;

float accelXBias, accelYBias, accelZBias;
float gyroXBias, gyroYBias, gyroZBias;

unsigned long previousTime;
const float alpha = 0.98; // Complementary filter coefficient

const int calibrationSamples = 1000;

void setup() {
    Serial.begin(115200);
    while (!Serial);
    
    if (myIMU.begin() != 0) {
        Serial.println("Device error");
    } else {
        //Serial.println("Device OK!");
    }
    
    calibrateSensors();
    previousTime = micros();

    // Print CSV header
    // Serial.println("Time,Roll,Pitch");
}

void calibrateSensors() {
    float sumAccelX = 0, sumAccelY = 0, sumAccelZ = 0;
    float sumGyroX = 0, sumGyroY = 0, sumGyroZ = 0;

    for (int i = 0; i < calibrationSamples; i++) {
        sumAccelX += myIMU.readFloatAccelX();
        sumAccelY += myIMU.readFloatAccelY();
        sumAccelZ += myIMU.readFloatAccelZ();
        sumGyroX += myIMU.readFloatGyroX();
        sumGyroY += myIMU.readFloatGyroY();
        sumGyroZ += myIMU.readFloatGyroZ();
        delayMicroseconds(100);
    }

    accelXBias = sumAccelX / calibrationSamples;
    accelYBias = sumAccelY / calibrationSamples;
    accelZBias = sumAccelZ / calibrationSamples - 1.0;
    gyroXBias = sumGyroX / calibrationSamples;
    gyroYBias = sumGyroY / calibrationSamples;
    gyroZBias = sumGyroZ / calibrationSamples;
}

void loop() {
  Serial.println(myIMU.readFloatAccelX());
  //measureRollPitch(1);
//    unsigned long currentTime = micros();
//    float deltaTime = (currentTime - previousTime) / 1000000.0;
//    previousTime = currentTime;
//
//    accelX = myIMU.readFloatAccelX() - accelXBias;
//    accelY = myIMU.readFloatAccelY() - accelYBias;
//    accelZ = myIMU.readFloatAccelZ() - accelZBias;
//    gyroX = myIMU.readFloatGyroX() - gyroXBias;
//    gyroY = myIMU.readFloatGyroY() - gyroYBias;
//    gyroZ = myIMU.readFloatGyroZ() - gyroZBias;
//
//    roll = atan2(accelY, accelZ) * 180.0 / M_PI;
//    pitch = atan2(-accelX, sqrt(accelY * accelY + accelZ * accelZ)) * 180.0 / M_PI;
//
//    complementaryRoll = alpha * (complementaryRoll + gyroX * deltaTime) + (1 - alpha) * roll;
//    complementaryPitch = alpha * (complementaryPitch + gyroY * deltaTime) + (1 - alpha) * pitch;
//
//    // Print time, roll, and pitch as CSV
//    // Serial.print(millis());
//    // Serial.print(",");
//    // Serial.print(accelX, 4);
//    // Serial.print(",");
//    // Serial.print(accelY, 4);
//    // Serial.print(",");
//    // Serial.print(accelZ, 4);
//    // Serial.print(",");
//    // Serial.print(gyroX, 4);
//    // Serial.print(",");
//    // Serial.print(gyroY, 4);
//    // Serial.print(",");
//    // Serial.print(gyroZ, 4);
//    // Serial.print(",");
//    Serial.print(complementaryRoll, 4);
//    Serial.print(",");
//    Serial.println(complementaryPitch, 4);
//
    delay(20);  // Adjust as needed
}
