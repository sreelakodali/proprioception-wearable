/*
 * Firmware Code for Proprioception Wearable Device
 * Using DeepPressureWearable library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */
#include <MightyZap.h>
//#include <DeepPressureWearableArr.h>
#include <dummy.h>

// create and initialize instance of DeepPressureWearable(INPUT_TYPE input, bool serial, bool c)

//const INPUT_TYPE in =  NO_INPUT; // NO_INPUT, FLEX_INPUT, KEYBOARD_INPUT
//const bool serialON = true; // and has serial output
//const int calibrateOn = false;
//int cPosition =0;
//DeepPressureWearableArr device(in, serialON, calibrateOn);

//
dummy device;
MightyZap* m = device.m_zap;


//MightyZap* m;


void setup() {
//    MightyZap m_zapObj(&Serial4, 12);
//    m = &m_zapObj;
//    (*m).begin(32);
//    
//    Serial.println(int(&device), HEX);
//    Serial.println(int(m), HEX);
    Serial.println("Device initialized.");
    (*m).GoalPosition(2,0);
    if (CrashReport) {
    /* print info (hope Serial Monitor windows is open) */
    Serial.print(CrashReport);
  }
    //device.beginTimer();

    //Serial.println(sizeof(device));
//    Serial.println(sizeof(*m));

Serial.print("Model Number        : ");
Serial.println((unsigned int)(*m).getModelNumber(2));
      Serial.print("Firmware Version    : ");
      Serial.println((*m).Version(2)*0.1);           
      Serial.print("Present Temperature : ");
      Serial.println((*m).presentTemperature(2));


//    Serial.println((*m).getResult());
//    (*m).GoalPosition(2,0);
//    Serial.println((*m).getResult());
//    delay(2000);
//    (*m).GoalPosition(2,500);
//    Serial.println((*m).getResult());
//    delay(2000);
//    
//    int cPosition = (*m).presentPosition(2);
//    Serial.println((*m).getResult());
//    Serial.print("Present position = ");
//   Serial.println(cPosition);
//   delay(2000);
//
//   (*m).GoalPosition(2,0);
//   Serial.println((*m).getResult());
//   delay(2000);
//   cPosition = (*m).presentPosition(2);
//   Serial.println((*m).getResult());
//    Serial.print("Present position = ");
//   Serial.println(cPosition);
    Serial.println("fin");
}

void loop() {
   //cPosition = (*m).presentPosition(2);
//   Serial.println(cPosition);
//    delay(2000);
  // pressing button can turn feedback on and off
  //device.directActuatorControl(2);
  //device.sweep(2000, 0);
}
