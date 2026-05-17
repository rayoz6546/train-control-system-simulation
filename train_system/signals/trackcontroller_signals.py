# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 11:46:07 2023

@author: RAYAN
"""

class TrackCTCSignals:
    def __init__(self) -> None:
        self.num_lights = 4

        #ctc -> wayside
        self.train_info = {} #key = train #, [0]auth [1]sug speed [2]route [3]location [4]passenger info
        self.authority = [] #index = train#, value = authority
        self.suggested_speed = [] #index = train#, value = speed
        self.route = [] #index = train#, contains a list holding block numbers in order
        self.sim_time = 0 #time in seconds from start

        #wayside -> ctc
        self.track_layout_red = {}
        self.track_layout_green = {}
        self.track_occupancy = [[0]*15, [0]*76, [0]*150]
        self.track_maintenance = [[0]*15, [0]*76, [0]*150]
        self.rail_status = [[0] * 15, [0] * 76, [0] * 150]
        self.light_status = {} #key = block number of the light #0 green 1 yellow 2 red
        self.light_status[76] = 1




        self.traffic_lights_green = {}   # example: {63:[False,True,False]} ==> yellow lights on block 63 (index0 in list--> green, index1-->yellow, index2-->red)
        self.traffic_lights_red = {}

        self.switch_positions_green = {}  # example: {63: True} ==> switch on block 63 is right
        self.switch_positions_red = {}

        self.switch_changes_green = [] #list containing lists[block #, new status]
        self.switch_changes_red = []  # list containing lists[block #, new status]

        self.ticketSales = [0, 0, 0] #list of ticket sales per line, 0:blue, 1:green, 2:red