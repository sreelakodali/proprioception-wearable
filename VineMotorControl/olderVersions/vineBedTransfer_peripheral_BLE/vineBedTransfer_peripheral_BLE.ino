/*
  Motor Control for Vine Bed Transfer
  Sreela Kodali kodali@stanford.edu

  This creates a BLE peripheral with a service that contains multiple
  characteristics to control different groups of the brushless motors.
*/

#include <ArduinoBLE.h>
#include <Servo.h>


# define N_ACT 9 // Number of actuators, 8 motors + 1 pressure regulator = 9
# define N_CMDS 6 // number of commands
//# define N_LEVELS 10 // number of distinct speed commands

// These are the range of PWM values the SPARK Max Controller understands
// See PWM Input Specs here for more details:
// https://docs.revrobotics.com/sparkmax/specifications 
// The PWM signal that goes to the Spark Max is generated by a function called
// writeMicroseconds(x).
// motor.writeMicroseconds(1025) = reverse max speed
// motor.writeMicroseconds(1500) = neutral, no movement
// motor.writeMicroseconds(2000) = forwawrd max speed

typedef enum {
  MOTOR_MIN = 1025,
  MOTOR_NEUTRAL = 1500,
  MOTOR_MAX = 2000
} MOTOR_LIMITS;


// You can ignore these pressure values below. I didn't really get to this
//// FIX: Set values for pressure regulator. These are random
typedef enum {
  PRESSURE_MIN = 1025,
  PRESSURE_NEUTRAL = 1500,
  PRESSURE_MAX = 2000
} PRESSURE_LIMITS;


// IF YOU WANT TO SEND THE SAME COMMAND TO GROUPS OF MOTORS
// I created a little structure "cmd" (short for "command") where you give it a name,
// and identify which motors you want to run with a binary array so you can run different
// groups of motors at the same time! For example, if I want to control motors 1-4 at the
// same time, I'd add the following to my allCommands[] array:
//         initializeCmd("myCommand", {1, 1, 1, 1, 0, 0, 0, 0, 0})
// Then, when I open the app and connect with the Arduino, "myCommand" will appear as an
// option where I can write/send one value that'll go to motors 1-4. 

struct cmd
{
  char* strname;
  int* motors;
  BLEIntCharacteristic ble;
};

cmd initializeCmd(char* s, int* m) {
  BLEIntCharacteristic bleCharacteristic("2A59", BLEWrite); // 2A59, analog output
  BLEDescriptor des("2901", s); // adding user description (2901) for the characteristic
  bleCharacteristic.addDescriptor(des);
  bleCharacteristic.writeValue(0);
  cmd c{s, m, bleCharacteristic};
  return c;
}

BLEService motorService("01D"); // Bluetooth® Low Energy, motorized device


// IMPORTANT!!!
// IF YOU WANT TO ADJUST THE RANGE, RESOLUTION, SPEEDS FOR THE MAPPING OF BLE-TO-MOTOR CMDS,
// ETC. BEYOND THE DEFAULT TEN PRESET VALUES, READ THIS!

// The default works simply and as follows: We have a small integer array of length 10 called
// uSCommandValues (abbreviation for // microsecondCommandValues) that has 10 distinct motor
// commands within the SparkMax's valid range between 1000 and 2000 (https://docs.revrobotics.com/sparkmax/specifications),
// as shown on line 90. 
// The BLE commands are the index for this array. So for example, if someone sends
// a "1" command via their phone to the motors, the motors would receive
// writeMicroseconds(usCommandValues[1])=MOTOR_MIN.
// If you'd like different values, feel free to change the content and/or length of USCommandVValues
const int uSCommandValues[10] = {MOTOR_NEUTRAL, MOTOR_MIN, 1185, 1285, 1385, MOTOR_NEUTRAL, 1650, 1750, 1850, MOTOR_MAX}; // 5 is neutral
const int uSCommandValues_V2[16] = {MOTOR_NEUTRAL, MOTOR_MIN, 1105, 1185, 1235, 1285, 1335, 1385, MOTOR_NEUTRAL, 1650, 1600, 1750, 1800, 1850, 1925, MOTOR_MAX}; // 8 is neutral

//const int uSCommandValues_custom[N_LEVELS + 1];

const int neutralCMD_min = 1450;
const int neutralCMD_max = 1550;
// which motors will be on for each command

// tcw1, tcw2, tcw3, tcw4, base1, base2, base3, base4, pressure regulator
int motors_CMD1[N_ACT] = {0, 0, 0, 0, 1, 1, 1, 1, 0};
int motors_CMD2[N_ACT] = {1, 1, 1, 1, 0, 0, 0, 0, 0};
int motors_CMD3[N_ACT] = {1, 1, 1, 1, 1, 1, 1, 1, 0};
int motors_CMD4[N_ACT] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
int motors_CMD5[N_ACT] = {0, 0, 0, 0, 0, 0, 0, 0, 1};

