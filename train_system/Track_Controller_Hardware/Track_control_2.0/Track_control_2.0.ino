#include <Wire.h>
#include <LiquidCrystal_I2C.h>
//#include <Block.cpp>
#include<Wayside.h>
#include<ezButton.h>

LiquidCrystal_I2C lcd(0x20,16,2);  // set the LCD address to 0x20(Cooperate with 3 short circuit caps) for a 16 chars and 2 line display
int SW_pin = 2;

Block blocks[77];

//Button set-up
ezButton button(SW_pin);

void setup() {

  //LCD Screen set up---------------------------------------------
  lcd.init();                      // initialize the lcd 
  lcd.backlight(); 
  lcd.home();
  //---------------------------------------------------------------
  //Set button debounce-------------------------------------------
  button.setDebounceTime(100);
  //--------------------------------------------------------------
  //Joystick set up-----------------------------------------------
  //pinMode(SW_pin, INPUT);
  //digitalWrite(SW_pin, HIGH);
  //--------------------------------------------------------------
  //Serial setup--------------------------------------------------
  Serial.begin(115200);
  //--------------------------------------------------------------

}

int backlightState = LOW;
long previousMillis = 0;
long interval = 1000;

//Which input/output is being looked at currently
int state = 0;
//Decides if input/output is expanded
int selected = 0;
int selected_state = 0;
//Variable for manual mode being activated
bool manual = false;
String tempMan = "Off";

//Sting for light display
String lightColor = "Green";
//String for Track Status
String trStatus = "Good";
//String for railway crossing
String railwayStr = "None";
//String for switch position
String switch_pos = "None";
//String for block occupancy
String block_oc = "Not Occupied";

//Serial read string
String serialData;

