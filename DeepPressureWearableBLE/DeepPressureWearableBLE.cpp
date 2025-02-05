// DeepPressureWearableBLE.cpp
// Written by: Sreela Kodali, kodali@stanford.edu

#include "Arduino.h"
#include "pins_arduino.h"
#include "DeepPressureWearableBLE.h"


//Constructor
DeepPressureWearableBLE::DeepPressureWearableBLE(INPUT_TYPE input, bool serial, bool c) {

	// settings
	inputType = input;
	serialON = serial;
  bleON = !(serialON);

  //N_ACTUATORS = n;

	// DEFAULT Calibration settings
	user_position_MIN = POSITION_MIN;
	user_position_MAX = POSITION_MAX;
	user_flex_MIN = FLEX_MIN;
	user_flex_MAX = FLEX_MAX;

  int i;
  for (i=0; i < N_ACTUATORS; ++i) {
    position_CommandArr[i] = user_position_MIN;
    zeroForceArr[i] = 0;
  }

  if (!(actuatorType)) Servo actuatorArr[N_ACT];
  // if (actuatorType) {
  //   MightyZap m_zapObj(&Serial4, mightyZapWen_OUT);
	//   m_zap = &m_zapObj;
  //   (*m_zap).begin(32);  // Baudrate -> 128: 9600, 32: 57600, 16: 115200 
  // }
  t_lastWrite = millis();
	powerOn = 0; // powerOn

	// flex sensor and angle
	ADS  capacitiveFlexSensor;
	flexSensor = 0.0;

	// Pushbutton & LED
	buttonState = 0; // button state
	oldButtonState = 0; // old button state
	buttonCount = 0; // button count

	initializeSystem(c);
}



// Public methods
void DeepPressureWearableBLE::testLed () {
  //digitalWrite(led_OUT, HIGH);   // turn the LED on (HIGH is the voltage level)
  analogWrite(led_OUT, 200);
  delay(1000);               // wait for a second
  //digitalWrite(led_OUT, LOW);    // turn the LED off by making the voltage LOW
  analogWrite(led_OUT, 10);
  delay(1000);               // wait for a second
}

void DeepPressureWearableBLE::testPushbutton () {
  digitalWrite(led_OUT, LOW);
  if (risingEdgeButton()) {
    if (serialON) Serial.println("Pushed!");
    digitalWrite(led_OUT, HIGH);
    delay(50);
    digitalWrite(led_OUT, LOW);
  }
}

void DeepPressureWearableBLE::blink_T (int t_d) {
  digitalWrite(led_OUT, LOW);
  delay(t_d);
  digitalWrite(led_OUT, HIGH);
  delay(t_d);
}

void DeepPressureWearableBLE::writeActuator(int idx, int pos) {
  // if (actuatorType) (*m_zap).GoalPosition(idx+1,pos); // mightyZap
  if (!(actuatorType)) actuatorArr[idx].write(pos); // actuonix
}

int DeepPressureWearableBLE::readFeedback(int idx) {
  int value;
  // if (actuatorType) {
  //   // MightyZap* device = (MightyZap*)obj;
  //   //delay(50);
  //   value = (*m_zap).presentPosition(idx+1); // if mightyZap
  // }
  if (!(actuatorType)) {
    value = analogRead(position_INArr[idx]); // if actuonix
  }

  return value;
}



void DeepPressureWearableBLE::safety() {
      // Safety withdraw actuator and stop
    if (risingEdgeButton()) {

      int i;

      for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, POSITION_MIN);

      if (serialON) Serial.println("Device off. Turn off power.");
      while (1);
    }
}

