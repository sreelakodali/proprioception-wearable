#include <MightyZap.h>
#define ID_NUM 1

MightyZap m_zap(&Serial1, 2);
int pos = 1024;
int t_d = 3000;

void setup() {
  // Initialize the MightyZap bus:
  // Baudrate -> 128: 9600, 32: 57600, 16: 115200 
  m_zap.begin(32);
  pinMode(13, OUTPUT);
}

void loop() {
  m_zap.ledOn(1,RED);
  m_zap.ledOn(2,GREEN);
  m_zap.GoalPosition(ID_NUM, 0); //ID 0 MightZap moves to position 0
  digitalWrite(13, LOW);
  Serial.println("0");
  delay(t_d);
  m_zap.GoalPosition(ID_NUM, pos);//ID 0 MightZap moves to position 4095
  digitalWrite(13, HIGH);
  Serial.println(pos);
  delay(t_d);
}
