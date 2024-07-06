// Morse Keyer
// This implements the paddle functionality.
// If at half the inter-element gap (called UNIT here) after a dit or dah has been played, the same key is still down, 
// the element (dit or dah will be repeated


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
