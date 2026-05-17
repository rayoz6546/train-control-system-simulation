# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 11:42:44 2023

@author: RAYAN
"""

import threading
import os
import statistics

# TODO set authority to 0 when broken rail to stop train (when commandedspeed=0)
# TODO make new clone of train_info that I change on my thing and then send updated one to track model
class Track_Controller:
    def __init__(self, ctc_signals, track_signals, test=False, testUI=False) -> None:
        # Key Inputs
        self._authority = [[""] * 15, [""] * 76, [""] * 150]  # str
        self._suggested_speed = [[0] * 15, [0] * 76, [0] * 150]  # int
        self._track_occupancy = [False] * 241  # bool
        self._broken_rail = [False] * 241
        self._circuit_failure = [False] * 241
        self._power_failure = [False] * 241
        
        self.maintenance_switches_green = []
        self.maintenance_switches_red = []

        self.rail_status = [False] * 241

        self.train_info = {}

        # Key Outputs
        self._traffic_lights_green = [[None] * 15,[None] * 76,[None] * 150]  # row = line (blue/red/green)
        self._traffic_lights_yellow = [[None] * 15, [None] * 76, [None] * 150]
        self._traffic_lights_red = [[None] * 15, [None] * 76, [None] * 150]



        self._commanded_speed = [[0] * 15, [0] * 76, [0] * 150]  # int

        self._crossings = [[None]*15,[None]*76,[None]*150]  # index0->blueline(none), index1-> redline, index2-> greenline

        self._switch_positions = [[None] * 15,[None] * 76,[None] * 150]  # True -> Right, False -> Left


        # for manual use/changing outputs
        self.manual_switches = 0
        self.manual_lights = 0
        self.manual_crossings = 0
        self.manual_speed = 0 

        self.ctc_signals = ctc_signals
        self.track_signals = track_signals
        self.ui_tr = None
        self.ui = None
        if not test and not testUI:
            self.update()




    def update(self):

        self.train_info  = self.ctc_signals.train_info
        
        for key in self.track_signals.train_info:
            self.ctc_signals.train_info[key][3] = self.track_signals.train_info[key][3] #update just location for ctc
        
        self.track_signals.train_info = self.ctc_signals.train_info #update dict for track model


        self.compute_commanded_speed()

        self.get_rail_status()
        
        self._track_occupancy[0:15] = self.track_signals.blueLineOccupancy
        self._track_occupancy[15:91] = self.track_signals.redLineOccupancy
        self._track_occupancy[91:241]= self.track_signals.greenLineOccupancy


        self._broken_rail[0:15] = self.track_signals.brokenRail_blue
        self._broken_rail[15:91] = self.track_signals.brokenRail_red
        self._broken_rail[91:241] = self.track_signals.brokenRail_green


        self._circuit_failure[0:15] = self.track_signals.circuitFailure_blue
        self._circuit_failure[15:91] = self.track_signals.circuitFailure_red
        self._circuit_failure[91:241] = self.track_signals.circuitFailure_green

        self._power_failure[0:15] = self.track_signals.powerFailure_blue
        self._power_failure[15:91] = self.track_signals.powerFailure_red
        self._power_failure[91:241] = self.track_signals.powerFailure_green

        
        self.track_signals.ticketSales = self.ctc_signals.ticketSales 

        for i, train in self.ctc_signals.train_info.items():

            authority, suggested_speed, route, location = train
            if authority == "G0" or authority == "R0":
                continue
            elif authority[0]=="G":
                self._authority[2][location- 1] = authority
                self._suggested_speed[2][location - 1] = suggested_speed
                self.track_signals.authority_fromWayside = self._authority[2][location-1]
                self.track_signals.commandedSpeed = self._commanded_speed[2][location - 1]


            
            elif authority[0]=="R":
                self._authority[1][location- 1] = authority
                self._suggested_speed[1][location - 1] = suggested_speed
                self.track_signals.authority_fromWayside = self._authority[1][location-1]
                self.track_signals.commandedSpeed = self._commanded_speed[1][location - 1]


        self.track_signals.time = self.ctc_signals.sim_time

        
        dict_lights_green, dict_lights_red = self.passing_lights()
        dict_switches_green, dict_switches_red = self.passing_switches()

        self.track_signals.traffic_lights_green = dict_lights_green
        self.track_signals.switch_positions_green = dict_switches_green
        self.track_signals.traffic_lights_red = dict_lights_red
        self.track_signals.switch_positions_red = dict_switches_red

        self.ctc_signals.traffic_lights_green=dict_lights_green
        self.ctc_signals.switch_positions_green=dict_switches_green
        self.ctc_signals.traffic_lights_red = dict_lights_red
        self.ctc_signals.switch_positions_red = dict_switches_red

        self.ctc_signals.track_layout_green = self.track_signals.greenLine_set
        self.ctc_signals.track_layout_red = self.track_signals.redLine_set


        self.maintenance_switches_green=self.ctc_signals.switch_changes_green
        self.maintenance_switches_red = self.ctc_signals.switch_changes_red


        self.ctc_signals.rail_status[0]=self.rail_status[0:15]
        self.ctc_signals.rail_status[1]=self.rail_status[15:91]
        self.ctc_signals.rail_status[2]=self.rail_status[91:241]


        self.ctc_signals.track_occupancy[0] = self._track_occupancy[0:15]
        self.ctc_signals.track_occupancy[1] = self._track_occupancy[15:91]
        self.ctc_signals.track_occupancy[2] = self._track_occupancy[91:241]


        
        self.track_signals.blueSwitches_set[0] = self._switch_positions[0][0]
        
        threading.Timer(0.01, self.update).start()

    def passing_lights(self):
        dict_lights_green = {}
        dict_lights_green[1]=[self._traffic_lights_green[2][0],self._traffic_lights_yellow[2][0],self._traffic_lights_red[2][0]]
        dict_lights_green[2]=[self._traffic_lights_green[2][1],self._traffic_lights_yellow[2][1],self._traffic_lights_red[2][1]]
        dict_lights_green[13]=[self._traffic_lights_green[2][12],self._traffic_lights_yellow[2][12],self._traffic_lights_red[2][12]]
        dict_lights_green[28]=[self._traffic_lights_green[2][27],self._traffic_lights_yellow[2][27],self._traffic_lights_red[2][27]]
        dict_lights_green[29]=[self._traffic_lights_green[2][28],self._traffic_lights_yellow[2][28],self._traffic_lights_red[2][28]]
        dict_lights_green[61]=[self._traffic_lights_green[2][60],self._traffic_lights_yellow[2][60],self._traffic_lights_red[2][60]]
        dict_lights_green[62]=[self._traffic_lights_green[2][61],self._traffic_lights_yellow[2][61],self._traffic_lights_red[2][61]]
        dict_lights_green[75]=[self._traffic_lights_green[2][74],self._traffic_lights_yellow[2][74],self._traffic_lights_red[2][74]]
        dict_lights_green[76]=[self._traffic_lights_green[2][75],self._traffic_lights_yellow[2][75],self._traffic_lights_red[2][75]]
        dict_lights_green[99]=[self._traffic_lights_green[2][98],self._traffic_lights_yellow[2][98],self._traffic_lights_red[2][98]]
        dict_lights_green[100]=[self._traffic_lights_green[2][99],self._traffic_lights_yellow[2][99],self._traffic_lights_red[2][99]]
        dict_lights_green[149]=[self._traffic_lights_green[2][148],self._traffic_lights_yellow[2][148],self._traffic_lights_red[2][148]]
        dict_lights_green[150]=[self._traffic_lights_green[2][149],self._traffic_lights_yellow[2][149],self._traffic_lights_red[2][149]]

        dict_lights_red = {}
        dict_lights_red[1] = [self._traffic_lights_green[1][0], self._traffic_lights_yellow[1][0],self._traffic_lights_red[1][0]]
        dict_lights_red[66] = [self._traffic_lights_green[1][65], self._traffic_lights_yellow[1][65],self._traffic_lights_red[1][65]]

        return dict_lights_green, dict_lights_red
    
    def passing_switches(self):
        dict_switches_green={}
        dict_switches_green[13]=self._switch_positions[2][12]
        dict_switches_green[28]=self._switch_positions[2][27]
        dict_switches_green[57]=self._switch_positions[2][56]
        dict_switches_green[62]=self._switch_positions[2][61]
        dict_switches_green[77]=self._switch_positions[2][76]
        dict_switches_green[85]=self._switch_positions[2][84]

        dict_switches_red={}
        dict_switches_red[16]=self._switch_positions[1][15]
        dict_switches_red[52]=self._switch_positions[1][51]

        return dict_switches_green, dict_switches_red

    def set_authority(self, authority: int, block: int, line: int):
        self._authority[line][block] = authority

    def get_authority(self):
        return self._authority

    def set_commanded_speed(self, speed: int, block: int, line: int):

        self._commanded_speed[line][block] = speed

    def compute_commanded_speed(self):

        if True in self.rail_status[91:241]:
            j = 0
            for i in range(91,241):
                if self._track_occupancy[i]==True:
                    self._commanded_speed[2][j]=0

                else:
                    self._commanded_speed[2][j] = self._suggested_speed[2][j]
                j+=1
        else:
            self._commanded_speed[2] = self._suggested_speed[2]


        if True in self.rail_status[15:91]:
            j=0
            for i in range(15,91):
                if self._track_occupancy[i]==True:
                    self._commanded_speed[1][j]=0

                else:
                    self._commanded_speed[1][j] = self._suggested_speed[1][j]

                j+=1

        else:
            self._commanded_speed[1] = self._suggested_speed[1]



    def get_commanded_speed(self):
        return self._commanded_speed

    def set_suggested_speed(self, ss: int, block: int, line: int):
        self._suggested_speed[line][block] = ss

    def get_suggested_speed(self):
        return self._suggested_speed

    def set_track_occupancy(self, occupancy: bool, block: int):
        self._track_occupancy[block] = occupancy

    def get_track_occupancy(self):
        return self._track_occupancy

    def set_broken_rail(self, br: bool, block: int):
        self._broken_rail[block] = br

    def get_broken_rail(self):
        return self._broken_rail

    def set_circuit_failure(self, cf: bool, block: int):
        self._circuit_failure[block] = cf

    def get_circuit_failure(self):
        return self._circuit_failure

    def set_power_failure(self, pf: bool, block: int):
        self._power_failure[block] = pf

    def get_power_failure(self):
        return self._power_failure

    def get_rail_status(self):
        for block in range(15,91):
            if (self._broken_rail[block] == True) or (self._circuit_failure[block] == True) or (self._power_failure[block] == True):
                self.rail_status[block] = True
            else:
                self.rail_status[block] = False   

        for block in range(91,241):
            if (self._broken_rail[block] == True) or (self._circuit_failure[block] == True) or (self._power_failure[block] == True):
                self.rail_status[block] = True
            else:
                self.rail_status[block] = False

        return self.rail_status

    def set_traffic_lights(self, lights: int, block: int, line: int, manual:int):
        if manual==1:
            self.manual_lights = 1  # if programmer wants to manually change it
            if lights == 0:
                self._traffic_lights_green[line][block] = True
                self._traffic_lights_yellow[line][block] = False
                self._traffic_lights_red[line][block] = False

            elif lights == 1:
                self._traffic_lights_yellow[line][block] = True
                self._traffic_lights_green[line][block] = False
                self._traffic_lights_red[line][block] = False

            else:
                self._traffic_lights_red[line][block] = True
                self._traffic_lights_yellow[line][block] = False
                self._traffic_lights_green[line][block] = False

        else:
            self.manual_lights = 0 # will continue with PLC automatically (see vote_greenline() and vote_redline() functions)


    def get_traffic_lights(self):
        return (self._traffic_lights_green,self._traffic_lights_yellow,self._traffic_lights_red)

    def set_switch_positions(self, positions: bool, block: int, line: int, manual: int):

        if manual==1:
            self.manual_switches=1
            self._switch_positions[line][block] = positions
        else:
            self.manual_switches = 0

    def get_switch_positions(self):
        return self._switch_positions

    def get_crossings(self):
        return self._crossings

    def set_crossings(self, val: bool, line_: int, block: int, manual: int):
        if manual==1:
            self.manual_crossings=1
            self._crossings[line_][block]=val
        else:
            self.manual_crossings=0


    def voter_greenline(self,plc_file):  # for redundancy
        green_1,yellow_1,red_1,sw_1,cr_1 = self.compute_greenline_1(plc_file)
        green_2,yellow_2,red_2,sw_2,cr_2 = self.compute_greenline_2(plc_file)
        green_3,yellow_3,red_3,sw_3,cr_3 = self.compute_greenline_3(plc_file)

        for key in green_1:
            if self.manual_lights==0:
                self._traffic_lights_green[2][key-1]=statistics.mode([green_1[key],green_2[key],green_3[key]])
                self._traffic_lights_yellow[2][key-1]=statistics.mode([yellow_1[key],yellow_2[key],yellow_3[key]])
                self._traffic_lights_red[2][key-1]=statistics.mode([red_1[key],red_2[key],red_3[key]])
            else:
                pass  # manual mode

        for key in sw_1:
            if self.maintenance_switches_green==[] and self.manual_switches==0:
                self._switch_positions[2][key-1]=statistics.mode([sw_1[key],sw_2[key],sw_3[key]])

            else:  # in case we are in maintenance mode (from CTC or from programmer)
                if self.maintenance_switches_green!=[] and self.manual_switches==0:
                    for m in range(len(self.maintenance_switches_green)):
                        if self.maintenance_switches_green[m][0]==key:
                            self._switch_positions[2][key-1]=self.maintenance_switches_green[m][1]
                elif self.manual_switches==1 and self.maintenance_switches_green==[]:
                    pass # manual mode

        for key in cr_1:
            if self.manual_crossings==0:
                self._crossings[2][key-1]=statistics.mode([cr_1[key],cr_2[key],cr_3[key]])
            else:
                pass #manual mode


    def voter_redline(self,plc_file):  # for redundancy
        green_1,yellow_1,red_1,sw_1,cr_1 = self.compute_redline_1(plc_file)
        green_2,yellow_2,red_2,sw_2,cr_2 = self.compute_redline_2(plc_file)
        green_3,yellow_3,red_3,sw_3,cr_3 = self.compute_redline_3(plc_file)

        for key in green_1:
            if self.manual_lights==0:
                self._traffic_lights_green[1][key-1]=statistics.mode([green_1[key],green_2[key],green_3[key]])
                self._traffic_lights_yellow[1][key-1]=statistics.mode([yellow_1[key],yellow_2[key],yellow_3[key]])
                self._traffic_lights_red[1][key-1]=statistics.mode([red_1[key],red_2[key],red_3[key]])
            else:
                pass

        for key in sw_1:
            if self.maintenance_switches_red==[] and self.manual_switches==0:
                self._switch_positions[1][key-1]=statistics.mode([sw_1[key],sw_2[key],sw_3[key]])

            else:  # in case we are in maintenance mode (from CTC or from programmer)
                if self.maintenance_switches_red!=[] and self.manual_switches==0:
                    for m in range(len(self.maintenance_switches_red)):
                        if self.maintenance_switches_red[m][0]==key:
                            self._switch_positions[1][key-1]=self.maintenance_switches_red[m][1]
                elif self.manual_switches==1 and self.maintenance_switches_red==[]:
                    pass

        for key in cr_1:
            if self.manual_crossings==0:
                self._crossings[1][key-1]=statistics.mode([cr_1[key],cr_2[key],cr_3[key]])
            else:
                pass
            

    def compute_greenline_1(self,plc_file):
        traffic_lights_green = {}
        traffic_lights_yellow = {}
        traffic_lights_red = {}
        switches = {}
        crossings = {}

        if plc_file!="":
            file = open(plc_file,"r")

            for line in file:
                if line[0] == "s":  # initilizing switch positions
                    if line[6] == "r":  # right
                        switches[int(line[3:5])]=True
                    else:  # left
                        switches[int(line[3:5])]=False

                elif line[0] == "i":  # if statement
                    line = line.split("then")
                    condition = line[0].split(" ")
                    result = line[1].split(" ")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    condition.remove("if")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")

                    n = len(condition)
                    m = len(result)

                    block_cond = []
                    block_res = []
                    val_cond = []
                    val_res = []

                    for i in range(n):
                        x = condition[i].split("=")
                        block_cond.append(x[0])
                        val_cond.append(x[1])
                    for i in range(m):
                        x = result[i].split("=")
                        block_res.append(x[0])
                        val_res.append(x[1])

                    if n == 1 and m == 1:  # 1 condition, 1 result
                        if self._track_occupancy[int(block_cond[0][3:]) + 90] == eval(val_cond[0]):
                            if val_res[0] == "green":
                                traffic_lights_green[int(block_res[0][3:])]=True
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=False
 
                            elif val_res[0] == "red":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=True

                            elif val_res[0] == "yellow":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=True
                                traffic_lights_red[int(block_res[0][3:])]=False

                            elif val_res[0] == "right":
                                switches[int(block_res[0][3:])]=True
                                
                            else:
                                switches[int(block_res[0][3:])]=False


                    elif n == 1 and m == 2:  # 1 condition, 2 results
                        if self._track_occupancy[int(block_cond[0][3:]) + 90] == eval(val_cond[0]):
                            if val_res[0] == "green":
                                traffic_lights_green[int(block_res[0][3:])]=True
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=False
 
                            elif val_res[0] == "red":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=True

                            elif val_res[0] == "yellow":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=True
                                traffic_lights_red[int(block_res[0][3:])]=False

                            elif val_res[0] == "right":
                                switches[int(block_res[0][3:])]=True
                                
                            else:
                                switches[int(block_res[0][3:])]=False

                            if val_res[1] == "green":
                                traffic_lights_green[int(block_res[1][3:])]=True
                                traffic_lights_yellow[int(block_res[1][3:])]=False
                                traffic_lights_red[int(block_res[1][3:])]=False
 
                            elif val_res[1] == "red":
                                traffic_lights_green[int(block_res[1][3:])]=False
                                traffic_lights_yellow[int(block_res[1][3:])]=False
                                traffic_lights_red[int(block_res[1][3:])]=True

                            elif val_res[1] == "yellow":
                                traffic_lights_green[int(block_res[1][3:])]=False
                                traffic_lights_yellow[int(block_res[1][3:])]=True
                                traffic_lights_red[int(block_res[1][3:])]=False

                            elif val_res[1] == "right":
                                switches[int(block_res[1][3:])]=True
                                
                            else:
                                switches[int(block_res[1][3:])]=False

                            

                    elif n == 2 and m == 1:  # 2 conditions, 1 result
                        if self._track_occupancy[int(block_cond[0][3:]) + 90] == eval(val_cond[0]) and self._track_occupancy[int(block_cond[1][3:]) + 90] == eval(val_cond[1]):
                            if val_res[0] == "green":
                                traffic_lights_green[int(block_res[0][3:])]=True
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=False
 
                            elif val_res[0] == "red":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=True

                            elif val_res[0] == "yellow":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=True
                                traffic_lights_red[int(block_res[0][3:])]=False

                            elif val_res[0] == "right":
                                switches[int(block_res[0][3:])]=True
                                
                            else:
                                switches[int(block_res[0][3:])]=False

                    elif n == 2 and m == 2:  # 2 conditions, 2 results
                        if self._track_occupancy[int(block_cond[0][3:]) + 90] == eval(val_cond[0]) and self._track_occupancy[int(block_cond[1][3:]) + 90] == eval(val_cond[1]):
                            if val_res[0] == "green":
                                traffic_lights_green[int(block_res[0][3:])]=True
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=False
 
                            elif val_res[0] == "red":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=True

                            elif val_res[0] == "yellow":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=True
                                traffic_lights_red[int(block_res[0][3:])]=False

                            elif val_res[0] == "right":
                                switches[int(block_res[0][3:])]=True
                                
                            else:
                                switches[int(block_res[0][3:])]=False

                            if val_res[1] == "green":
                                traffic_lights_green[int(block_res[1][3:])]=True
                                traffic_lights_yellow[int(block_res[1][3:])]=False
                                traffic_lights_red[int(block_res[1][3:])]=False
 
                            elif val_res[1] == "red":
                                traffic_lights_green[int(block_res[1][3:])]=False
                                traffic_lights_yellow[int(block_res[1][3:])]=False
                                traffic_lights_red[int(block_res[1][3:])]=True

                            elif val_res[1] == "yellow":
                                traffic_lights_green[int(block_res[1][3:])]=False
                                traffic_lights_yellow[int(block_res[1][3:])]=True
                                traffic_lights_red[int(block_res[1][3:])]=False

                            elif val_res[1] == "right":
                                switches[int(block_res[1][3:])]=True
                                
                            else:
                                switches[int(block_res[1][3:])]=False


                elif line[0]=="^":
                    line = line.split("then")
                    condition = line[0].split(" ")
                    result = line[1].split(" ")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    condition.remove("^if")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")

                    n = len(condition)
                    m = len(result)

                    block_cond = []
                    block_res = []
                    val_cond = []
                    val_res = []
                    for i in range(n):
                        x = condition[i].split("=")
                        block_cond.append(x[0])
                        val_cond.append(x[1])
                    for i in range(m):
                        x = result[i].split("=")
                        block_res.append(x[0])
                        val_res.append(x[1])

                    if n==1 and m == 2:
                        if eval(val_cond[0])==False:

                            if True not in self._track_occupancy[(90+int(block_cond[0][3:5])):(91+int(block_cond[0][7:9]))]:  # so if no train on any of the blocks
                                if val_res[0] == "green":
                                    traffic_lights_green[int(block_res[0][3:])]=True
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=False
    
                                elif val_res[0] == "red":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=True

                                elif val_res[0] == "yellow":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=True
                                    traffic_lights_red[int(block_res[0][3:])]=False

                                elif val_res[0] == "right":
                                    switches[int(block_res[0][3:])]=True
                                    
                                else:
                                    switches[int(block_res[0][3:])]=False

                                if val_res[1] == "green":
                                    traffic_lights_green[int(block_res[1][3:])]=True
                                    traffic_lights_yellow[int(block_res[1][3:])]=False
                                    traffic_lights_red[int(block_res[1][3:])]=False
    
                                elif val_res[1] == "red":
                                    traffic_lights_green[int(block_res[1][3:])]=False
                                    traffic_lights_yellow[int(block_res[1][3:])]=False
                                    traffic_lights_red[int(block_res[1][3:])]=True

                                elif val_res[1] == "yellow":
                                    traffic_lights_green[int(block_res[1][3:])]=False
                                    traffic_lights_yellow[int(block_res[1][3:])]=True
                                    traffic_lights_red[int(block_res[1][3:])]=False

                                elif val_res[1] == "right":
                                    switches[int(block_res[1][3:])]=True
                                    
                                else:
                                    switches[int(block_res[1][3:])]=False

                        else:

                            if True in self._track_occupancy[(90+int(block_cond[0][3:5])):(91+int(block_cond[0][7:9]))]:
                                if val_res[0] == "green":
                                    traffic_lights_green[int(block_res[0][3:])]=True
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=False
    
                                elif val_res[0] == "red":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=True

                                elif val_res[0] == "yellow":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=True
                                    traffic_lights_red[int(block_res[0][3:])]=False

                                elif val_res[0] == "right":
                                    switches[int(block_res[0][3:])]=True
                                    
                                else:
                                    switches[int(block_res[0][3:])]=False

                                if val_res[1] == "green":
                                    traffic_lights_green[int(block_res[1][3:])]=True
                                    traffic_lights_yellow[int(block_res[1][3:])]=False
                                    traffic_lights_red[int(block_res[1][3:])]=False
    
                                elif val_res[1] == "red":
                                    traffic_lights_green[int(block_res[1][3:])]=False
                                    traffic_lights_yellow[int(block_res[1][3:])]=False
                                    traffic_lights_red[int(block_res[1][3:])]=True

                                elif val_res[1] == "yellow":
                                    traffic_lights_green[int(block_res[1][3:])]=False
                                    traffic_lights_yellow[int(block_res[1][3:])]=True
                                    traffic_lights_red[int(block_res[1][3:])]=False

                                elif val_res[1] == "right":
                                    switches[int(block_res[1][3:])]=True
                                    
                                else:
                                    switches[int(block_res[1][3:])]=False

                    elif n==2 and m==1:
                        if eval(val_cond[0])==False:

                            if (True not in self._track_occupancy[(90+int(block_cond[0][3:5])):(91+int(block_cond[0][7:9]))]) and self._track_occupancy[int(block_cond[1][3:]) + 90] == eval(val_cond[1]):
                                if val_res[0] == "green":
                                    traffic_lights_green[int(block_res[0][3:])]=True
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=False
    
                                elif val_res[0] == "red":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=True

                                elif val_res[0] == "yellow":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=True
                                    traffic_lights_red[int(block_res[0][3:])]=False

                                elif val_res[0] == "right":
                                    switches[int(block_res[0][3:])]=True
                                    
                                else:
                                    switches[int(block_res[0][3:])]=False

                        else:

                            if ((True in self._track_occupancy[(90+int(block_cond[0][3:5])):(91+int(block_cond[0][7:9]))]) and self._track_occupancy[int(block_cond[1][3:]) + 90] == eval(val_cond[1])) and self._track_occupancy[int(block_cond[1][3:5]) + 90] == eval(val_cond[1]):
                                if val_res[0] == "green":
                                    traffic_lights_green[int(block_res[0][3:])]=True
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=False
    
                                elif val_res[0] == "red":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=True

                                elif val_res[0] == "yellow":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=True
                                    traffic_lights_red[int(block_res[0][3:])]=False

                                elif val_res[0] == "right":
                                    switches[int(block_res[0][3:])]=True
                                    
                                else:
                                    switches[int(block_res[0][3:])]=False

                elif line[0]=="c":  # crossings
                    line = line.split("then")
                    condition = line[0].split(" ")
                    result = line[1].split(" ")
                    and_or=0    # if and => 0, if or => 1
                    if "and" in condition:
                        and_or = 0
                    if "or" in condition:
                        and_or = 1
                    while "or" in condition:
                        condition.remove("or")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    condition.remove("cif")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")

                    n = len(condition)
                    m = len(result)

                    block_cond = []
                    block_res = []
                    val_cond = []
                    val_res = []
                    for i in range(n):
                        x = condition[i].split("=")
                        block_cond.append(x[0])
                        val_cond.append(x[1])
                    for i in range(m):
                        x = result[i].split("=")
                        block_res.append(x[0])
                        val_res.append(x[1])

                    if and_or==0:
                        if self._track_occupancy[int(block_cond[0][3:]) + 90] == eval(val_cond[0]) and self._track_occupancy[int(block_cond[1][3:]) + 90] == eval(val_cond[1]) and self._track_occupancy[int(block_cond[2][3:])+90]==eval(val_cond[2]):
                            crossings[int(block_res[0][3:])]=eval(val_res[0])
                            
                    if and_or==1:
                        if self._track_occupancy[int(block_cond[0][3:]) + 90] == eval(val_cond[0]) or self._track_occupancy[int(block_cond[1][3:]) + 90] == eval(val_cond[1]) or self._track_occupancy[int(block_cond[2][3:])+90]==eval(val_cond[2]):
                            crossings[int(block_res[0][3:])]=eval(val_res[0])

        return traffic_lights_green, traffic_lights_yellow, traffic_lights_red, switches, crossings
    

    def compute_greenline_2(self,plc_file):
        # This method has different way of reading the PLC text file than compute_greenline_1
        traffic_lights_green = {}
        traffic_lights_yellow = {}
        traffic_lights_red = {}
        switches = {}
        crossings = {}

        if plc_file != "":
            file = open(plc_file,"r")

            for line in file:

                if line[0]=="s": # First few lines in PLC text file are to initialize switches
                    if line[6]=="l":
                        switches[int(line[3:5])]=False
                    else:
                        switches[int(line[3:5])]=True

                else: 
                    line_=line.split("then")
                    condition = line_[0].split(" ")
                    result = line_[1].split(" ")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    while "or" in condition:
                        condition.remove("or")
                    if "if" in condition:
                        condition.remove("if")
                    if "^if" in condition:
                        condition.remove("^if")
                    if "cif" in condition:
                        condition.remove("cif")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")
                    # so now we have for example: condition = ['to_13=True','to_28=False'] and result=['tl_19=green','tl_33=red']
                    # which would translate to "if to_13=True and to_28=False then tl_19=green and tl_33=red"

                    n=len(condition)  # This can only be 1 or 2 except for crossings
                    m=len(result) # This can only be 1 or 2 except for crossings

                    if line[0]=="i": # normal if statement

                        if n==1 and m==1: # If we have 1 condition and 1 result
                            if condition[0][5]=="=":  
                                if self._track_occupancy[int(condition[0][3:5])+90] == eval(condition[0][6:]):
                                    if result[0][6:]=="right": 
                                        switches[int(result[0][3:5])]=True

                                    elif result[0][6:]=="left":
                                        switches[int(result[0][3:5])]=False

                            else:   # this is just because we have a case "to_150=True", so since 150 is a 3 digit number I need to change indexing of eval(condition[0][...])
                                if self._track_occupancy[int(condition[0][3:5])+90] == eval(condition[0][7:]):
                                    if result[0][6:]=="right": 
                                        switches[int(result[0][3:5])]=True
                                    elif result[0][6:]=="left":
                                        switches[int(result[0][3:5])]=False        

                        elif n==1 and m==2: #1 condition, 2 results
                            if self._track_occupancy[int(condition[0][3:5])+90] == eval(condition[0][6:]):
                                if result[0][6:]=="green": 
                                    traffic_lights_green[int(result[0][3:5])]=True
                                    traffic_lights_yellow[int(result[0][3:5])]=False
                                    traffic_lights_red[int(result[0][3:5])]=False

                                elif result[0][6:]=="red":
                                    traffic_lights_green[int(result[0][3:5])]=False
                                    traffic_lights_yellow[int(result[0][3:5])]=False
                                    traffic_lights_red[int(result[0][3:5])]=True

                                elif result[0][6:]=="yellow":
                                    traffic_lights_green[int(result[0][3:5])]=False
                                    traffic_lights_yellow[int(result[0][3:5])]=True
                                    traffic_lights_red[int(result[0][3:5])]=False


                                if result[1][6:]=="green": 
                                    traffic_lights_green[int(result[1][3:5])]=True
                                    traffic_lights_yellow[int(result[1][3:5])]=False
                                    traffic_lights_red[int(result[1][3:5])]=False

                                elif result[1][6:]=="red":
                                    traffic_lights_green[int(result[1][3:5])]=False
                                    traffic_lights_yellow[int(result[1][3:5])]=False
                                    traffic_lights_red[int(result[1][3:5])]=True

                                elif result[1][6:]=="yellow":
                                    traffic_lights_green[int(result[1][3:5])]=False
                                    traffic_lights_yellow[int(result[1][3:5])]=True
                                    traffic_lights_red[int(result[1][3:5])]=False

                    elif line[0]=="^": #if statement but here we're checking for a group/large number of blocks 
                    # (ex: "if to_77->85=True" means if any of blocks between 77 and 85 is True/occupied)
                    # (ex: if to_77->85=False" means if all blocks between 77 and 85 are False/unoccupied)

                        if n==1 and m==2:
                            if condition[0][10:]=="True":
                                if (True in self._track_occupancy[int(condition[0][3:5])+90:int(condition[0][7:9])+91]):
                                    if result[0][5]!="=":
                                        if result[0][7:]=="green": 
                                            traffic_lights_green[int(result[0][3:6])]=True
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=False

                                        elif result[0][7:]=="red":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=True

                                        elif result[0][7:]=="yellow":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=True
                                            traffic_lights_red[int(result[0][3:6])]=False

                                    elif result[0][5]=="=":
                                        if result[0][6:]=="green": 
                                            traffic_lights_green[int(result[0][3:5])]=True
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=False

                                        elif result[0][6:]=="red":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=True

                                        elif result[0][6:]=="yellow":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=True
                                            traffic_lights_red[int(result[0][3:5])]=False

                                    if result[1][5]=="=":
                                        if result[1][6:]=="green": 
                                            traffic_lights_green[int(result[1][3:5])]=True
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=False

                                        elif result[1][6:]=="red":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=True

                                        elif result[1][6:]=="yellow":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=True
                                            traffic_lights_red[int(result[1][3:5])]=False

                                    elif result[1][5]!="=":
                                        if result[1][7:]=="green": 
                                            traffic_lights_green[int(result[1][3:6])]=True
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=False

                                        elif result[1][7:]=="red":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=True

                                        elif result[1][7:]=="yellow":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=True
                                            traffic_lights_red[int(result[1][3:6])]=False


                            else: 
                                if (True not in self._track_occupancy[int(condition[0][3:5])+90:int(condition[0][7:9])+91]):
                                    if result[0][5]!="=":
                                        if result[0][7:]=="green": 
                                            traffic_lights_green[int(result[0][3:6])]=True
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=False

                                        elif result[0][7:]=="red":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=True

                                        elif result[0][7:]=="yellow":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=True
                                            traffic_lights_red[int(result[0][3:6])]=False

                                    elif result[0][5]=="=":
                                        if result[0][6:]=="green": 
                                            traffic_lights_green[int(result[0][3:5])]=True
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=False

                                        elif result[0][6:]=="red":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=True

                                        elif result[0][6:]=="yellow":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=True
                                            traffic_lights_red[int(result[0][3:5])]=False

                                    if result[1][5]=="=":
                                        if result[1][6:]=="green": 
                                            traffic_lights_green[int(result[1][3:5])]=True
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=False

                                        elif result[1][6:]=="red":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=True

                                        elif result[1][6:]=="yellow":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=True
                                            traffic_lights_red[int(result[1][3:5])]=False

                                    elif result[1][5]!="=":
                                        if result[1][7:]=="green": 
                                            traffic_lights_green[int(result[1][3:6])]=True
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=False

                                        elif result[1][7:]=="red":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=True

                                        elif result[1][7:]=="yellow":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=True
                                            traffic_lights_red[int(result[1][3:6])]=False
                                        
                        else:
                            if (True not in self._track_occupancy[(int(condition[0][3:5])+90):(int(condition[0][7:9])+91)]) and self._track_occupancy[int(condition[1][3:6])+90]==eval(condition[1][7:]):
                                if result[0][6:]=="right": 
                                    switches[int(result[0][3:5])]=True

                                elif result[0][6:]=="left":
                                    switches[int(result[0][3:5])]=False

                    elif line[0]=="c": #crossings, here n=3 and m=1 for all cases
                        if condition[0][6]=="T": #then we all evals are True in condition, so we are doing "or" operation
                            if self._track_occupancy[int(condition[0][3:5])+90]==eval(condition[0][6:]) or self._track_occupancy[int(condition[1][3:5])+90]==eval(condition[1][6:]) or self._track_occupancy[int(condition[2][3:5])+90]==eval(condition[2][6:]):
                                crossings[int(result[0][3:5])]=eval(result[0][6:])
                        else:
                            if self._track_occupancy[int(condition[0][3:5])+90]==eval(condition[0][6:]) and self._track_occupancy[int(condition[1][3:5])+90]==eval(condition[1][6:]) and self._track_occupancy[int(condition[2][3:5])+90]==eval(condition[2][6:]):
                                crossings[int(result[0][3:5])]=eval(result[0][6:])  

        
        return traffic_lights_green, traffic_lights_yellow, traffic_lights_red, switches, crossings

    
    def compute_greenline_3(self,plc_file):  
        # This method reads the PLC text file in exactly the same way as compute_greenline_2. But the difference
        # here is with the if statements. I used logic equivalence to write them in different ways
        # e.g: "If trackOccupancy=True" becomes "if not(not(trackOccupancy=True))""   (A = not(not(A)))
        # e.g: "If trackOccupancy=True and trackOccupancy=False" becomes "If not(not(trackOccupancy=True) or not(trackOccupancy=False))"   A and B = not(not(A) or not(B))
        # Similarily A or B or C = not(not(A) and not(B) and not(C)) etc...

        traffic_lights_green = {}
        traffic_lights_yellow = {}
        traffic_lights_red = {}
        switches = {}
        crossings = {}

        if plc_file != "":
            file = open(plc_file,"r")

            for line in file:

                if line[0]=="s": # First few lines in PLC text file are to initialize switches
                    if line[6]=="l":
                        switches[int(line[3:5])]=False
                    else:
                        switches[int(line[3:5])]=True

                else: 
                    line_=line.split("then")
                    condition = line_[0].split(" ")
                    result = line_[1].split(" ")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    while "or" in condition:
                        condition.remove("or")
                    if "if" in condition:
                        condition.remove("if")
                    if "^if" in condition:
                        condition.remove("^if")
                    if "cif" in condition:
                        condition.remove("cif")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")
                    # so now we have for example: condition = ['to_13=True','to_28=False'] and result=['tl_19=green','tl_33=red']
                    # which would translate to "if to_13=True and to_28=False then tl_19=green and tl_33=red"

                    n=len(condition)  # This can only be 1 or 2 except for crossings
                    m=len(result) # This can only be 1 or 2 except for crossings

                    if line[0]=="i": # normal if statement

                        if n==1 and m==1: # If we have 1 condition and 1 result
                            if condition[0][5]=="=":  
                                if not(not(self._track_occupancy[int(condition[0][3:5])+90] == eval(condition[0][6:]))):
                                    if result[0][6:]=="right": 
                                        switches[int(result[0][3:5])]=True

                                    elif result[0][6:]=="left":
                                        switches[int(result[0][3:5])]=False

                            else:   # this is just because we have a case "to_150=True", so since 150 is a 3 digit number I need to change indexing of eval(condition[0][...])
                                if not(not(self._track_occupancy[int(condition[0][3:5])+90] == eval(condition[0][7:]))):
                                    if result[0][6:]=="right": 
                                        switches[int(result[0][3:5])]=True
                                    elif result[0][6:]=="left":
                                        switches[int(result[0][3:5])]=False        

                        elif n==1 and m==2: #1 condition, 2 results
                            if not(not(self._track_occupancy[int(condition[0][3:5])+90] == eval(condition[0][6:]))):
                                if result[0][6:]=="green": 
                                    traffic_lights_green[int(result[0][3:5])]=True
                                    traffic_lights_yellow[int(result[0][3:5])]=False
                                    traffic_lights_red[int(result[0][3:5])]=False

                                elif result[0][6:]=="red":
                                    traffic_lights_green[int(result[0][3:5])]=False
                                    traffic_lights_yellow[int(result[0][3:5])]=False
                                    traffic_lights_red[int(result[0][3:5])]=True

                                elif result[0][6:]=="yellow":
                                    traffic_lights_green[int(result[0][3:5])]=False
                                    traffic_lights_yellow[int(result[0][3:5])]=True
                                    traffic_lights_red[int(result[0][3:5])]=False


                                if result[1][6:]=="green": 
                                    traffic_lights_green[int(result[1][3:5])]=True
                                    traffic_lights_yellow[int(result[1][3:5])]=False
                                    traffic_lights_red[int(result[1][3:5])]=False

                                elif result[1][6:]=="red":
                                    traffic_lights_green[int(result[1][3:5])]=False
                                    traffic_lights_yellow[int(result[1][3:5])]=False
                                    traffic_lights_red[int(result[1][3:5])]=True

                                elif result[1][6:]=="yellow":
                                    traffic_lights_green[int(result[1][3:5])]=False
                                    traffic_lights_yellow[int(result[1][3:5])]=True
                                    traffic_lights_red[int(result[1][3:5])]=False

                    elif line[0]=="^": #if statement but here we're checking for a group/large number of blocks 
                    # (ex: "if to_77->85=True" means if any of blocks between 77 and 85 is True/occupied)
                    # (ex: if to_77->85=False" means if all blocks between 77 and 85 are False/unoccupied)

                        if n==1 and m==2:
                            if condition[0][10:]=="True":
                                if not(not((True in self._track_occupancy[int(condition[0][3:5])+90:int(condition[0][7:9])+91]))):
                                    if result[0][5]!="=":
                                        if result[0][7:]=="green": 
                                            traffic_lights_green[int(result[0][3:6])]=True
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=False

                                        elif result[0][7:]=="red":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=True

                                        elif result[0][7:]=="yellow":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=True
                                            traffic_lights_red[int(result[0][3:6])]=False

                                    elif result[0][5]=="=":
                                        if result[0][6:]=="green": 
                                            traffic_lights_green[int(result[0][3:5])]=True
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=False

                                        elif result[0][6:]=="red":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=True

                                        elif result[0][6:]=="yellow":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=True
                                            traffic_lights_red[int(result[0][3:5])]=False

                                    if result[1][5]=="=":
                                        if result[1][6:]=="green": 
                                            traffic_lights_green[int(result[1][3:5])]=True
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=False

                                        elif result[1][6:]=="red":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=True

                                        elif result[1][6:]=="yellow":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=True
                                            traffic_lights_red[int(result[1][3:5])]=False

                                    elif result[1][5]!="=":
                                        if result[1][7:]=="green": 
                                            traffic_lights_green[int(result[1][3:6])]=True
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=False

                                        elif result[1][7:]=="red":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=True

                                        elif result[1][7:]=="yellow":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=True
                                            traffic_lights_red[int(result[1][3:6])]=False


                            else: 
                                if not(not((True not in self._track_occupancy[int(condition[0][3:5])+90:int(condition[0][7:9])+91]))):
                                    if result[0][5]!="=":
                                        if result[0][7:]=="green": 
                                            traffic_lights_green[int(result[0][3:6])]=True
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=False

                                        elif result[0][7:]=="red":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=True

                                        elif result[0][7:]=="yellow":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=True
                                            traffic_lights_red[int(result[0][3:6])]=False

                                    elif result[0][5]=="=":
                                        if result[0][6:]=="green": 
                                            traffic_lights_green[int(result[0][3:5])]=True
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=False

                                        elif result[0][6:]=="red":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=True

                                        elif result[0][6:]=="yellow":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=True
                                            traffic_lights_red[int(result[0][3:5])]=False

                                    if result[1][5]=="=":
                                        if result[1][6:]=="green": 
                                            traffic_lights_green[int(result[1][3:5])]=True
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=False

                                        elif result[1][6:]=="red":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=True

                                        elif result[1][6:]=="yellow":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=True
                                            traffic_lights_red[int(result[1][3:5])]=False

                                    elif result[1][5]!="=":
                                        if result[1][7:]=="green": 
                                            traffic_lights_green[int(result[1][3:6])]=True
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=False

                                        elif result[1][7:]=="red":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=True

                                        elif result[1][7:]=="yellow":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=True
                                            traffic_lights_red[int(result[1][3:6])]=False
                                        
                        else:
                            if not(not(True not in self._track_occupancy[(int(condition[0][3:5])+90):(int(condition[0][7:9])+91)]) or not(self._track_occupancy[int(condition[1][3:6])+90]==eval(condition[1][7:]))):
                                if result[0][6:]=="right": 
                                    switches[int(result[0][3:5])]=True

                                elif result[0][6:]=="left":
                                    switches[int(result[0][3:5])]=False

                    elif line[0]=="c": #crossings, here n=3 and m=1 for all cases
                        if condition[0][6]=="T": #then we all evals are True in condition, so we are doing "or" operation
                            if not(not(self._track_occupancy[int(condition[0][3:5])+90]==eval(condition[0][6:])) and not(self._track_occupancy[int(condition[1][3:5])+90]==eval(condition[1][6:])) and not(self._track_occupancy[int(condition[2][3:5])+90]==eval(condition[2][6:]))):
                                crossings[int(result[0][3:5])]=eval(result[0][6:])
                        else:
                            if not(not(self._track_occupancy[int(condition[0][3:5])+90]==eval(condition[0][6:])) or not(self._track_occupancy[int(condition[1][3:5])+90]==eval(condition[1][6:])) or not(self._track_occupancy[int(condition[2][3:5])+90]==eval(condition[2][6:]))):
                                crossings[int(result[0][3:5])]=eval(result[0][6:])  

        
        return traffic_lights_green, traffic_lights_yellow, traffic_lights_red, switches, crossings
    


    def compute_redline_1(self,plc_file):
        traffic_lights_green = {}
        traffic_lights_yellow = {}
        traffic_lights_red = {}
        switches = {}
        crossings = {}

        if plc_file!="":
            file = open(plc_file,"r")

            for line in file:
                if line[0] == "s":  # initilizing switch positions
                    if line[6] == "r":  # right
                        switches[int(line[3:5])]=True
                    else:  # left
                        switches[int(line[3:5])]=False

                elif line[0] == "i":  # if statement
                    line = line.split("then")
                    condition = line[0].split(" ")
                    result = line[1].split(" ")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    condition.remove("if")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")

                    n = len(condition)
                    m = len(result)

                    block_cond = []
                    block_res = []
                    val_cond = []
                    val_res = []

                    for i in range(n):
                        x = condition[i].split("=")
                        block_cond.append(x[0])
                        val_cond.append(x[1])
                    for i in range(m):
                        x = result[i].split("=")
                        block_res.append(x[0])
                        val_res.append(x[1])

                    if n == 1 and m == 1:  # 1 condition, 1 result
                        if self._track_occupancy[int(block_cond[0][3:]) + 14] == eval(val_cond[0]):
                            if val_res[0] == "green":
                                traffic_lights_green[int(block_res[0][3:])]=True
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=False
 
                            elif val_res[0] == "red":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=True

                            elif val_res[0] == "yellow":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=True
                                traffic_lights_red[int(block_res[0][3:])]=False

                            elif val_res[0] == "right":
                                switches[int(block_res[0][3:])]=True
                                
                            else:
                                switches[int(block_res[0][3:])]=False


                    elif n == 1 and m == 2:  # 1 condition, 2 results
                        if self._track_occupancy[int(block_cond[0][3:]) + 14] == eval(val_cond[0]):
                            if val_res[0] == "green":
                                traffic_lights_green[int(block_res[0][3:])]=True
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=False
 
                            elif val_res[0] == "red":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=True

                            elif val_res[0] == "yellow":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=True
                                traffic_lights_red[int(block_res[0][3:])]=False

                            elif val_res[0] == "right":
                                switches[int(block_res[0][3:])]=True
                                
                            else:
                                switches[int(block_res[0][3:])]=False

                            if val_res[1] == "green":
                                traffic_lights_green[int(block_res[1][3:])]=True
                                traffic_lights_yellow[int(block_res[1][3:])]=False
                                traffic_lights_red[int(block_res[1][3:])]=False
 
                            elif val_res[1] == "red":
                                traffic_lights_green[int(block_res[1][3:])]=False
                                traffic_lights_yellow[int(block_res[1][3:])]=False
                                traffic_lights_red[int(block_res[1][3:])]=True

                            elif val_res[1] == "yellow":
                                traffic_lights_green[int(block_res[1][3:])]=False
                                traffic_lights_yellow[int(block_res[1][3:])]=True
                                traffic_lights_red[int(block_res[1][3:])]=False

                            elif val_res[1] == "right":
                                switches[int(block_res[1][3:])]=True
                                
                            else:
                                switches[int(block_res[1][3:])]=False

                            

                    elif n == 2 and m == 1:  # 2 conditions, 1 result
                        if self._track_occupancy[int(block_cond[0][3:]) + 14] == eval(val_cond[0]) and self._track_occupancy[int(block_cond[1][3:]) + 14] == eval(val_cond[1]):
                            if val_res[0] == "green":
                                traffic_lights_green[int(block_res[0][3:])]=True
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=False
 
                            elif val_res[0] == "red":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=True

                            elif val_res[0] == "yellow":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=True
                                traffic_lights_red[int(block_res[0][3:])]=False

                            elif val_res[0] == "right":
                                switches[int(block_res[0][3:])]=True
                                
                            else:
                                switches[int(block_res[0][3:])]=False

                    elif n == 2 and m == 2:  # 2 conditions, 2 results
                        if self._track_occupancy[int(block_cond[0][3:]) + 14] == eval(val_cond[0]) and self._track_occupancy[int(block_cond[1][3:]) + 14] == eval(val_cond[1]):
                            if val_res[0] == "green":
                                traffic_lights_green[int(block_res[0][3:])]=True
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=False
 
                            elif val_res[0] == "red":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=False
                                traffic_lights_red[int(block_res[0][3:])]=True

                            elif val_res[0] == "yellow":
                                traffic_lights_green[int(block_res[0][3:])]=False
                                traffic_lights_yellow[int(block_res[0][3:])]=True
                                traffic_lights_red[int(block_res[0][3:])]=False

                            elif val_res[0] == "right":
                                switches[int(block_res[0][3:])]=True
                                
                            else:
                                switches[int(block_res[0][3:])]=False

                            if val_res[1] == "green":
                                traffic_lights_green[int(block_res[1][3:])]=True
                                traffic_lights_yellow[int(block_res[1][3:])]=False
                                traffic_lights_red[int(block_res[1][3:])]=False
 
                            elif val_res[1] == "red":
                                traffic_lights_green[int(block_res[1][3:])]=False
                                traffic_lights_yellow[int(block_res[1][3:])]=False
                                traffic_lights_red[int(block_res[1][3:])]=True

                            elif val_res[1] == "yellow":
                                traffic_lights_green[int(block_res[1][3:])]=False
                                traffic_lights_yellow[int(block_res[1][3:])]=True
                                traffic_lights_red[int(block_res[1][3:])]=False

                            elif val_res[1] == "right":
                                switches[int(block_res[1][3:])]=True
                                
                            else:
                                switches[int(block_res[1][3:])]=False


                elif line[0]=="^":
                    line = line.split("then")
                    condition = line[0].split(" ")
                    result = line[1].split(" ")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    condition.remove("^if")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")

                    n = len(condition)
                    m = len(result)

                    block_cond = []
                    block_res = []
                    val_cond = []
                    val_res = []
                    for i in range(n):
                        x = condition[i].split("=")
                        block_cond.append(x[0])
                        val_cond.append(x[1])
                    for i in range(m):
                        x = result[i].split("=")
                        block_res.append(x[0])
                        val_res.append(x[1])

                    if n==1 and m == 2:
                        if eval(val_cond[0])==False:

                            if True not in self._track_occupancy[(14+int(block_cond[0][3:5])):(15+int(block_cond[0][7:9]))]:  # so if no train on any of the blocks
                                if val_res[0] == "green":
                                    traffic_lights_green[int(block_res[0][3:])]=True
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=False
    
                                elif val_res[0] == "red":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=True

                                elif val_res[0] == "yellow":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=True
                                    traffic_lights_red[int(block_res[0][3:])]=False

                                elif val_res[0] == "right":
                                    switches[int(block_res[0][3:])]=True
                                    
                                else:
                                    switches[int(block_res[0][3:])]=False

                                if val_res[1] == "green":
                                    traffic_lights_green[int(block_res[1][3:])]=True
                                    traffic_lights_yellow[int(block_res[1][3:])]=False
                                    traffic_lights_red[int(block_res[1][3:])]=False
    
                                elif val_res[1] == "red":
                                    traffic_lights_green[int(block_res[1][3:])]=False
                                    traffic_lights_yellow[int(block_res[1][3:])]=False
                                    traffic_lights_red[int(block_res[1][3:])]=True

                                elif val_res[1] == "yellow":
                                    traffic_lights_green[int(block_res[1][3:])]=False
                                    traffic_lights_yellow[int(block_res[1][3:])]=True
                                    traffic_lights_red[int(block_res[1][3:])]=False

                                elif val_res[1] == "right":
                                    switches[int(block_res[1][3:])]=True
                                    
                                else:
                                    switches[int(block_res[1][3:])]=False

                        else:

                            if True in self._track_occupancy[(14+int(block_cond[0][3:5])):(15+int(block_cond[0][7:9]))]:
                                if val_res[0] == "green":
                                    traffic_lights_green[int(block_res[0][3:])]=True
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=False
    
                                elif val_res[0] == "red":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=True

                                elif val_res[0] == "yellow":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=True
                                    traffic_lights_red[int(block_res[0][3:])]=False

                                elif val_res[0] == "right":
                                    switches[int(block_res[0][3:])]=True
                                    
                                else:
                                    switches[int(block_res[0][3:])]=False

                                if val_res[1] == "green":
                                    traffic_lights_green[int(block_res[1][3:])]=True
                                    traffic_lights_yellow[int(block_res[1][3:])]=False
                                    traffic_lights_red[int(block_res[1][3:])]=False
    
                                elif val_res[1] == "red":
                                    traffic_lights_green[int(block_res[1][3:])]=False
                                    traffic_lights_yellow[int(block_res[1][3:])]=False
                                    traffic_lights_red[int(block_res[1][3:])]=True

                                elif val_res[1] == "yellow":
                                    traffic_lights_green[int(block_res[1][3:])]=False
                                    traffic_lights_yellow[int(block_res[1][3:])]=True
                                    traffic_lights_red[int(block_res[1][3:])]=False

                                elif val_res[1] == "right":
                                    switches[int(block_res[1][3:])]=True
                                    
                                else:
                                    switches[int(block_res[1][3:])]=False

                    elif n==2 and m==1:
                        if eval(val_cond[0])==False:

                            if (True not in self._track_occupancy[(14+int(block_cond[0][3:5])):(15+int(block_cond[0][7:9]))]) and self._track_occupancy[int(block_cond[1][3:]) + 14] == eval(val_cond[1]):
                                if val_res[0] == "green":
                                    traffic_lights_green[int(block_res[0][3:])]=True
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=False
    
                                elif val_res[0] == "red":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=True

                                elif val_res[0] == "yellow":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=True
                                    traffic_lights_red[int(block_res[0][3:])]=False

                                elif val_res[0] == "right":
                                    switches[int(block_res[0][3:])]=True
                                    
                                else:
                                    switches[int(block_res[0][3:])]=False

                        else:

                            if ((True in self._track_occupancy[(14+int(block_cond[0][3:5])):(15+int(block_cond[0][7:9]))]) and self._track_occupancy[int(block_cond[1][3:]) + 14] == eval(val_cond[1])) and self._track_occupancy[int(block_cond[1][3:5]) + 14] == eval(val_cond[1]):
                                if val_res[0] == "green":
                                    traffic_lights_green[int(block_res[0][3:])]=True
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=False
    
                                elif val_res[0] == "red":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=False
                                    traffic_lights_red[int(block_res[0][3:])]=True

                                elif val_res[0] == "yellow":
                                    traffic_lights_green[int(block_res[0][3:])]=False
                                    traffic_lights_yellow[int(block_res[0][3:])]=True
                                    traffic_lights_red[int(block_res[0][3:])]=False

                                elif val_res[0] == "right":
                                    switches[int(block_res[0][3:])]=True
                                    
                                else:
                                    switches[int(block_res[0][3:])]=False

                elif line[0]=="c":  # crossings
                    line = line.split("then")
                    condition = line[0].split(" ")
                    result = line[1].split(" ")
                    and_or=0    # if and => 0, if or => 1
                    if "and" in condition:
                        and_or = 0
                    if "or" in condition:
                        and_or = 1
                    while "or" in condition:
                        condition.remove("or")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    condition.remove("cif")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")

                    n = len(condition)
                    m = len(result)

                    block_cond = []
                    block_res = []
                    val_cond = []
                    val_res = []
                    for i in range(n):
                        x = condition[i].split("=")
                        block_cond.append(x[0])
                        val_cond.append(x[1])
                    for i in range(m):
                        x = result[i].split("=")
                        block_res.append(x[0])
                        val_res.append(x[1])

                    if and_or==0:
                        if self._track_occupancy[int(block_cond[0][3:]) + 14] == eval(val_cond[0]) and self._track_occupancy[int(block_cond[1][3:]) + 14] == eval(val_cond[1]) and self._track_occupancy[int(block_cond[2][3:])+14]==eval(val_cond[2]):
                            crossings[int(block_res[0][3:])]=eval(val_res[0])
                            
                    if and_or==1:
                        if self._track_occupancy[int(block_cond[0][3:]) + 14] == eval(val_cond[0]) or self._track_occupancy[int(block_cond[1][3:]) + 14] == eval(val_cond[1]) or self._track_occupancy[int(block_cond[2][3:])+14]==eval(val_cond[2]):
                            crossings[int(block_res[0][3:])]=eval(val_res[0])

        return traffic_lights_green, traffic_lights_yellow, traffic_lights_red, switches, crossings
    

    def compute_redline_2(self,plc_file):
        # This method has different way of reading the PLC text file than compute_redline_1
        traffic_lights_green = {}
        traffic_lights_yellow = {}
        traffic_lights_red = {}
        switches = {}
        crossings = {}

        if plc_file != "":
            file = open(plc_file,"r")

            for line in file:

                if line[0]=="s": # First few lines in PLC text file are to initialize switches
                    if line[6]=="l":
                        switches[int(line[3:5])]=False
                    else:
                        switches[int(line[3:5])]=True

                else: 
                    line_=line.split("then")
                    condition = line_[0].split(" ")
                    result = line_[1].split(" ")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    while "or" in condition:
                        condition.remove("or")
                    if "if" in condition:
                        condition.remove("if")
                    if "^if" in condition:
                        condition.remove("^if")
                    if "cif" in condition:
                        condition.remove("cif")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")
                    # so now we have for example: condition = ['to_13=True','to_28=False'] and result=['tl_19=green','tl_33=red']
                    # which would translate to "if to_13=True and to_28=False then tl_19=green and tl_33=red"

                    n=len(condition)  # This can only be 1 or 2 except for crossings
                    m=len(result) # This can only be 1 or 2 except for crossings

                    if line[0]=="i": # normal if statement

                        if n==1 and m==1: # If we have 1 condition and 1 result
                            #if condition[0][5]=="=":  
                            if self._track_occupancy[int(condition[0][3:5])+14] == eval(condition[0][6:]):
                                if result[0][6:]=="right": 
                                    switches[int(result[0][3:5])]=True

                                elif result[0][6:]=="left":
                                    switches[int(result[0][3:5])]=False

                            # else:   # this is just because we have a case "to_150=True", so since 150 is a 3 digit number I need to change indexing of eval(condition[0][...])
                            #     if self._track_occupancy[int(condition[0][3:5])+14] == eval(condition[0][7:]):
                            #         if result[0][6:]=="right": 
                            #             switches[int(result[0][3:5])]=True
                            #         elif result[0][6:]=="left":
                            #             switches[int(result[0][3:5])]=False        

                        elif n==1 and m==2: #1 condition, 2 results
                            if self._track_occupancy[int(condition[0][3:5])+14] == eval(condition[0][6:]):
                                if result[0][6:]=="green": 
                                    traffic_lights_green[int(result[0][3:5])]=True
                                    traffic_lights_yellow[int(result[0][3:5])]=False
                                    traffic_lights_red[int(result[0][3:5])]=False

                                elif result[0][6:]=="red":
                                    traffic_lights_green[int(result[0][3:5])]=False
                                    traffic_lights_yellow[int(result[0][3:5])]=False
                                    traffic_lights_red[int(result[0][3:5])]=True

                                elif result[0][6:]=="yellow":
                                    traffic_lights_green[int(result[0][3:5])]=False
                                    traffic_lights_yellow[int(result[0][3:5])]=True
                                    traffic_lights_red[int(result[0][3:5])]=False


                                if result[1][6:]=="green": 
                                    traffic_lights_green[int(result[1][3:5])]=True
                                    traffic_lights_yellow[int(result[1][3:5])]=False
                                    traffic_lights_red[int(result[1][3:5])]=False

                                elif result[1][6:]=="red":
                                    traffic_lights_green[int(result[1][3:5])]=False
                                    traffic_lights_yellow[int(result[1][3:5])]=False
                                    traffic_lights_red[int(result[1][3:5])]=True

                                elif result[1][6:]=="yellow":
                                    traffic_lights_green[int(result[1][3:5])]=False
                                    traffic_lights_yellow[int(result[1][3:5])]=True
                                    traffic_lights_red[int(result[1][3:5])]=False

                        elif n==2 and m==1:
                            if self._track_occupancy[int(condition[0][3:5])+14] == eval(condition[0][6:]) and self._track_occupancy[int(condition[1][3:5])+14]==eval(condition[0][6:]):
                                if result[0][6:]=="right": 
                                    switches[int(result[0][3:5])]=True

                                elif result[0][6:]=="left":
                                    switches[int(result[0][3:5])]=False

                    elif line[0]=="^": #if statement but here we're checking for a group/large number of blocks 
                    # (ex: "if to_77->85=True" means if any of blocks between 77 and 85 is True/occupied)
                    # (ex: if to_77->85=False" means if all blocks between 77 and 85 are False/unoccupied)

                        if n==1 and m==2:
                            if condition[0][10:]=="True":
                                if (True in self._track_occupancy[int(condition[0][3:5])+14:int(condition[0][7:9])+15]):
                                    if result[0][5]!="=":
                                        if result[0][7:]=="green": 
                                            traffic_lights_green[int(result[0][3:6])]=True
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=False

                                        elif result[0][7:]=="red":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=True

                                        elif result[0][7:]=="yellow":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=True
                                            traffic_lights_red[int(result[0][3:6])]=False

                                    elif result[0][5]=="=":
                                        if result[0][6:]=="green": 
                                            traffic_lights_green[int(result[0][3:5])]=True
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=False

                                        elif result[0][6:]=="red":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=True

                                        elif result[0][6:]=="yellow":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=True
                                            traffic_lights_red[int(result[0][3:5])]=False

                                    if result[1][5]=="=":
                                        if result[1][6:]=="green": 
                                            traffic_lights_green[int(result[1][3:5])]=True
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=False

                                        elif result[1][6:]=="red":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=True

                                        elif result[1][6:]=="yellow":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=True
                                            traffic_lights_red[int(result[1][3:5])]=False

                                    elif result[1][5]!="=":
                                        if result[1][7:]=="green": 
                                            traffic_lights_green[int(result[1][3:6])]=True
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=False

                                        elif result[1][7:]=="red":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=True

                                        elif result[1][7:]=="yellow":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=True
                                            traffic_lights_red[int(result[1][3:6])]=False


                            else: 
                                if (True not in self._track_occupancy[int(condition[0][3:5])+14:int(condition[0][7:9])+15]):
                                    if result[0][5]!="=":
                                        if result[0][7:]=="green": 
                                            traffic_lights_green[int(result[0][3:6])]=True
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=False

                                        elif result[0][7:]=="red":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=True

                                        elif result[0][7:]=="yellow":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=True
                                            traffic_lights_red[int(result[0][3:6])]=False

                                    elif result[0][5]=="=":
                                        if result[0][6:]=="green": 
                                            traffic_lights_green[int(result[0][3:5])]=True
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=False

                                        elif result[0][6:]=="red":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=True

                                        elif result[0][6:]=="yellow":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=True
                                            traffic_lights_red[int(result[0][3:5])]=False

                                    if result[1][5]=="=":
                                        if result[1][6:]=="green": 
                                            traffic_lights_green[int(result[1][3:5])]=True
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=False

                                        elif result[1][6:]=="red":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=True

                                        elif result[1][6:]=="yellow":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=True
                                            traffic_lights_red[int(result[1][3:5])]=False

                                    elif result[1][5]!="=":
                                        if result[1][7:]=="green": 
                                            traffic_lights_green[int(result[1][3:6])]=True
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=False

                                        elif result[1][7:]=="red":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=True

                                        elif result[1][7:]=="yellow":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=True
                                            traffic_lights_red[int(result[1][3:6])]=False
                                        
                        else:
                            if (True not in self._track_occupancy[(int(condition[0][3:5])+14):(int(condition[0][7:9])+15)]) and self._track_occupancy[int(condition[1][3:5])+14]==eval(condition[1][6:]):
                                if result[0][6:]=="right": 
                                    switches[int(result[0][3:5])]=True

                                elif result[0][6:]=="left":
                                    switches[int(result[0][3:5])]=False

                    elif line[0]=="c": #crossings, here n=3 and m=1 for all cases
                        if condition[0][6]=="T": #then we all evals are True in condition, so we are doing "or" operation
                            if self._track_occupancy[int(condition[0][3:5])+14]==eval(condition[0][6:]) or self._track_occupancy[int(condition[1][3:5])+14]==eval(condition[1][6:]) or self._track_occupancy[int(condition[2][3:5])+14]==eval(condition[2][6:]):
                                crossings[int(result[0][3:5])]=eval(result[0][6:])
                        else:
                            if self._track_occupancy[int(condition[0][3:5])+14]==eval(condition[0][6:]) and self._track_occupancy[int(condition[1][3:5])+14]==eval(condition[1][6:]) and self._track_occupancy[int(condition[2][3:5])+14]==eval(condition[2][6:]):
                                crossings[int(result[0][3:5])]=eval(result[0][6:])  

        
        return traffic_lights_green, traffic_lights_yellow, traffic_lights_red, switches, crossings

    
    def compute_redline_3(self,plc_file):  
        # This method reads the PLC text file in exactly the same way as compute_redline_2. But the difference
        # here is with the if statements. I used logic equivalence to write them in different ways
        # e.g: "If trackOccupancy=True" becomes "if not(not(trackOccupancy=True))""   (A = not(not(A)))
        # e.g: "If trackOccupancy=True and trackOccupancy=False" becomes "If not(not(trackOccupancy=True) or not(trackOccupancy=False))"   A and B = not(not(A) or not(B))
        # Similarily A or B or C = not(not(A) and not(B) and not(C)) etc...

        traffic_lights_green = {}
        traffic_lights_yellow = {}
        traffic_lights_red = {}
        switches = {}
        crossings = {}

        if plc_file != "":
            file = open(plc_file,"r")

            for line in file:

                if line[0]=="s": # First few lines in PLC text file are to initialize switches
                    if line[6]=="l":
                        switches[int(line[3:5])]=False
                    else:
                        switches[int(line[3:5])]=True

                else: 
                    line_=line.split("then")
                    condition = line_[0].split(" ")
                    result = line_[1].split(" ")
                    while "and" in condition:
                        condition.remove("and")
                    while "and" in result:
                        result.remove("and")
                    while "or" in condition:
                        condition.remove("or")
                    if "if" in condition:
                        condition.remove("if")
                    if "^if" in condition:
                        condition.remove("^if")
                    if "cif" in condition:
                        condition.remove("cif")
                    while "" in condition:
                        condition.remove("")
                    while "" in result:
                        result.remove("")
                    while "\n" in result:
                        result.remove("\n")
                    # so now we have for example: condition = ['to_13=True','to_28=False'] and result=['tl_19=green','tl_33=red']
                    # which would translate to "if to_13=True and to_28=False then tl_19=green and tl_33=red"

                    n=len(condition)  # This can only be 1 or 2 except for crossings
                    m=len(result) # This can only be 1 or 2 except for crossings

                    if line[0]=="i": # normal if statement

                        if n==1 and m==1: # If we have 1 condition and 1 result
                            #if condition[0][5]=="=":  
                            if not(not(self._track_occupancy[int(condition[0][3:5])+14] == eval(condition[0][6:]))):
                                if result[0][6:]=="right": 
                                    switches[int(result[0][3:5])]=True

                                elif result[0][6:]=="left":
                                    switches[int(result[0][3:5])]=False

                            # else:   # this is just because we have a case "to_150=True", so since 150 is a 3 digit number I need to change indexing of eval(condition[0][...])
                            #     if not(not(self._track_occupancy[int(condition[0][3:5])+14] == eval(condition[0][7:]))):
                            #         if result[0][6:]=="right": 
                            #             switches[int(result[0][3:5])]=True
                            #         elif result[0][6:]=="left":
                            #             switches[int(result[0][3:5])]=False        

                        elif n==1 and m==2: #1 condition, 2 results
                            if not(not(self._track_occupancy[int(condition[0][3:5])+14] == eval(condition[0][6:]))):
                                if result[0][6:]=="green": 
                                    traffic_lights_green[int(result[0][3:5])]=True
                                    traffic_lights_yellow[int(result[0][3:5])]=False
                                    traffic_lights_red[int(result[0][3:5])]=False

                                elif result[0][6:]=="red":
                                    traffic_lights_green[int(result[0][3:5])]=False
                                    traffic_lights_yellow[int(result[0][3:5])]=False
                                    traffic_lights_red[int(result[0][3:5])]=True

                                elif result[0][6:]=="yellow":
                                    traffic_lights_green[int(result[0][3:5])]=False
                                    traffic_lights_yellow[int(result[0][3:5])]=True
                                    traffic_lights_red[int(result[0][3:5])]=False


                                if result[1][6:]=="green": 
                                    traffic_lights_green[int(result[1][3:5])]=True
                                    traffic_lights_yellow[int(result[1][3:5])]=False
                                    traffic_lights_red[int(result[1][3:5])]=False

                                elif result[1][6:]=="red":
                                    traffic_lights_green[int(result[1][3:5])]=False
                                    traffic_lights_yellow[int(result[1][3:5])]=False
                                    traffic_lights_red[int(result[1][3:5])]=True

                                elif result[1][6:]=="yellow":
                                    traffic_lights_green[int(result[1][3:5])]=False
                                    traffic_lights_yellow[int(result[1][3:5])]=True
                                    traffic_lights_red[int(result[1][3:5])]=False

                        elif n==2 and m==1:
                            if not(not(self._track_occupancy[int(condition[0][3:5])+14] == eval(condition[0][6:]))) and not(not(self._track_occupancy[int(condition[1][3:5])+14]==eval(condition[1][6:]))):
                                if result[0][6:]=="right": 
                                    switches[int(result[0][3:5])]=True

                                elif result[0][6:]=="left":
                                    switches[int(result[0][3:5])]=False

                    elif line[0]=="^": #if statement but here we're checking for a group/large number of blocks 
                    # (ex: "if to_77->85=True" means if any of blocks between 77 and 85 is True/occupied)
                    # (ex: if to_77->85=False" means if all blocks between 77 and 85 are False/unoccupied)

                        if n==1 and m==2:
                            if condition[0][10:]=="True":
                                if not(not((True in self._track_occupancy[int(condition[0][3:5])+14:int(condition[0][7:9])+15]))):
                                    if result[0][5]!="=":
                                        if result[0][7:]=="green": 
                                            traffic_lights_green[int(result[0][3:6])]=True
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=False

                                        elif result[0][7:]=="red":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=True

                                        elif result[0][7:]=="yellow":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=True
                                            traffic_lights_red[int(result[0][3:6])]=False

                                    elif result[0][5]=="=":
                                        if result[0][6:]=="green": 
                                            traffic_lights_green[int(result[0][3:5])]=True
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=False

                                        elif result[0][6:]=="red":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=True

                                        elif result[0][6:]=="yellow":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=True
                                            traffic_lights_red[int(result[0][3:5])]=False

                                    if result[1][5]=="=":
                                        if result[1][6:]=="green": 
                                            traffic_lights_green[int(result[1][3:5])]=True
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=False

                                        elif result[1][6:]=="red":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=True

                                        elif result[1][6:]=="yellow":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=True
                                            traffic_lights_red[int(result[1][3:5])]=False

                                    elif result[1][5]!="=":
                                        if result[1][7:]=="green": 
                                            traffic_lights_green[int(result[1][3:6])]=True
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=False

                                        elif result[1][7:]=="red":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=True

                                        elif result[1][7:]=="yellow":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=True
                                            traffic_lights_red[int(result[1][3:6])]=False


                            else: 
                                if not(not((True not in self._track_occupancy[int(condition[0][3:5])+14:int(condition[0][7:9])+15]))):
                                    if result[0][5]!="=":
                                        if result[0][7:]=="green": 
                                            traffic_lights_green[int(result[0][3:6])]=True
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=False

                                        elif result[0][7:]=="red":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=False
                                            traffic_lights_red[int(result[0][3:6])]=True

                                        elif result[0][7:]=="yellow":
                                            traffic_lights_green[int(result[0][3:6])]=False
                                            traffic_lights_yellow[int(result[0][3:6])]=True
                                            traffic_lights_red[int(result[0][3:6])]=False

                                    elif result[0][5]=="=":
                                        if result[0][6:]=="green": 
                                            traffic_lights_green[int(result[0][3:5])]=True
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=False

                                        elif result[0][6:]=="red":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=False
                                            traffic_lights_red[int(result[0][3:5])]=True

                                        elif result[0][6:]=="yellow":
                                            traffic_lights_green[int(result[0][3:5])]=False
                                            traffic_lights_yellow[int(result[0][3:5])]=True
                                            traffic_lights_red[int(result[0][3:5])]=False

                                    if result[1][5]=="=":
                                        if result[1][6:]=="green": 
                                            traffic_lights_green[int(result[1][3:5])]=True
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=False

                                        elif result[1][6:]=="red":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=False
                                            traffic_lights_red[int(result[1][3:5])]=True

                                        elif result[1][6:]=="yellow":
                                            traffic_lights_green[int(result[1][3:5])]=False
                                            traffic_lights_yellow[int(result[1][3:5])]=True
                                            traffic_lights_red[int(result[1][3:5])]=False

                                    elif result[1][5]!="=":
                                        if result[1][7:]=="green": 
                                            traffic_lights_green[int(result[1][3:6])]=True
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=False

                                        elif result[1][7:]=="red":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=False
                                            traffic_lights_red[int(result[1][3:6])]=True

                                        elif result[1][7:]=="yellow":
                                            traffic_lights_green[int(result[1][3:6])]=False
                                            traffic_lights_yellow[int(result[1][3:6])]=True
                                            traffic_lights_red[int(result[1][3:6])]=False
                                        
                        else:
                            if not(not(True not in self._track_occupancy[(int(condition[0][3:5])+14):(int(condition[0][7:9])+15)]) or not(self._track_occupancy[int(condition[1][3:5])+14]==eval(condition[1][6:]))):
                                if result[0][6:]=="right": 
                                    switches[int(result[0][3:5])]=True

                                elif result[0][6:]=="left":
                                    switches[int(result[0][3:5])]=False

                    elif line[0]=="c": #crossings, here n=3 and m=1 for all cases
                        if condition[0][6]=="T": #then we all evals are True in condition, so we are doing "or" operation
                            if not(not(self._track_occupancy[int(condition[0][3:5])+14]==eval(condition[0][6:])) and not(self._track_occupancy[int(condition[1][3:5])+14]==eval(condition[1][6:])) and not(self._track_occupancy[int(condition[2][3:5])+14]==eval(condition[2][6:]))):
                                crossings[int(result[0][3:5])]=eval(result[0][6:])
                        else:
                            if not(not(self._track_occupancy[int(condition[0][3:5])+14]==eval(condition[0][6:])) or not(self._track_occupancy[int(condition[1][3:5])+14]==eval(condition[1][6:])) or not(self._track_occupancy[int(condition[2][3:5])+14]==eval(condition[2][6:]))):
                                crossings[int(result[0][3:5])]=eval(result[0][6:])  

        
        return traffic_lights_green, traffic_lights_yellow, traffic_lights_red, switches, crossings
    

    def compute_blueline(self, plc_file):
        if plc_file != "":
            file = open(plc_file, "r")

            lights = []
            switch = []
            for line in file:
                if line[0] == "t":
                    line = line.split(",")

                    l1 = line[0]
                    lights.append(l1)
                    l2 = line[1]
                    lights.append(l2)
                    l3 = line[2]
                    lights.append(l3)
                else:
                    switch = line

            block_ = []
            li = []
            for i in range(len(lights)):
                l = lights[i].split("=")
                block_.append(l[0])
                li.append(l[1])

            for i in range(len(lights)):
                if li[i] == "green":
                    self._traffic_lights_green[0][int(block_[i][3:]) - 1] = True
                    self._traffic_lights_yellow[0][int(block_[i][3:]) - 1] = False
                    self._traffic_lights_red[0][int(block_[i][3:]) - 1] = False
                elif li[i] == "red":
                    self._traffic_lights_green[0][int(block_[i][3:]) - 1] = False
                    self._traffic_lights_yellow[0][int(block_[i][3:]) - 1] = False
                    self._traffic_lights_red[0][int(block_[i][3:]) - 1] = True
                else:
                    self._traffic_lights_green[0][int(block_[i][3:]) - 1] = False
                    self._traffic_lights_yellow[0][int(block_[i][3:]) - 1] = True
                    self._traffic_lights_red[0][int(block_[i][3:]) - 1] = False

            if switch[5] == "r":
                self._switch_positions[0][0] = True
            else:
                self._switch_positions[0][0] = False




    def launch_tr_controller(self):
        from TrackControllerSoftware.programmerUI import programmer_UI
        from TrackControllerSoftware.UI import ui
        #from TrackControllerSoftware.testUI import test_ui

        self.ui_tr = programmer_UI(self)
        self.ui = ui(self)
        #self.ui = test_ui(self)