void DeepPressureWearableBLE::runtime(void (*mapping)(int)) {
    short data[N_ACTUATORS];
    int position_MeasuredArr[N_ACTUATORS];
    unsigned long myTime;
    int i;

    myTime = millis(); // time for beginning of the loop

    // read flex sensor and map angle to actuator command. keep values in the bounds
    if (inputType == FLEX_INPUT) {
      if (capacitiveFlexSensor.available() == true) flexSensor = abs(capacitiveFlexSensor.getX());
    }
    else if (inputType == SERIAL_INPUT) {
      if (Serial.available() > 0) flexSensor = (Serial.read() - '0')*100 + (Serial.read() - '0')*10 + (Serial.read() - '0')*1 ;
    }
    else if (inputType == IMU_INPUT) {
      measureRollPitch(0);
      flexSensor = roll;
    }
    mapping(int(flexSensor));
    //position1_Command = map(int(flexSensor), int(user_flex_MIN), int(user_flex_MAX), user_position_MIN, user_position_MAX);
    
    for (i=0; i < N_ACTUATORS; ++i) {
        if(position_CommandArr[i] > user_position_MAX) position_CommandArr[i] = user_position_MAX;
        else if(position_CommandArr[i] < user_position_MIN) position_CommandArr[i] = user_position_MIN;
     }

    // Send command to actuator and measure actuator position

    if (!(buttonCount % 2)) {
      for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, position_CommandArr[i]);
    }
    else {
      for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, POSITION_MIN);
    }

    if ((myTime - t_lastWrite) > T_SAMPLING) {
      for (i=0; i < N_ACTUATORS; ++i) data[i] = readDataFromSensor(I2C_ADDRArr[i]);
      for (i=0; i < N_ACTUATORS; ++i) position_MeasuredArr[i] = readFeedback(i);//analogRead(position_INArr[i]); // could put this in the interrupt too
      writeOutData(N_ACTUATORS, myTime, flexSensor, position_CommandArr, position_MeasuredArr, data); // FIX: writeoutData needs to include roll, pitch
      t_lastWrite = millis();
    }

    risingEdgeButton();
    if (T_CYCLE > 0) delay(T_CYCLE);    
}

// n is how many actuators to control at the same time, not idx

void DeepPressureWearableBLE::serialActuatorControl(int n) {
    short data[N_ACTUATORS];
    int position_MeasuredArr[N_ACTUATORS];
    unsigned long myTime;
    int i;

    myTime = millis(); // time for beginning of the loop

    // parse serial input for command value
    //if (inputType == SERIAL_INPUT) {
      if (Serial.available() > 0) {
        position_CommandArr[0] = Serial.parseInt();
        Serial.parseInt(); // FIX: Comment out if not using arduino serial monitor!
        Serial.println(position_CommandArr[0]);
        //bound the command
        if(position_CommandArr[0] > user_position_MAX) position_CommandArr[0] = user_position_MAX;
        else if(position_CommandArr[0] < user_position_MIN) position_CommandArr[0] = user_position_MIN;

        // pass the command to other actuators
        if (n > 1) {
            for (i=1; i < n; ++i) position_CommandArr[i] = position_CommandArr[0];
        }
      }
    //}

    // Send command to actuator and measure actuator position
    if (!(buttonCount % 2)) {
       for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, position_CommandArr[i]);
    } else {
       for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, POSITION_MIN);
    }

    // read force data and write out data at lower frequency
    if ((myTime - t_lastWrite) > T_SAMPLING) {

      for (i=0; i < N_ACTUATORS; ++i) data[i] = readDataFromSensor(I2C_ADDRArr[i]);;
      for (i=0; i < N_ACTUATORS; ++i) position_MeasuredArr[i] = readFeedback(i);//analogRead(position_INArr[i]); // could put this in the interrupt too
      writeOutData(N_ACTUATORS, myTime, flexSensor, position_CommandArr, position_MeasuredArr, data);
      t_lastWrite = millis();
    }
    risingEdgeButton();
    if (T_CYCLE > 0) delay(T_CYCLE);    
}

