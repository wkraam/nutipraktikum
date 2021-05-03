#include <SoftwareSerial.h>

SoftwareSerial bt(3,2); //rx,tx

void setup() {
  Serial.begin(9600);
  Serial.println("Serial initialized");
  bt.begin(9600);
  Serial.println("bt module initialized");

}

void loop() {

  if(bt.available()){
    Serial.write(bt.read());
  }
  if(Serial.available()){
    bt.write(Serial.read());
  }
  
}
