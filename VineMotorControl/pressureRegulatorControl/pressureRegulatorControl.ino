/*
  Pressure Regulator Control for QB4TANKKZP25PSG
  Sreela Kodali kodali@stanford.edu, June 8th 2024

  Adapted from code written by Yimeng Qin
*/


#define t_SendCommands 3000 // 3 seconds
#define t_dataRate 100 // 100 ms

const float systemMax = 15.0; // MAX PRESSURE FOR OUR OURPUT


const int nPoints_movingAvg = 48;
int average[nPoints_movingAvg];
int count = 0;
float averagedFeedback = 0.0;

const int pressureCommandOUT = 11;
const int pressureFeedbackIN = A0;
const bool serialOn = true;

float pressureCommand = 0.0;
float pressureFeedbackProcessed = 0.0;
int pwmCommand= 0;

const float regulatorMin = 0.0; // for mapping
const float regulatorMax = 25.0;


typedef enum {
  PRESSURE_CMD_MIN = 0,
  PRESSURE_CMD_MAX = 255,
  MAX_UNITS = 1024
} PRESSURE_CMD_LIMITS;

void setup() {

  if (serialOn) {
    Serial.begin(9600);
    while (!Serial);
    Serial.println("Initialized.");
  }
  pinMode(pressureCommandOUT, OUTPUT);

  // default 
  analogWrite(pressureCommandOUT, PRESSURE_CMD_MIN);

  for (int i = 0; i < nPoints_movingAvg; i++ ) {
    average[i] = 0;
  }

  
}

void loop() {

  // check and receive pressure command
  if (Serial.available() > 0) {
    pressureCommand = Serial.parseFloat();

    if (pressureCommand > systemMax) {
      pressureCommand = systemMax;
    } else if (pressureCommand < 0) {
      pressureCommand = 0.0;
    }
    Serial.read();
    Serial.println("NEW COMMAND: " + String(pressureCommand));
    // map pressure command to DAC PWM output. float to int
    pwmCommand = mapFloat(true, pressureCommand, PRESSURE_CMD_MIN, PRESSURE_CMD_MAX, regulatorMin,regulatorMax);
    if (pwmCommand > PRESSURE_CMD_MAX) {
      pwmCommand = PRESSURE_CMD_MAX;
    } else if (pwmCommand < PRESSURE_CMD_MIN) {
     pwmCommand = PRESSURE_CMD_MIN;
    }
    analogWrite(pressureCommandOUT, pwmCommand);
    delay(t_SendCommands);
  }

  // measure raw value of pressure feedback and map it, int to float
  int rawFeedback = analogRead(pressureFeedbackIN);
  
  average[count] = rawFeedback;
  count = count + 1;
  if (count == nPoints_movingAvg) {
    count = 0;
  }
  float sum = 0.0;
  for (int i = 0; i < nPoints_movingAvg; i++ ) {
    sum = sum + average[i];
  }
  averagedFeedback = sum/nPoints_movingAvg;

  averagedFeedback = (ceil)(averagedFeedback);
  pressureFeedbackProcessed = (averagedFeedback / MAX_UNITS) * regulatorMax;
  Serial.println("Pressure Command: " + (String)(pressureCommand) + ", Pressure CMD: " + (String)(pwmCommand) + ", Pressure Measured: " + (String)(pressureFeedbackProcessed));
  

  delay(t_dataRate);
}

float mapFloat(bool type, float x, int int_min, int int_max, float float_min, float float_max) {
  float output;
  if (type) { // float to int

    output = (float) (((x - float_min) * (int_max - int_min) / (float_max - float_min) + int_min));

  } else { // int to float. in case    
    output = (float) (((x - int_min) * (float_max - float_min) / (int_max - int_min) + float_min));
  }
  return output;
}


void sequence(float p1, int t_d, float p2, int t_d2) {
  
}