// sweeping actuator position, increasing and decreasing. infinite loop.
// t_d is time between actuator steps. n is which actuator
int DeepPressureWearableBLE::sweep(int t_d, int n) {
    unsigned long myTime;
    short data;
    bool retracting = false;
    int position_Measured = 0;
    int counter = user_position_MIN-1;
    int inc = 1;
    int minValue = 1000;
    unsigned long startTime = millis();
    String dataString;
    t_lastWrite = millis();

    while(1) {
      
      myTime = millis();

      // update counter
      if (int(myTime - startTime) > t_d) {
        counter = counter + inc;
        
        //bound the command
        if(counter > user_position_MAX) counter = user_position_MAX;
        else if(counter < user_position_MIN) counter = user_position_MIN;
        //Serial.println(counter);

        writeActuator(n, counter);
        //Serial.println(counter);
        startTime = millis();
      }

      if ((myTime - t_lastWrite) > T_SAMPLING) {
        dataString = "";
        data = readDataFromSensor(I2C_ADDRArr[n]);;
        position_Measured = readFeedback(n);
        if (position_Measured < minValue) minValue = position_Measured;
        dataString += (String(myTime) + "," + String(counter) + "," + String(position_Measured) + "," + data);
        if (serialON) Serial.println(dataString);
        //writeOutData(N_ACTUATORS, myTime, flexSensor, position_CommandArr, position_MeasuredArr, data);
        t_lastWrite = millis();
      }

      if (counter >= user_position_MAX) {
        inc = -1 * inc;
        retracting = true;
      }
      else if (counter <= (user_position_MIN) && retracting) break;

    }
    return minValue;    
}


// using the servo writeMicroseconds() command intentionally
void DeepPressureWearableBLE::sweep_uS(int t_d, int n) {
    unsigned long myTime;
    short data;
    int counter = 900;
    int position_Measured;
    
    actuatorArr[n].writeMicroseconds(counter);
    position_Measured = 0;
    data = 0;
  

    while (counter <= 2100) {
        String dataString = "";
        actuatorArr[n].writeMicroseconds(counter);
        position_Measured = readFeedback(n);
        myTime = millis();
        data = readDataFromSensor(I2C_ADDRArr[n]);
        
        if (serialON) {
          dataString += (String(myTime) + "," + String(counter) + "," + String(position_Measured) + "," + String(data));        
            Serial.println(dataString);
        }
        counter = counter + 1;
        delay(t_d);
    }
      counter = 2100; // user_position_MIN + (user_position_MAX-user_position_MIN)/2
      actuatorArr[n].writeMicroseconds(counter);
}

// Calibration
void DeepPressureWearableBLE::calibrationActuatorFeedback(int n) {
  int i;
  int ACTUATOR_FEEDBACK_MAX = 500;
  int ACTUATOR_FEEDBACK_MIN = 500;

  // Calibration: Sweep and record the actuator position feedback positions
  for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, POSITION_MIN);

  
  delay(500);
  ACTUATOR_FEEDBACK_MAX = readFeedback(n);
  ACTUATOR_FEEDBACK_MIN = sweep(300, n);
  Serial.println(ACTUATOR_FEEDBACK_MAX);
  Serial.println(ACTUATOR_FEEDBACK_MIN);
}

void DeepPressureWearableBLE::calibrationZeroForce() {
  int i;
  for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, POSITION_MIN);

  // Calibration Stage: Get the zero force of the device
  for (i=0; i < N_ACTUATORS; ++i) {
    zeroForceArr[i] = readDataFromSensor(I2C_ADDRArr[i]);
    Serial.println(( zeroForceArr[i] - 255) * (45.0)/512);
  }
}

void DeepPressureWearableBLE::calibrationFlexSensor(unsigned long timeLength) {
  unsigned long startTime;
  unsigned long endTime;
  int i;
  //unsigned long timeLength = 50000;

  for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, POSITION_MIN);

  // use the initial value as baseline. otherwise user_flex is set at 0 180 default
   if (capacitiveFlexSensor.available() == true) user_flex_MIN = capacitiveFlexSensor.getX();
   user_flex_MAX = user_flex_MIN;
   Serial.println(user_flex_MIN);
   delay(2*T_CYCLE);
 
  // record flex values for x seconds
  startTime = millis();
  endTime = millis();

  while((endTime - startTime) < timeLength) {
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    if (flexSensor < user_flex_MIN) user_flex_MIN = flexSensor;
    else if (flexSensor > user_flex_MAX) user_flex_MAX = flexSensor;
    Serial.println(flexSensor);
    endTime = millis();
    delay(2*T_CYCLE);
  }

  startTime = millis();
  endTime = millis();
  while((endTime - startTime) < timeLength) {
    if (capacitiveFlexSensor.available() == true) flexSensor = capacitiveFlexSensor.getX();
    Serial.println(flexSensor);
    endTime = millis();
    delay(2*T_CYCLE);
  }
