// DeepPressureWearable.h
// Written by: Sreela Kodali, kodali@stanford.edu

#ifndef DeepPressureWearable_h
#define DeepPressureWearable_h

#include "Arduino.h"
// #else
// #include "WProgram.h"
// #endif

#include "SparkFun_Displacement_Sensor_Arduino_Library.h"
#include <Servo.h>
#include <Wire.h>
#include <SD.h>
#include <SPI.h>


// Notes: haven't added SD card stuff yet, single actuator

typedef enum {
	FLEX_MIN = 0,
	FLEX_MAX = 180
} FLEX_SENSOR_LIMITS;

typedef enum {
	POSITION_MIN = 47,
	POSITION_MAX = 139
} ACTUATOR_LIMITS;

// Calibration states
typedef enum { NONE, ZERO_FORCE, FLEX, MAX_PRESSURE, ACTUATOR  
} CALIBRATION_OPTIONS;


class DeepPressureWearable {
	public:
	// methods
	DeepPressureWearable(bool keyboard, bool serial);
	void runtime();
	void calibration();

	void testLed();
	void testPushbutton();
	void blink_T(int t_d);
	void safety();
	int sweep(int t_d);

	private:
	

	// variables

	// Settings
	bool keyboardON;
	bool serialON;
	bool sdWriteON;
	int WRITE_COUNT = 8;
	int T_CYCLE = 15;

	// Calibration 
	int  user_position_MIN;
	int  user_position_MAX;
	float  user_flex_MIN;
	float  user_flex_MAX;
	short zeroForce;

	// Linear Actuator, command, position
	Servo actuator1;
	int  position1_Command;
	int  position1_Measured;
	const  int position1_IN = 21;// analog read in position pin
	const  int position1_OUT = 7;// PWM output pin
	const  byte I2C_ADDR = 0x04; // force sensor's i2C addr
	
	int  cycleCount; // cycleCount
	bool  powerOn; // powerOn
	const int CHIP_SELECT = 10;

	// flex sensor and angle
	ADS  capacitiveFlexSensor;
	float  flexSensor;

	// Pushbutton & LED
	int  buttonState; // button state
	int  oldButtonState; // old button state
	int  buttonCount; // button count
	const int  button_IN = 4;
	const int  led_OUT = 5;

	// methods
	void blinkN(int n, int t_d);
	bool initializeSystem();
	bool initializeSerial();
	bool initializeSDCard();
	bool initializeActuator();
	bool initializeFlexSensor();
	bool initializeIO();
	bool risingEdgeButton();
	void writeOutData(unsigned long t, float f, int c, int m, short d);
	short readDataFromSensor(short address);

	void calibrationActuatorFeedback();
	void calibrationZeroForce();
	void calibrationFlexSensor(unsigned long timeLength);
	int calibrationMaxDeepPressure();

};
#endif