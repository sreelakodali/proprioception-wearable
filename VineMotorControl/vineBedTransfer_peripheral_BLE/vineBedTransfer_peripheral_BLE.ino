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
# define N_CMDS 2

struct cmd
{
  char* strname;
  int*[] motors;
  BLEIntCharacteristic ble;
};

cmd initializeCmd(char* s, int m) {
  BLEIntCharacteristic bleCharacteristic("2A59", BLEWrite);
  BLEDescriptor des("2901", s);
  bleCharacteristic.addDescriptor(des);
  bleCharacteristic.writeValue(0);
  cmd c{s, m, bleCharacteristic};
  return c;
}

BLEService motorService("01D"); // Bluetooth® Low Energy, motorized device
cmd allCommands[N_CMDS] = {initializeCmd("cmd1", 0), initializeCmd("cmd2", 1)};
Servo motorArr[N_ACT];
const  int pins_CommandOUTArr[8] = {3, 5, 7, 9};

void setup() {

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
  }

  for (int i = 0; i < N_CMDS; ++i) {
      motorService.addCharacteristic(((allCommands[i]).ble)); // add the characteristic to the service
    }
    
    BLE.addService(motorService); // add service
    BLE.advertise(); // start advertising
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

//      for (int i = 0; i < N_CMDS; ++i) {
//         if ((cmdCharacteristics[i]).written()) {
//          int x = (cmdCharacteristics[i]).value();
//          int y = map(x, 0, 15, 1200, 1700);
//          motorArr[i].writeMicroseconds(y);
//          delay(500);
//         }
//      }
      
      if (((allCommands[0]).ble).written()) {
        int x = ((allCommands[0]).ble).value();
        switch (x) {
          case 01:
             //Serial.println("Backward");
              digitalWrite(LED_BUILTIN, HIGH);         // will turn the LED on
              delay(500);
              digitalWrite(LED_BUILTIN, LOW);
              delay(500);
              digitalWrite(LED_BUILTIN, HIGH);         // will turn the LED on
              motorArr[0].writeMicroseconds(1450);
              delay(500);
            break;
          case 02:
            //Serial.println("Forward");
            digitalWrite(LED_BUILTIN, HIGH);         // will turn the LED on
            motorArr[0].writeMicroseconds(1550);
            delay(500);
            break;
          case 0:
           // Serial.println(F("LED off"));
            digitalWrite(LED_BUILTIN, LOW);          // will turn the LED off
            motorArr[0].writeMicroseconds(1500);
            delay(500);
            break;
          default:
            //Serial.println(F("LED off"));
            digitalWrite(LED_BUILTIN, LOW);          // will turn the LED off
            motorArr[0].writeMicroseconds(1500);
            delay(500);
            break;
        }
      }

        if (((allCommands[1]).ble).written()) {
            int y = ((allCommands[1]).ble).value();
        switch (y) {
          case 01:
              digitalWrite(LEDR, LOW);
              digitalWrite(LEDG, HIGH);
              digitalWrite(LEDB, HIGH);
              motorArr[1].writeMicroseconds(1450);
              delay(500);
            break;
          case 02:
             digitalWrite(LEDR, HIGH);
             digitalWrite(LEDG, LOW);
             digitalWrite(LEDB, HIGH);
            motorArr[1].writeMicroseconds(1550);
            delay(500);
            break;
          case 0:
             digitalWrite(LEDR, HIGH);
             digitalWrite(LEDG, HIGH);
             digitalWrite(LEDB, LOW);
            motorArr[1].writeMicroseconds(1500);
            delay(500);
            break;
          default:
             digitalWrite(LEDR, HIGH);
             digitalWrite(LEDG, HIGH);
             digitalWrite(LEDB, HIGH);           
            //Serial.println(F("LED off"));
            digitalWrite(LED_BUILTIN, LOW);          // will turn the LED off
            motorArr[1].writeMicroseconds(1500);
            delay(500);
            break;
        }
      }
      
    }

    // when the central disconnects, print it out:
    // Serial.print(F("Disconnected from central: "));
    // Serial.println(central.address());
  }
}
