#include <Servo.h>

Servo myservo;

void setup() {
  Serial.begin(9600); 
  myservo.attach(9); 
  delay(1000);
}

void loop() {
  myservo.write(0);
  delay(1000);
  myservo.write(90);
  delay(1000);
  myservo.write(88);
  delay(1000);
}
