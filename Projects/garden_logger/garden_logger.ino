/*
  garden datalogger v0.1

  This sketch logs one measurement per minute to an SD Card.

  It uses a HiLetGo data logger shield.

  Solar intensity is read from A0.
  CDS Photocell is connected between GND and A0.
  A 10K resistor is connected between A0 and +5
  
  The SD card is attached to the SPI bus as follows:
     ** MOSI - pin 11
     ** MISO - pin 12
     ** CLK - pin 13
     ** CS - pin 10 (for HiLetGo data logger)

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
#include "RTClib.h"

const int chipSelect = 10;
int sensorPin = A0;    // input pin for voltage divider
int sensorValue = 0;  // variable to store the value coming from the sensor
float rm = 0.0;
int sampleMillis = 30000;
char buffer[20]; // datetime string
RTC_DS1307 rtc;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    abort();
  }

  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");

  // get the file names and incriment

}

void loop() {
  // make a string for assembling the data to log:
  String dataString = "";

  DateTime now = rtc.now();
  snprintf(buffer, sizeof(buffer), "%4d/%02d/%02dT%02d:%02d:%02d", now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());
  dataString += String(buffer);
  dataString += ", ";

  sensorValue = analogRead(sensorPin);
  rm = (float)sensorValue / (1024.0 - (float)sensorValue) * 10000.0;
  dataString += String(rm, 1);

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = SD.open("garden.csv", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    Serial.println(dataString);
  }
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening gardenlog.csv");
  }
  delay(sampleMillis);
  delay(sampleMillis);
}