//  Serial.println(user_flex_MIN);
//  Serial.println(user_flex_MAX);
}


// Calibration Stage: Get the detection and pain thresholds
int DeepPressureWearableBLE::calibrationMaxDeepPressure(int n) {
   int counter = POSITION_MIN;
   int x;
   short data;
   int position_Measured;
   String dataString;
   short maxForce = 0;
   short minForce = 0; // detection threshold
   int nClicks = 0;
   int i;

   for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, counter);
   blinkN(5,1000);
   for (i=0; i < N_ACTUATORS; ++i) zeroForceArr[i] = readDataFromSensor(I2C_ADDRArr[i]);

    while (counter <= POSITION_MAX) {
       // Measure force and actuator position
      dataString = "";
      data = readDataFromSensor(I2C_ADDRArr[n]);
      position_Measured = readFeedback(n);
      // Send command to actuator
      writeActuator(n, counter);
      dataString += (String(counter) + "," + String(position_Measured) + "," + String((data - 255) * (45.0)/512));
      Serial.println(dataString);
        
      //if (serialON) Serial.println((data - 255) * (45.0)/512);
      if (Serial.available() > 0) x = (Serial.read() - '0');
//      Serial.println(x);
      if (risingEdgeButton() || (x == 5)) {
        nClicks = nClicks + 1;
        x = 0;
      }
      if (nClicks == 1) {
          //Serial.println("min detected!");
          user_position_MIN = counter;
          delay(3000);
          minForce = readDataFromSensor(I2C_ADDRArr[n]);
          nClicks = nClicks + 1;
      }
      if (nClicks == 3) { // NOTE: nClicks = 3 is deliebrate. rising edge of click
          user_position_MAX = counter - 2; // NOTE: the -2 is arbitrary
          maxForce = readDataFromSensor(I2C_ADDRArr[n]);
          delay(3000);
          writeActuator(n, POSITION_MIN);
          break; 
      }
      delay(250);
      counter = counter + 1;
  }

  for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, POSITION_MIN);

  Serial.println(zeroForceArr[n]);
  Serial.println(minForce); // new
  Serial.println(maxForce);
  Serial.println(user_position_MIN); // new
  Serial.println(user_position_MAX);

  return user_position_MAX;
}

