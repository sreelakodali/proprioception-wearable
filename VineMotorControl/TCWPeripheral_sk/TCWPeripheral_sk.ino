// Nick Cerone
// ceronj26@mit.edu
// 4.20.24
// Modified from Examples > ArduinoBLE > Peripheral > LED (public domain)
// Edited by Sreela Kodali, 5/19/24, kodali@stanford.edu

/* ***NOTE***

  Each independent winch needs a different UUID so that the controller can distinguish them.
  This can be changed in the line:

  BLEService ledService("[INSERT UUID HERE]");

  By default, I have set the controller to interpret UUIDs beginning with "19B10000-E8F2-537E-4F6C-D104768A120",
  and incrementing the last digit by 1 for each new winch (i.e. winch 0 has UUID "19B10000-E8F2-537E-4F6C-D104768A120",
  winch 1 has UUID "19B10000-E8F2-537E-4F6C-D104768A121"). Therefore, for every new winch to which this code gets uploaded,
  ensure that you increment this one digit so as to give the new winch an independend ID. The BLEByteCharacteristic line
  (the next line under that) stays the same.


  Additionally (but not necessary for the controller) you would like to control the winches via a Bluetooth scanner (I use
  the BLE scanner on my iPhone), you can more easily distinguish the winches by changing their local name in the setup
  under the line BLE.setLocalName("TCW_0");. Again, this is not really necessary unless you would like to distinguish them
  in some format where you see thier local name.

***NOTE*** */





#include <ArduinoBLE.h>                               // v Change this last digit depending on what index winch the code gets posted to
BLEService ledService("19B10000-E8F2-537E-4F6C-D104768eA120");  // Bluetooth® Low Energy LED Service
BLEByteCharacteristic switchCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLEWrite); // This should be the same for all winches (do not modify)

# define onLedPin LEDB // Edit: onboard wiring issue. weirdly LEDB is name of green led and LEDG is name of blue led!
# define bleLedPin LEDG
# define actLedPin LED_BUILTIN
# define failLedPin LEDR

// define analog pins to send PWM to motor controller
const int pwm0Pin = A1;         // IN1
const int pwm1Pin = A0;         // IN2
const int in[2] = { 255, 0 };   // retracted PWMs
const int out[2] = { 0, 255 };  // Extended PWMs
const int neutral[2] = {0, 0};  // Edited: coast
const int t_d = 12000; // Edited: x seconds after sending motor command before returning it to neutral state, drawing no current
const char devicename[10] = "TCW_3";


// =============== SETUP  ===============

void setup() {

  // set all pins to output mode
  pinMode(onLedPin, OUTPUT);
  pinMode(bleLedPin, OUTPUT);
  pinMode(actLedPin, OUTPUT);
  pinMode(failLedPin, OUTPUT);
  pinMode(pwm0Pin, OUTPUT);
  pinMode(pwm1Pin, OUTPUT);


  // === BLE SETUP (mostly based on the LedControl example) ===
  // begin initialization
  if (!BLE.begin()) {
    digitalWrite(failLedPin, LOW);  // if ble fails, indicate
    while (1); // stop evertything
  } else {
     digitalWrite(failLedPin, HIGH);
     digitalWrite(bleLedPin, HIGH);
     digitalWrite(onLedPin, HIGH);
     digitalWrite(actLedPin, LOW);
  }

  // set advertised local name and service UUID:
  BLE.setLocalName(devicename);
  BLE.setAdvertisedService(ledService);

  // add the characteristic to the service
  ledService.addCharacteristic(switchCharacteristic);

  // add service
  BLE.addService(ledService);

  // set the initial value for the characeristic:
  switchCharacteristic.writeValue(0x0F); // 0x0F is "forwards" on the actuator

  // start advertising
  BLE.advertise();
  // ======


  // set default motor value to extend
  analogWrite(pwm0Pin, out[0]);
  analogWrite(pwm1Pin, out[1]);
  digitalWrite(actLedPin, HIGH);

  // setup complete. indicate that the bluetooth connection is being advertised
  digitalWrite(onLedPin, LOW);


}  // end setup()

// =============== SETUP  ===============





// =============== LOOP  ===============

void loop() {
  digitalWrite(bleLedPin, HIGH); // Always default that we're not connected to BLE

  // listen for Bluetooth® Low Energy peripherals to connect:
  BLEDevice central = BLE.central();

  // if the controller accesses this peripheral
  if (central) {
    digitalWrite(bleLedPin, LOW); // indicate

    // while the central is still connected to peripheral:
    while (central.connected()) {

      // if the remote device wrote to the characteristic, use the value to control the LED:
      if (switchCharacteristic.written()) {
        int input = switchCharacteristic.value();     // the value written by central

        if (input == 0x0F || input == 0xFF) {         // forwards (this 0x0F and 0x0B convention was devised while we were still using the BLE scanner app)
          digitalWrite(actLedPin, HIGH);              // will turn the LED on to indicate
          analogWrite(pwm0Pin, out[0]);
          analogWrite(pwm1Pin, out[1]);               // will drive actuator forwards (outwards)

          //Edited: After waiting x amount of time for actuators to drive forward, h-bridge set to coast/neutral
          delay(t_d);
          analogWrite(pwm0Pin, neutral[0]);
          analogWrite(pwm1Pin, neutral[1]);        
        } else if (input == 0x0B || input == 0xBB) {  // backwards
          digitalWrite(actLedPin, LOW);               // will turn the LED off
          analogWrite(pwm0Pin, in[0]);
          analogWrite(pwm1Pin, in[1]);                // will drive actuator backwards (inwards)

          //Edited: After waiting x amount of time for actuators to drive forward, h-bridge set to coast/neutral
          delay(t_d);
          analogWrite(pwm0Pin, neutral[0]);
          analogWrite(pwm1Pin, neutral[1]);          // h-bridge is in coast, neutral 

          // Edited: input of 0 will result in neutral/coast for linear acutator, no current being drawn
        } else if (input == 0x00 || input == 0x0) {
          digitalWrite(actLedPin, LOW);               // will turn the LED off
          analogWrite(pwm0Pin, neutral[0]);
          analogWrite(pwm1Pin, neutral[1]);          // h-bridge is in coast, neutral

          // Edited: default, any other input sent will result in neutral/coast for linear acutator, no current being drawn
        } else {
          digitalWrite(actLedPin, LOW);               // will turn the LED off
          analogWrite(pwm0Pin, neutral[0]);
          analogWrite(pwm1Pin, neutral[1]);          // h-bridge is in coast, neutral
        }
      }

    }  // end while (central.connected())

  } // end if (central)

}  // end loop()

// =============== LOOP  ===============