void loop() {
  //Start button loop
  button.loop();

  //Set serial timeout
  Serial.setTimeout(100);
  //Read Serial data
  serialData = Serial.readStringUntil(',');
 
/*Send block data
12 size string
0 - 1 = Current Block number
2 = Light state
3 - 4 = Commanded speed
5 = Occupancy
6 = Track Status
7 = Switch Position
8 = Railway Crossings
9-11 = Authority
Adds block number
*/

  int auth = 0;

  char recivedBlock0 = serialData[0];
  char recivedBlock1 = serialData[1];
  int block_index = ((int(recivedBlock0)-48)*10) + (int(recivedBlock1)-48);

  blocks[block_index].SetLightState(int(serialData[2])-48);
  

  //String recivedSpeed = serialData[5] + serialData[6] + serialData[7];
  //char recivedCS0 = serialData[3];
  char recivedCS1 = serialData[3];
  char recivedCS2 = serialData[4];
  //int recivedCS = ((int(recivedCS0)-48)*100) + ((int(recivedCS1)-48)*10) + (int(recivedCS2)-48);
  int recivedCS = ((int(recivedCS1)-48)*10) + (int(recivedCS2)-48);

  blocks[block_index].SetCommandedSpeed(recivedCS);

  blocks[block_index].SetOccupancy(int(serialData[5])-48);

  blocks[block_index].SetTrackStatus(int(serialData[6])-48);

  if((int(serialData[7])-48) != 2){
    blocks[block_index].SetSwitchPos(int(serialData[7])-48);
  }

  if((int(serialData[8])-48) != 2){
    blocks[block_index].SetRailwayCrossing(int(serialData[8])-48);
  }



  if(serialData[9] != 0){

    char recivedA0 = serialData[10];
    char recivedA1 = serialData[11];
    auth = ((int(recivedA0)-48)*10) + (int(recivedA1)-48);

  }

  //blocks[recivedBlock.toInt()].SetCommandedSpeed(recivedSpeed.toInt());

  //Logic for changing inputs if in manual mode----------------------
    if(manual == true){
      if(selected == 1){
        if(selected_state == 1){
          if(button.isPressed()){
            blocks[state].toggleSwitchPos();
          }
        }
        if(selected_state == 2){
          if(analogRead(A0) > 800){
            blocks[state].SetLightState((blocks[state].GetLightState()) + (1));
            if(blocks[state].GetLightState() > 2){
              blocks[state].SetLightState(0);
            }
          }
        }
        if(selected_state == 4){
          if(button.isPressed()){
            blocks[state].toggleRailwayCrossing();
          }
        }
        if(selected_state == 5){
          if(analogRead(A0) > 800){
            blocks[state].SetCommandedSpeed((blocks[state].GetCommandedSpeed()) + (10));
            if(blocks[state].GetCommandedSpeed() > 300){
              blocks[state].SetCommandedSpeed(0);
            }
          }
        }        
      }
    }
  //-----------------------------------------------------------------

  //Statements for what to display to LCD----------------------------
  if(selected == 0){
    if(state<76){
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("Block "+String(state + 1));
    }
    if(state == 76){
      if(manual == false){
        tempMan = "Off";
      }
      else{
        tempMan = "On";
      }
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("Manual mode: "+ tempMan);

    }


  }
  if(selected == 1){
    if(state < 76){
     switch(selected_state){
      case 0:
        lcd.clear();
        lcd.setCursor(0, 1);
        lcd.print("Occupancy:");
        lcd.setCursor(5, 2);
        if(String(blocks[state].GetOccupancy()) == "0"){
          block_oc = "Not Occupied";
        }
        else{
          block_oc = "Occupied";
        }
        lcd.print(block_oc);
        break;
      case 1:
        lcd.clear();
        lcd.setCursor(0, 1);
        lcd.print("Switch Position:");
        lcd.setCursor(5, 2);
        if(state == 15 || state == 51){
          if(String(blocks[state].GetSwitchPos()) == "0"){
            switch_pos = "Left";
          }
          else{
            switch_pos = "Right";
          }
        }
        else{
          switch_pos = "None";
        }
        lcd.print(switch_pos);
        break;
      case 2:
        lcd.clear();
        lcd.setCursor(0, 1);
        lcd.print("Light State:");
        lcd.setCursor(5, 2);
        if(state == 0 || state == 1 || state == 64 || state == 65){
          switch(blocks[state].GetLightState()){
            case 0:
              lightColor = "Green";
              break;
            case 1:
              lightColor = "Yellow";
              break;
            case 2:
              lightColor = "Red";
              break;
            default:
              lightColor = "None";
            }
        }
        else{
          lightColor = "None";
        }
        lcd.print(lightColor);
        break;
      case 3:
        lcd.clear();
        lcd.setCursor(0, 1);
        lcd.print("Track Status:");
        lcd.setCursor(5, 2);
        if(blocks[state].GetTrackStatus() == 0){
          trStatus = "Bad";
        }
        else{
          trStatus = "Good";
        }
        lcd.print(trStatus);
        break;
      case 4:
        lcd.clear();
        lcd.setCursor(0, 1);
        lcd.print("Railway Crossing:");
        lcd.setCursor(5, 2);
        if(state == 46){
          if(blocks[state].GetRailwayCrossing() == 1){
            railwayStr = "Up";
          }
          else{
            railwayStr = "Down";
          }
        }
        else{
          railwayStr = "None";
        }
        lcd.print(railwayStr);
        break;
      case 5:
        lcd.clear();
        lcd.setCursor(0, 1);
        lcd.print("Authority:");
        lcd.setCursor(5, 2);
        lcd.print(String(auth));
        break;
      default:
        lcd.clear();
        lcd.setCursor(0, 1);
        lcd.print("Commanded Speed:");
        lcd.setCursor(5, 2);
        lcd.print(String(blocks[state].GetCommandedSpeed()));
        break;
      }
    }
    else{
      selected = 0;
    }
  }
  //-----------------------------------------------------------------

  //Main input/output toggle-----------------------------------------
  if(selected == 0){  
    if(analogRead(A1) < 200){
      state = state - 1;
    }
    if(analogRead(A1) > 800){
      state = state + 1;
    }
    if(analogRead(A0) > 800){
      selected = 1;
    }

  }

  //Selected input output toggle------------------------------------------
  if(selected == 1){
    if(analogRead(A1) < 200){
      selected_state = selected_state - 1;
   }
    if(analogRead(A1) > 800){
      selected_state = selected_state + 1;
    }
    if(analogRead(A0) < 200){
      selected = 0;
    }
  }
  //Toggle manual mode-----------------------------------------------------
  if(state == 76){
    if(button.isPressed()){
      if(manual == false){
        manual = true;
      }
      else{
        manual = false;
      }
    }
  }
  
  //------------------------------------------------------------------------
  //Go from top to bottom or bottom to top----------------------------------
  if(state >= 77){
    state = 0;
  }

  if(state < 0){
    state = 76;
  }


  if(selected_state >= 7){
    selected_state = 0;
  }

  if(selected_state < 0){
    selected_state = 6;
  }
  //------------------------------------------------------------------------

  //Send serial data
  /*
  5 size string
  0-1 = Current Block number
  2 = Switch position
  3 = Light state
  4 = Railway Crossing
  */

  String sendData = "";

  //Send manual mode


  //Add current block
  int sentState = 0;

  if(state >= 76){
    sentState = 75;
  }
  else{
    sentState = state;
  }

  if(state <10){

    sendData = sendData + '0' + String(state);

  }
  else{

    sendData = sendData + String(sentState);

  }

  //Add switch position for red line

  sendData = sendData + String(blocks[sentState].GetSwitchPos());

  //Add Light State
  sendData = sendData +  String(blocks[state].GetLightState());
  
  //Add Railway crossing
  sendData = sendData + String(blocks[state].GetRailwayCrossing());

  sendData = sendData + "000";
 
  sendData = sendData + "\n";

  if(manual == true && state != 75){
    Serial.print(sendData+"\n");
  }
  else{
    Serial.print(String(sentState)+"\n");
  }
  delay(100);
  

}
