/*
Morse Keyer
This implements the paddle functionality.
If at half the inter-element gap (called UNIT here) after a dit or dah has been played, the same key is still down, 
the element (dit or dah will be repeated

Copyright 2024 Nezumi Workbench

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


Key "I"
  ┌────────┐┐┐┐┐┐┐┐┐┐    
 ─┘        └└└└└└└└└└────
Output     
   ┌────┐ 	 ┌────┐    
 ──┘    └────┘    └────
	




*/
const int DIT = 2; // connect dit to pin 2
const int DAH = 3; // connect dah to pin 3
const int SPEAKER = 10; // connect the speaker to pin 10
const int TONE = 800;
const int UNIT = 120; // 120 = 10 wpm

void setup() {
  pinMode(DIT, INPUT_PULLUP);
  pinMode(DAH, INPUT_PULLUP);
  pinMode(SPEAKER, OUTPUT); 
}

void loop() {
  if(!digitalRead(DIT)){
    tone(SPEAKER, TONE);
    delay(UNIT);
    noTone(SPEAKER);
    delay(UNIT / 2);
    while(!digitalRead(DIT)){
      delay(UNIT / 2);
      tone(SPEAKER, TONE);
      delay(UNIT);
      noTone(SPEAKER);
      delay(UNIT / 2);
    }
  }
  if(!digitalRead(DAH)){
    tone(SPEAKER, TONE);
    delay(UNIT * 3);
    noTone(SPEAKER);
      delay(UNIT / 2);
    while(!digitalRead(DAH)){
      delay(UNIT / 2);
      tone(SPEAKER, TONE);
      delay(UNIT * 3);
      noTone(SPEAKER);
      delay(UNIT / 2);
    }
  }
}
