#include "Wayside.h"

Wayside::Wayside(){

	//blocks.resize(100);

}
void Wayside::SetBlockOccupancy(int num, bool occ){
	
	blocks[num].SetOccupancy(occ);
	
}
bool Wayside::GetBlockOccupancy(int num){
	
	return blocks[num].GetOccupancy();
	
}
void Wayside::SetBlockSwitchPos(int num, bool pos){
	
	blocks[num].SetSwitchPos(pos);
	
}
bool Wayside::GetBlockSwitchPos(int num){
	
	return blocks[num].GetSwitchPos();
	
}
void Wayside::SetBlockLightState(int num, int state){
	
	blocks[num].SetLightState(state);
	
}
int Wayside::GetBlockLightState(int num){
	
	return blocks[num].GetLightState();
	
}
void Wayside::SetBlockTrackStatus(int num, bool status){
	
	blocks[num].SetTrackStatus(status);
	
}
bool Wayside::GetBlockTrackStatus(int num){
	
	return blocks[num].GetTrackStatus();
	
}
void Wayside::SetBlockRailwayCrossing(int num, bool rail){
	
	blocks[num].SetSwitchPos(rail);
	
}
bool Wayside::GetBlockRailwayCrossing(int num){
	
	return blocks[num].GetRailwayCrossing();
	
}
Wayside::~Wayside(){
	
	
	
}
