
/*
 * AA_TEST
 */

#include <float.h>

#include "WProgram.h"
void setup();
void loop();
void printFloat(float value, int places);
int ledPin = 7; // transistor base driver connected to pin 7
int val = 0;
int batt01 = 1023;
int batt02 = 1023;
int batt03 = 1023;
int batt04 = 1023;
int mins = 0;
int secs = 0;
//int vMin = 829;
int vMin = 1025/5;
int timeStart;
float minElapsed;

void setup()
{
pinMode(ledPin, OUTPUT); // sets the digital pin as output
Serial.begin(9600);
} 

void loop()
{
mins = 0;
secs = 0;
digitalWrite(ledPin, LOW);
Serial.println("#Send g for start discharge test.");
Serial.print('#');
 while(val != 'g') val = Serial.read();
Serial.println("#g found.");
digitalWrite(ledPin, HIGH);
val = 0;
//if (val == 'A')digitalWrite(ledPin, HIGH);
//if (val == 'a')digitalWrite(ledPin, LOW);
    timeStart = millis();
    Serial.print('#');
    Serial.println(timeStart);
     
    delay(1000);
    delay(1000);
    delay(1000);
     batt01 = analogRead(0);
     batt02 = analogRead(1)-batt01;
     batt03 = analogRead(2)-batt02-batt01;
     batt04 = analogRead(3)-batt03-batt02-batt03+1025/5;
    
    Serial.print("#");
    Serial.print("vMin = ");
    Serial.println(vMin);
    Serial.print("#");
    Serial.print("batt01 = ");
    Serial.println(batt01);
    Serial.print("#");
    Serial.print("batt02 = ");
    Serial.println(batt02);
    Serial.print("#");
    Serial.print("batt03 = ");
    Serial.println(batt03);
    Serial.print("#");
    Serial.print("batt04 = ");
    Serial.println(batt04);
    

  while((batt01 > vMin) && (batt02 > vMin) && (batt03 > vMin) && (batt04 > vMin) && (Serial.read() != '#')){  
     delay(1000);
     batt01 = analogRead(0);
     batt02 = analogRead(1)-batt01;
     batt03 = analogRead(2)-batt02-batt01;
     batt04 = analogRead(3)-batt03-batt02-batt03+1025/5;
     
// comment this next line out as well as its corresponding brace and mins will actually be equal to secs. 
//     if (secs > 59) {  
        //Serial.print(",  "); //delete this if the number of dots is correct.
        Serial.print(millis());
        Serial.print("   ");
        Serial.print(mins);
        Serial.print("   ");
        minElapsed = ((float)millis()-(float)timeStart)/60000.0;
        printFloat((float)minElapsed,3);
        Serial.print("   ");
        Serial.print(batt01);
        Serial.print("   ");
        printFloat((float)batt01*5.0/1023.0,3);
        Serial.print("   ");
        Serial.print(batt02);
        Serial.print("   ");
        printFloat((float)batt02*5.0/1023.0,3);
        Serial.print("   ");
        Serial.print(batt03);
        Serial.print("   ");
        printFloat((float)batt03*5.0/1023.0,3);
        Serial.print("   ");
        Serial.print(batt04);
        Serial.print("   ");
        printFloat((float)batt04*5.0/1023.0,3);
        Serial.println("");
        mins += 1;
        secs = 0;
  //}
    secs += 1;
    //Serial.print("."); //delete this if the number of dots is correct.
}
  Serial.println("#Discharge complete.");
}



void printFloat(float value, int places) {
   // this is used to cast digits
   int digit;
   float tens = 0.1;
   int tenscount = 0;
   int i;
   float tempfloat = value;
 
   // if value is negative, set tempfloat to the abs value
   // make sure we round properly. this could use pow from  
   //<math.h>, but doesn't seem worth the import
   // if this rounding step isn't here, the value  54.321 prints as  
   //54.3209
 
   // calculate rounding term d:   0.5/pow(10,places)
   float d = 0.5;
   if (value < 0)
     d *= -1.0;
   // divide by ten for each decimal place
   for (i = 0; i < places; i++)
     d/= 10.0;
   // this small addition, combined with truncation will round our  
   // values properly
   tempfloat +=  d;
 
   // first get value tens to be the large power of ten less than value
   // tenscount isn't necessary but it would be useful if you wanted  
   // to know after this how many chars the number will take
 
   if (value < 0)
     tempfloat *= -1.0;
   while ((tens * 10.0) <= tempfloat) {
     tens *= 10.0;
     tenscount += 1;
   }
 
 
   // write out the negative if needed
   if (value < 0)
     Serial.print('-');
 
   if (tenscount == 0)
     Serial.print(0, DEC);
 
   for (i=0; i< tenscount; i++) {
     digit = (int) (tempfloat/tens);
     Serial.print(digit, DEC);
     tempfloat = tempfloat - ((float)digit * tens);
     tens /= 10.0;
   }
 
   // if no places after decimal, stop now and return
   if (places <= 0)
     return;
 
   // otherwise, write the point and continue on
   Serial.print('.');
 
   // now write out each decimal place by shifting digits one by one  
   // into the ones place and writing the truncated value
   for (i = 0; i < places; i++) {
     tempfloat *= 10.0;
     digit = (int) tempfloat;
     Serial.print(digit,DEC);
     // once written, subtract off that digit
     tempfloat = tempfloat - (float) digit;
   }
}

int main(void)
{
	init();

	setup();
    
	for (;;)
		loop();
        
	return 0;
}

