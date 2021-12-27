#include <SoftwareSerial.h>

#define rxPin D1
#define txPin D2

SoftwareSerial gps = SoftwareSerial(rxPin,txPin);//rxPin, txPin

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  pinMode(rxPin, INPUT);
//  pinMode(txPin, OUTPUT);
  gps.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (gps.available()>0){
    gps.read();
    Serial.println("$"+gps.readStringUntil('\n'));
  }
}
