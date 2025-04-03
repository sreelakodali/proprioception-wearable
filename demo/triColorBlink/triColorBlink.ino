/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 */

#define LENGTH 3
#define td 500

int ledArr[LENGTH] = {13, 12, 11}; //14,
int transistorArr[LENGTH] = {11, 8, 2};
int transistor = 11;
int led = 14;
void setup() {
  // initialize the digital pin as an output.
//   pinMode(transistor, OUTPUT);
//   pinMode(led, OUTPUT);

  for (int i = 0; i < LENGTH; i ++ ) {
    pinMode(ledArr[i], OUTPUT);
    pinMode(transistorArr[i], OUTPUT);
  }
}

// the loop routine runs over and over again forever:
void loop() {
  for (int i = 0; i < LENGTH; i ++ ) {
    digitalWrite(ledArr[i], LOW);   // turn the LED on (HIGH is the voltage level)
    //digitalWrite(transistorArr[i], HIGH);
    delay(td);               // wait for a second
    
    digitalWrite(ledArr[i], HIGH);    // turn the LED off by making the voltage LOW
    //digitalWrite(transistorArr[i], LOW);
    delay(td);               // wait for a second
  }

//    digitalWrite(transistor, HIGH);   // turn the LED on (HIGH is the voltage level)
//    digitalWrite(led, LOW);
//    delay(td);               // wait for a second
//    
//    digitalWrite(transistor, LOW);    // turn the LED off by making the voltage LOW
//    digitalWrite(led, HIGH);
//    delay(td);               // wait for a second
}
