/*
  Based on example code, LED, in ArduinoBLE Examples

  Motor Control for Vine Bed Transfer
  Sreela Kodali kodali@stanford.edu

  This example creates a Bluetooth® Low Energy peripheral with services that contains a
  characteristic to control an LED.
*/

#include <ArduinoBLE.h>
#include <Servo.h>


# define N_ACT 9 // 8 motors + 1 pressure regulator
# define N_CMDS 6

typedef enum {
  MOTOR_MIN = 1025,
  MOTOR_NEUTRAL = 1500,
  MOTOR_MAX = 2000
} MOTOR_LIMITS;

// FIX: Set values for pressure regulator
typedef enum {
  PRESSURE_MIN = 1025,
  PRESSURE_NEUTRAL = 1500,
  PRESSURE_MAX = 2000
} PRESSURE_LIMITS;

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
const int uSCommandValues[10] = {MOTOR_NEUTRAL, MOTOR_MIN, 1185, 1285, 1385, MOTOR_NEUTRAL, 1650, 1750, 1850, MOTOR_MAX};

const int neutralCMD_min = 1450;
const int neutralCMD_max = 1550;
// which motors will be on for each command
// FIX or something to think about later: motors might be on, but base/tcw might have opposite directions and different speeds
// maybe combine some of the commands, like instead of base* and tcw*, perhaps individual motors

// tcw1, tcw2, tcw3, tcw4, base1, base2, base3, base4, pressure regulator
int motors_CMD1[N_ACT] = {0, 0, 0, 0, 1, 1, 1, 1, 0};
int motors_CMD2[N_ACT] = {1, 1, 1, 1, 0, 0, 0, 0, 0};
int motors_CMD3[N_ACT] = {1, 1, 1, 1, 1, 1, 1, 1, 0};
int motors_CMD4[N_ACT] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
int motors_CMD5[N_ACT] = {0, 0, 0, 0, 0, 0, 0, 0, 1};

cmd allCommands[N_CMDS] = {initializeCmd("allBase", motors_CMD1), initializeCmd("allTCWTurn", motors_CMD2), initializeCmd("allBaseTCWTurn", motors_CMD3), 
                           initializeCmd("individualMotor", motors_CMD4), initializeCmd("pressureReg", motors_CMD5),
                           initializeCmd("TCW_linAct", motors_CMD4)};

Servo motorArr[N_ACT];
const  int pins_CommandOUTArr[N_ACT] = {2, 3, 4, 5, 6, 7, 8, 9, 10};

BLE.setEventHandler(BLECo

void setup() {

//   Serial.begin(9600);
//   while (!Serial);

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


    // TEST CODE:
    BLE.setEventHandler(BLEDiscovered, ); // if needed as central

    BLE.seteventHandler(BLEConnected, );
    BLE.setEventHandler(BLEDisconnected, );
    
    BLE.advertise(); // start advertising

//    Serial.println("Initialized.");
}

void loop() {

    BLE.poll();
}
//  // listen for Bluetooth® Low Energy peripherals to connect:
//  BLEDevice central = BLE.central();
//
//  // if a central is connected to peripheral:
//  if (central) {
//    // Serial.print("Connected to central: ");
//    // print the central's MAC address:
//    // Serial.println(central.address());
//
//    // while the central is still connected to peripheral:
//    while (central.connected()) {
//      // if the remote device wrote to the characteristic,
//      // use the value to control the LED:
//
//      for (int i = 0; i < N_CMDS; ++i) {
//         if (((allCommands[i]).ble).written()) {
//          
//            digitalWrite(LED_BUILTIN, HIGH); // turn on LED value for commmand being sent
////            char* n = (allCommands[i]).strname;
////            
////            // if TCW_linAct is called, find the TCW peripherals, and change its LED for test
////            if (n == "TCW_linAct") {
////
////                BLE.scanForName("TCW_3");
////                BLEDevice peripheral = BLE.available(); 
////                
//////                if (peripheral && peripheral.hasLocalName()) {
//////
//////                  if (peripheral.localName() == "TCW_3") {
////                    digitalWrite(LEDG, HIGH);  //blink to show invalid input
////                    delay(250);
////                    digitalWrite(LEDG, LOW);
////                    delay(250);
////                    digitalWrite(LEDG, HIGH); 
////                    delay(250);
////                    digitalWrite(LEDG, LOW);
////                     delay(250);
////                    digitalWrite(LEDG, HIGH);
////               //   } 
//////                } else {
//////                    digitalWrite(LEDR, LOW);
//////                    delay(250);
//////                    digitalWrite(LEDR, HIGH);
//////                    delay(250);
//////                    digitalWrite(LEDR, LOW); 
//////                    delay(250);
//////                    digitalWrite(LEDR, HIGH);
//////                }
//////
////                //BLE.stopScan(); 
////                  
////            } else {
//            
//            unsigned long x = ((allCommands[i]).ble).value();
//            unsigned long z = (x & 0b11110000) >> 4; 
//            x = (x & 0b00001111); 
//            int y = MOTOR_NEUTRAL; // Fix: if it's command for pressure, different default value
////            Serial.println(x, HEX);
//
//            // if value > 16, change motorArr to make sure motor of MSB turns on
//            if (z) {
//              for (int j = 0; j < N_ACT; ++j) {
//                if (z-1 == j) {
//                   (allCommands[i]).motors[j] = 1;
//                } else {
//                  (allCommands[i]).motors[j] = 0;
//                }
//              }
//            }
//
//               // otherwise read LSB as motor command
//            if (x >= 0 && x < 10) {
//              y = uSCommandValues[(int)x]; // Fix: if it's command for pressure, different value
//              //Serial.println(y);
//            } else {
//              //Serial.println("Invalid input");
//              digitalWrite(LED_BUILTIN, HIGH);  //blink to show invalid input
//              delay(250);
//              digitalWrite(LED_BUILTIN, LOW);
//              delay(250);
//              digitalWrite(LED_BUILTIN, HIGH); 
//              delay(250);
//              digitalWrite(LED_BUILTIN, LOW);
//               delay(250);
//              digitalWrite(LED_BUILTIN, HIGH); 
//              delay(250);
//              digitalWrite(LED_BUILTIN, LOW); 
//            }
//
//            if (y > neutralCMD_min && y < neutralCMD_max) {
//              digitalWrite(LEDR, HIGH);
//              digitalWrite(LEDG, HIGH);
//              digitalWrite(LEDB, LOW); 
//            } else if (y < neutralCMD_min) {
//              digitalWrite(LEDR, LOW);
//              digitalWrite(LEDG, HIGH);
//              digitalWrite(LEDB, HIGH);
//            } else if (y > neutralCMD_max){
//              digitalWrite(LEDR, HIGH);
//              digitalWrite(LEDG, LOW);
//              digitalWrite(LEDB, HIGH);
//            } else {
//              digitalWrite(LEDR, HIGH);
//              digitalWrite(LEDG, HIGH);
//              digitalWrite(LEDB, HIGH); 
//            }
//
//            for (int j = 0; j < N_ACT; ++j) {
//                if ((allCommands[i]).motors[j]) {
//                   motorArr[j].writeMicroseconds(y);
//                } else {
//                   motorArr[j].writeMicroseconds(MOTOR_NEUTRAL);
//                }
//            }
//
//         //}
//            delay(500);
//         }
//         digitalWrite(LED_BUILTIN, LOW); // turn off LED
//      }
//    }
//
//    // when the central disconnects, print it out:
//    // Serial.print(F("Disconnected from central: "));
//    // Serial.println(central.address());
//  }
//}
