#include "Block.h"
//#include "Arduino.h"

Block::Block(){
    Occupancy = false;
    Switch_pos = false;
    Light_state = 0;
    Track_status = true;
    Railway_crossing = false;
    Commanded_speed = 0;
    //Authority = "00";
}
void Block::SetOccupancy(bool Oc){
    Occupancy = Oc;
}
bool Block::GetOccupancy(){
    return Occupancy;
}
void Block::SetSwitchPos(bool sw){
    Switch_pos = sw;
}
bool Block::GetSwitchPos(){
    return Switch_pos;
}
void Block::toggleSwitchPos(){
	if(Switch_pos == true){
		Switch_pos = false;
	}
	else{
		Switch_pos = true;
	}
}
void Block::SetLightState(int ls){
    Light_state = ls;
}
int Block::GetLightState(){
    return Light_state;
}
void Block::SetTrackStatus(bool ts){
    Track_status = ts;
}
bool Block::GetTrackStatus(){
    return Track_status;
}
void Block::toggleTrackStatus(){
	if(Track_status == true){
		Track_status = false;
	}
	else{
		Track_status = true;
	}
}
void Block::SetRailwayCrossing(bool rc){
    Railway_crossing = rc;
}
bool Block::GetRailwayCrossing(){
    return Railway_crossing;
}
void Block::toggleRailwayCrossing(){
	if(Railway_crossing == true){
		Railway_crossing = false;
	}
	else{
		Railway_crossing = true;
	}
}
void Block::SetCommandedSpeed(int sp){
	Commanded_speed = sp;
}
int Block::GetCommandedSpeed(){
	return Commanded_speed;
}
/*void Block::SetAuthority(string st){
	
	Authority = st;
	
}
string Block::GetAuthority(){
	return Authority;
}*/
Block::~Block(){
	
}
