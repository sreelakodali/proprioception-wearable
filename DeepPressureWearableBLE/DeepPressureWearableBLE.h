// DeepPressureWearableBLE.h
// Written by: Sreela Kodali, kodali@stanford.edu

#ifndef DeepPressureWearableBLE_h
#define DeepPressureWearableBLE_h

# define N_ACT 2
# define T_SAMPLING 100 // milliseconds
#include "Arduino.h"
#include "SparkFun_Displacement_Sensor_Arduino_Library.h"
#include <math.h>
#include <Servo.h>
#include <Wire.h>
#include "LSM6DS3.h"

typedef enum {
	FLEX_MIN = 0,
	FLEX_MAX = 180
} FLEX_SENSOR_LIMITS;

// actuonix command limits
typedef enum {
	POSITION_MIN = 47, // 900us mightyZap
	POSITION_MAX = 139 // 2100us mightyZap
} ACTUATOR_LIMITS;


// Calibration states
typedef enum { NONE, ZERO_FORCE, FLEX, MAX_PRESSURE, ACTUATOR  
} CALIBRATION_OPTIONS;

typedef enum {
	NO_INPUT,
	FLEX_INPUT,
	SERIAL_INPUT, // previously known as keyboard_input
	IMU_INPUT
} INPUT_TYPE;

class DeepPressureWearableBLE {
	public:
	// methods
	DeepPressureWearableBLE(INPUT_TYPE input, bool serial, bool c);

	int  N_ACTUATORS = N_ACT;

	// Calibration 
	int  user_position_MIN;
	int  user_position_MAX;
	float  user_flex_MIN;
	float  user_flex_MAX;
	int position_CommandArr[N_ACT];
    int  buttonCount; // button count. global!
    const  int position_INArr[4] = {A0, A1, A2, A3}; // analog adc pins

	void calibration();
	void runtime(void (*mapping)(int));
	void serialActuatorControl(int n);
	short readDataFromSensor(short address);
	
	void sweep_uS(int t_d, int n);

	void testLed();
	void testPushbutton();
	void blink_T(int t_d);
	void safety();
	int sweep(int t_d, int n);
	void blinkN(int n, int t_d);
	bool risingEdgeButton();

	void writeActuator(int idx, int pos);
	int readFeedback(int idx);


	private:
	

	// variables

	// Settings
	INPUT_TYPE inputType;
	bool serialON;
	bool bleON;
	const  byte I2C_ADDRArr[4] = {0x06, 0x08, 0x0A, 0x0C};
	// FIX: don't forget to change these
	const bool actuatorType = 0; // keep actuatorType at 0 for actuonix
	Servo actuatorArr[N_ACT]; // Array version for multiple actuators
	
	
	int WRITE_COUNT = 8;
	int T_CYCLE = 15; // minimum delay to ensure not sampling at too high a rate for sensors
	short zeroForceArr[N_ACT]; // should this be local?
	
	const int position_OUTArr[4] = {8, 9, 8, 9}; // pwm output
	const int  button_IN = 10;
	const int  led_OUT = 13;
	
	
	unsigned long t_lastWrite;
	bool  powerOn; // powerOn

	// flex sensor and angle
	ADS  capacitiveFlexSensor;
	float  flexSensor; // could be local(?)

	// Pushbutton & LED
	int  buttonState; // button state
	int  oldButtonState; // old button state
	


	// Aarya's code
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




	// methods
	
	void initializeSystem(bool c);
	bool initializeSerial();
	bool initializeActuator();
	bool initializeFlexSensor();
	bool initializeIO();
	void writeOutData(int l, unsigned long t, float f, int *c, int *m, short *d);
	
	// Aarya's code
	bool initializeIMU(); 
	float complementaryFilter(float value, float dt, bool isRoll);
	void calibrateSensors();
	float computeRoll();
	float computePitch();
	void readAllAccelGyro();
	void measureRollPitch(bool print)

	void calibrationActuatorFeedback(int n);
	void calibrationZeroForce();
	void calibrationFlexSensor(unsigned long timeLength);
	int calibrationMaxDeepPressure(int n);

};
#endif