cmd allCommands[N_CMDS] = {initializeCmd("allBase", motors_CMD1), initializeCmd("allTCWTurn", motors_CMD2), initializeCmd("allBaseTCWTurn", motors_CMD3), 
                           initializeCmd("individualMotor", motors_CMD4), initializeCmd("pressureReg", motors_CMD5), initializeCmd("PreLoadValues", motors_CMD4)};
                          // initializeCmd("PreLoadValues_Acc", motors_CMD4)};

Servo motorArr[N_ACT];

// these pins correspond  to different motor's input 
const  int pins_CommandOUTArr[N_ACT] = {2, 3, 4, 5, 6, 7, 8, 9, 10};

void setup() {
//
//  Serial.begin(9600);
//  while (!Serial);

    // begin initialization
  if (!BLE.begin()) {
    while (1); // Serial.println("starting Bluetooth® Low Energy module failed!");
  }

  // set advertised local name and service UUID:
  BLE.setLocalName("Nano 33 BLE");
  BLE.setAdvertisedService(motorService);
  
  // set LED pin to output mode
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  digitalWrite(LEDR, HIGH); // off
  digitalWrite(LEDG, HIGH); // off
  digitalWrite(LEDB, HIGH); // off


//  // initialize custom uSCommandLevels_Custom
//  uSCommandValues_custom[0] = MOTOR_NEUTRAL;
//  int inc = (MOTOR_MAX - MOTOR_MIN)/N_LEVELS;
//  for (int i = 0; i < (N_LEVELS + 1); ++i) {
//    uSCommandValues_custom[i] = MOTOR_MIN + (i * (inc));
//  }

  for (int i = 0; i < N_ACT; ++i) {
     motorArr[i].attach(pins_CommandOUTArr[i]);     // connect each motor to PWM output
     if (i == (N_ACT-1)) {
      motorArr[i].writeMicroseconds(PRESSURE_NEUTRAL); 
     } else {
      motorArr[i].writeMicroseconds(MOTOR_NEUTRAL);
     }
  }

  for (int i = 0; i < N_CMDS; ++i) {
      motorService.addCharacteristic(((allCommands[i]).ble)); // add the characteristic to the service
  }
    
    BLE.addService(motorService); // add service
    BLE.advertise(); // start advertising

//    Serial.println("Initialized.");
}

