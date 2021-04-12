
// include the library code:
#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
SoftwareSerial bt(2, 3); //rx, tx

void setup() {
  Serial.begin(9600);
  bt.begin(9600);

  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("hello, world!");
}

void loop() {
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(0, 1);
  // print the number of seconds since reset:
  lcd.print(millis() / 1000);
  if(bt.available()){
    Serial.write(bt.read());
  }
  if(Serial.available()){
    bt.write(Serial.read());
  }
}
