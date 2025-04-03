#ifndef nrf52840DeepPressureWearable_h
#define nrf52840DeepPressureWearable_h

#include "Arduino.h"
#include <Servo.h>
#include <Wire.h>
#include "LSM6DS3.h"
#include <math.h>

class nrf52840DeepPressureWearable {


	public:
		nrf52840DeepPressureWearable(); // constructor
		void measureRollPitch(bool p);
		void initializeIMU();
	  	void calibrateSensors();

	private:
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
	  

	  // methods
	  
	  //void initializeSystem();
	  void readAllAccelGyro();
	  float computeRoll();
	  float computePitch();
	  float complementaryFilter(float v, float dt, bool isRoll);
	  //void measureRollPitch(bool p);

};


#endif