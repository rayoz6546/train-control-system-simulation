#ifndef WAYSIDE_H
#define WAYSIDE_H

#include "Block.h"
//#include <vector>

using namespace std;

class Wayside {
private:
	Block blocks[100];

public:
	Wayside();
	~Wayside();
	void SetBlockOccupancy(int,bool);
    bool GetBlockOccupancy(int);
    void SetBlockSwitchPos(int,bool);
    bool GetBlockSwitchPos(int);
    void SetBlockLightState(int,int);
    int GetBlockLightState(int);
    void SetBlockTrackStatus(int,bool);
    bool GetBlockTrackStatus(int);
    void SetBlockRailwayCrossing(int,bool);
    bool GetBlockRailwayCrossing(int);
};

#endif
