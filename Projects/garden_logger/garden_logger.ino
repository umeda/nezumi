/*
  garden datalogger v0.3

  This sketch logs one measurement per minute to an SD Card.

  It uses a HiLetGo data logger shield.

  Solar intensity is read from A0.
    CDS Photocell is connected between GND and A0.
    A 10K resistor is connected between A0 and +5
  
  For the DHT-22 temp/humidy sensor:
    Connect pin 1 (on the left) of the sensor to +5V
    NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
    to 3.3V instead of 5V!
    Connect pin 2 of the sensor to whatever your DHTPIN is
    Connect pin 4 (on the right) of the sensor to GROUND
    Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

  For DS18B20 temp sensors 

    These sensors have a 10K pull up, althogh the spec sheet says they need 4.7k.
    If need be,the internal pull-ups can be enabled.
    The sensors are connected to pins 3, 4, and 5.
    
  
  The SD card is attached to the SPI bus as follows:
     MOSI - pin 11
     MISO - pin 12
     CLK - pin 13
     CS - pin 10 (for HiLetGo data logger)
     
   Some code snippets from Adafruit Industries.
   Other code snipppets from http://www.pjrc.com/teensy/td_libs_OneWire.html
   Copyright 2020 Nezumi Workbench

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

#include <SPI.h>
#include <SD.h>
#include <OneWire.h>
#include "RTClib.h"
#include "DHT.h"

#define DHTPIN 2     
//#define DHTTYPE DHT11   // DHT 11
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)
const int chipSelect = 10;
int sensorPin = A0;    // input pin for voltage divider
int sensorValue = 0;  // variable to store the value coming from the sensor
int sm1 = A1;
int sm2 = A2;
int sm3 = A3;
float rm = 0.0;
int sampleMillis = 30000;
char buffer[20]; // datetime string
RTC_DS1307 rtc;
DHT dht(DHTPIN, DHTTYPE);
OneWire  ds1(3);  // on pin 3 (a 4.7K resistor is necessary)
OneWire  ds2(4);  // on pin 4 (a 4.7K resistor is necessary)
OneWire  ds3(5);  // on pin 5 (a 4.7K resistor is necessary)

String measurands = "time, light, air_temp, air_rh, temp_1, temp_2, temp_3, sm_1, sm_2, sm_3";

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  if (! rtc.begin()) {
    // Serial.println("Couldn't find RTC");
    // Serial.flush();
    sendData("msg", "Couldn't find RTC.");
    abort();
  }

  // Serial.print("Initializing SD card...");
  sendData("msg", "Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    // Serial.println("Card failed or not present.");
    sendData("msg", "Card failed or not present.");
    // don't do anything more:
    while (1);
  }
  // Serial.println("card initialized.");
  sendData("msg", "Card initialized.");
  saveData(measurands);
  
  
  dht.begin();
  
  
  
  // get the file names and increment
  

}

void loop() {
  // make a string for assembling the data to log:
//  Serial.println("top of the loop");
//  Serial.flush();
  String dataString = "";

  DateTime now = rtc.now();
  snprintf(buffer, sizeof(buffer), "%4d/%02d/%02dT%02d:%02d:%02d", now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());
  dataString += String(buffer);
  dataString += ", ";

  sensorValue = analogRead(sensorPin);
  rm = (float)sensorValue / (1024.0 - (float)sensorValue) * 10000.0;

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float t1 = getTemp(ds1);
  float t2 = getTemp(ds2);
  float t3 = getTemp(ds3);
  float m1 = analogRead(sm1);
  float m2 = analogRead(sm2);
  float m3 = analogRead(sm3);
  
  
  dataString += String(rm);
  dataString += ", ";
  dataString += String(t);
  dataString += ", ";
  dataString += String(h);
  dataString += ", ";
  dataString += String(t1);
  dataString += ", ";
  dataString += String(t2);
  dataString += ", ";
  dataString += String(t3);
  dataString += ", ";
  dataString += String(m1);
  dataString += ", ";
  dataString += String(m2);
  dataString += ", ";
  dataString += String(m3);

  saveData(dataString); 
  sendData("data, " + measurands, dataString);

//  delay(5000);
  delay(sampleMillis);
  delay(sampleMillis);
}

/*
#################################################################
#################################################################
#################################################################
*/

void saveData(String monitordata){
  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = SD.open("garden.csv", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(monitordata);
    dataFile.close();
  }
  // if the file isn't open, pop up an error:
  else {
    // Serial.println("error opening gardenlog.csv");
    sendData("msg", "error opening gardenlog.csv.");
    }
   }

void sendData(String message, String monitordata){
    // print to the serial port
    Serial.print(message);
    Serial.print(", ");
    Serial.print(monitordata);
    Serial.println("");
    Serial.flush();
    }

float getTemp(OneWire ds) {
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  float celsius, fahrenheit;
  
  if ( !ds.search(addr)) {
    //Serial.println("No more addresses.");
    //Serial.println();
    ds.reset_search();
    delay(250);
    return;
  }
  
  //Serial.print("ROM =");
  for( i = 0; i < 8; i++) {
    //Serial.write(' ');
    //Serial.print(addr[i], HEX);
  }

  if (OneWire::crc8(addr, 7) != addr[7]) {
      //Serial.println("CRC is not valid!");
      return;
  }
  //Serial.println();
 
  // the first ROM byte indicates which chip
  switch (addr[0]) {
    case 0x10:
      //Serial.println("  Chip = DS18S20");  // or old DS1820
      type_s = 1;
      break;
    case 0x28:
      //Serial.println("  Chip = DS18B20");
      type_s = 0;
      break;
    case 0x22:
      //Serial.println("  Chip = DS1822");
      type_s = 0;
      break;
    default:
      //Serial.println("Device is not a DS18x20 family device.");
      return;
  } 

  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1);        // start conversion, with parasite power on at the end
  
  delay(1000);     // maybe 750ms is enough, maybe not
  // we might do a ds.depower() here, but the reset will take care of it.
  
  present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);         // Read Scratchpad

  //Serial.print("  Data = ");
  //Serial.print(present, HEX);
  //Serial.print(" ");
  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds.read();
    //Serial.print(data[i], HEX);
    //Serial.print(" ");
  }
  //Serial.print(" CRC=");
  //Serial.print(OneWire::crc8(data, 8), HEX);
  //Serial.println();

  // Convert the data to actual temperature
  // because the result is a 16 bit signed integer, it should
  // be stored to an "int16_t" type, which is always 16 bits
  // even when compiled on a 32 bit processor.
  int16_t raw = (data[1] << 8) | data[0];
  if (type_s) {
    raw = raw << 3; // 9 bit resolution default
    if (data[7] == 0x10) {
      // "count remain" gives full 12 bit resolution
      raw = (raw & 0xFFF0) + 12 - data[6];
    }
  } else {
    byte cfg = (data[4] & 0x60);
    // at lower res, the low bits are undefined, so let's zero them
    if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
    else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
    else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    //// default is 12 bit resolution, 750 ms conversion time
  }
  celsius = (float)raw / 16.0;
  fahrenheit = celsius * 1.8 + 32.0;
  //Serial.print("  Temperature = ");
  //Serial.print(celsius);
  //Serial.print(" Celsius, ");
  //Serial.print(fahrenheit);
  //Serial.println(" Fahrenheit");
  return(celsius);
}
