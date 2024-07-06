
int wave[16][4] = {
  {1, 0, 0, 0},
  {1, 0, 1, 0},
  {1, 1, 0, 1},
  {1, 1, 1, 0},
  {1, 1, 1, 1},
  {1, 1, 1, 0},
  {1, 1, 0, 1},
  {1, 0, 1, 0},
  {1, 0, 0, 0},
  {0, 1, 0, 1},
  {0, 0, 1, 0},
  {0, 0, 0, 1},
  {0, 0, 0, 0},
  {0, 0, 0, 1},
  {0, 0, 1, 0},
  {0, 1, 0, 1}
};

int onebit[16][4] = {
  {0, 0, 0, 1},
  {0, 0, 0, 1},
  {0, 0, 0, 1},
  {0, 0, 0, 1},
  {0, 0, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 0},
  {0, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 0, 0},
  {1, 0, 0, 0},
  {1, 0, 0, 0},
  {1, 0, 0, 0},
  {1, 0, 0, 0}
};
int square[16][4] = {
  {0, 0, 0, 0},
  {0, 0, 0, 0},
  {0, 0, 0, 0},
  {0, 0, 0, 0},
  {0, 0, 0, 0},
  {0, 0, 0, 0},
  {0, 0, 0, 0},
  {0, 0, 0, 0},
  {1, 1, 1, 1},
  {1, 1, 1, 1},
  {1, 1, 1, 1},
  {1, 1, 1, 1},
  {1, 1, 1, 1},
  {1, 1, 1, 1},
  {1, 1, 1, 1}
};



int rampdn[16][4] = {
  {1, 1, 1, 1},
  {1, 1, 1, 0},
  {1, 1, 0, 1},
  {1, 1, 0, 0},
  {1, 0, 1, 1},
  {1, 0, 1, 0},
  {1, 0, 0, 1},
  {1, 0, 0, 0},
  {0, 1, 1, 1},
  {0, 1, 1, 0},
  {0, 1, 0, 1},
  {0, 1, 0, 0},
  {0, 0, 1, 1},
  {0, 0, 1, 0},
  {0, 0, 0, 1},
  {0, 0, 0, 0}
};

int rampup[16][4] = {
  {0, 0, 0, 0},
  {0, 0, 0, 1},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 1, 0, 0},
  {0, 1, 0, 1},
  {0, 1, 1, 0},
  {0, 1, 1, 1},
  {1, 0, 0, 0},
  {1, 0, 0, 1},
  {1, 0, 1, 0},
  {1, 0, 1, 1},
  {1, 1, 0, 0},
  {1, 1, 0, 1},
  {1, 1, 1, 0},
  {1, 1, 1, 1}
};

int tri[16][4] = {
  {0, 0, 0, 0},
  {0, 0, 1, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {1, 0, 0, 0},
  {1, 0, 1, 0},
  {1, 1, 0, 0},
  {1, 1, 1, 0},
  {1, 1, 1, 1},
  {1, 1, 0, 1},
  {1, 0, 1, 1},
  {1, 0, 0, 1},
  {0, 1, 1, 1},
  {0, 1, 0, 1},
  {0, 0, 1, 1},
  {0, 0, 0, 1}
};


int ms = 63;
//int wave = sine;
float freq = 1.0;
char cmd[16];
// int wave[16][4];
// wave = sine;

void setup() {
  Serial.begin(9600);
  Serial.write("hello");
  pinMode(13, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() 
{
  for (int sample = 0; sample < 16 ; sample++)
  {
    for (int pin = 0; pin < 4; pin++)
    {
      digitalWrite(5-pin, wave[sample][pin]); // write to pins 5, 4, 3, 2 with samples 0, 1, 2, 3. 
//    digitalWrite(5, wave[sample][0]);
//    digitalWrite(4, wave[sample][1]);
//    digitalWrite(3, wave[sample][2]);
//    digitalWrite(2, wave[sample][3]);
    }
    delay(ms);
    if( Serial.available() > 0 )
    {
      // String cmd = Serial.readString();
      delay(50);
      int availableBytes = Serial.available();

      for(int i=0; i<availableBytes; i++)
      {
        if(i<16) // do not let it overrun the cmd array
        {
          cmd[i] = Serial.read();
        }
      }
      Serial.println(cmd);
    
      if (cmd[0] == 'f') 
      {
        Serial.println("found f");;
        Serial.print(cmd);
        // Serial.println(23.4);
        // example of 1 Hz = f001.0
        float freq = (cmd[1]-48)*100 + (cmd[2]-48)*10 + (cmd[3]-48) + (cmd[5]-48)/10.0;
        Serial.println(freq);
        ms = int(round(1/freq/16 * 1000));
        Serial.println(ms);
        // Serial.println(sizeof(cmd));
        // Serial.println(index_of_dot(cmd));
        // Serial.println(index_of_newline(cmd)); 
        // when we are done - clear the character array.
          for( int i = 0; i < sizeof(cmd);  ++i ) cmd[i] = (char)0;
           
        }
        if (cmd[0] == 'w') 
        {
          Serial.println("found w");;
          Serial.print(cmd);
//          if(cmd[1] == '1') wave = sine;
//          if(cmd[1] == '2') wave = tri;
//          if(cmd[1] == '3') wave = rampup;
//          if(cmd[1] == '4') wave = rampdn;
//           if(cmd[1] == '5') wave = bin;
          for( int i = 0; i < sizeof(cmd);  ++i ) cmd[i] = (char)0;
           
        }
    }}
}

int index_of_dot(char cmdstr[])
{
  Serial.println("in dot function");
  Serial.println(cmdstr);
  Serial.println(sizeof(cmdstr));
  int pos;
  for(int i=0; i<16; i++)
  {
    Serial.print(i);
    Serial.print(" ");
    Serial.println(cmdstr[i]);
    if(cmdstr[i]==46)
    {
      Serial.println("found the dot");
      pos=i;
    }

  }
  return pos;
}


int index_of_newline(char cmdstr[])
{
  Serial.println("in newline function");
  Serial.println(cmdstr);
  Serial.println(sizeof(cmdstr));
  int pos;
  for(int i=0; i<16; i++)
  {
    Serial.print(i);
    Serial.print(" ");
    Serial.println(cmdstr[i]);
    if(cmdstr[i]==10)
    {
      Serial.println("found the newline");
      pos=i;
    }

  }
  return pos;
}
