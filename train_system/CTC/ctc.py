import copy
import sys
import time
import threading
from CTC.train import Train
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime


class CTC:
    def __init__(self, signals, test = False):
        # link signals class
        self.signals = signals
        self.sim_speed = 1
        self.start = time.time()
        self.t = self.start
        self.prev_time = time.time()
        self.sim_time = 0
        self.time_toggle = 1
        self.test = True
        self.arrive = 0

        # initialize variables
        self.numTrains = 0
        self.train = Train()
        self.trainList = []
        self.track = [[1] * 15, [1] * 76, [1] * 150]
        self.track_layout = {}
        self.light_status = {}
        self.maintenance = [[0] * 15, [0] * 76, [0] * 150]
        self.rail_status = [[0] * 15, [0] * 76, [0] * 150]
        self.red_id = []
        self.green_id = []

        # index = station, value = #passengers waiting
        self.station = []
        self.station.append(int(0))
        self.station.append(int(0))
        if not test:
            self.update()

    def handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):
        # update all values for all trains
        self.updateSwitch()
        self.calcAuthority()
        self.calcSuggestedSpeed()
        self.calcRoute()
        self.timer1()
        # upload to signals
        index = []
        for i, train in enumerate(self.trainList):
            if train.completed == 1 or train.location == -1:

                continue
                #self.trainList.pop(i + 1)
            # calculate what time the train should arrive in seconds
            h, m, s = train.arrival_time.split(":")
            arrival_time = int(h) * 3600 + int(m) * 60 + int(s)
            # find the time to the destination station
            time_to_station = self.timeToStation(train.destination, train.line)
            # print(train.train_id, train.authority, train.suggested_speed)
            # check if a train needs to be added to signals
            if len(self.signals.train_info) < i + 1:
                # check if it is time for train to be released
                if self.sim_time >= (arrival_time - time_to_station):
                    self.signals.train_info[i] = [
                        train.authority,
                        train.suggested_speed,
                        train.route,
                        train.location,
                    ]
                else:
                    if self.trainList[i].line == "Green":
                        self.signals.train_info[i] = ["G0", 0, [], 0]
                    elif self.trainList[i].line == "Red":
                        self.signals.train_info[i] = ["R0", 0, [], 0]
            else:
                if (self.sim_time >= arrival_time - time_to_station and self.signals.train_info[i][3] == 0):
                    self.signals.train_info[i] = [
                        train.authority,
                        train.suggested_speed,
                        train.route,
                        train.location,
                    ]
                elif self.signals.train_info[i][3] != 0:
                    self.signals.train_info[i][0] = train.authority
                    self.signals.train_info[i][1] = train.suggested_speed
                    self.signals.train_info[i][2] = train.route
                    train.location = self.signals.train_info[i][3]

        # read in from signals
        #  for i in range(len(self.track)):
        #             if len(self.signals.track_info) < i:
        #       self.signals.track_info[i] = self.track[i]

        # read passenger info from signals
        # for i in range(len(self.signals.train_info)):
        #     train.passengers = self.signals.train_info[i]

        # send the maintenance info for the three lines
        for i in range(len(self.maintenance)):
            for j in range(len(self.maintenance[i])):
                self.signals.track_maintenance[i][j] = self.maintenance[i][j]

        # read in occupancies
        for i in range(len(self.signals.track_occupancy)):
            for j in range(len(self.signals.track_occupancy[i])):
                self.track[i][j] = self.signals.track_occupancy[i][j]

        # read in track failure
        for i in range(len(self.signals.rail_status)):
            for j in range(len(self.signals.rail_status[i])):
                self.rail_status[i][j] = self.signals.rail_status[i][j]

        # read in the track layout
        self.light_status = self.signals.traffic_lights_green
        self.track_layout_green = self.signals.track_layout_green
        self.track_layout_red = self.signals.track_layout_red

        # send sim time to signals
        self.signals.sim_time = self.sim_time

        threading.Timer(0.1, self.update).start()

    def timer1(self):
        # increase the time by 1*sim_speed
        if self.time_toggle:
            elapsed = time.time() - self.prev_time
            self.sim_time += elapsed * self.sim_speed
            self.prev_time = time.time()
            self.timeformatted()
        else:
            self.prev_time = time.time()

    def timeformatted(self):
        # format the time into HH:MM:SS
        return time.strftime("%H:%M:%S", time.gmtime(self.sim_time))

    def editTrack(self, line: int, index: int, value: int):
        self.maintenance[line][index] = not value
        # print(self.maintenance[line])

    def editStation(self, index: int, value: int):
        self.station[index] = value

    def editTrain(self, id: int, destination: int, arrival_time: str):
        self.trainList[id].destination = int(destination)
        self.trainList[id].destinationList.clear()
        if len(self.trainList[id].destinationList) == 0:
            if self.trainList[id].line == "Green":
                self.trainList[id].destinationList.append(56)
            elif self.trainList[id].line == "Red":
                self.trainList[id].destinationList.append(16)
            self.trainList[id].destinationList.append(0)
        self.trainList[id].arrival_time = arrival_time

    def editTrain2(self, id: int, loc: int, passengers: int):
        self.trainList[id].location = loc
        self.trainList[id].passengers = passengers

    def addTrain(self, destination: int, arrival_time: str, line: str):
        New = Train()
        New.line = line
        New.setTrainID(self.numTrains + 1)
        New.setDestination(destination)

        #add the final station for each line
        if New.line == "Green":
            New.destinationList.append(56)
        #elif New.line == "Red":
            #New.destinationList.append(16)

        #add yard after the final station
        New.destinationList.append(0)

        #set arrival time
        New.setArrival_time(arrival_time)

        #set starting location
        if line == "Green":
            New.location = 63
            self.green_id.append(New.train_id)
        elif line == "Red":
            New.location = 9
            self.red_id.append(New.train_id)

        #add to list
        self.trainList.append(New)
        self.numTrains = self.numTrains + 1
    def addTrain2(self, destinationList: [], arrival_time: str, line: str):
        New = Train()
        New.setTrainID(self.numTrains + 1)
        New.line = line
        #set destination to the first element and remove
        New.setDestination(int(destinationList.pop(0)))

        #append the remaining destinations to the list
        for i in destinationList:
            New.destinationList.append(int(i))

        if line == "Green":
            New.destinationList.append(int(56))
        New.destinationList.append(int(0))
        New.setArrival_time(arrival_time)

        if line == "Green":
            New.location = 63
            self.green_id.append(New.train_id)
        elif line == "Red":
            New.location = 9
            self.red_id.append(New.train_id)

        self.trainList.append(New)
        self.numTrains = self.numTrains + 1

    def calcAuthority(self):

        # calc authority for every train in list
        for train in self.trainList:
            if train.location == -1:
                train.completed = 1
                continue
            if train.line == "Green":
                # green line
                # authority is the lesser of, next intersection, destination station, closed track block
                # interections = [76, 150, ]
                # update for every intersection
                # coming from yard
                if train.location == 63:  # and switch green
                    train.authority = "G76"

                #between 63-76
                elif 63 < train.location < 76 and 63 < train.destination < 76:
                    train.authority = "G" + str(train.destination)

                #destination outside of 63-76
                elif 63 < train.location < 76 and (63 > train.destination or train.destination > 76):
                    train.authority = "G76"

                #at intersection
                elif train.location == 76 and bool(self.light_status[76][0]):
                    train.authority = "G100"

                elif 77 <= train.location <= 85 and train.prevBlock < train.location:
                    if train.destination == 77:
                        train.authority = "G77"
                    else:
                        train.authority = "G100"

                elif 77 <= train.location <= 85 and train.prevBlock > train.location:
                    if train.destination == 77:
                        train.authority = "G77"
                    else:
                        train.authority = "G150"

                #between 77-99
                elif 85 < train.location < 99 and 63 < train.destination < 76:
                    train.authority = "G" + str(train.destination)



                #destination outside of 77-99
                elif 85 < train.location < 99 and (77 > train.destination or train.destination > 99):
                    train.authority = "G100"

                #at intersection
                elif train.location == 100 and self.light_status[100][0]:
                    train.authority = "G150"

                #between 101-149
                elif 101 < train.location < 149 and 101 < train.destination < 149:
                    train.authority = "G" + str(train.destination)

                # destination outside of 101-149
                elif 101 < train.location < 149 and (101 > train.destination or train.destination > 149):
                    train.authority = "G150"

                # at intersection
                elif train.location == 150 and self.light_status[150][0]:
                    train.authority = "G1"

                # at intersection
                elif train.location == 1 and self.light_status[1][0]:
                    train.authority = "G57"

                # between 1-57
                elif 1 < train.location < 57 and 1 < train.destination < 57:
                    train.authority = "G" + str(train.destination)

                # destination outside of 1-57
                elif 1 < train.location < 57 and (1 > train.destination or train.destination > 57):
                    train.authority = "G57"

                # yard
                elif (train.location == 57 and not self.signals.switch_positions_green[57] and train.destination == 0):
                    train.authority = "Gyard"
                    # train complete remove

                elif (train.location == 57 and self.signals.switch_positions_green[57] and train.destination != 0):
                    train.authority = "G76"

                # print(train.location, self.signals.switch_positions_green[57], train.destination)

                # check for track error
                for t in range(150):
                    # print("BLock:", t+1, "Status:", self.maintenance[2][t] or self.rail_status[2][t])
                    # if error found authority can only be as far as a block behind closure
                    if self.maintenance[2][t] or self.rail_status[2][t]:
                        if 63 <= train.location <= 150 and 63 <= t <= 150:
                            train.authority = "G" + str(train.location)
                        elif 1 <= train.location <= 62 and 1 <= t <= 62:
                            train.authority = "G" + str(train.location)

            # red line
            elif train.line == "Red":
                # base case
                if train.location == 9 and train.destination == 7:
                    train.authority = "R7"
                elif train.location == 9:
                    train.authority = "R1"
                elif 1 < train.location < 9 and train.destination != 7:
                    train.authority = "R1"

                # waiting at first intersection
                if train.location == 1 and self.signals.traffic_lights_red[1][0]:
                    if train.destination == 0:
                        train.authority = "R66"
                    else:
                        train.authority = "R" + str(train.destination)

                # between intersections
                if 66 > train.location >= 16:
                    if 66 > train.destination >= 16:
                        if (train.destination < train.location and train.prevBlock < train.location):
                            train.authority = "R66"
                        else:
                            train.authority = "R" + str(train.destination)

                    elif train.prevBlock < train.location:
                        train.authority = "R66"
                    elif train.prevBlock > train.location and train.destination == 0 and train.location != 16:
                        train.destination = 16
                        train.destinationList.append(0)
                        train.authority = "R16"
                    elif train.prevBlock > train.location and train.destination == 0:
                        train.authority = "Ryard"

                # check for track error
                for t in range(76):
                    # print("BLock:", t+1, "Status:", self.maintenance[2][t] or self.rail_status[2][t])
                    # if error found authority can only be as far as a block behind closure
                    if self.maintenance[1][t] or self.rail_status[1][t]:
                        print(t)
                        if t == 15:
                            train.authority = "R" + str(train.location)
                        if t == 52:
                            train.authority = "R" + str(train.location)
                        if 1 <= train.location <= 9 and 1 <= t <= 9:
                            train.authority = "R" + str(train.location)
                        elif 16 <= train.location <= 66 and 16 <= t <= 66:
                            train.authority = "R" + str(train.location)


                # last intersection
                if (train.location == 66 and self.signals.traffic_lights_red[66][0] == True):
                    if train.destination == 0:
                        train.authority = "Ryard"
                    else:
                        train.authority = "R" + str(train.destination)

            elif train.line == "Blue":
                # train enters from yard
                if train.location == 1:
                    train.authority = "B5"
                # auth intersection(yard) to station B
                elif (
                    train.location == 5 and train.destination == 1
                ):  # and #light status green:
                    train.authority = "B10"
                # auth intersection(yard) to station C
                elif (
                    train.location == 5 and train.destination == 2
                ):  # and light status green:
                    train.authority = "B15"

                # from station B to intersection
                if train.location == 10:
                    train.authority = "B6"
                # auth station B to station C
                elif (
                    train.location == 6 and train.destination == 2
                ):  # and #light status green:
                    train.authority = "B15"
                # auth station B to yard
                elif (
                    train.location == 6 and train.destination == 0
                ):  # and light status green:
                    train.authority = "B1"

                # from station C to intersection
                if train.location == 15:
                    train.authority = "B11"
                # auth station C to station B
                elif (
                    train.location == 11 and train.destination == 1
                ):  # and #light status green:
                    train.authority = "B10"
                # auth station C to yard
                elif (
                    train.location == 11 and train.destination == 0
                ):  # and light status green:
                    train.authority = "B1"

                else:
                    train.authority = "B1"
            if train.location != train.destination:
                train.prevBlock = train.location
    def getThroughput(self, line: int):
        return str(round(self.signals.ticketSales[line] / (self.sim_time) * 3600))
    def calcRoute(self):
        for train in self.trainList:
            if 0:
                # yard to station 1/2
                if train.location == 1 and train.destination == 1:
                    train.route = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                elif train.location == 1 and train.destination == 2:
                    train.route = [1, 2, 3, 4, 5, 11, 12, 13, 14, 15]

                # station 1/2 back to yard
                elif train.location == 10 and train.destination == 0:
                    train.route = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
                elif train.location == 15 and train.destination == 0:
                    train.route = [15, 14, 13, 12, 11, 5, 4, 3, 2, 1]

                # station 1/2 to station 1/2
                elif train.location == 10 and train.destination == 2:
                    train.route = [10, 9, 8, 7, 6, 11, 12, 13, 14, 15]
                elif train.location == 15 and train.destination == 1:
                    train.route = [15, 14, 13, 12, 11, 6, 7, 8, 9, 10]
            # red line
            elif train.line == "Red":
                pass

            # green line
            elif train.line == "Green" and len(train.route) == 0:
                # green line route information
                for i in range(63, 100):
                    train.route.append(i)
                for i in range(85, 77, -1):
                    train.route.append(i)
                for i in range(101, 150):
                    train.route.append(i)
                for i in range(28, 1, -1):
                    train.route.append(i)
                for i in range(13, 57):
                    train.route.append(i)

    def findNextTrain(self, id: int, line: str):
        distance = 75
        if id == 1:
            return 75

        #green line
        if line == "Green":
            #check trains in green index
            if self.green_id.index(id) != 0:
                #find the next train in green list
                next = self.green_id.index(id) - 1
                next_id = self.green_id[next] - 1
                #distance to the next train
                distance = abs(self.trainList[next_id].location - self.trainList[id - 1].location)
            else:
                return 75
        #red line
        elif line == "Red":
            #check trains in red
            if self.red_id.index(id) != 0:
                #find next train in red list
                next = self.red_id.index(id) - 1
                next_id = self.red_id[next] - 1
                #distance to the next train
                distance = abs(self.trainList[next_id].location - self.trainList[id - 1].location)
            else:
                return 75

        return distance

    def setSwitch(self, position: str, switchnum: int, line: str):
        print(position, switchnum, line)
        # convert to true or false
        if position == "Left":
            pos = False
        elif position == "Right":
            pos = True

        # add to list
        temp = [switchnum, pos]

        # edit if already in changes
        if line == "Green":
            for i in self.signals.switch_changes_green:
                if i[0] == switchnum:
                    i[1] == pos
        elif line == "Red":
            for i in self.signals.switch_changes_red:
                if i[0] == switchnum:
                    i[1] == pos

        if line == "Green":
            # append for line if the block is in maintenance
            if self.maintenance[2][switchnum - 1]:
                self.signals.switch_changes_green.append(temp)
        elif line == "Red":
            if self.maintenance[1][switchnum - 1]:
                self.signals.switch_changes_red.append(temp)
        print(self.signals.switch_changes_red, self.signals.switch_changes_green)
    def updateSwitch(self):
        # holds the indexes of the blocks in maintenance
        list1 = []
        list2 = []

        # find maintenance index red line
        for i in range(len(self.maintenance[1])):
            if self.maintenance[1][i] == True:
                list1.append(i + 1)
        # remove changes if not in maintenance
        for i in self.signals.switch_changes_red:
            if i[0] not in list1:
                self.signals.switch_changes_red.remove(i)

        # green line
        for i in range(len(self.maintenance[2])):
            if self.maintenance[2][i] == True:
                list1.append(i + 1)

        for i in self.signals.switch_changes_green:
            if i[0] not in list1:
                self.signals.switch_changes_green.remove(i)

    def timeToStation(self, station_id: int, line: str):
        t = 0
        # time to station = block length/speed limit for each block until destination is reached

        # error check
        if line == "Green" and len(self.track_layout_green.keys()) == 0:
            return 200
        elif line == "Red" and len(self.track_layout_red.keys()) == 0:
            return 200

        # green line calculations
        if line == "Green":
            # if destination is on first section of the track
            if 63 <= station_id <= 150:
                for i in range(63, station_id):
                    t += float(self.track_layout_green[i][1]) / self.track_layout_green[i][3]


            # otherwise destination is on the second section of the track
            else:
                for i in range(63, 150):
                    t += float(self.track_layout_green[i][1]) / self.track_layout_green[i][3]
                for i in range(1, station_id):
                    t += float(self.track_layout_green[i][1]) / self.track_layout_green[i][3]

        # red line calculation
        elif line == "Red":
            if 9 <= station_id <= 1:
                for i in range(9, station_id, -1):
                    t += float(self.track_layout_red[i][1]) / self.track_layout_red[i][3]

            # otherwise destination is on the second section of the track
            else:
                for i in range(9, 0, -1):
                    t += float(self.track_layout_red[i][1]) / self.track_layout_red[i][3]
                for i in range(16, 76):
                    t += float(self.track_layout_red[i][1]) / self.track_layout_red[i][3]

        # convert from hours to seconds
        return t * 3600

    def calcSuggestedSpeed(self):
        #update all trains

        for train in self.trainList:
            # base speed
            if train.location == -1:
                train.completed = 1
                continue
            train.suggested_speed = 50

            #authority to yard case
            if train.authority == "Gyard":
                train.suggested_speed = 10
                return
            if train.authority == "Ryard":
                train.suggested_speed = int(self.track_layout_red[train.location - 1][3])
                return

            # green line
            if train.line == "Green":
                # check if empty
                if len(self.track_layout_green.keys()) == 0:
                    speed_limit = 50
                # get speed limit
                else:
                    speed_limit = int(self.track_layout_green[train.location - 1][3])  # self.track_layout[train.location][3]

            elif train.line == "Red":
                # check if empty
                if len(self.track_layout_red.keys()) == 0:
                    speed_limit = 50
                # get speed limit
                else:
                    speed_limit = int(self.track_layout_red[train.location - 1][3])  # self.track_layout[train.location][3]

            # calculate how many increments
            increments = speed_limit / 10

            # find distance to next train, destination, and authority
            distance = self.findNextTrain(train.train_id, train.line)

            #emergency case for train 1 block ahead
            if distance <= 2:
                #green line
                if train.line == "Green":
                    train.authority = "G" + str(train.location)
                #red line
                elif train.line == "Red":
                    train.authority = "R" + str(train.location)
                train.suggested_speed = 0
                continue

            #distance to the location
            distance2 = abs(int(train.destination) - train.location)

            #trim authority for block
            if len(train.authority) == 3:
                auth = train.authority[1:3]
            else:
                auth = train.authority[1:4]

            #distance to end of authority
            if len(auth) > 0:
                distance3 = abs(float(int(auth)) - train.location)
            else:
                distance3 = 5

            # pick the min of the distances
            if distance3 <= distance2:
                if distance3 <= distance:
                    distance = distance3
            if distance2 <= distance3:
                if distance2 <= distance:
                    distance = distance2

            # if distance more than safe speed = speed limit
            if distance > increments:
                train.suggested_speed = speed_limit

            # start slowing down based on how close
            elif distance <= increments:
                train.suggested_speed = speed_limit - 10 * (increments - distance)

            # start time for dwell
            if int(train.location) == int(train.destination) and self.test:
                train.suggested_speed = 0
                self.arrive = self.sim_time
                self.test = False

            # check dwell time
            if train.location == train.destination and not self.test:
                dwell_time = self.sim_time - self.arrive
                # dwell over set next destination
                if dwell_time >= 60:
                    train.destination = train.destinationList.pop(0)
                    self.test = True

    def getTrainList(self):
        return self.trainList

    def getTrackList(self, line: int):
        t = [[1] * 15, [1] * 76, [1] * 150]
        for i in range(len(self.track)):
            for j in range(len(self.track[i])):
                if self.maintenance[i][j] or self.rail_status[i][j]:
                    t[i][j] = int(2)
                elif self.track[i][j] == 0:
                    t[i][j] = int(0)
                elif self.track[i][j] == 1:
                    t[i][j] = int(1)

        return t[line]

    def getStationList(self):
        return self.station

    def getStationCount(self, id: int):
        return self.station[id]

    def getArrivalTime(self, id: int):
        return self.trainList(id).arrival_time

    def timer(self):
        self.time = "00:00:00"

    def launch_main_ui(self):
        from CTC.main_ui import mainUI

        self._mui = mainUI(self)

    def launch_test_ui(self):
        from CTC.test_ui import testUI

        self._tui = testUI(self)
