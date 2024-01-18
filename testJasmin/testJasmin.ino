void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  int w;
  
  if (Serial.available() > 0) {
    w = (Serial.read() - '0');

    //Serial.println("received!");
    Serial.println(w);
    
   // w = (Serial.read() - '0');
  }

}