void loop() {
    
  // listen for Bluetooth® Low Energy peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {

    // while the central is still connected to peripheral:
    while (central.connected()) {
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:

      for (int i = 0; i < N_CMDS; ++i) {
         if (((allCommands[i]).ble).written()) {
          
            digitalWrite(LED_BUILTIN, HIGH); // turn on LED value for commmand being sent

            char* n = (allCommands[i]).strname;

          if (n == "PreLoadValues") {
              unsigned long x = ((allCommands[i]).ble).value(); 
              int commands[8];

              for (int k = 0; k < N_ACT-1; ++k) {
                commands[k] = 0;
              }

              commands[0] = (x & 0x000000F0) >> 4;
              commands[1] = (x & 0x0000000F) >> 0;
              commands[2] = (x & 0x0000F000) >> 12;
              commands[3] = (x & 0x00000F00) >> 8;
              commands[4] = (x & 0x00F00000) >> 20;
              commands[5] = (x & 0x000F0000) >> 16;
              commands[6] = (x & 0xF0000000) >> 28;
              commands[7] = (x & 0x0F000000) >> 24;

              bool noSendCommand = false;
              for (int k = 0; k < N_ACT-1; ++k) {
                int idx = commands[k];
                //Serial.println(idx);
                if (idx == 0 or idx > 15 or idx < 1) {
                //if (idx > 10 or idx < 1) { // COMMENTING OUT TEMPORARILY FOR NEW CHANGE
                  noSendCommand = true;
                }
              } 
              if (!(noSendCommand)) { // if valid commands and/or no zero sent, pass values
                for (int k = 0; k < N_ACT-1; ++k) {
                    int idx = commands[k]; 
                    //Serial.println(commands[k]);
                    motorArr[k].writeMicroseconds(uSCommandValues_V2[idx]);
                }
                // write commands
              } else {
                for (int k = 0; k < N_ACT-1; ++k) {
                    motorArr[k].writeMicroseconds(MOTOR_NEUTRAL);
                    //Serial.println("STOP");
                }
                
              }

            //}

          } else if  (n == "PreLoadValues_Acc"){
            unsigned long x = ((allCommands[i]).ble).value();
            
              if (x == 0) {
                for (int k = 0; k < N_ACT-1; ++k) {
                  motorArr[k].writeMicroseconds(MOTOR_NEUTRAL);
                }
              } else { 
              int commands[16];

              commands[15] = (x & 0x000000F000000000) >> 36;
              commands[14] = (x & 0x0000000F00000000) >> 32;
              commands[13] = (x & 0x0000F00000000000) >> 44;
              commands[12] = (x & 0x00000F0000000000) >> 40;
              commands[11] = (x & 0x00F0000000000000) >> 52;
              commands[10] = (x & 0x000F000000000000) >> 48;
              commands[9] = (x & 0xF000000000000000) >> 60;
              commands[8] = (x & 0x0F00000000000000) >> 56;
              
              commands[7] = (x & 0x000000F0) >> 4;
              commands[6] = (x & 0x0000000F) >> 0;
              commands[5] = (x & 0x0000F000) >> 12;
              commands[4] = (x & 0x00000F00) >> 8;
              commands[3] = (x & 0x00F00000) >> 20;
              commands[2] = (x & 0x000F0000) >> 16;
              commands[1] = (x & 0xF0000000) >> 28;
              commands[0] = (x & 0x0F000000) >> 24;


//              //      
//              Serial.println(commands[0]);
//              Serial.println(commands[1]);
//              Serial.println(commands[2]);
//              Serial.println(commands[3]);
//              Serial.println(commands[4]);
//              Serial.println(commands[5]);
//              Serial.println(commands[6]);
//              Serial.println(commands[7]);
//              Serial.println(commands[8]);
//              Serial.println(commands[9]);
//              Serial.println(commands[10]);
//              Serial.println(commands[11]);
//              Serial.println(commands[12]);
//              Serial.println(commands[13]);
//              Serial.println(commands[14]);
//              Serial.println(commands[15]);
            
              }
            // following logic holds for allBase, allTCWTurn, allBaseTCWTurn, individualMotors
         } else {

            unsigned long x = ((allCommands[i]).ble).value();
            unsigned long z = (x & 0b11110000) >> 4; 
            x = (x & 0b00001111); 
            int y = MOTOR_NEUTRAL; // Fix: if it's command for pressure, different default value
//            Serial.println(x, HEX);

            // if value > 16, change motorArr to make sure motor of MSB turns on
            if (z) {
              for (int j = 0; j < N_ACT; ++j) {
                if (z-1 == j) {
                   (allCommands[i]).motors[j] = 1;
                } else {
                  (allCommands[i]).motors[j] = 0;
                }
              }
            }

               // otherwise read LSB as motor command
            if (x >= 0 && x < 10) {
              y = uSCommandValues[(int)x]; // Fix: if it's command for pressure, different value
              //Serial.println(y);
            } else {
              //Serial.println("Invalid input");
              digitalWrite(LED_BUILTIN, HIGH);  //blink to show invalid input
              delay(250);
              digitalWrite(LED_BUILTIN, LOW);
              delay(250);
              digitalWrite(LED_BUILTIN, HIGH); 
              delay(250);
              digitalWrite(LED_BUILTIN, LOW);
               delay(250);
              digitalWrite(LED_BUILTIN, HIGH); 
              delay(250);
              digitalWrite(LED_BUILTIN, LOW); 
            }

            if (y > neutralCMD_min && y < neutralCMD_max) {
              digitalWrite(LEDR, HIGH);
              digitalWrite(LEDG, HIGH);
              digitalWrite(LEDB, LOW); 
            } else if (y < neutralCMD_min) {
              digitalWrite(LEDR, LOW);
              digitalWrite(LEDG, HIGH);
              digitalWrite(LEDB, HIGH);
            } else if (y > neutralCMD_max){
              digitalWrite(LEDR, HIGH);
              digitalWrite(LEDG, LOW);
              digitalWrite(LEDB, HIGH);
            } else {
              digitalWrite(LEDR, HIGH);
              digitalWrite(LEDG, HIGH);
              digitalWrite(LEDB, HIGH); 
            }

            for (int j = 0; j < N_ACT; ++j) {
                if ((allCommands[i]).motors[j]) {
                   motorArr[j].writeMicroseconds(y);
                } else {
                   motorArr[j].writeMicroseconds(MOTOR_NEUTRAL);
                }
            }
         }
            delay(500);
         }
         digitalWrite(LED_BUILTIN, LOW); // turn off LED
      }
    }

    // when the central disconnects, print it out:
    // Serial.print(F("Disconnected from central: "));
    // Serial.println(central.address());
  }
}