/* Applying multiple points of contact with hapknit
for evaluating presence of spatial summation

Written by: Sreela Kodali, kodali@stanford.edu

Code based on the robust and thorough documentation by
Yannie Tan and Ian Scholl - thank you to both of them!
*/

#include <PortFlow8.h>
#define btnPin 7
#define N_TACTORS 8

typedef enum {
  PRESSURE_MIN = 0,
  PRESSURE_MAX = 210
} PRESSURE_LIMITS;

// ** DEFINE PORTS **
uint8_t port1 = 0b10000000;
uint8_t port2 = 0b01000000;
uint8_t port3 = 0b00100000;  
uint8_t port4 = 0b00010000;
uint8_t port5 = 0b00001000;
uint8_t port6 = 0b00000100;
uint8_t port7 = 0b00000010;
uint8_t port8 = 0b00000001;
uint8_t allports = 0b11111111;

// USER INPUT PARAMETERS

uint8_t ports = port1 | port2; // bitwise 'or' which ports you want active
uint8_t pwmValue = 50;
//int targetPressure = 210; //absolute (!) pressure, max. 230 with current system
int holdTime = 400; // in milliseconds
int deflationTime = holdTime;
Unit unit = KPA;

// Variables
PortFlow8 portflow8;
bool buttonState = 0;         // current state of the button
bool oldButtonState = 0;     // previous state of the button
int buttonCount = 0;

// Setup, executed once at start-up
void setup() {
  
  // initialize 'UserSW' button
  pinMode(btnPin,INPUT_PULLUP); 
  
  // initialize PortFlow8 Class
  portflow8 = PortFlow8(); 
  portflow8.blueLED(HIGH);
  Serial.begin(115200); //4608000
  Serial.println("Initialized");
  
  // initialize Pressure Sensor
  while(portflow8.activateSensor()==false){
    portflow8.pixel(10,0,10);
    delay(10);
  }
  Serial.println("Pressure Sensor activated");
  portflow8.pixel(10,10,10);
}

void loop() {
  //Serial.println(portflow8.getPressure(unit));
   serialHapknitControl();
}

// if serial is available, read the value and send it to active ports
void serialHapknitControl() {
  int pressureCommand;

  // if serial is available, read the value
  if (Serial.available() > 0) {
    pressureCommand = Serial.parseInt();
    //Serial.read(); // Uncomment if using Serial monitor.

    //Serial.println(pressureCommand);

    
    // make sure the command is valid and within bounds
    if(pressureCommand > PRESSURE_MAX) pressureCommand = PRESSURE_MAX;
    else if (pressureCommand > PRESSURE_MIN) pressureCommand = PRESSURE_MIN;

    if (!(buttonCount % 2)) {
      // Pressurize
      writeOut("Starting pressure = ", "PRESSURIZE TO ", String(pressureCommand));
      portflow8.pixel(0,10,10);
      while (portflow8.inflateP(ports, pressureCommand, unit, pwmValue) == 1) {
      }
  
      // Holding
      writeOut("Pressure after inflation = ", "HOLDING FOR ", String(holdTime/1000));
      portflow8.pixel(0,0,10);
      delay(holdTime);
  
      // Deflate
      writeOut("Pressure after holding = ", "DEFLATING FOR ", String(deflationTime/1000));
      portflow8.pixel(10,0,0);
      portflow8.vacuumT(ports, deflationTime, pwmValue);
    }
  }
 
   // keep in idle
    writeOut("Pressure at start of idling is: ", "IDLING", "");
    portflow8.pixel(10,10,10);
    portflow8.stopAction(ports);

    risingEdgeButton();
    delay(50);  
}

void writeOut(String intro, String state, String parameter) {
  Serial.print(intro);
  Serial.println(portflow8.getPressure(unit));
  Serial.print(state);
  Serial.println(parameter);
}


bool risingEdgeButton() {
  buttonState = digitalRead(btnPin);
  //Serial.println(buttonState);
  if (buttonState != oldButtonState) {
    if (buttonState == LOW) { // changed to low because its pullup
      buttonCount = buttonCount + 1;
      oldButtonState = buttonState;
      delay(300);
      return true;
    }
  }
  oldButtonState = buttonState; 
  return false;
}
