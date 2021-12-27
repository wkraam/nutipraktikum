#include <SoftwareSerial.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <ESP8266WiFi.h>

WiFiServer server(80);

String refreshPage = R"=====(
<head>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'/>
  <meta charset='utf-8'>
  <style>
    body {font-size:100%;} 
    #main {display: table; margin: auto;  padding: 0 10px 0 10px; } 
    h2 {text-align:center; } 
    p { text-align:center; }
  </style>
  <script>
   function refresh(refreshPeriod) 
   {
      setTimeout("location.reload(true);", refreshPeriod);
   } 
   window.onload = refresh(5000);
  </script>
  <title>GPS speed indicator</title>
 </head>
)=====";

// Set WiFi credentials
#define ssid "WaltheriTelefon"
#define password "waltherKr"
LiquidCrystal_I2C lcd(0x27, 16, 2);

#define rxPin D3
#define txPin D4

String kiiruseRida, rida, nmea[15], lbl[3]{"LAT: ", "LONG: ", "SPEED KM/H: "}, nmeaVajalik[3], latitudes[100], longitudes[100];
float kiirus;
int arrayPointer = 0;

SoftwareSerial gps = SoftwareSerial(rxPin,txPin);//rxPin, txPin

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print(F("Connecting to "));
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }
  Serial.println();
  Serial.println(F("WiFi connected"));

  // Start the server
  server.begin();
  Serial.println(F("Server started"));

  // Print the IP address
  Serial.println(WiFi.localIP());
  
  gps.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("speed: ");
  lcd.setCursor(12,0);
  lcd.print("KM/H");
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
      Serial.print(lbl[i]);
      Serial.println(nmeaVajalik[i]);
    }
    Serial.println("Array pointer: " + String(arrayPointer));

    if(arrayPointer != 100){
      if (nmeaVajalik[0].indexOf(".000000") > -1){
        Serial.println("fix not found");
        lcd.setCursor(0,1);
        lcd.print("fix unavailable");
      }
      else if (arrayPointer == 0){
        latitudes[0] = nmeaVajalik[0];
        longitudes[0] = nmeaVajalik[1];
        arrayPointer++;
        Serial.println("first pos");
        lcd.setCursor(0,1);
        lcd.print("fix available  ");
      }
      
      else if (significantChange(nmeaVajalik[0], latitudes[arrayPointer-1]) || significantChange(nmeaVajalik[1], longitudes[arrayPointer-1])){
        latitudes[arrayPointer] = nmeaVajalik[0];
        longitudes[arrayPointer] = nmeaVajalik[1];
        arrayPointer++;
        Serial.println("new pos");
        lcd.setCursor(0,1);
        lcd.print("fix available  ");
      }
    }
    else {
      lcd.setCursor(0,1);
      lcd.print("loc array full");
      Serial.println("latitude and longitude arrays full, not recording location!");
    }
  }
  lcd.setCursor(6,0);
  lcd.print(nmeaVajalik[2]);
  Serial.println("");

  //------ wifi part -------
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  Serial.println(F("new client"));

  client.setTimeout(5000); // default is 1000

  // Read the first line of the request
  String req = client.readStringUntil('\r');
  Serial.println(F("request: "));
  Serial.println(req);

  // Match the request
  int val;
  if (req.indexOf(F("/gpio/0")) != -1) {
    val = 0;
  } else if (req.indexOf(F("/gpio/1")) != -1) {
    val = 1;
  } else {
    Serial.println(F("invalid request"));
    
  }
  

  // read/ignore the rest of the request
  // do not client.flush(): it is for output only, see below
  while (client.available()) {
    // byte by byte is not very efficient
    client.read();
  }

  // Send the response to the client
  // it is OK for multiple small client.print/write,
  // because nagle algorithm will group them into one single packet
  client.print(F("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>\r\n"));
  client.print(refreshPage);
  client.print(F("Kiirus on: "));
  client.print(nmeaVajalik[2]);
  client.print(F("<br><br>Array pointer: "));
  client.print(arrayPointer);
  client.print(F("<br><br>Click <a href='https://www.google.com/maps/search/"));
  client.print(nmeaVajalik[0]);
  client.print(F(","));
  client.print(nmeaVajalik[1]);
  client.print(F("' target='_blank'>here</a> to show current location."));
  client.print(F("<br>Click<a href='https://www.google.com/maps/dir/"));
  client.print(directions(arrayPointer, latitudes, longitudes));
  client.print(F("' target='_blank'>here</a> to get the traveled distance.</html>"));

  // The client will actually be *flushed* then disconnected
  // when the function returns and 'client' object is destroyed (out-of-scope)
  // flush = ensure written data are received by the other side
  Serial.println(F("Disconnecting from client"));
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

boolean significantChange(String coord1, String coord2){
  float change;//variable to hold the change of coordinates
  float Fcoord1 = coord1.toFloat();//cast first coordiante to float
  float Fcoord2 = coord2.toFloat();//cast seccond coordinate to float
  change = abs(Fcoord1 - Fcoord2);
  if (change > 0.0001A21  00) return true;
  else return false;
}

String getKiirus(){
  return nmeaVajalik[2];
}

String directions(int arrayPointer, String latitudes[100], String longitudes[100]){
  String lõppString="";
  for(int i=0; i<=arrayPointer-1; i++){
    lõppString+=latitudes[i];
    lõppString+=",";
    lõppString+=longitudes[i];
    if (i!=(arrayPointer-1)) lõppString+="/";
  }
  return lõppString;
}
