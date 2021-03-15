char dataString[50] = {0};
int led = 2;
int incommingByte = 0;
int blinkStatus = 0;
int ledStatus = 0;
void setup() {                
  Serial.begin(9600);    
  pinMode(led, OUTPUT);
  Serial.println("Ready!");
}


void loop() {
  
  if(Serial.available()>0){
    incommingByte = Serial.parseInt();
    if (incommingByte == 1) {
      ledStatus = 1;
      Serial.println("Turned the LED on");
    } else if(incommingByte == 0){
      ledStatus = 0;
      Serial.println("Turned the LED off");
    } else if(incommingByte == 2){
      Serial.print("Led is currently ");
      if (ledStatus == 0){
        Serial.println("off");
      } else if (ledStatus == 1) {
        Serial.println("on");
      }
    }
  }
  digitalWrite(led, ledStatus);
  delay(100);
}
