/*
 
  Copyright 2021 Nezumi Workbench
 
  Canon Remote Intervalometer

  Remote Intervalometer for Canon EOS cameras.

  This sketch uses an Arduino Nano to send an IR signal to the camera, once per minute, to snap a photo.
  The photos can then be sequenced into a time-lapse video. The count-down display is made from three HP 5082-7340 LED modules.
  The below schematic diagram was made with asciiflow.com.

  +5  ──────────────────────────────┬────────┬────────┐
                                    │        │        │
  GND  ─────────────────────────────┼─┬──────┼──┬─────┼─┐
                                    │ │      │  │     │ │
  D8 - Latch Enable A ──────────────┼─┼─┐    │  │     │ │ 
                                    │ │ │    │  │     │ │
  D7 - Latch Enable B ──────────────┼─┼─┼────┼──┼─┐   │ │
                                    │ │ │    │  │ │   │ │
  D6 - Latch Enable C ──────────────┼─┼─┼────┼──┼─┼───┼─┼┐
                                    │ │ │    │  │ │   │ ││
  D2 - Input 1 ───────────────────┬─┼─┼─┼──┬─┼──┼─┼─┐ │ ││
                                  │ │ │ │  │ │  │ │ │ │ ││
                                ┌─┴─┴─┴─┴─┬┴─┴──┴─┴┬┴─┴─┴┴──┐
                                │         │        │        │
                                │         │        │        │
                                │         │        │        │
                                │         │        │        │
                                │o        │o       │o       │
                                └─┬─┬─┬─┬─┴┬─┬─┬─┬─┴─┬─┬─┬─┬┘
                                  │ │ │ │  │ │ │ │   │ │ │ │
  D3 - Input 2 ───────────────────┴─┼─┼─┼──┴─┼─┼─┼───┘ │ │ │
                                    │ │ │    │ │ │     │ │ │
  D4 - Input 4 ─────────────────────┴─┼─┼────┴─┼─┼─────┘ │ │
                                      │ │      │ │       │ │
  D5 - Input 9 ───────────────────────┴─┼──────┴─┼───────┘ │
                                        │        │         │
  D9 - Blanking Control ────────────────┴────────┴─────────┘

  The energy-saving blanking control has not been added. What is planned is for the count-down timer to only flash for a couple hundred
  milliseconds.
  
  The 950 nm LED is driven through a 50 ohm resistor. Current should be about 50 mA.

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights 
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
  copies of the Software, and to permit persons to whom the Software is furnished
  to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  
*/


int interval = 60;

byte ones = 9;
byte tens = 9;
byte huns = 0;

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(A5, INPUT_PULLUP); //A6 and A7 cant be used this way on a Nano
  Serial.begin(9600);  pinMode(0, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  
}



void loop() {
  // while(digitalRead(A5)){
  // Serial.print("!");
  // }
  
  Serial.println("hello!");
  
  for (int i = 0; i <= 15; i++) {  
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delayMicroseconds(13);                       // 13 uS results in about 33 kHz
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delayMicroseconds(13);                       // 13 uS results in about 33 kHz
  }
  delayMicroseconds(5360);                       // trigger shutter with 2 second delay
  delayMicroseconds(2000);                       // additional 2 ms to trigger shutter immediately
  for (int i = 0; i <= 15; i++) {  
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delayMicroseconds(13);                       // 13 uS results in about 33 kHz
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delayMicroseconds(13);                       // 13 uS results in about 33 kHz
  }
  for (int i = interval; i >= 1; i--) {
    delay(1000);
    Serial.println(i);
    huns = i / 100;
    tens = i / 10;
    ones = i % 10;
    // huns = 10;
    dispChars();
  } 
  
}


void dispChars(){
  Serial.println(ones);
  digitalWrite(2, ones & 1);   // set 2 ^ 0
  digitalWrite(3, ones & 2);   // 
  digitalWrite(4, ones & 4);   // 
  digitalWrite(5, ones & 8);   // 
  digitalWrite(6, LOW);   // Latch
  delay(10);
  digitalWrite(6, HIGH);   // Latch
  delay(10);
  digitalWrite(2, tens & 1);   // set 2 ^ 0
  digitalWrite(3, tens & 2);   // 
  digitalWrite(4, tens & 4);   // 
  digitalWrite(5, tens & 8);   // 
  digitalWrite(7, LOW);   // Latch
  delay(10);
  digitalWrite(7, HIGH);   // Latch
  delay(10);
  digitalWrite(2, huns & 1);   // set 2 ^ 0
  digitalWrite(3, huns & 2);   // 
  digitalWrite(4, huns & 4);   // 
  digitalWrite(5, huns & 8);   // 
  digitalWrite(8, LOW);   // Latch 
  delay(10);
  digitalWrite(8, HIGH);   // Latch
  delay(50);
}