/* Calibration: Interfaces with python gui */
void DeepPressureWearableBLE::calibration() {
  CALIBRATION_OPTIONS mode;
  bool calibrationComplete = false;
  int nMaxPressure = 0;
  int sum = 0;
  int sum1 = 0;
  int lenUserArr = 10; // User can do max of 10 attempts for deep pressure calibration
  int user_position_MAX_arr[lenUserArr];
  int user_position_MIN_arr[lenUserArr];
  int d1 = 0;
  int d2 = 0;
  int d3 = 0;
  int i;

  // initialize blank array
  for (int j = 0; j< lenUserArr; j++) {
     user_position_MAX_arr[j] = 0;
     user_position_MIN_arr[j] = 0;
  }
          
  // Reset position of actuator
  for (i=0; i < N_ACTUATORS; ++i) writeActuator(i, POSITION_MIN);

  while(!(calibrationComplete)){
    if (Serial.available() > 0) {
      mode = CALIBRATION_OPTIONS(Serial.read() - '0');
      switch (mode) {

        // THIS ISN'T ACTUALLY ZERO_FORCE. If experiment got interrupted and I don't want to redo
        // calibration, and i know the calibration values, I can pass in min + max directly.
        // FIX: should rename to LOAD_MIN_MAX 
        case ZERO_FORCE: // test for passing min AND max
          while (!(Serial.available() > 0));
          user_position_MIN = (Serial.read() - '0')*10 + (Serial.read() - '0')*1;
          d1 = (Serial.read() - '0');
          d2 = (Serial.read() - '0');
          user_position_MAX = d1*10 + d2*1;
          if (d1 == 1) {
            d3 = (Serial.read() - '0');
            user_position_MAX = user_position_MAX * 10 + d3*1;
          }

          // I don't necessarily need this, but in case I get interrupted mid-calibration
          // and I want to load in previous values and continue calibration.
          user_position_MAX_arr[nMaxPressure] = user_position_MAX;
          user_position_MIN_arr[nMaxPressure] = user_position_MIN;
          nMaxPressure = nMaxPressure + 1;

          Serial.println(user_position_MIN);
          Serial.println(user_position_MAX);
          break;
        case FLEX:
          calibrationFlexSensor(50000);
          break;
        case MAX_PRESSURE:
          user_position_MAX_arr[nMaxPressure] = calibrationMaxDeepPressure(0); // FIX
          user_position_MIN_arr[nMaxPressure] = user_position_MIN;
          nMaxPressure = nMaxPressure + 1;
          sum = 0;
          sum1 = 0;
          for (int i = 0; i< nMaxPressure; i++) {
            sum = sum + user_position_MAX_arr[i];
            sum1 = sum1 + user_position_MIN_arr[i];
          }
          user_position_MAX = sum/nMaxPressure;
          user_position_MIN = sum1/nMaxPressure;
          Serial.println(user_position_MIN);
          Serial.println(user_position_MAX);
          break;
        case ACTUATOR:
          calibrationActuatorFeedback(0); // FIX
          break;
        case NONE:
          calibrationComplete = true;
        default:
          break;
      }
      delay(50); 
    }
  }
}


// Private methods

void DeepPressureWearableBLE::blinkN (int n, int t_d) {
  //noInterrupts();
  for(int i=0; i < n; i++) {
    analogWrite(led_OUT, 10);
    delay(t_d/2);
    analogWrite(led_OUT, 200);
    delay(t_d/2);
  }
  //interrupts();
}

void DeepPressureWearableBLE::initializeSystem(bool c) {
  Wire.begin(); // join i2c bus
  initializeSerial(); // start serial for output
  initializeActuator(); // initialize actuator and set in min position
  
  initializeIO(); // initialize IO pins, i.e. button and led
  analogWrite(led_OUT, 10);
  

  if (inputType == FLEX_INPUT) initializeFlexSensor(); // initialize flex sensor
  else if (inputType == IMU_INPUT) initializeIMU();
  else {
    flexSensor = 180;
  }

  if (c) {
    Serial.println("Entering calibration...");
    calibration();
  }
  
}

bool DeepPressureWearableBLE::initializeSerial() {
    Serial.begin(4608000);  
    Serial.flush();
    while (!Serial);
    return (true); 
    Serial.println("serialIn");
}

bool DeepPressureWearableBLE::initializeActuator() {
  int i;

  for (i=0; i < N_ACTUATORS; ++i) {
    if (!(actuatorType)) actuatorArr[i].attach(position_OUTArr[i]); // attach servo 
    writeActuator(i, POSITION_MIN);
  }
  return (true);
}

bool DeepPressureWearableBLE::initializeFlexSensor() {
    if (capacitiveFlexSensor.begin() == false) {
      Serial.println(("No sensor detected. Check wiring. Freezing..."));
      while (1);
  }
  capacitiveFlexSensor.enableStretching(true);
  return (true);
}

bool DeepPressureWearableBLE::initializeIO() {
  pinMode(button_IN, INPUT); // set button and led
  pinMode(led_OUT, OUTPUT);
  return (true); 
}

// Aarya
bool DeepPressureWearableBLE::initializeIMU() {
  if (myIMU.begin() != 0) {
    if (serialON) Serial.println("Device error");
  }
  calibrateSensors();
  previousTime = micros();
  return (true); 
}

