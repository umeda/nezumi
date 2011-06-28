/*
 * WiiMIDI -- 
 * b01 display change in value as soon as joysttick crosses threshold. Not tested yet - previous verson works.
 * merging with wii_peak_c02
 * 
 *23-Apr-11 b05
 *Increasing sensitivity.
 *Adjustable scaling.
 *Joystick action on first limit
 *
 *30-Apr-11 c05
 *revised UI
 */

#include <ardumidi.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include "nunchuck_funcs.h"

#define rxPin 2
#define txPin 3

int loop_cnt=0;
byte accx,accy,accz,zbut,cbut,joyx,joyy;
int ledPin = 13;
int note_on = 0;

int amp = 0;
int amp_2 = 0;
int ampNew = 0;


int page = 0;

int voice = 116;
int note = 68;
int channel = 0;
int beats = 0;
int scaler = 5;
int threshold = 15;
int hold_off = 200;

int voice_2 = 60;
int note_2 = 62;
int channel_2 = 9;
int beats_2 = 0;
int scaler_2 = 5;
int threshold_2 = 15;
int hold_off_2 = 100;

int adjustment = 0;

SoftwareSerial mySerial =  SoftwareSerial(rxPin, txPin);

int debounce;

void setup()
{
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  midi_program_change(0, voice);
  
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  
  nunchuck_setpowerpins();
  nunchuck_init(); // send the initilization handshake
  printSettings();
  midi_program_change(0, voice);
  nunchuck_get_data(); //first read seems bogus

  mySerial.print(0xFE, BYTE);
  mySerial.print(0x01, BYTE);
  mySerial.print("Wii_MIDI_c08");  
  delay(2000);



}

