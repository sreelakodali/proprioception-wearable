// Nick Cerone
// ceronj26@mit.edu
// 4.20.24
// Modified from Examples > ArduinoBLE > Central > LED


/* ***NOTE***

  Note 1:
This code is currently configured to run with the controller plugged into a computer, providing Serial output on the
Arduino Serial Monitor. It can be run by battery (reference the TCWCentral.fzz schematic), but the code may need a simple,
slight modification. If it does not work properly when running on battery, try commenting out every line that includes a Serial
command.


  Note 2:
This code is configured to access 4 (or fewer) winches at once. If you wanted to increasew the number of winches
this controller is able to access:

1) Change the value of numWinches
2) Append the digital pin connecting the switch that controls the new winch to array W
3) Append new default values to the switchStates and oldSwitchStates arrays
4) Append a new UUID for the new winch to the UUID array (I have set a convention of incrementing the last digit by 1, but this is just convention)

***NOTE*** */





#include <ArduinoBLE.h>

// define winch control switch pins
const int numWinches = 4;
const int W[numWinches] = { 5, 6, 7, 8 };       // digital pins controlling each winch
int switchStates[numWinches] = { 1, 1, 1, 1 };  // default to all switches being open -- in reality set these in setup.
int oldSwitchStates[numWinches] = { 1, 1, 1, 1 };

// UUIDs (by convention, the same UUID with the final digit changed. Each of these UUIDs is given to a single peripheral, as explained in TCWPeripheral.ino)
const String UUID[numWinches] = { "19B10000-E8F2-537E-4F6C-D104768A1210", "19b10000-e8f2-537e-4f6c-d104768a1211", "19b10000-e8f2-537e-4f6c-d104768a1212", "19b10000-e8f2-537e-4f6c-d104768a1213" };

// define LED pins
const int onLedPin = 2;    // LED indicator: setup is complete (ble is advertising)
const int bleLedPin = 3;   // LED indicator: nano is connected to a peripheral
const int failLedPin = 4;  // LED indicator: ble has failed





// =============== SETUP  ===============

void setup() {
  // Serial.begin(9600);

  // set led pins to output mode
  pinMode(onLedPin, OUTPUT);
  pinMode(bleLedPin, OUTPUT);
  pinMode(failLedPin, OUTPUT);

  // set switch pins to input pullup
  for (int i = 0; i < numWinches; i++) {
    pinMode(W[i], INPUT_PULLUP);
  }

  // begin initialization
  if (!BLE.begin()) {
    digitalWrite(failLedPin, HIGH);  // if ble fails, indicate
    while (1);  // halt evertything. reset
  }

  // if initialization completes, indicate
  digitalWrite(onLedPin, HIGH);
}

// =============== SETUP  ===============





// =============== LOOP  ===============

void loop() {

  // iterate through all the winches and check if any of the current winch states does not match the old switch states
  for (int i = 0; i < numWinches; i++) {
    switchStates[i] = digitalRead(W[i]);

    // check if the switch state changed. if so, connect to that peripheral and update
    if (switchStates[i] != oldSwitchStates[i]) {
      // Serial.print("Switch state ");
      // Serial.print(i);
      // Serial.println(" changed. Updating winch:");
      BLE.scanForUuid(UUID[i]);

      // search for a peripheral with the UUID specified in BLE.scanForUUID
      BLEDevice peripheral = BLE.available();
      while (!peripheral) {  // keep searching until the controller accesses the peripheral
        peripheral = BLE.available();
      }

      // if we find the intended periphral
      if (peripheral) {

        // stop scanning
        BLE.stopScan();

        // indicate that we are connected to BLE
        digitalWrite(bleLedPin, HIGH);

        // send the command to write to the peripheral
        controlWinch(peripheral, i);

        // indicate that we are disconnected from ble
        digitalWrite(bleLedPin, LOW);
      }  // end if(peripheral)

    }  // end if(switchStates[i] != oldSwitchStates[i])

  }  // end for(int i = 0; i < numWinches; i++)

}  // end loop()

// =============== LOOP  ===============





// =============== controlWinch  ===============

/*
Connects and writes to the peripheral to control the actuator

Parameters:
    BLEDevice peripheral -- the peripheral object to which the controller connects
    int i -- the index of the winch
Return: void
*/

void controlWinch(BLEDevice peripheral, int i) {
  // connect to the peripheral
  // Serial.println("Connecting ...");

  // if there is an error in connecting, terminate
  if (!peripheral.connect()) {
    return;
  }

  // discover peripheral attributes
  if (!peripheral.discoverAttributes()) {
    // Serial.println("Attribute discovery failed!");
    peripheral.disconnect();
    return;
  }

  // retrieve the LED characteristic
  BLECharacteristic ledCharacteristic = peripheral.characteristic("19b10001-e8f2-537e-4f6c-d104768a1214");  // this value is constant for all winches

  // if the peripheral does not have an ledCharaacteristic, or if we cannot write to that ledCharacteristic, terminate
  if (!ledCharacteristic) {
    // Serial.println("Peripheral does not have LED characteristic!");
    peripheral.disconnect();
    return;
  } else if (!ledCharacteristic.canWrite()) {
    // Serial.println("Peripheral does not have a writable LED characteristic!");
    peripheral.disconnect();
    return;
  }


  // if everything above passes, then we are properly connected to a perpiperal to which we can write.
  while (peripheral.connected()) {

    oldSwitchStates[i] = switchStates[i];

    // check is the switch is closed or opwn
    if (switchStates[i]) {  // switch open
      // Serial.println("button pressed");

      // switch is open, write 0x0F to extend the actuator
      ledCharacteristic.writeValue((byte)0x0F);
    } else {  // switch closed
      // Serial.println("button released");

      // switch is closed, write 0x0B to retract the actuator
      ledCharacteristic.writeValue((byte)0x0B);
    }

    // Since we have written, disconnect
    peripheral.disconnect();
  }

  // Serial.println("Peripheral disconnected");
}

// =============== controlWinch  ===============
