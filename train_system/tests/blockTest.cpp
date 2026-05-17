#include "Block.cpp"
#include <stdio.h>
#include <assert.h>

int main(){

	Block blocks;
	
	blocks.SetCommandedSpeed(250);
	blocks.SetTrackStatus(false);
	blocks.SetRailwayCrossing(true);
	blocks.SetLightState(2);
	
	
	assert(blocks.GetCommandedSpeed() == 250);
	assert(blocks.GetTrackStatus() == false);
	assert(blocks.GetRailwayCrossing() == true);
	assert(blocks.GetLightState() == 2);
	
	printf("No errors");

	return 0;