void loop()
{
      //DoN
      amp = 0;
      ampNew = 0;
      amp = analogRead(0);
      if (amp > threshold)
      {
        for (int i = 0; i < 15; i = i+1) 
        {
          ampNew = analogRead(0);
          if (ampNew > amp)
          { 
            amp = ampNew;
          }
        }
        amp=amp/scaler;
        if (amp>127)
        {
          amp = 127;
        }
        //might neeed to do a midi program change here.
        //unless we use two different channels. 0 for don and 9 for kara
        //although some docmentation says midi program change isn't needed for what I'm doing.
        midi_note_on(channel, note, amp);
        digitalWrite(ledPin, HIGH);
        delay(hold_off);
        
        midi_note_off(channel, note, amp);        
        digitalWrite(ledPin, LOW);
        beats = beats +1;
        printPlay();        
       }
  
      //KaRa
      amp = 0;
      ampNew = 0;
      amp = analogRead(1);
      if (amp > threshold_2)
      {
        for (int i = 0; i < 15; i = i+1) 
        {
          ampNew = analogRead(1);
          if (ampNew > amp)
          { 
            amp = ampNew;
          }
        }
        amp=amp/scaler_2;
        if (amp>127)
        {
          amp = 127;
        }
        //might neeed to do a midi program change here.
        //unless we use two different channels. 0 for don and 9 for kara
        //although some docmentation says midi program change isn't needed for what I'm doing.
        midi_note_on(channel_2, note_2, amp);
        digitalWrite(ledPin, HIGH);
        delay(hold_off_2);
        
        midi_note_off(channel_2, note_2, amp);        
        digitalWrite(ledPin, LOW);
        beats_2 = beats_2 +1;
        amp_2 = amp; //kara needs it's own amp
        printPlay();        
       }
 

       delay(1);
       nunchuck_get_data();

        //accx  = nunchuck_accelx(); // ranges from approx 70 - 182
        //accy  = nunchuck_accely(); // ranges from approx 65 - 173
        //accz  = nunchuck_accelz();
        zbut = nunchuck_zbutton();
        cbut = nunchuck_cbutton(); 
        joyx  = nunchuck_joyx(); //33L - 133C - 225R 
        joyy  = nunchuck_joyy(); //25B - 128C - 224B
        

        if(joyy > 175)
        {
          adjustment = 1;
          adjValue(page);
          printPage(page);
          while(joyy > 150)
          {
            delay(100); //why does this delay prevent the app from getting hung up?
            nunchuck_get_data();
            joyy  = nunchuck_joyy(); //25B - 128C - 224B
            //printMsg((char*)"inc v");
          }
          //midi_program_change(0, voice);
          beats = 0;
          beats_2 = 0;
        }
        
        if(joyy < 75)
        {
          adjustment = -1;
          adjValue(page);
          printPage(page);
          while(joyy < 100)
          {
            delay(100);
            nunchuck_get_data();
            joyy  = nunchuck_joyy(); //25B - 128C - 224B
            //printMsg((char*)"dec v");
          }
          //midi_program_change(0, voice);
          beats = 0;
          beats_2 = 0;
        }


        if(joyx > 175)
        {
          page++;
          if (page > 11)
          {
            page = 0;
          }
          printPage(page);
          while(joyx > 150)
          {
            delay(100); //why does this delay prevent the app from getting hung up?
            nunchuck_get_data();
            joyx  = nunchuck_joyx(); //33L - 133C - 225R 
            //printMsg((char*)"inc n");
          }
        beats = 0;
        }
        
        if(joyx < 75)
        {
          page--;
          if (page < 0)
          {
            page = 11;
          }
          printPage(page);
          while(joyx < 100)
          {
            delay(100);
            nunchuck_get_data();
            joyx  = nunchuck_joyx(); //33L - 133C - 225R 
            //printMsg((char*)"dec n");
          }
          beats = 0;
          beats_2 = 0;
        }






        if(zbut == 1)
        {
        ///midi_note_off(channel, note, 127);
        midi_note_on(channel, note, 127);
        digitalWrite(ledPin, HIGH);
        while(zbut == 1)
          {
            delay(100);
            nunchuck_get_data();
            zbut = nunchuck_zbutton(); 
            //printMsg((char*)"release button");
          }
        midi_note_off(channel, note, 127);        
        digitalWrite(ledPin, LOW);
        //printSettings();
          beats = 0;
          beats_2 = 0;
        }


        if(cbut == 1)
        {
        ///midi_note_off(channel, note, 127);
        midi_note_on(channel_2, note_2, 127);
        digitalWrite(ledPin, HIGH);
        while(cbut == 1)
          {
            delay(100);
            nunchuck_get_data();
            cbut = nunchuck_cbutton(); 
            //printMsg((char*)"release button");
          }
        midi_note_off(channel_2, note_2, 127);        
        digitalWrite(ledPin, LOW);
        //printSettings();
          beats = 0;
          beats_2 = 0;
        }


        joyx  = 125; 
        joyy  = 125; 





//        channel = cbut;
//        printSettings();
/*            
        mySerial.print("accx: "); Serial.print((byte)accx,DEC);
        mySerial.print("\taccy: "); Serial.print((byte)accy,DEC);
        mySerial.print("\taccz: "); Serial.print((byte)accz,DEC);
        mySerial.print("\tzbut: "); Serial.print((byte)zbut,DEC);
        mySerial.print("\tcbut: "); Serial.print((byte)cbut,DEC);
        mySerial.print("\tjoyx: "); Serial.print((byte)joyx,DEC);
        mySerial.print("\tjoyy: "); Serial.println((byte)joyy,DEC);
*/ 

//    if( loop_cnt > 100 ) 
//    { // every 100 msecs get new data
//        loop_cnt = 0;
//    }
//    loop_cnt++;
//    delay(100);
}


void printSettings()
{
  mySerial.print(0xFE, BYTE);
  mySerial.print(0x01, BYTE);
  mySerial.print("c:");  
  mySerial.print(channel);
  mySerial.print(" v:");  
  mySerial.print(voice);
  mySerial.print(" n:");  
  mySerial.print(note);
  //delay(1000);
}

void printMsg(char* msg)
{
  mySerial.print(0xFE, BYTE);
  mySerial.print(0x01, BYTE);
  mySerial.print(msg);  
  delay(1000);
}

void printDon()
{
  mySerial.print(0xFE, BYTE);
  mySerial.print(0x01, BYTE);
  mySerial.print("beats:");  
  mySerial.print(beats);
  mySerial.print(" amp:");  
  mySerial.print(amp);
  //delay(1000);
}

