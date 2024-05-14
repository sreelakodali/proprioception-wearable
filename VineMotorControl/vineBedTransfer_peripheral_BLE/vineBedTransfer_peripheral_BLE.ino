/*
  Based on example code, LED, in ArduinoBLE Examples

  Motor Control for Vine Bed Transfer
  Sreela Kodali kodali@stanford.edu

  This example creates a Bluetooth® Low Energy peripheral with services that contains a
  characteristic to control an LED.
*/

#include <ArduinoBLE.h>
#include <Servo.h>


# define N_ACT 8
# define N_CMDS 4

struct cmd
{
  char* strname;
  int* motors;
  BLEIntCharacteristic ble;
};

cmd initializeCmd(char* s, int* m) {
  BLEIntCharacteristic bleCharacteristic("2A59", BLEWrite);
  BLEDescriptor des("2901", s);
  bleCharacteristic.addDescriptor(des);
  bleCharacteristic.writeValue(0);
  cmd c{s, m, bleCharacteristic};
  return c;
}

BLEService motorService("01D"); // Bluetooth® Low Energy, motorized device
const int uSCommandValues[10] = {1500, 1300, 1375, 1400, 1425, 1500, 1575, 1600, 1625, 1700};

// which motors will be on for each command
// FIX or something to think about later: motors might be on, but base/tcw might have opposite directions and different speeds
// maybe combine some of the commands, like instead of base* and tcw*, perhaps individual motors

int motors_CMD1[N_ACT] = {1, 1, 1, 1, 0, 0, 0, 0};
int motors_CMD2[N_ACT] = {0, 0, 0, 0, 1, 1, 1, 1};
int motors_CMD3[N_ACT] = {1, 1, 1, 1, 1, 1, 1, 1};
int motors_CMD4[N_ACT] = {0, 0, 0, 0, 0, 0, 0, 0};

cmd allCommands[N_CMDS] = {initializeCmd("ALLBase", motors_CMD1), initializeCmd("ALLTCW", motors_CMD2), initializeCmd("ALL", motors_CMD3), 
                           initializeCmd("individualMotor", motors_CMD4)};

Servo motorArr[N_ACT];
const  int pins_CommandOUTArr[N_ACT] = {2, 3, 4, 5, 6, 7, 8, 9};

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
     motorArr[i].writeMicroseconds(1500);
  }

  for (int i = 0; i < N_CMDS; ++i) {
      motorService.addCharacteristic(((allCommands[i]).ble)); // add the characteristic to the service
  }
    
    BLE.addService(motorService); // add service
    BLE.advertise(); // start advertising

    //Serial.println("Initialized.");
}

void loop() {
    
  // listen for Bluetooth® Low Energy peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    // Serial.print("Connected to central: ");
    // print the central's MAC address:
    // Serial.println(central.address());

    // while the central is still connected to peripheral:
    while (central.connected()) {
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:

      for (int i = 0; i < N_CMDS; ++i) {
         if (((allCommands[i]).ble).written()) {
          
            digitalWrite(LED_BUILTIN, HIGH); // turn on LED value for commmand being sent
          
            unsigned long x = ((allCommands[i]).ble).value();
            unsigned long z = (x & 0b11110000) >> 4; 
            x = (x & 0b00001111); 
            int y = 1500;
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
              y = uSCommandValues[(int)x]; //map(x, 0, 9, 1200, 1800);
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

            if (y > 1425 && y < 1525) {
              digitalWrite(LEDR, HIGH);
              digitalWrite(LEDG, HIGH);
              digitalWrite(LEDB, LOW); 
            } else if (y <= 1425) {
              digitalWrite(LEDR, LOW);
              digitalWrite(LEDG, HIGH);
              digitalWrite(LEDB, HIGH);
            } else if (y >= 1525){
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
                   motorArr[j].writeMicroseconds(1500);
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
