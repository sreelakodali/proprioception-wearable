// DeepPressureWearable.cpp
// Written by: Sreela Kodali, kodali@stanford.edu

#include "Arduino.h"
#include "pins_arduino.h"
#include "DeepPressureWearable.h"


//Constructor
DeepPressureWearable::DeepPressureWearable(INPUT_TYPE input, bool serial, bool c) {

	// settings
	inputType = input;
	serialON = serial;
  sdWriteON = !(serialON); // if outputting data via serial, no need to write to SD card

	// DEFAULT Calibration settings
	user_position_MIN = POSITION_MIN;
	user_position_MAX = POSITION_MAX;
	user_flex_MIN = FLEX_MIN;
	user_flex_MAX = FLEX_MAX;
  zeroForce = 0;

	// Linear Actuator, command, position
	position1_Command = 0;
	position1_Measured = 0;
	
  // Linear Actuator, command, position
  position2_Command = 0;
  position2_Measured = 0;
	
	cycleCount = 0; // cycleCount
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
void DeepPressureWearable::testLed () {
  digitalWrite(led_OUT, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);               // wait for a second
  digitalWrite(led_OUT, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);               // wait for a second
}

void DeepPressureWearable::testPushbutton () {
  digitalWrite(led_OUT, LOW);
  if (risingEdgeButton()) {
    if (serialON) Serial.println("Pushed!");
    digitalWrite(led_OUT, HIGH);
    delay(50);
    digitalWrite(led_OUT, LOW);
  }
}

void DeepPressureWearable::blink_T (int t_d) {
  digitalWrite(led_OUT, LOW);
  delay(t_d);
  digitalWrite(led_OUT, HIGH);
  delay(t_d);
}

void DeepPressureWearable::safety() {
      // Safety withdraw actuator and stop
    if (risingEdgeButton()) {
      actuator1.write(POSITION_MIN);
      if (serialON) Serial.println("Device off. Turn off power.");
      if (sdWriteON) {
        File dataFile = SD.open("raw_data.csv", FILE_WRITE);
        if (dataFile) {
            //dataFile.print(buf);
            dataFile.close();
        }
      }
      while (1);
    }
}

void DeepPressureWearable::runtime(void (*mapping)(int)) {
    short data;
    unsigned long myTime;

    myTime = millis(); // time for beginning of the loop

    // read flex sensor and map angle to actuator command. keep values in the bounds
    if (inputType == FLEX_INPUT) {
      if (capacitiveFlexSensor.available() == true) flexSensor = abs(capacitiveFlexSensor.getX());
    }
    else if (inputType == KEYBOARD_INPUT) {
      if (Serial.available() > 0) flexSensor = (Serial.read() - '0')*100 + (Serial.read() - '0')*10 + (Serial.read() - '0')*1 ;
    }
    mapping(int(flexSensor));
    //position1_Command = map(int(flexSensor), int(user_flex_MIN), int(user_flex_MAX), user_position_MIN, user_position_MAX);
    if(position1_Command > POSITION_MAX) position1_Command = POSITION_MAX;
    else if(position1_Command < POSITION_MIN) position1_Command = POSITION_MIN;

    if(position2_Command > POSITION_MAX) position2_Command = POSITION_MAX;
    else if(position2_Command < POSITION_MIN) position2_Command = POSITION_MIN;

    // Send command to actuator and measure actuator position
    // actuator1.write(position1_Command);
    //Serial.println(buttonCount % 2);
    if (!(buttonCount % 2)) {
      actuator1.write(position1_Command);
      actuator2.write(position2_Command);
    }
    else {
      actuator1.write(POSITION_MIN);
      actuator2.write(POSITION_MIN);
    }
    position1_Measured = analogRead(position1_IN);
    position2_Measured = analogRead(position2_IN);

    // read force data and write out data at lower frequency
    cycleCount = cycleCount + 1;
    if ((cycleCount == WRITE_COUNT)) {
      data = readDataFromSensor(I2C_ADDR);
      powerOn = (data >= 150);
      if (powerOn) analogWrite(led_OUT, 255);
      else analogWrite(led_OUT, 30);
      writeOutData(myTime, flexSensor, position1_Command, position1_Measured, data);
      cycleCount = 0;
    }
    risingEdgeButton();
    if (T_CYCLE > 0) delay(T_CYCLE);    
}

void DeepPressureWearable::miniPilot_patternsSequence(int t_d) {
        int i;
      int j;
      int x;
      int patterns[3] = {user_position_MIN, user_position_MIN + (user_position_MAX-user_position_MIN)/2, user_position_MAX};

     actuator1.write(POSITION_MIN);
      actuator2.write(POSITION_MIN);

      for (i=0; i<3; ++i) {
        position1_Command = patterns[i];
        for (j=0; j<3; ++j) {
          Serial.print(i);
          Serial.print(" ");
          Serial.println(j);
          position2_Command = patterns[j];
          actuator1.write(position1_Command);
          actuator2.write(position2_Command);
          delay(t_d);
        }
      }

      actuator1.write(POSITION_MIN);
      actuator2.write(POSITION_MIN);

      delay(t_d);

}


void DeepPressureWearable::miniPilot_patternsCommand() {
      int i;
      int j;
      int x;
      int y;
      int patterns[3] = {user_position_MIN, user_position_MIN + (user_position_MAX-user_position_MIN)/2, user_position_MAX};

     // actuator1.write(POSITION_MIN);
     //  actuator2.write(POSITION_MIN);

      if (Serial.available() > 0) {
        x = (Serial.read() - '0');
        y = (Serial.read() - '0');
        (Serial.read() - '0');
        if ((x < 0) or (y < 0) or (x > 2) or (y > 2)) {
          Serial.println("Error: invalid input. Try again.");
        }
        else {
          Serial.print(x);
      Serial.print(" ");
      Serial.println(y);
      actuator1.write(patterns[x]);
      actuator2.write(patterns[y]);
       }
      }

}

void DeepPressureWearable::miniPilot_patternsCommandbyLetter() {
      int i;
      int j;
      int x;
      int y;
      int z;
      int patterns[3] = {user_position_MIN, user_position_MIN + (user_position_MAX-user_position_MIN)/2, user_position_MAX};

      if (Serial.available() > 0) {
        x = (Serial.read());
        (Serial.read());
        
         // Serial.print(": ");
        if ((x < 65) or (x > 73)) {
          Serial.println("Error: invalid input. Try again.");
        }
        else {
          Serial.println((char) x);
          z = (x < 68) + (x >= 68 and x < 71)*2 + (x >= 71 and x <74)*3 - 1;

          y = (x+1) % 3;
      //     Serial.print(z);
      // Serial.print(" ");
      // Serial.println(y);
          actuatorArr[0].write(patterns[z]);
          actuatorArr[1].write(patterns[y]);
          actuator1.write(patterns[z]);
          actuator2.write(patterns[y]);

        }

      }

}

// sweeping actuator position, increasing and decreasing. infinite loop.
// t_d is time between actuator steps
int DeepPressureWearable::sweep(int t_d) {
    unsigned long myTime;
    short data;
    int counter = user_position_MIN;
    int extending = 1;
    int minValue = 1000;
    
    
    while (counter <= user_position_MAX) {
      String dataString = "";
      actuator1.write(counter);
      actuator2.write(counter);
      position1_Measured = analogRead(position1_IN);
      myTime = millis();
      if (position1_Measured < minValue) minValue = position1_Measured;
      data = readDataFromSensor(I2C_ADDR);

      if (serialON) {
        writeOutData(myTime, 0, counter, position1_Measured, data);
        // dataString += (String(myTime) + "," + String(counter) + "," \
        // + String(position1_Measured));
        // Serial.println(dataString);
      }

      if (extending == 1) {
        if (counter == (user_position_MAX)) {
          counter = counter - 1;
          extending = 0;
        } else counter = counter + 1;
      }
      else if (extending == 0) {
        if (counter == user_position_MIN) {
          counter = counter + 1;
          extending = 1;
          break; // comment if I want infinite sweeping
        } else counter = counter - 1;
      }
      delay(t_d);
    }
    return minValue;    
}


// sweeping actuator position, increasing and decreasing. infinite loop.
// t_d is time between actuator steps
void DeepPressureWearable::miniPilot_sweep(int t_d) {
    unsigned long myTime;
    short data;
    int counter = user_position_MIN; // user_position_MIN + (user_position_MAX-user_position_MIN)/2
    //int extending = 1;
    //int minValue = 1000;
    
    actuator1.write(counter);
    actuator2.write(counter);
    
    while (counter <= user_position_MAX) {
      actuator1.write(counter);
      position1_Measured = analogRead(position1_IN);
      myTime = millis();
      data = readDataFromSensor(I2C_ADDR);

      if (serialON) {
        writeOutData(myTime, 0, counter, position1_Measured, data);
      }
      counter = counter + 1;
      delay(t_d);
    }
    counter = user_position_MIN; // user_position_MIN + (user_position_MAX-user_position_MIN)/2
    actuator1.write(counter);

    while (counter <= user_position_MAX) {
      actuator2.write(counter);
      position2_Measured = analogRead(position2_IN);
      myTime = millis();
      data = readDataFromSensor(I2C_ADDR);

      if (serialON) {
        writeOutData(myTime, 0, counter, position2_Measured, data);
      }
      counter = counter + 1;
      delay(t_d);
    }


}

void DeepPressureWearable::miniPilot_sweepKeyboard() {
    unsigned long myTime;
    short data;
    int counter = user_position_MIN; // user_position_MIN + (user_position_MAX-user_position_MIN)/2
    int x;
    //int extending = 1;
    //int minValue = 1000;
    
    actuator1.write(counter);
    actuator2.write(counter);

    while (1) {

      if (Serial.available() > 0) {
        x = (Serial.read());
         //Serial.println(x);

      if ( (x < 52) or (x > 53)) {
        Serial.println("Error: invalid input. Try again.");
      }

      else if (x == 52) {
        counter = counter - 1;
        Serial.println(counter);
      }
      else if (x == 53) {
        counter = counter + 1;
        Serial.println(counter);
      }

      if(counter < user_position_MIN) counter = user_position_MIN;
      else if(counter > (2*user_position_MAX + 1 - user_position_MIN)) counter = (2*user_position_MAX + 1 - user_position_MIN);

      if ((counter >= user_position_MIN) and (counter <= user_position_MAX)) {
        actuator1.write(counter);
        actuator2.write(user_position_MIN);
      }
      else if ((counter > user_position_MAX) and (counter < (2*user_position_MAX + 1 - user_position_MIN))) {
        actuator1.write(user_position_MIN);
        actuator2.write(counter-(user_position_MAX + 1 - user_position_MIN));
      }

      }      


    }

}

// Calibration
void DeepPressureWearable::calibrationActuatorFeedback() {
  int ACTUATOR_FEEDBACK_MAX = 500;
  int ACTUATOR_FEEDBACK_MIN = 500;
  
  // Calibration: Sweep and record the actuator position feedback positions
  actuator1.write(POSITION_MIN);
  
  delay(500);
  ACTUATOR_FEEDBACK_MAX = analogRead(position1_IN);
  ACTUATOR_FEEDBACK_MIN = sweep(300);
  Serial.println(ACTUATOR_FEEDBACK_MAX);
  Serial.println(ACTUATOR_FEEDBACK_MIN);
}

void DeepPressureWearable::calibrationZeroForce() {
  zeroForce = 0;
  
  // Calibration Stage: Get the zero force of the device
  actuator1.write(POSITION_MIN);
  zeroForce = readDataFromSensor(I2C_ADDR);
  Serial.println((zeroForce - 255) * (45.0)/512);
}

void DeepPressureWearable::calibrationFlexSensor(unsigned long timeLength) {
  unsigned long startTime;
  unsigned long endTime;
  //unsigned long timeLength = 50000;

  actuator1.write(POSITION_MIN);

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
int DeepPressureWearable::calibrationMaxDeepPressure() {
   int counter = POSITION_MIN;
   int x;
   short data;
   String dataString;
   short maxForce = 0;
   short minForce = 0; // detection threshold
   int nClicks = 0;

   zeroForce = 0;
   actuator1.write(counter);
   blinkN(5,1000);
   zeroForce = readDataFromSensor(I2C_ADDR);

    while (counter <= POSITION_MAX) {
       // Measure force and actuator position
      dataString = "";
      data = readDataFromSensor(I2C_ADDR);
      position1_Measured = analogRead(position1_IN);
      // Send command to actuator
      actuator1.write(counter);
      dataString += (String(counter) + "," + String(position1_Measured) + "," + String((data - 255) * (45.0)/512));
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
          minForce = readDataFromSensor(I2C_ADDR);
          nClicks = nClicks + 1;
      }
      if (nClicks == 3) { // NOTE: nClicks = 3 is deliebrate. rising edge of click
          user_position_MAX = counter - 2; // NOTE: the -2 is arbitrary
          maxForce = readDataFromSensor(I2C_ADDR);
          delay(3000);
          actuator1.write(POSITION_MIN);
          break; 
      }
      delay(250);
      counter = counter + 1;
  }
  actuator1.write(POSITION_MIN);

  Serial.println(zeroForce);
  Serial.println(minForce); // new
  Serial.println(maxForce);
  Serial.println(user_position_MIN); // new
  Serial.println(user_position_MAX);

  return user_position_MAX;
}

/* Calibration: Interfaces with python gui */
void DeepPressureWearable::calibration() {
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

  // initialize blank array
  for (int j = 0; j< lenUserArr; j++) {
     user_position_MAX_arr[j] = 0;
     user_position_MIN_arr[j] = 0;
  }
          
  // Reset position of actuator
  actuator1.write(POSITION_MIN);

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
          user_position_MAX_arr[nMaxPressure] = calibrationMaxDeepPressure();
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
          calibrationActuatorFeedback();
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

void DeepPressureWearable::blinkN (int n, int t_d) {
  for(int i=0; i < n; i++) {
    analogWrite(led_OUT, 10);
    delay(t_d/2);
    analogWrite(led_OUT, 200);
    delay(t_d/2);  
  }
}

void DeepPressureWearable::initializeSystem(bool c) {
  Wire.begin(); // join i2c bus
  initializeSerial(); // start serial for output
  initializeSDCard(); // initialize sd card
  initializeActuator(); // initialize actuator and set in min position
  if (inputType == FLEX_INPUT) initializeFlexSensor(); // initialize flex sensor
  else {
    WRITE_COUNT = 30;
    flexSensor = 180;
  }
  initializeIO(); // initialize IO pins, i.e. button and led
  analogWrite(led_OUT, 30);
  if (c) {
    Serial.println("Entering calibration...");
    calibration();
  }
}

bool DeepPressureWearable::initializeSerial() {
    Serial.begin(4608000);  
    Serial.flush();
    while (!Serial);
    return (true); 
}

bool DeepPressureWearable::initializeSDCard() {
  if (sdWriteON) {
    // See if the card is present and can be initialized:
    if (!SD.begin(CHIP_SELECT)) {
      Serial.println("Card failed, or not present");
      while (1);
    }
    Serial.println("card initialized.");
    // fix test code
    //    SD.remove("raw_data.csv");
    //    Serial.println("Removed old data");
  }
}

bool DeepPressureWearable::initializeActuator() {
  actuator1.attach(position1_OUT); // attach servo 
  actuator1.write(POSITION_MIN); //put in minimum position

  actuator2.attach(position2_OUT); // attach servo 
  actuator2.write(POSITION_MIN); //put in minimum position
  return (true);
}

bool DeepPressureWearable::initializeFlexSensor() {
    if (capacitiveFlexSensor.begin() == false) {
      Serial.println(("No sensor detected. Check wiring. Freezing..."));
      while (1);
  }
  capacitiveFlexSensor.enableStretching(true);
  return (true);
}

bool DeepPressureWearable::initializeIO() {
  pinMode(button_IN, INPUT); // set button and led
  pinMode(led_OUT, OUTPUT);
  return (true); 
}

bool DeepPressureWearable::risingEdgeButton() {
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

void DeepPressureWearable::writeOutData(unsigned long t, float f, int c, int m, short d) {
  String dataString = "";
  if (sdWriteON || serialON) {
    dataString += (String(t) + "," + String(f) + "," + String(c) + "," \
    + String(m) + "," + String(d));
    if (sdWriteON) {
      File dataFile = SD.open("raw_data.csv", FILE_WRITE);
      if (dataFile) {
        dataFile.println(dataString);
        dataFile.close();
      } else if (serialON) Serial.println("error opening datalog");
    }
        if (serialON) Serial.println(dataString);
  }  
}

short DeepPressureWearable::readDataFromSensor(short address) {
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


