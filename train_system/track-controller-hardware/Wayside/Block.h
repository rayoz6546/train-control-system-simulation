#ifndef Block_H
#define Block_H
//#include <iostream>
//#include <string>

using namespace std;
 
class Block {
private:
        bool Occupancy;
        bool Switch_pos;
        int Light_state;
        bool Track_status;
        bool Railway_crossing;
        int Commanded_speed;
        //string Authority;
public:
        Block();
        ~Block();
        void SetOccupancy(bool);
        bool GetOccupancy();
        void SetSwitchPos(bool);
        bool GetSwitchPos();
        void toggleSwitchPos();
        void SetLightState(int);
        int GetLightState();
        void SetTrackStatus(bool);
        bool GetTrackStatus();
        void toggleTrackStatus();
        void SetRailwayCrossing(bool);
        bool GetRailwayCrossing();
        void toggleRailwayCrossing();
        void SetCommandedSpeed(int);
        int GetCommandedSpeed();
        //void setAuthority(string);
        //string GetAuthority();
        //int addTenSpeed();
        
};
 
#endif
