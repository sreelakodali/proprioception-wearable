/*
 * test MightyZap with another library
 * Written by Sreela Kodali (kodali@stanford.edu) 
 * 
 * */
#include <MightyZap.h>
#include <dummy.h>
#define ID_NUM 2

dummy device;
MightyZap* m = device.m_zap;

//MightyZap* m; // uncomment if just MightyZap object alone


void setup() {

//    MightyZap m_zapObj(&Serial4, 12); // uncomment if just MightyZap object alone
//    m = &m_zapObj; // uncomment if just MightyZap object alone
//    (*m).begin(32); // uncomment if just MightyZap object alone
    
//    Serial.println(int(&device), HEX);
//    Serial.println(int(m), HEX);

    // bring device to 0 position
    Serial.println("Device initialized.");
    (*m).GoalPosition(ID_NUM,0);

    if (CrashReport) {
    /* print info (hope Serial Monitor windows is open) */
    Serial.print(CrashReport);
  }

    //Serial.println(sizeof(device));
    //Serial.println(sizeof(*m));

    // print information
    Serial.print("Model Number        : ");
    Serial.println((unsigned int)(*m).getModelNumber(ID_NUM));
      Serial.print("Firmware Version    : ");
      Serial.println((*m).Version(ID_NUM)*0.1);           
      Serial.print("Present Temperature : ");
      Serial.println((*m).presentTemperature(ID_NUM));
    delay(2000);

    (*m).GoalPosition(ID_NUM,500);
    delay(2000);
    
    int cPosition = (*m).presentPosition(2);
    Serial.print("Present position = ");
    Serial.println(cPosition);
    delay(2000);

   (*m).GoalPosition(ID_NUM,0);
   delay(2000);
   cPosition = (*m).presentPosition(2);
    Serial.print("Present position = ");
   Serial.println(cPosition);
}

void loop() {

}