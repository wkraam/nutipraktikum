int potPin = A1;
int value;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(potPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  value = analogRead(potPin);
  Serial.println(value);
  delay(200);
}
