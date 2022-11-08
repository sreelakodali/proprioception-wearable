/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/
#define a01_const 988
#define a2_const 986
#define a3_const 984
#define a4_const 821
#define a5_const 820
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue0 = analogRead(A0);
  int sensorValue1 = analogRead(A1);
  int sensorValue2 = analogRead(A2);
  int sensorValue3 = analogRead(A3);
  int sensorValue4 = analogRead(A4);
  int sensorValue5 = analogRead(A5);
  
//  float voltage0= (a01_const-sensorValue0) * (5.0 / 1023.0);
//  float voltage1= (a01_const-sensorValue1) * (5.0 / 1023.0);
//  float voltage2= (a2_const-sensorValue2) * (5.0 / 1023.0);
//  float voltage3= (a3_const-sensorValue3) * (5.0 / 1023.0);
//  float voltage4= (a4_const-sensorValue4) * (5.0 / 1023.0);
//  float voltage5= (a5_const-sensorValue5) * (5.0 / 1023.0);

  float voltage0= (sensorValue0) * (5.0 / 1023.0);
  float voltage1= (sensorValue1) * (5.0 / 1023.0);
  float voltage2= (sensorValue2) * (5.0 / 1023.0);
  float voltage3= (sensorValue3) * (5.0 / 1023.0);
  float voltage4= (sensorValue4) * (5.0 / 1023.0);
  float voltage5= (sensorValue5) * (5.0 / 1023.0);
  // print out the value you read:
//  Serial.print("A0 = ");
//  Serial.print(sensorValue0);
//  Serial.print("\t");
//  Serial.print("A1 = ");
//  Serial.print(sensorValue1);
//  Serial.print("\t");
//  Serial.print("A2 = ");
//  Serial.print(sensorValue2);
//  Serial.print("\t");
//  Serial.print("A3 = ");
//  Serial.print(sensorValue3);
//  Serial.print("\t");
//  Serial.print("A4 = ");
//  Serial.print(sensorValue4);
//  Serial.print("\t");
//  Serial.print("A5 = ");
//  Serial.println(sensorValue5);


  Serial.print("A0 = ");
  Serial.print(voltage0);
  Serial.print("\t");
  Serial.print("A1 = ");
  Serial.print(voltage1);
  Serial.print("\t");
  Serial.print("A2 = ");
  Serial.print(voltage2);
  Serial.print("\t");
  Serial.print("A3 = ");
  Serial.print(voltage3);
  Serial.print("\t");
  Serial.print("A4 = ");
  Serial.print(voltage4);
  Serial.print("\t");
  Serial.print("A5 = ");
  Serial.println(voltage5);
  delay(1);        // delay in between reads for stability
}