void printPlay()
{
  mySerial.print(0xFE, BYTE);
  mySerial.print(0x01, BYTE);
  
  //print DoN
  mySerial.print(0xC4, BYTE);
  mySerial.print(0xDE, BYTE);
  mySerial.print(0xDD, BYTE);
  mySerial.print(beats);
  
  mySerial.print(0xFE, BYTE);
  mySerial.print(0x88, BYTE); //middle of line 1
  mySerial.print("Amp:");  
  mySerial.print(amp);
  
  mySerial.print(0xFE, BYTE);
  mySerial.print(0xC0, BYTE); //start of line 2
  //Print KaRa
  mySerial.print(0xB6, BYTE);
  mySerial.print(0xD7, BYTE);
  mySerial.print(beats_2);
  
  mySerial.print(0xFE, BYTE);
  mySerial.print(0xC8, BYTE); //middle of line 2
  mySerial.print("Amp:");  
  mySerial.print(amp_2);
  //delay(1000);
}



void printPage(int pg)
{

  //perhaps there should be a play page so you wouldn't ave to play a note to clear the screen
  mySerial.print(0xFE, BYTE);
  mySerial.print(0x01, BYTE);

  if (pg < 6)
  {
    //print DoN
    mySerial.print(0xC4, BYTE);
    mySerial.print(0xDE, BYTE);
    mySerial.print(0xDD, BYTE);
  }

  if (pg > 5)
  {
    //Print KaRa
    mySerial.print(0xB6, BYTE);
    mySerial.print(0xD7, BYTE);
  }

  //mySerial.print(0xFE, BYTE);
  //mySerial.print(0x8B, BYTE);

  //mySerial.print(pg);


  mySerial.print(0xFE, BYTE);
  mySerial.print(0xC0, BYTE);

  //mySerial.print(pg);
  if (pg == 0)
  {  
    mySerial.print("voice: ");  
    mySerial.print(voice);
  }
  if (pg == 1)
  {  
    mySerial.print("note: ");  
    mySerial.print(note);
  }
  if (pg == 2)
  {  
    mySerial.print("channel: ");  
    mySerial.print(channel);
  }
  if (pg == 3)
  {  
    mySerial.print("scaler: ");  
    mySerial.print(scaler);
  }
  if (pg == 4)
  {  
    mySerial.print("threshold: ");  
    mySerial.print(threshold);
  }
  if (pg == 5)
  {  
    mySerial.print("hold off: ");  
    mySerial.print(hold_off);
  }
  if (pg == 6)
  {  
    mySerial.print("voice: ");  
    mySerial.print(voice_2);
  }
  if (pg == 7)
  {  
    mySerial.print("note: ");  
    mySerial.print(note_2);
  }
  if (pg == 8)
  {  
    mySerial.print("channel: ");  
    mySerial.print(channel_2);
  }
  if (pg == 9)
  {  
    mySerial.print("scaler: ");  
    mySerial.print(scaler_2);
  }
  if (pg == 10)
  {  
    mySerial.print("threshold: ");  
    mySerial.print(threshold_2);
  }
  if (pg == 11)
  {  
    mySerial.print("hold off: ");  
    mySerial.print(hold_off_2);
  }
}

void adjValue(int pg)
{
  if (pg == 0)
  {  
    voice = voice + adjustment;
    midi_program_change(0, voice);
  }
  if (pg == 1)
  {  
    note = note + adjustment;
  }
  if (pg == 2)
  {  
    channel = channel + adjustment;
  }
  if (pg == 3)
  {  
    scaler = scaler + adjustment;
  }
  if (pg == 4)
  {  
    threshold = threshold + adjustment;
  }
  if (pg == 5)
  {  
    hold_off = hold_off + adjustment;
  }
  if (pg == 6)
  {  
    voice_2 = voice_2 + adjustment;
  }
  if (pg == 7)
  {  
    note_2 = note_2 + adjustment;
  }
  if (pg == 8)
  {  
    channel_2 = channel_2 + adjustment;
  }
  if (pg == 9)
  {  
    scaler_2 = scaler_2 + adjustment;
  }
  if (pg == 10)
  {  
    threshold_2 = threshold_2 + adjustment;
  }
  if (pg == 11)
  {  
    hold_off_2 = hold_off_2 + adjustment;
  }
}


