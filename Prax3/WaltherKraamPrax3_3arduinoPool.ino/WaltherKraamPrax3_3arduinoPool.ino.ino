// https://arduinogetstarted.com/tutorials/arduino-temperature-sensor

#include <OneWire.h>
#include <DallasTemperature.h>

float temp = 0;
const int tempPin = 5;

OneWire oneWire(tempPin);
DallasTemperature sensors(&oneWire);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  sensors.begin();
  //pinMode(A7, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  sensors.requestTemperatures();
  temp = sensors.getTempCByIndex(0);
  Serial.println(temp);
  delay(200);
}
