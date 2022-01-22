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
  D9 - Input 1 ───────────────────┬─┼─┼─┼──┬─┼──┼─┼─┐ │ ││
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
  A0 - Mode Blanking Control ───────────┘        │         │
                                                 │         │
  A1 - Time Blanking Control ────────────────────┴─────────┘

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

#include <Arduino.h>
#include <RotaryEncoder.h>

#define SWITCH 2
#define PIN_IN1 10
#define PIN_IN2 11
#define MODE_BLANK A0
#define TIME_BLANK A1
#define RUN_0S 10
#define RUN_2S 11

// A pointer to the dynamic created rotary encoder instance.
// This will be done in setup()
RotaryEncoder *encoder = nullptr;

void checkPosition()
{
  encoder->tick(); // just call tick() to check the state.
}

int interval = 60;

byte ones = 9;
byte tens = 9;
byte huns = 0;

byte dim = 0;
byte mode = 10;

int pos = 0;
int dir = 0;

volatile int state = 0;

void setup() {

  Serial.begin(115200);
  while (!Serial)
    ;
    
  // setup the rotary encoder functionality
  // use FOUR3 mode when PIN_IN1, PIN_IN2 signals are always HIGH in latch position.
  encoder = new RotaryEncoder(PIN_IN1, PIN_IN2, RotaryEncoder::LatchMode::FOUR3);


  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(A5, INPUT_PULLUP); //A6 and A7 cant be used this way on a Nano
  Serial.begin(9600);  pinMode(0, OUTPUT);
  pinMode(SWITCH, INPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(MODE_BLANK, OUTPUT);
  pinMode(TIME_BLANK, OUTPUT);
  digitalWrite(MODE_BLANK,LOW);
  digitalWrite(TIME_BLANK,LOW);

  // register interrupt routine
  attachInterrupt(digitalPinToInterrupt(PIN_IN1), checkPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_IN2), checkPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(SWITCH), incState, CHANGE);

}



void loop() {
  // while(digitalRead(A5)){
  // Serial.print("!");
  // }
  
  while(state == 0) {
    for (int i = 0; i <= 15; i++) {  
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delayMicroseconds(13);                       // 13 uS results in about 33 kHz
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delayMicroseconds(13);                       // 13 uS results in about 33 kHz
    }
    delayMicroseconds(5360);                       // trigger shutter with 2 second delay
    if(mode == 10 or mode == 12){
      delayMicroseconds(2000);                       // additional 2 ms to trigger shutter immediately
    }
    for (int i = 0; i <= 15; i++) {  
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delayMicroseconds(13);                       // 13 uS results in about 33 kHz
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delayMicroseconds(13);                       // 13 uS results in about 33 kHz
    }
    for (int i = interval; i >= 1; i--) {
      Serial.println(i);
      for (int j = 0; j < 9; j++){ 
        digitalWrite(TIME_BLANK,LOW);
        if(j > dim) {
          digitalWrite(TIME_BLANK,HIGH);
        }
        delay(100); // interrupts ignored during delay
          if(state != 0) {
            j = 10;  // bail out early!
            i = 0;
          }
      }
      // huns = i / 100;
      huns = mode;
      tens = i / 10;
      ones = i % 10;
      dispChars();  // this takes 100 mS! timing is off by 10 percent if j doesn't stop at 9
    }
  }
  
  digitalWrite(TIME_BLANK,HIGH);   
  while(state == 1) {
    static int pos = 0;
    static int dir = 0;
    encoder->tick(); // just call tick() to check the state.
    int newPos = encoder->getPosition();
    if (pos != newPos) {
//      Serial.print("pos:");
//      Serial.print(newPos);
//      Serial.print(" dir:");
//      Serial.println((int)(encoder->getDirection()));
      dir = (int)(encoder->getDirection());
      mode -= dir; // kinda wrong direction 
      // Serial.println(mode);
      pos = newPos;
      if(mode == 9) mode = 13;
      if(mode == 14) mode = 10;
      // Serial.println(mode);
      // Serial.println("");
      huns = mode;
      tens = 0;
      ones = 0;
      dispChars();    
    }    
  }


  huns = interval / 100;
  tens = interval / 10;
  ones = interval % 10;
  dispChars();
  digitalWrite(TIME_BLANK,LOW);
  digitalWrite(MODE_BLANK,LOW);
  while(state == 2) {
    static int pos = 0;
    static int dir = 0;
    encoder->tick(); // just call tick() to check the state.
    int newPos = encoder->getPosition();
    if (pos != newPos) {
//      Serial.print("pos:");
//      Serial.print(newPos);
//      Serial.print(" dir:");
//      Serial.println((int)(encoder->getDirection()));
      dir = (int)(encoder->getDirection());
      interval -= dir; // kinda wrong direction 
      // Serial.println(mode);
      pos = newPos;
      if(interval == 0) interval = 1;
      if(interval == 100) interval = 99;
      // Serial.println(mode);
      // Serial.println("");
      huns = interval / 100;
      tens = interval / 10;
      ones = interval % 10;
      dispChars();    
    }    
  }


  huns = dim;
  dispChars();
  digitalWrite(TIME_BLANK,HIGH);
  digitalWrite(MODE_BLANK,LOW);
  while(state == 3) {
    static int pos = 0;
    static int dir = 0;
    encoder->tick(); // just call tick() to check the state.
    int newPos = encoder->getPosition();
    if (pos != newPos) {
//      Serial.print("pos:");
//      Serial.print(newPos);
//      Serial.print(" dir:");
//      Serial.println((int)(encoder->getDirection()));
      dir = (int)(encoder->getDirection());
      dim -= dir; // kinda wrong direction 
      // Serial.println(mode);
      pos = newPos;
      if(dim == -1) interval = 0;
      if(dim == 10) dim = 9;
      // Serial.println(mode);
      // Serial.println("");
      huns = dim;
      dispChars();    
    }    
  }





}


void dispChars(){
  // Serial.println(ones);
  digitalWrite(9, ones & 1);   // set 2 ^ 0
  digitalWrite(3, ones & 2);   // 
  digitalWrite(4, ones & 4);   // 
  digitalWrite(5, ones & 8);   // 
  digitalWrite(6, LOW);   // Latch
  delay(10);
  digitalWrite(6, HIGH);   // Latch
  delay(10);
  digitalWrite(9, tens & 1);   // set 2 ^ 0
  digitalWrite(3, tens & 2);   // 
  digitalWrite(4, tens & 4);   // 
  digitalWrite(5, tens & 8);   // 
  digitalWrite(7, LOW);   // Latch
  delay(10);
  digitalWrite(7, HIGH);   // Latch
  delay(10);
  digitalWrite(9, huns & 1);   // set 2 ^ 0
  digitalWrite(3, huns & 2);   // 
  digitalWrite(4, huns & 4);   // 
  digitalWrite(5, huns & 8);   // 
  digitalWrite(8, LOW);   // Latch 
  delay(10);
  digitalWrite(8, HIGH);   // Latch
  delay(50);
}

void incState(){

  if(digitalRead(SWITCH) == HIGH) {
    state++;
    if(state == 4) {
      state = 0;
    }
  }
}
