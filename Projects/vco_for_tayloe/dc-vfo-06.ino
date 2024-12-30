/*
    Simple VFO for a direct conversion receiver.

    Si5351 controlled by a rotary encoder.
    Frequency shown on a pcf8574 OLED display.
    With second phase-shifted output for Tayloe mixer.
    Display easier to read and adjust with added spaces.

    Based on code from Peter, VK3TPM. who made a bare bones si5251 VFO. 
    https://bitbucket.org/peter_marks/dc-vfo/src/master/

    Based on code from Paul, VK3HN
    https://github.com/prt459/Arduino_si5351_VFO_Controller_Keyer



    dc-vfo-01 original plus font change
    dc-vfo-02 add second vfo
              add phase shift of 90 degrees (set value to 50 - not working yet...) 
    dc-vfo-03 Add spaces for powers of 10^3
    dc-vfo-04 Add bands, band edges, and band memory.
    dc-vfo-05 abandoned
    dc-vfo-06 replace use of set_freq with set_freq_manual from si5351_phase_test - phase shift implemented.
    

*/

const unsigned long int FREQ_DEFAULT = 7100000ULL;
//const unsigned long int FREQ_DEFAULT = 10000ULL;


// maybe account for 3kHz sidebands.
const unsigned long int bandEdgesLower[] = {
   7100000ULL, 
  10100000ULL, 
  14000000ULL, 
  18068000ULL, 
  21000000ULL, 
  24890000ULL, 
  28000000ULL, 
};

const unsigned long int bandEdgesUpper[] = {
   7300000ULL, 
  10150000ULL, 
  14350000ULL, 
  18168000ULL, 
  21450000ULL, 
  24990000ULL, 
  29700000ULL, 
};

unsigned long int bandMemory[] = {
   7100000ULL, 
  10100000ULL, 
  14000000ULL, 
  18068000ULL, 
  21000000ULL, 
  24890000ULL, 
  28000000ULL, 
};

unsigned long int bandMult[] = {
       100ULL, 
        70ULL, 
        50ULL, 
        40ULL, 
        35ULL, 
        30ULL, 
        25ULL, 
};


#define ENCODER_A 3
#define ENCODER_B 2
#define ENCODER_BTN A2
#define OLED_128X32
#define I2C_OLED_ADDRESS 0x3C

#include <RotaryEncoder.h>   // by Maattias Hertel http://www.mathertel.de/Arduino/RotaryEncoderLibrary.aspx
#include "si5351.h"     // Etherkit Si3531 library Jason Mildrum,  V2.1.4  
                      // https://github.com/etherkit/Si5351Arduino
#include "Wire.h"       // built in
//#include <SSD1306Ascii.h>         // SSD1306Ascii by Bill Greiman 1.3.5 https://github.com/greiman/SSD1306Ascii
#include <SSD1306AsciiAvrI2c.h>   // part of the above library


// Global objects - globals mostly start with a lower case g.

SSD1306AsciiAvrI2c oled;
Si5351 si5351;                // I2C address defaults to x60 in the NT7S lib
RotaryEncoder gEncoder = RotaryEncoder(ENCODER_A, ENCODER_B, RotaryEncoder::LatchMode::FOUR3);
long gEncoderPosition = 0;

unsigned long int gFrequency = FREQ_DEFAULT;
const unsigned long int gMult = 100ULL;

int belIndex = 0; // lower band edge index starts at zero.

long int gStepPowerOfTen = 1;
const long int kMaxPowerOfTen = 6;

long int gStep = round(pow(10, gStepPowerOfTen));

void setup() {
  Serial.begin(115200);
  Wire.begin();
  setupOscillator();
  // while(1){};
  setupDisplay();
  refresh_display();
  setupRotaryEncoder();
  // delay(500);
  // while(1){};
  // si5351.set_freq(FREQ_DEFAULT * SI5351_FREQ_MULT, SI5351_CLK0);  // this seems to be needed to be called for display to work. WHY?
  // si5351.output_enable(SI5351_CLK0, 1);
}

void loop() {
  // check for change in the rotary encoder
  gEncoder.tick();
  long newEncoderPosition = gEncoder.getPosition();
  if(newEncoderPosition != gEncoderPosition) {
    long encoderDifference = newEncoderPosition - gEncoderPosition;
    gEncoderPosition = newEncoderPosition;
    Serial.println(encoderDifference);
    frequencyAdjust(encoderDifference);
  }
  static bool last_button_state = 0;
  int button_value = analogRead(ENCODER_BTN);
  bool new_button_state = false;
  if(button_value > 1000) {
    // button closed
    new_button_state = true;
  }
  if(last_button_state != new_button_state) {
    if(new_button_state == true) {
      Serial.println("button closed");
      onPushButton();
    } else {
      Serial.println("button open");
    }
    
    last_button_state = new_button_state;
  }  
}