void DeepPressureWearableBLE::measureRollPitch(bool print){
  unsigned long currentTime = micros();
  float deltaTime = (currentTime - previousTime) / 1000000.0;
  previousTime = currentTime;

  readAllAccelGyro()
  roll = computeRoll();
  pitch = computePitch();
  complementaryRoll = complementaryFilter(roll, deltaTime, 1);
  complementaryPitch = complementaryFilter(pitch, deltaTime, 0);

  if (print) {
    if (serialON) Serial.print(complementaryRoll, 4);
    if (serialON) Serial.print(",");
    if (serialON) Serial.println(complementaryPitch, 4);
  }
  if (T_CYCLE > 0) delay(T_CYCLE);
}

// Aarya's code
void DeepPressureWearableBLE::calibrateSensors() {
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

float DeepPressureWearableBLE::complementaryFilter(float value, float dt, bool isRoll) {
  float complementaryValue;

  if (isRoll) complementaryValue = alpha * (complementaryRoll + gyroX * dt) + (1 - alpha) * value;
  else complementaryValue = alpha * (complementaryPitch + gyroY * dt) + (1 - alpha) * value;

  return complementaryValue;
}

float DeepPressureWearableBLE::computeRoll() {
  return atan2(accelY, accelZ) * 180.0 / M_PI;
}

float DeepPressureWearableBLE::computePitch() {
  return atan2(-accelX, sqrt(accelY * accelY + accelZ * accelZ)) * 180.0 / M_PI;
}


void DeepPressureWearableBLE::readAllAccelGyro() {
  accelX = myIMU.readFloatAccelX() - accelXBias;
  accelY = myIMU.readFloatAccelY() - accelYBias;
  accelZ = myIMU.readFloatAccelZ() - accelZBias;
  gyroX = myIMU.readFloatGyroX() - gyroXBias;
  gyroY = myIMU.readFloatGyroY() - gyroYBias;
  gyroZ = myIMU.readFloatGyroZ() - gyroZBias;
}

bool DeepPressureWearableBLE::risingEdgeButton() {
  buttonState = digitalRead(button_IN);
  //Serial.println(buttonState);
  if (buttonState != oldButtonState) {
    if (buttonState == HIGH) {
      buttonCount = buttonCount + 1;
      oldButtonState = buttonState;
      delay(300);
      return true;
    }
  }
  oldButtonState = buttonState; 
  return false;
}

void DeepPressureWearableBLE::writeOutData(int l, unsigned long t, float f, int *c, int *m, short *d) {
  int i;
  String dataString = "";
  if (bleON || serialON) {
    dataString += (String(t) + "," + String(f));

    for (i=0; i < l; ++i) {
      dataString += ( "," + String(c[i]) + "," + String(m[i]) + "," + String(d[i]));
    }
    
    if (inputType == IMU_INPUT) {
      String angles = ("," + String(complementaryRoll) + "," + String(complementaryPitch));
      dataString += angles;
    }  
    // if (bleON) {

    // }
    if (serialON) Serial.println(dataString);
  }  
}

short DeepPressureWearableBLE::readDataFromSensor(short address) {
  byte i2cPacketLength = 6;//i2c packet length. Just need 6 bytes from each peripheral
  byte outgoingI2CBuffer[3];//outgoing array buffer
  byte incomingI2CBuffer[6];//incoming array buffer
  bool debug;

  debug = false;

  outgoingI2CBuffer[0] = 0x01;//I2c read command
  outgoingI2CBuffer[1] = 128;//peripheral data offset
  outgoingI2CBuffer[2] = i2cPacketLength;//require 6 bytes

  if (debug) Serial.println("Transmit address");  
  Wire.beginTransmission(address); // transmit to device 
  Wire.write(outgoingI2CBuffer, 3);// send out command
  if (debug) Serial.println("Check sensor status");
  byte error = Wire.endTransmission(); // stop transmitting and check peripheral status
  if (debug) Serial.println("bloop");
  if (error != 0) return -1; //if peripheral not exists or has error, return -1
  Wire.requestFrom((uint8_t)address, i2cPacketLength);//require 6 bytes from peripheral
  if (debug) Serial.println("Request bytes from sensor");
  
  byte incomeCount = 0;
  while (incomeCount < i2cPacketLength)    // peripheral may send less than requested
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


