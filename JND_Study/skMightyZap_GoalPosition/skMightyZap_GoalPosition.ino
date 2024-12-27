#include <MightyZap.h>
#define ID_NUM 1

const int loopTime = 250;
const int mightyZapWen_OUT = 12; // write enable output signal for buffer
MightyZap m_zap(&Serial5, mightyZapWen_OUT);
unsigned long td = millis();


void setup() {
  // Initialize the MightyZap bus:
  // Baudrate -> 128: 9600, 32: 57600, 16: 115200 
  Serial.begin(4608000); 
  m_zap.begin(32);
  m_zap.GoalPosition(ID_NUM, 100);
}

void loop() {
  unsigned long tLoop = millis();
  if ( (tLoop - td) >  loopTime) {
    int measuredPos = m_zap.presentPosition(ID_NUM);
    String dataString = String(tLoop) + ", " + String(measuredPos);
    Serial.println(dataString);
    td = millis();
  }
}
