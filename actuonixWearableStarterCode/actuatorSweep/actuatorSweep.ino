/*
 * Actuonix Actuator
 * 
 * */
#include <math.h>
#include <Servo.h>
#include <Wire.h>
#include "LSM6DS3.h"

# define N_ACT 2
# define T_SAMPLING 100 // milliseconds

typedef enum {
  POSITION_MIN = 47, // 900us mightyZap
  POSITION_MAX = 139 // 2100us mightyZap
} ACTUATOR_LIMITS;


void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