void setupRotaryEncoder() {
  attachInterrupt(digitalPinToInterrupt(ENCODER_A), checkPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_B), checkPosition, CHANGE);
}

// This interrupt routine will be called on any change of one of the input signals
void checkPosition()
{
  gEncoder.tick(); // just call tick() to check the state.
}

void onPushButton() {
  gStepPowerOfTen++;

  if(gStepPowerOfTen > kMaxPowerOfTen) {
    gStepPowerOfTen = 0;
  }
  gStep = round(pow(10, gStepPowerOfTen));
  Serial.print(gStepPowerOfTen);
  Serial.print(" ");
  Serial.println(gStep);
  refresh_display();
}

void refresh_display() {
  //oled.clear();
  //oled.set2X();
  oled.setCursor(0, 0);

  // convert gFrequency to a string. If it's less that 10MHz, prepend a space.
  String freqstr = ""; // gFrequency represnted by string
  if (gFrequency < 10000000ULL) freqstr.concat(" ");
  freqstr.concat(String(gFrequency));
  // Serial.print("###");
  // Serial.print(freqstr);
  // Serial.println("###");
  
  // insert space in the kilo and mega places
  String freqspc = ""; // gFrequency string with spaces for 10^3 places.
  int freqstrCount = 0 ;
  for(int i =0; i < 11; i++ ) {
    if (i==2 || i==5) {
      freqspc.concat(String(" "));
    }
    freqspc.concat(String(freqstr[i]));
    freqstrCount++;
  
    // Serial.println(freqspc);
  }
  
  oled.print(freqspc);
  oled.println(" Hz");
  Serial.println(freqspc);
  
  // Underline the digit that we're changing by when turning the encoder
  String stepString = "";
  int pad = 1;
  if (gStepPowerOfTen < 6) pad++;
  if (gStepPowerOfTen < 3) pad++;
  // Serial.print("gStepPowerOfTen = ");
  // Serial.println(gStepPowerOfTen);
  for(int i = 0; i < (kMaxPowerOfTen - gStepPowerOfTen + pad); i++) {
    stepString += " ";
  }
  stepString += "^";
  // overwrite the old markers
  for(int i = 0; i < (gStepPowerOfTen + pad); i++) {
    stepString += " ";
  }
  
  //oled.setCursor(x, 30);
  oled.print(stepString);
}

void frequencyAdjust(int delta) {
  Serial.print("Adjust: ");
  Serial.println(delta);
  Serial.print("gStep: ");
  Serial.println(gStep);
  if (gStep < 1000000) {
    gFrequency += (delta * gStep);
    if (gFrequency < bandEdgesLower[belIndex]){
      gFrequency = bandEdgesLower[belIndex];  // maybe beep when op passes lower limit
    }
    if (gFrequency > bandEdgesUpper[belIndex]){
      gFrequency = bandEdgesUpper[belIndex];  // maybe beep when op passes upper limit
    }
    bandMemory[belIndex] = gFrequency;
  }
  else {
    belIndex += delta;
    if (belIndex < 0) belIndex = 0;
    if (belIndex > 6) belIndex = 6;
    gFrequency = bandMemory[belIndex];
    // gFrequency =  bandEdgesLower[belIndex];
    Serial.print("change band to: ");  
    Serial.println(bandEdgesLower[belIndex]);
  } 
  setVfoFrequency(gFrequency); // correct out-of-band here.
  refresh_display();
}

void setVfoFrequency(unsigned long int frequency) {
  Serial.println("setVfoFrequency");  
  si5351.reset();
  // si5351.set_freq(frequency * SI5351_FREQ_MULT, SI5351_CLK0); //  
  // si5351.set_freq(frequency * SI5351_FREQ_MULT, SI5351_CLK1); //  
  // second vfo -  may use a different frequency
  // si5351.set_freq((frequency + 000ULL) * SI5351_FREQ_MULT, SI5351_CLK1); //  

  Serial.print("set frequency: ");
  print_ull(frequency);
  Serial.println("");
  
  // si5351.init(SI5351_CRYSTAL_LOAD_8PF, 0, 0); // is this really required to make the next freq change?
//  si5351.reset();
//  si5351.set_freq_manual(700000000ULL, 35000000000ULL, SI5351_CLK0);
//  si5351.set_freq_manual(700000000ULL, 35000000000ULL, SI5351_CLK1);
  si5351.set_freq_manual(frequency, frequency * bandMult[belIndex], SI5351_CLK0);
  si5351.set_freq_manual(frequency, frequency * bandMult[belIndex], SI5351_CLK1);
//  si5351.set_freq_manual(frequency, frequency * gMult, SI5351_CLK0); // two in a row is fine...
//  si5351.set_freq_manual(frequency, frequency * gMult, SI5351_CLK1);
  
  //set phase again
  //si5351.set_phase(SI5351_CLK0, 0);
  //si5351.set_phase(SI5351_CLK1, 100ULL);
  // si5351.set_phase(SI5351_CLK1, SI5351_FREQ_MULT);
  
  si5351.set_phase(SI5351_CLK0, 0);
  si5351.set_phase(SI5351_CLK1, bandMult[belIndex]);
//  Serial.print("set phase: ");  
//  print_ull(gMult);
//  Serial.println("");
  si5351.pll_reset(SI5351_PLLA); // I think both oscillators use PLLA

  //printSi5351Status();
}

