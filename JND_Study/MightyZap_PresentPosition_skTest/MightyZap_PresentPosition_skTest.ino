#include <MightyZap.h>
#define ID_NUM 2

//int ID_NUM = 0;
MightyZap m_zap(&Serial4, 12);

int Position;
int cPosition;
int cPosition2;
int Display =1;

void setup() {
  Serial.begin(9600);    
  m_zap.begin(32);  
  while (! Serial);  
  m_zap.GoalSpeed(1,50);
  m_zap.GoalSpeed(2,50);
  m_zap.ledOn(1,RED);
  m_zap.ledOn(2,GREEN);
  m_zap.GoalPosition(ID_NUM,0);
  m_zap.GoalPosition(2,0);
}
void loop() {  
  if(Display == 1){
    Serial.print("*New Position[0~4095] : ");
    Display = 0;
  }
  if(Serial.available())  {
    Position = Serial.parseInt();
//    if (Position > 4095) {
//      ID_NUM = 2;
//      Position = Position - 4095;
//    } else {
//      ID_NUM=1;
//    }
//    Serial.println(ID_NUM);
    Serial.read(); 
    Serial.println(Position);    
    //delay(200);

    m_zap.GoalPosition(ID_NUM,Position);
    m_zap.GoalPosition(2,Position);
    //delay(50);
//    while(m_zap.Moving(ID_NUM)) {
//      cPosition = m_zap.presentPosition(ID_NUM);
//      Serial.print("  - Position : ");
//      Serial.println(cPosition);
//    }
    delay(5000);   
    //delay(200);
    cPosition = m_zap.presentPosition(ID_NUM);
    cPosition2 = m_zap.presentPosition(2);
    Serial.print("  - final Position : ");
    Serial.print(cPosition);
    Serial.print(" ");
    Serial.println(cPosition2);
    Display = 1;
  }  
}
