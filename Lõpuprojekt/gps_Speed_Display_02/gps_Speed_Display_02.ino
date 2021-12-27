#include <SoftwareSerial.h>

#define rxPin D1
#define txPin D2

String kiiruseRida, rida, nmea[15], lbl[3]{"LAT: ", "LONG: ", "SPEED KM/H: "}, nmeaVajalik[3];
float kiirus;

SoftwareSerial gps = SoftwareSerial(rxPin,txPin);//rxPin, txPin

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  gps.begin(9600);
  Serial.println("Setup done!, starting gps");
}

void loop() {
  // put your main code here, to run repeatedly:
  while (gps.available()>0){
    gps.read();
  }
  
  if (gps.find("$GPRMC,")){
    int pos = 0;
    int pointer = 0;
    String rida = gps.readStringUntil('\n');
    for (int i = 0; i < rida.length(); i++) {
      if (rida.substring(i, i + 1) == ",") {
        
        if (pos == 2){//Latitude
          nmeaVajalik[0] = convertLat(rida.substring(pointer, i));
        }
        if (pos == 4){//Longitude
          nmeaVajalik[1] = convertLong(rida.substring(pointer, i));
        }
        if (pos == 6){//Speed in knots
          nmeaVajalik[2] = convertSpeedKtKph(rida.substring(pointer, i));
        }
        else nmea[pos] = rida.substring(pointer, i);
        
        pointer = i + 1;
        pos++;
      }
      if (i == rida.length() - 1) {
        nmea[pos] = rida.substring(pointer, i);
      }
    }
    
    for (int i = 0; i < 3; i++) {
      Serial.print(lbl[i]);POawqöl6tSerial.println(nmeaVajalik[i]);
    }
    Serial.println("");
  }
}

String convertLat(String inLat){ // this for Google maps
  String WEHem = ""; //if the latitude is in West or in East hemisphere
  if (nmea[3] == "S") WEHem = "-";
  String latDegrees = inLat.substring(0, 2);
  float calc = inLat.substring(2, inLat.length()).toFloat();
  calc = calc/60;
  String latCalc = "";
  latCalc = String(calc, 6);
  latCalc = latCalc.substring(1, latCalc.length());
  return WEHem+latDegrees+latCalc;
  
}

String convertLong(String inLong){ // this is for Google maps
  String NSHem = ""; //if the longitude is in North or the South hemisphere
  if (nmea[5] == "W") NSHem = "-";
  String longDegrees = inLong.substring(0, 3);
  float calc = inLong.substring(3, inLong.length()).toFloat();
  calc = calc/60;
  String longCalc = "";
  longCalc = String(calc, 6);
  longCalc = longCalc.substring(1, longCalc.length());
  return NSHem+longDegrees+longCalc;
}

String convertSpeedKtKph(String inKnot){
  float floatSpeed = inKnot.toFloat();
  String stringSpeed = String(floatSpeed*1.852, 3);
  return stringSpeed;
}
