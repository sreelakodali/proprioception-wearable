/* Applying multiple points of contact with hapknit
for evaluating presence of spatial summation

Written by: Sreela Kodali, kodali@stanford.edu

Code based on the robust and thorough documentation by
Yannie Tan and Ian Scholl - thank you to both of them!
*/

#include <AirPort.h>
#define btnPin 7
#define N_TACTORS 8

typedef enum {
  PRESSURE_MIN = 103,
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

uint8_t ports = (port1 | port5); // bitwise 'or' which ports you want active
uint8_t pwmValue = 50;
//int targetPressure = 210; //absolute (!) pressure, max. 230 with current system
int holdTime = 3000; // in milliseconds
int deflationTime = 400;
Unit unit = KPA;

// Variables
AirPort portflow8;
bool buttonState = 0;         // current state of the button
bool oldButtonState = 0;     // previous state of the button
int buttonCount = 0;

// Setup, executed once at start-up
void setup() {
  
  // initialize 'UserSW' button
  pinMode(btnPin,INPUT_PULLUP); 
  
  // initialize PortFlow8 Class
  portflow8 = AirPort(); 
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
  portflow8.stopAction(ports);
}

void loop() {
  //Serial.println(portflow8.getPressure(unit));
   //serialPressureControl();
   serialPortControl();
}

uint8_t generatePort(int n) {
  uint8_t val = 0b00000001;
  val = val << n;
  return val;
}

// send port numbers via serial to activate them to a constant
// pressure, hold, and release
void serialPortControl() {
  float pressureCommand;
  int n = 0;
  float measuredPressure = portflow8.getPressure(unit);
  // if serial is available, read the value
  if (Serial.available() > 0) {
    n = Serial.parseInt();
    
    Serial.read(); // Uncomment if using Serial monitor.

    //Serial.println(pressureCommand);

    // make sure the command is valid and within bounds
    //if(pressureCommand > 800) pressureCommand = 800; // for time
    pressureCommand = 210;
    switch(n) {
      case 1:
        ports = port1;
        break;
      case 2:
        ports = port2;
        break;
      case 3:
        ports = port3;
        break;
      case 4:
        ports = port4;
        break;
      case 5:
        ports = port5;
        break;
      case 6:
        ports = port6;
        break;
      case 7:
        ports = port7;
        break;
      case 8:
        ports = port8;
        break;
      case 9:
        ports = (port1 | port5);
        pressureCommand = 120;
        break;
      case 10:
        ports = (port2 | port6);
        pressureCommand = 120;
        break;
      case 11:
        ports = (port6 | port7);
        pressureCommand = 120;
        break;
      case 12:
        ports = (port4 | port8);
        pressureCommand = 120;
        break;
      case 13:
        ports = (port1 | port5 | port2 | port6);
        break;
      case 14:
        ports = (port1 | port5 | port2 | port6 | port3 | port7);
        break;
    }
    
    
//    if(pressureCommand > PRESSURE_MAX) pressureCommand = PRESSURE_MAX; // for pressure
//    else if (pressureCommand < PRESSURE_MIN) pressureCommand = PRESSURE_MIN;

    if (!(buttonCount % 2)) {
      // Pressurize
      writeOut("Starting pressure = ", "PRESSURIZE TO ", String(pressureCommand));
      portflow8.pixel(0,10,10);
      
      // pressure-based command
      while (portflow8.inflateP(ports, pressureCommand, unit, pwmValue) == 1) {
      }

      // time-based command
      // portflow8.inflateT(ports, pressureCommand, pwmValue);
      
      // manual pressure-based commanded
//      portflow8.startInflation(ports, pwmValue);
//      while (measuredPressure < pressureCommand) {
//        measuredPressure = portflow8.getPressure(unit);
//        Serial.println(measuredPressure);
//        delay(100);
//      }
//      portflow8.stopAction(ports);
  
      // Holding
      //portflow8.openPorts(~(allports));
      writeOut("Pressure after inflation = ", "HOLDING FOR ", String(holdTime));
      portflow8.pixel(0,0,10);
      delay(holdTime);
      
  
      // Deflate
      writeOut("Pressure after holding = ", "DEFLATING FOR ", String(deflationTime));
      portflow8.pixel(10,0,0);
      portflow8.vacuumT(ports, deflationTime, pwmValue);
    }
  }
 
   // keep in idle
    writeOut("Pressure at start of idling is: ", "IDLING", "");
    portflow8.pixel(10,10,10);
    portflow8.stopAction(ports);

    risingEdgeButton();
    delay(1000); 
}

// send a pressure value via serial to active ports
void serialPressureControl() {
  float pressureCommand;
  float measuredPressure = portflow8.getPressure(unit);
  // if serial is available, read the value
  if (Serial.available() > 0) {
    pressureCommand = Serial.parseFloat();
    
    Serial.read(); // Uncomment if using Serial monitor.

    //Serial.println(pressureCommand);

    // make sure the command is valid and within bounds
    //if(pressureCommand > 800) pressureCommand = 800; // for time
    if(pressureCommand > PRESSURE_MAX) pressureCommand = PRESSURE_MAX; // for pressure
    else if (pressureCommand < PRESSURE_MIN) pressureCommand = PRESSURE_MIN;

    if (!(buttonCount % 2)) {
      // Pressurize
      writeOut("Starting pressure = ", "PRESSURIZE TO ", String(pressureCommand));
      portflow8.pixel(0,10,10);
      
      // pressure-based command
      while (portflow8.inflateP(ports, pressureCommand, unit, pwmValue) == 1) {
      }

      // time-based command
      // portflow8.inflateT(ports, pressureCommand, pwmValue);
      
      // manual pressure-based commanded
//      portflow8.startInflation(ports, pwmValue);
//      while (measuredPressure < pressureCommand) {
//        measuredPressure = portflow8.getPressure(unit);
//        Serial.println(measuredPressure);
//        delay(100);
//      }
//      portflow8.stopAction(ports);
  
      // Holding
      //portflow8.openPorts(~(allports));
      writeOut("Pressure after inflation = ", "HOLDING FOR ", String(holdTime));
      portflow8.pixel(0,0,10);
      delay(holdTime);
      
  
      // Deflate
      writeOut("Pressure after holding = ", "DEFLATING FOR ", String(deflationTime));
      portflow8.pixel(10,0,0);
      portflow8.vacuumT(ports, deflationTime, pwmValue);
    }
  }
 
   // keep in idle
    writeOut("Pressure at start of idling is: ", "IDLING", "");
    portflow8.pixel(10,10,10);
    portflow8.stopAction(ports);

    risingEdgeButton();
    delay(1000);  
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
      //Serial.println("boink!");
      buttonCount = buttonCount + 1;
      oldButtonState = buttonState;
      delay(300);
      return true;
    }
  }
  oldButtonState = buttonState; 
  return false;
}