void setupDisplay() {
  oled.begin(&Adafruit128x32, I2C_OLED_ADDRESS);
  //oled.setFont(fixed_bold10x15);
  oled.setFont(font8x8);
  oled.clear();
}

void setupOscillator() {
//  bool i2c_found = si5351.init(SI5351_CRYSTAL_LOAD_8PF, 0, 0);
//  Serial.print("si5351: ");
//  Serial.println(i2c_found ? "Found" : "Missing");
  si5351.init(SI5351_CRYSTAL_LOAD_8PF, 0, 0);
  si5351.reset();
  // how long should I wait to recover?
  // si5351.set_correction(135000, SI5351_PLL_INPUT_XO);    // Library update 26/4/2020: requires destination register address  ... si5351.set_correction(19100, SI5351_PLL_INPUT_XO);
  Serial.print("gFrequency: ");
  print_ull(gFrequency);
  Serial.println("");
  Serial.print("gMult: ");
  print_ull(gMult);
  Serial.println("");
  //delay(500);

//  si5351.set_freq_manual(700000000ULL, 35000000000ULL, SI5351_CLK0);
//  si5351.set_freq_manual(700000000ULL, 35000000000ULL, SI5351_CLK1);

  unsigned long long freq =       705000000ULL;
  unsigned long long pll_freq = 70500000000ULL;

  si5351.set_freq_manual(gFrequency, gFrequency * gMult, SI5351_CLK0);
  si5351.set_freq_manual(gFrequency, gFrequency * gMult, SI5351_CLK1);
  Serial.println("freq set");
  //delay(500);

  si5351.drive_strength(SI5351_CLK0, SI5351_DRIVE_4MA); 
  si5351.drive_strength(SI5351_CLK1, SI5351_DRIVE_4MA); 
  //delay(500);

  si5351.output_enable(SI5351_CLK0, 1);  // turn VFO on 
  si5351.output_enable(SI5351_CLK1, 1);  // turn VFO on 
  //delay(500);

  // hmmm. wait for status before trying this?
  si5351.set_phase(SI5351_CLK0, 0);
  si5351.set_phase(SI5351_CLK1, 100);
  Serial.println("phase set");
  //delay(500);

  // We need to reset the PLL before they will be in phase alignment (per library example)
  si5351.pll_reset(SI5351_PLLA); // I think both oscillators use PLLA
  // si5351.pll_reset(SI5351_PLLB); // I think both oscillators use PLLA
  Serial.println("pll reset performed");
  //delay(500);

  // printSi5351Status();
  //delay(5000);
  // printSi5351Status();
  //delay(5000);
  // printSi5351Status();
  //delay(5000);
}

/*
The nominal status for each of those flags is a 0. When the program indicates 1, 
there may be a reference clock problem, tuning problem, or some kind of other issue. 
(Note that it may take the Si5351 a bit of time to return the proper status flags, 
so in program initialization issue update_status() and then give the Si5351 a 
few hundred milliseconds to initialize before querying the status flags again.)
*/
void printSi5351Status(){
  si5351.update_status();
  delay(500);
  Serial.print("SYS_INIT: ");
  Serial.print(si5351.dev_status.SYS_INIT);
  Serial.print("  LOL_A: ");
  Serial.print(si5351.dev_status.LOL_A);
  Serial.print("  LOL_B: ");
  Serial.print(si5351.dev_status.LOL_B);
  Serial.print("  LOS: ");
  Serial.print(si5351.dev_status.LOS);
  Serial.print("  REVID: ");
  Serial.println(si5351.dev_status.REVID);
}


void print_ull(unsigned long long int value) {
  if (value == 0) {
    Serial.print('0');
    return;
  }

  char buffer[21]; // Maximum 20 digits for 64-bit unsigned integer + null terminator
  int i = 20;
  buffer[i--] = '\0';

  do {
    buffer[i--] = (value % 10) + '0';
    value /= 10;
  } while (value > 0);

  Serial.print(&buffer[i + 1]); // Print from the first non-null 
}

void setVfoPhase(unsigned long int phase) {
  //set phase again
  si5351.set_phase(SI5351_CLK0, 0);
  si5351.set_phase(SI5351_CLK1, phase);
  
  Serial.print("set phase: "); 
  print_ull(phase); 
  Serial.println(" ");
}
