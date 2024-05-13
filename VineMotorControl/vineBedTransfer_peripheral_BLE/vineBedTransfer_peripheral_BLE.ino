/*
  Based on example code, LED, in ArduinoBLE Examples

  Motor Control for Vine Bed Transfer
  Sreela Kodali kodali@stanford.edu

  This example creates a Bluetooth® Low Energy peripheral with services that contains a
  characteristic to control an LED.
*/

#include <ArduinoBLE.h>
#include <Servo.h>


# define N_ACT 2
# define N_CMDS 3

struct cmd
{
  char* strname;
  const int* motors;
  BLEIntCharacteristic ble;
};

cmd initializeCmd(char* s, const int* m) {
  BLEIntCharacteristic bleCharacteristic("2A59", BLEWrite);
  BLEDescriptor des("2901", s);
  bleCharacteristic.addDescriptor(des);
  bleCharacteristic.writeValue(0);
  cmd c{s, m, bleCharacteristic};
  return c;
}

BLEService motorService("01D"); // Bluetooth® Low Energy, motorized device
const int uSCommandValues[10] = {1500, 1300, 1375, 1400, 1425, 1500, 1575, 1600, 1625, 1700};

const int motors_CMD1[N_ACT] = {1, 0};
const int motors_CMD2[N_ACT] = {0, 1};
const int motors_CMD3[N_ACT] = {1, 1};
cmd allCommands[N_CMDS] = {initializeCmd("motor1", motors_CMD1), initializeCmd("motor2", motors_CMD2), initializeCmd("both", motors_CMD3)};
Servo motorArr[N_ACT];
const  int pins_CommandOUTArr[8] = {3, 5, 7, 9};

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
          
            int x = ((allCommands[i]).ble).value();
            int y = 1500;
            if (x >= 0 && x < 10) {
              y = uSCommandValues[x]; //map(x, 0, 9, 1200, 1800);
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
            } else if (y < 1425) {
              digitalWrite(LEDR, LOW);
              digitalWrite(LEDG, HIGH);
              digitalWrite(LEDB, HIGH);
            } else if (y > 1525){
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
