import sys, os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from signals.track_signals import TrackSignals
from signals.track_to_train_signals import TracktoTrainSignals
import threading
import random


class TrackModel:
    # TODO find issue with speed limit
    def __init__(self, track_signals: TrackSignals):
        self.curr_time = time.time()
        self.prev_time = self.curr_time
        self.lineChoice = ""
        # TODO figure out how to keep track of trains, list w/ index train then value is curr block number?
        self.trainsGreen = (
            {}
        )  # dict key train number from CTC, list of trackAuth [0], current block[1], prev block[2],distance traveled[3], CTC auth[4]
        self.trainsRed = {}
        signals = track_signals
        self.brokenRail_blue = [0] * 15
        self.circuitFailure_blue = [
            0
        ] * 15  # FIXME update with better initalization method
        self.powerFailure_blue = [0] * 15

        self.blueLine_set = {}
        self.blueSwitches_set = {}
        self.switchNextBlocks_blue = {}
        self.blueLineOccupancy = [0] * 15  # send list of 0 unoccupied, 1 occupied
        self.blueLineTrackFailures = []  # list of blue line track failures
        self.stations_blue = {}

        self.greenLine_set = {}
        self.greenSwitches_set = {}
        self.switchNextBlocks_green = {}
        self.stations_green = {}
        self.stationPeeps_green = {}
        self.greenLineOccupancy = [0] * 150
        self.greenLineDirection = [
            0
        ] * 150  # direction of travel, 1 north, 2 east, 3 south, 4 west

        self.redLine_set = {}
        self.redSwitches_set = {}
        self.switchNextBlocks_red = {}
        self.stations_red = {}
        self.stationPeeps_red = {}
        self.redLineOccupancy = [0] * 76
        self.redLineDirection = [
            0
        ] * 76  # direction of travel, 1 north, 2 east, 3 south, 4 west

        self.greenAccelLimit = -1
        self.redAccelLimit = -1
        self.blueAccelLimit = -1

        self.authorityInput = ""
        self.authorityOutput = 0
        self.commandedSpeed = 0
        self.lights = {}
        self.crossings = {}
        self.heating = "Off"  # if temp below 35 heat track

        # TODO have class handle different instances of train models w/ diff current speeds
        self.distanceTraveled = 0  # distance traveled per block
        self.currentBlock = 0
        self.previousBlock = 0
        self.newPeeps = 0

        self._signals = signals
        self.main_ui = None
        self.test_ui = None

        self.update()

    def update(self):
        # self.setCommandedSpeed(self._signals.commandedSpeed)
        self.calculateOccupancy()
        # self.updateAuthority()
        # self.updateAuthorityTrainsGreen()
        # self.updateAuthorityTrainsRed()
        # self.calcOccupancyGreen()
        # self.calcOccupancyRed()
        # self._signals.lineChoice = self.lineChoice
        threading.Timer(0.1, self.update).start()

    def getTrackLayout(self, line):  # send track layout based on what line desired
        # send track layout info
        if line == "blue":
            return self.blueLine_set

    def setRedLine(self, redLine):
        """takes a red line as a set with block number as key, list as value"""
        self.redLine_set = redLine
        self._signals.redLine_set = redLine
        self.setTracktoTrain_red(redLine)

    def getRedLine(self):
        return self._signals.redLine_set

    def setBlueLine(self, blueLine):
        """takes the line as a set with block number as key, list as value"""
        self.blueLine_set = blueLine
        self._signals.blueLine_set = blueLine
        self.setTracktoTrain_blue(
            blueLine
        )  # set values for train model to receive initially

    def getBlueLine(self):
        return self._signals.blueLine_set

    def setGreenLine(self, greenLine):
        """takes the line as a set with block number as key, list as value"""
        self.greenLine_set = greenLine
        self._signals.greenLine_set = greenLine
        self.setTracktoTrain_green(
            greenLine
        )  # set values for train model to receive initially

    def getGreenLine(self):
        return self._signals.greenLine_set

    def getBrokenRail_blue(self):
        return self._signals.brokenRail_blue

    def getBrokenRail_green(self):
        return self._signals.brokenRail_green

    def getBrokenRail_red(self):
        return self._signals.brokenRail_red

    def setBrokenRail_blue(self, blockNumber, broken: bool):
        self._signals.brokenRail_blue[blockNumber] = broken

    def setBrokenRail_green(self, blockNumber, broken: bool):
        self._signals.brokenRail_green[blockNumber] = broken

    def setBrokenRail_red(self, blockNumber, broken: bool):
        self._signals.brokenRail_red[blockNumber] = broken

    def setCircuitFailure_blue(self, blockNumber, broken: bool):
        self._signals.circuitFailure_blue[blockNumber] = broken

    def setCircuitFailure_green(self, blockNumber, broken: bool):
        self._signals.circuitFailure_green[blockNumber] = broken

    def setCircuitFailure_red(self, blockNumber, broken: bool):
        self._signals.circuitFailure_red[blockNumber] = broken

    def getCircuitFailure_blue(self):
        return self._signals.circuitFailure_blue

    def getCircuitFailure_green(self):
        return self._signals.circuitFailure_green

    def getCircuitFailure_red(self):
        return self._signals.circuitFailure_red

    def setPowerFailure_blue(self, blockNumber, broken: bool):
        self._signals.powerFailure_blue[blockNumber] = broken

    def setPowerFailure_green(self, blockNumber, broken: bool):
        self._signals.powerFailure_green[blockNumber] = broken

    def setPowerFailure_red(self, blockNumber, broken: bool):
        self._signals.powerFailure_red[blockNumber] = broken

    def getPowerFailure_blue(self):
        return self._signals.powerFailure_blue

    def getPowerFailure_green(self):
        return self._signals.powerFailure_green

    def getPowerFailure_red(self):
        return self._signals.powerFailure_red

    def initialRedSwitches(self, switches):
        """pass inital values of all switches"""
        self.redSwitches_set = switches
        self._signals.redSwitches_set = switches

    def set_RedSwitch(self, switchNumber, position):
        """switchNumber: index of the switch, position: 0 left, 1 right"""
        self.redSwitches_set[switchNumber] = position

    def get_redSwitches(self):
        return self._signals.redSwitches_set

    def initialBlueSwitches(self, switches):
        """pass inital values of all switches"""
        self.blueSwitches_set = switches
        self._signals.blueSwitches_set = switches

    def set_BlueSwitch(self, switchNumber, position):
        """switchNumber: index of the switch, position: 0 left, 1 right"""
        self.blueSwitches_set[switchNumber] = position

    def get_blueSwitches(self):
        return self._signals.blueSwitches_set

    def get_blueSwitch(self, index):
        return self._signals.blueSwitches_set[index]

    def initialGreenSwitches(self, switches):
        """pass inital values of all switches"""
        self.greenSwitches_set = switches
        self._signals.greenSwitches_set = switches

    def set_GreenSwitch(self, switchNumber, position):
        """switchNumber: index of the switch, position: 0 left, 1 right"""
        self.greenSwitches_set[switchNumber] = position

    def get_greenSwitches(self):
        return (
            self._signals.switch_positions_green
        )  # example: {63: True} ==> switch on block 63 is left

    def get_greenLights(self):
        """example: {63:[False,True,False]} ==> yellow lights on block 63 (index0 in list--> green, index1-->yellow, index2-->red)"""
        return self._signals.traffic_lights_green

    def get_greenLineLight(self, blockNumber):
        """returns string of green, yellow, red if set else N/A"""
        if blockNumber in self._signals.traffic_lights_green:
            lightList = self._signals.traffic_lights_green[blockNumber]
            if lightList[0] == 1:
                return "Green"
            elif lightList[1] == 1:
                return "Yellow"
            else:
                return "Red"
        else:
            return "N/A"

    def get_redLineLight(self, blockNumber):
        """returns string of green, yellow, red if set else N/A"""
        if blockNumber in self._signals.traffic_lights_red:
            lightList = self._signals.traffic_lights_red[blockNumber]
            if lightList[0] == 1:
                return "Green"
            elif lightList[1] == 1:
                return "Yellow"
            else:
                return "Red"
        else:
            return "N/A"

    def get_greenSwitch(self, index):
        """return switch position at block number"""
        return self._signals.greenSwitches_set[index]

    def setTracktoTrain_blue(self, blueLine):
        """set signals for inital loading of train: sets values (grade, speed limit, elevation, station side)"""
        detailsforModel = {}
        detailsforController = {}
        for i in range(len(blueLine)):
            blockDetails = blueLine[i]
            detailsforModel[i] = (
                blockDetails[2],
                blockDetails[6],
                "UNDERGROUND" in blockDetails[4],
            )  # grade, elev, underground
            detailsforController[i] = (
                blockDetails[3],
                blockDetails[5],
                "UNDERGROUND" in blockDetails[4],
            )  # speed limit, station side : string

        self._signals.track_grade_elev_blue = detailsforModel  # dict key = block number, value is tuple of (grade, elevation), TODO add underground + other lines
        self._signals.track_speedLim_stat_blue = detailsforController

    def setTracktoTrain_green(self, greenLine):
        """set signals for inital loading of train: sets values (grade, speed limit, elevation, station side)"""
        detailsforModel = {}
        detailsforController = {}
        for i in range(len(greenLine)):
            blockDetails = greenLine[i]
            detailsforModel[i + 1] = (
                blockDetails[2],
                blockDetails[6],
                "UNDERGROUND" in blockDetails[4],
            )  # grade, elev, underground
            detailsforController[i + 1] = (
                blockDetails[3],
                blockDetails[5],
                "UNDERGROUND" in blockDetails[4],
            )  # speed limit, station side : string

        self._signals.track_grade_elev_green = detailsforModel  # dict key = block number, value is tuple of (grade, elevation), TODO add underground + other lines
        self._signals.track_speedLim_stat_green = detailsforController

    def setTracktoTrain_red(self, redLine):
        """set signals for inital loading of train: sets values (grade, speed limit, elevation, station side)"""
        detailsforModel = {}
        detailsforController = {}
        for i in range(len(redLine)):
            blockDetails = redLine[i]
            detailsforModel[i + 1] = (
                blockDetails[2],
                blockDetails[6],
                "UNDERGROUND" in blockDetails[4],
            )  # grade, elev, underground
            detailsforController[i + 1] = (
                blockDetails[3],
                blockDetails[5],
                "UNDERGROUND" in blockDetails[4],
            )  # speed limit, station side : string

        self._signals.track_grade_elev_red = detailsforModel  # dict key = block number, value is tuple of (grade, elevation), TODO add underground + other lines
        self._signals.track_speedLim_stat_red = detailsforController

    def setOccupancy(self, line, blockNumber, occupied):
        if "blue" in line:
            self.blueLineOccupancy[blockNumber] = occupied
        elif "red" in line:
            self.redLineOccupancy[blockNumber] = occupied
        elif "green" in line:
            self.greenLineOccupancy[blockNumber] = occupied
        self.currentBlock = blockNumber

    def getDirection(self, line, index):
        """returns NESW str direction at block index (index is blockNumber-1)"""
        direction = 0
        if "g" in line:
            direction = self.greenLineDirection[index]
        elif "r" in line:
            direction = self.redLineDirection[index]

        if direction == 4:
            return "West"
        elif direction == 3:
            return "South"
        elif direction == 2:
            return "East"
        else:
            return "North"

    def getPassengersBoarding(self, block):
        """block is which station, return number of people at station"""
        if "g" in self.lineChoice and block in self.stationPeeps_green:
            return self.stationPeeps_green[block]
        elif "r" in self.lineChoice and block in self.stationPeeps_green:
            return self.stationPeeps_green[block]

    def calculateOccupancy(self):
        # TODO make general to blocks and use current block number
        # get current train speed
        # self.train_info = {}  #key = train #, [0]auth [1]sug speed [2]route [3]location
        if len(self._signals.train_info) > 0:
            keys = list(self._signals.train_info.keys())
            # print(f'print train info location: {self._signals.train_info[0][3]}')
            # check green trains
            for trainKey in keys:
                # print(f'train key for occ: {trainKey}')
                if (
                    "G" in self._signals.train_info[trainKey][0]
                ):  # check if train in Green or red line
                    if trainKey in self.trainsGreen:
                        # print(f'auth update key {trainKey}: {self._signals.train_info[trainKey][0]} ')
                        self.trainsGreen[trainKey][4] = self._signals.train_info[
                            trainKey
                        ][
                            0
                        ]  # update str auth from CTC
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].time = self._signals.time
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].commandedSpeed = self._signals.train_info[trainKey][1]
                        if (
                            self._signals.train_info[trainKey][3] == 63
                        ):  # check if on starting block
                            self.trainsGreen[trainKey][1] = 63
                            self.greenLineOccupancy[
                                62
                            ] = 1  # subtract 1 for correct index
                            self._signals.greenLineOccupancy = self.greenLineOccupancy
                            self._signals.signals_trackToTrain[
                                trainKey
                            ].currentBlock = self.trainsGreen[trainKey][1]
                    else:
                        self.trainsGreen[trainKey] = [
                            0,
                            self._signals.train_info[trainKey][3],
                            0,
                            0,
                            self._signals.train_info[trainKey][0],
                            self._signals.time,
                            0,
                        ]  # set auth [0], current block[1], prev block[2], distance traveled[3], CTC auth[4], prevTime [5], new people on train [6]
                        self._signals.signals_trackToTrain[
                            trainKey
                        ] = TracktoTrainSignals()  # set train signals
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].track_grade_elev_green = self._signals.track_grade_elev_green
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].track_speedLim_stat_green = (
                            self._signals.track_speedLim_stat_green
                        )
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].lineChoice = "green"
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].time = self._signals.time
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].commandedSpeed = self._signals.train_info[trainKey][1]
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].currentBlock = self.trainsGreen[trainKey][1]

                elif (
                    "R" in self._signals.train_info[trainKey][0]
                ):  # check if train in Green or red line
                    if trainKey in self.trainsRed:
                        # print(f'updating auth: {self._signals.train_info[trainKey][0]} ')
                        self.trainsRed[trainKey][4] = self._signals.train_info[
                            trainKey
                        ][
                            0
                        ]  # update str auth from CTC
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].time = self._signals.time
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].commandedSpeed = self._signals.train_info[trainKey][1]
                        if (
                            self._signals.train_info[trainKey][3] == 9
                        ):  # check if on starting block
                            self.trainsRed[trainKey][1] = 9
                            self.redLineOccupancy[8] = 1  # subtract 1 for correct index
                            self._signals.redLineOccupancy = self.redLineOccupancy
                            self._signals.signals_trackToTrain[
                                trainKey
                            ].currentBlock = self.trainsRed[trainKey][1]
                    else:
                        self.trainsRed[trainKey] = [
                            0,
                            self._signals.train_info[trainKey][3],
                            0,
                            0,
                            self._signals.train_info[trainKey][0],
                            self._signals.time,
                            0,
                        ]  # set auth [0], current block[1], prev block[2], distance traveled[3], CTC auth[4], prevTime [5], new people on train [6]
                        self._signals.signals_trackToTrain[
                            trainKey
                        ] = TracktoTrainSignals()  # set train signals
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].track_grade_elev_red = self._signals.track_grade_elev_red
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].track_speedLim_stat_red = (
                            self._signals.track_speedLim_stat_red
                        )
                        self._signals.signals_trackToTrain[trainKey].lineChoice = "red"
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].time = self._signals.time
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].commandedSpeed = self._signals.train_info[trainKey][1]
                        self._signals.signals_trackToTrain[
                            trainKey
                        ].currentBlock = self.trainsRed[trainKey][1]
                self.calcOccupancyGreen()
                self.calcOccupancyRed()
                self.updateAuthorityTrainsGreen()
                self.updateAuthorityTrainsRed()
            # if self._signals.train_info[0][3] == 63: #if train on first block new train TODO update for mult trains
            #     self.greenLineOccupancy[63-1] = 1 #subtract 1 for correct index
            #     self.currentBlock = 63
            #     self._signals.currentBlock = self.scurrentBlock
            #     self.updateAuthority()

    def calcOccupancyGreen(self):
        keys = list(self.trainsGreen.keys())
        for (
            key
        ) in (
            keys
        ):  # value list: trackAuth [0], current block[1], prev block[2],distance traveled[3], CTC auth[4]
            curr_time = self._signals.time / (60 * 60)  # time from CTC seconds passed
            hrsPassed = curr_time - self.trainsGreen[key][5]  # hours passed
            self.trainsGreen[key][5] = curr_time  # update prev time

            # trainSpeed = self._signals.actual_velocity
            trainSpeed = self._signals.signals_trackToTrain[key].actual_velocity
            self.trainsGreen[key][3] = self.trainsGreen[key][3] + (
                hrsPassed * trainSpeed
            )  # update distance traveled for train
            # print(f'key: {key}, distance traveled: {self.trainsGreen[key][3]}, vel: {self._signals.signals_trackToTrain[key].actual_velocity}')

            # for green line
            # print(f'key:{key}, self.trainsGreen[key][1]: {self.trainsGreen[key][1]}')
            if (
                self.trainsGreen[key][1] > 0
                and self.trainsGreen[key][3]
                >= self.greenLine_set[self.trainsGreen[key][1] - 1][1]
            ):  # train[1] is current block
                oldBlock = self.trainsGreen[key][1]
                self.greenLineOccupancy[oldBlock - 1] = 0
                self.trainsGreen[key][3] = (
                    self.trainsGreen[key][3]
                    - self.greenLine_set[self.trainsGreen[key][1] - 1][1]
                )  # reset distancetraveled
                currBlock = self.trainsGreen[key][1]
                prevBlock = self.trainsGreen[key][2]
                newBlock = 0
                if currBlock == 100:  # 100 goes to 85
                    newBlock = 85
                elif currBlock == 150:  # 150 to 28
                    newBlock = 28
                elif currBlock == 1:  # 150 to 28
                    newBlock = 13
                elif (
                    currBlock <= 28 or (currBlock > 77 and currBlock <= 85)
                ) and prevBlock > currBlock:  # 28 -1 or N block: count blocks down
                    newBlock = currBlock - 1
                else:
                    newBlock = currBlock + 1
                if (
                    currBlock in self._signals.switch_positions_green
                ) and currBlock != 63:  # if at a switch positon, check switch position for next block
                    switchInfo = self.switchNextBlocks_green[
                        currBlock - 1
                    ]  # return list of switch index, left next block, right next block
                    switchPos = self._signals.switch_positions_green[currBlock]
                    if (
                        "yard" in str(switchInfo[switchPos]).lower()
                    ):  # train disappears!
                        newBlock = -1  # set to -1 bc train no longer on track

                    # elif (currBlock == 77 and prevBlock == 76) or (currBlock == 13 and prevBlock == 1): #ignore next switch pos if train coming from 76, 77 never goest o 76
                    #     newBlock = currBlock + 1
                    # elif currBlock== 77 and prevBlock == 78: #if train coming from loop go to 101
                    #     newBlock = 101
                    elif currBlock == 28 and (
                        prevBlock == 150 or prevBlock == 29
                    ):  # check direction of train coming to switch
                        newBlock = 27
                    elif currBlock == 13 and (prevBlock == 1 or prevBlock == 12):
                        newBlock = 14
                    elif currBlock == 85 and (prevBlock == 100 or prevBlock == 86):
                        newBlock = 84
                    elif currBlock == 77 and (prevBlock == 101 or prevBlock == 76):
                        newBlock = 78
                    else:
                        # print(f'old block {self.currentBlock}, new block {switchInfo[switchPos]}, switch pos for {self.currentBlock}, {self._signals.switch_positions_green[self.currentBlock]} ')
                        newBlock = switchInfo[switchPos]

                # else:
                #     newBlock = currBlock + 1

                # get direction of travel
                if (
                    (newBlock >= 63 and newBlock <= 73)
                    or (newBlock >= 17 and newBlock <= 35)
                    or (newBlock >= 95 and newBlock <= 100)
                ):
                    self.greenLineDirection[newBlock - 1] = 3  # south
                elif (newBlock >= 74 and newBlock <= 88) or (
                    newBlock >= 122 and newBlock <= 143
                ):
                    self.greenLineDirection[newBlock - 1] = 4  # west
                elif (newBlock >= 36 and newBlock <= 56) or (
                    newBlock >= 13 and newBlock <= 16
                ):
                    self.greenLineDirection[newBlock - 1] = 2  # east
                else:
                    self.greenLineDirection[newBlock - 1] = 4  # north

                self.trainsGreen[key][1] = newBlock
                self.trainsGreen[key][2] = oldBlock
                self._signals.train_info[key][3] = self.trainsGreen[key][
                    1
                ]  # update CTC dict
                self._signals.signals_trackToTrain[key].currentBlock = newBlock
                self.currentBlock = (
                    newBlock  # FIXME remove when implement train class signals
                )
                # self.updateAuthority()

                # print(f'curr block: {self.currentBlock} , {self.trainsGreen[key][1]}')
                if newBlock > 0:  # if train still on track
                    self.greenLineOccupancy[self.trainsGreen[key][1] - 1] = 1
                    self._signals.currentBlock = self.trainsGreen[key][1]
                self._signals.greenLineOccupancy = self.greenLineOccupancy

                statBeac = ""
                switchBeac = ""
                # check for beacon
                if newBlock - 1 in self.stations_green:
                    statBeac = self.stations_green[newBlock - 1]
                    self._signals.beacon = self.stations_green[newBlock - 1]
                if newBlock in self._signals.switch_positions_green:
                    switchBeac = "Switch Block " + str(newBlock)

                self._signals.signals_trackToTrain[key].beacon = (
                    statBeac + " " + switchBeac
                )
                self._signals.beacon = (
                    statBeac + " " + switchBeac
                )  # update beacon to include switches

            # print(f'newblock-1: {self.trainsGreen[key][1]-1}, vel: {self._signals.signals_trackToTrain[key].actual_velocity }, auth: {self._signals.signals_trackToTrain[key].authority_fromTrack}, newPeeps {self.trainsGreen[key][6]  == 0} ')
            if (
                self.trainsGreen[key][1] - 1 in self.stations_green
                and self._signals.signals_trackToTrain[key].actual_velocity == 0
                and self._signals.signals_trackToTrain[key].authority_fromTrack == 0
                and self.trainsGreen[key][6] == 0
            ):  # update passengers getting on when stopped at a station
                if (
                    self.trainsGreen[key][1] == 56
                ):  # if at last station, note -1 for indexing
                    self._signals.signals_trackToTrain[key].passenger_count = 0
                    self._signals.passenger_count = 0
                else:
                    # print(f'before passenger cnt: {self._signals.signals_trackToTrain[key].passenger_count}')
                    newPassengerCount = random.randint(
                        self._signals.signals_trackToTrain[key].passenger_count, 222
                    )  # 222 max passengers on train
                    self.trainsGreen[key][6] = (
                        newPassengerCount
                        - self._signals.signals_trackToTrain[key].passenger_count
                    )  # find newPeeps
                    self._signals.passenger_count = newPassengerCount
                    self._signals.signals_trackToTrain[
                        key
                    ].passenger_count = newPassengerCount
                    self._signals.ticketSales[1] = (
                        self._signals.ticketSales[1] + self.trainsGreen[key][6]
                    )  # 1 is index for green line

                    self.stationPeeps_green[
                        self.trainsGreen[key][1] - 1
                    ] = self.trainsGreen[key][6]
                    # print(f' new peeps = {self.trainsGreen[key][6] }, newPassCnt: {self._signals.signals_trackToTrain[key].passenger_count}')
            elif self.trainsGreen[key][1] - 1 not in self.stations_green:
                self.trainsGreen[key][
                    6
                ] = 0  # set new peeps to 0 bc no one getting on if not station
            elif self.trainsGreen[key][1] - 2 in self.stations_green:
                self.stationPeeps_green[self.trainsGreen[key][1] - 1] = random.randint(
                    self._signals.signals_trackToTrain[key].passenger_count, 222
                )

            if (
                self.trainsGreen[key][1] == -1 and self._signals.ticketSales[1] > 0
            ):  # if block in yard remove from dict
                self._signals.signals_trackToTrain.pop(key)
                self.trainsGreen.pop(key)

        # FIXME seperate functionality for diff lines
        # if ( self.distanceTraveled >= 50 ):  # FIXME have distance traveled > block size for the train + add func extending to other trains
        #     self.blueLineOccupancy[self.currentBlock-1] = 0
        #     if (  self.currentBlock in self.switchNextBlocks_blue):  # if at a switch positon, check switch position for next block
        #         switchInfo = self.switchNextBlocks_blue[ self.currentBlock]  # return list of switch index, left next block, right next block
        #         switchPos = self.get_blueSwitch(switchInfo[0])
        #         self.currentBlock = switchInfo[switchPos + 1]  # add 1 offset to get correct next block value
        #     elif self.currentBlock == 10 or self.currentBlock == 15: #FIXME what does train do at end? do nothing end of the line for blue
        #         self.currentBlock = self.currentBlock
        #     else:
        #         self.currentBlock = self.currentBlock + 1

        #     # TODO do if check if need to send beacon?
        #     self.blueLineOccupancy[self.currentBlock] = 1
        #     self._signals.blockChange = 1
        #     self.distanceTraveled = self.distanceTraveled - 50

        # else:
        #     self._signals.blockChange = 0

    def calcOccupancyRed(self):
        keys = list(self.trainsRed.keys())
        for (
            key
        ) in (
            keys
        ):  # value list: trackAuth [0], current block[1], prev block[2],distance traveled[3], CTC auth[4]
            curr_time = self._signals.time / (
                60.0 * 60.0
            )  # time from CTC seconds passed
            hrsPassed = curr_time - self.trainsRed[key][5]  # hours passed
            # print(f'key: {key}, hrsPassed: {hrsPassed}, curr: {curr_time}, prev: {self.trainsRed[key][5]}')
            self.trainsRed[key][5] = curr_time  # update prev time

            # trainSpeed = self._signals.actual_velocity
            trainSpeed = self._signals.signals_trackToTrain[key].actual_velocity
            self.trainsRed[key][3] = self.trainsRed[key][3] + (
                hrsPassed * trainSpeed
            )  # update distance traveled for train
            # print(f'distance traveled: {self.trainsRed[key][3]}, block dis:  {self.redLine_set[self.currentBlock-1][1]}, vel: {self._signals.actual_velocity}, hrs {hrsPassed}, speed{trainSpeed}')
            # print(f'distance traveled: {self.trainsRed[key][3]}, hrs {hrsPassed}, speed{trainSpeed}')
            # for red line
            if (
                self.trainsRed[key][1] > 0
                and self.trainsRed[key][3]
                >= self.redLine_set[self.trainsRed[key][1] - 1][1]
            ):  # train[1] is current block
                oldBlock = self.trainsRed[key][1]
                self.redLineOccupancy[oldBlock - 1] = 0
                self.trainsRed[key][3] = (
                    self.trainsRed[key][3]
                    - self.redLine_set[self.trainsRed[key][1] - 1][1]
                )  # reset distancetraveled
                currBlock = self.trainsRed[key][1]
                prevBlock = self.trainsRed[key][2]
                newBlock = 0

                if currBlock == 1 and prevBlock == 2:  # 1 goes to 16
                    newBlock = 16
                elif currBlock == 9 and prevBlock == 10:
                    newBlock = -1  # remove
                elif currBlock <= 15:  # blocks count down from 15 to 1
                    newBlock = currBlock - 1
                elif (
                    currBlock == 16 and prevBlock == 17
                ):  # 16 goes to 15 if train coming back
                    newBlock = 15
                elif (
                    (currBlock == 52 and prevBlock == 66)
                    or (currBlock > 16 and currBlock <= 51 and prevBlock > currBlock)
                    or (currBlock > 52 and currBlock <= 66 and prevBlock > currBlock)
                ):
                    newBlock = currBlock - 1
                elif currBlock == 16 and prevBlock == 1:
                    newBlock = currBlock + 1
                elif currBlock == 76:
                    newBlock = 27
                elif currBlock == 66 and prevBlock == 65:
                    newBlock = 52
                else:
                    newBlock = currBlock + 1
                if (
                    currBlock in self._signals.switch_positions_red
                ):  # if at a switch positon, check switch position for next block
                    # print(f'switchNextblock_red {self.switchNextBlocks_red}')
                    switchInfo = self.switchNextBlocks_red[
                        currBlock - 1
                    ]  # return list of switch index, left next block, right next block
                    switchPos = self._signals.switch_positions_red[currBlock]
                    if (
                        "yard" in str(switchInfo[switchPos]).lower()
                    ):  # train disappears!
                        newBlock = -1  # set to 0 bc train no longer on track
                    elif currBlock == 16 and (prevBlock == 1 or prevBlock == 15):
                        newBlock = currBlock + 1
                    elif currBlock == 52 and (prevBlock == 66 or prevBlock == 53):
                        newBlock = currBlock - 1
                    elif currBlock == 9 and prevBlock == 10:  # go to yard
                        newBlock = -1
                    else:
                        # print(f'old block {self.currentBlock}, new block {switchInfo[switchPos]}, switch pos for {self.currentBlock}, {self._signals.switch_positions_green[self.currentBlock]} ')
                        newBlock = switchInfo[
                            switchPos
                        ]  # add 1 offset to get correct next block value

                if (newBlock >= 24 and newBlock <= 45 and prevBlock < newBlock) or (
                    newBlock >= 61 and newBlock <= 66
                ):
                    self.redLineDirection[newBlock - 1] = 3  # south
                elif (newBlock >= 13 and newBlock <= 24 and prevBlock < newBlock) or (
                    newBlock >= 49 and newBlock <= 54 and prevBlock < newBlock
                ):
                    self.redLineDirection[newBlock - 1] = 2  # east
                elif (newBlock >= 13 and newBlock <= 24 and prevBlock > newBlock) or (
                    newBlock >= 49 and newBlock <= 54 and prevBlock > newBlock
                ):
                    self.redLineDirection[newBlock - 1] = 4  # west
                else:
                    self.redLineDirection[newBlock - 1] = 1  # north
                # else:
                #     newBlock = currBlock + 1

                # print(f'newBlock: {newBlock}, curr: {currBlock}, prev {prevBlock} ')

                self.trainsRed[key][2] = oldBlock
                self.trainsRed[key][1] = newBlock
                self._signals.train_info[key][3] = self.trainsRed[key][
                    1
                ]  # update CTC dict
                self.currentBlock = (
                    newBlock  # FIXME remove when implement train class signals
                )
                # self.updateAuthority()

                # print(f'curr block: {self.currentBlock}')
                if newBlock > 0:  # if train still on track
                    self._signals.train_info[key][3] = self.trainsRed[key][
                        1
                    ]  # update CTC dict
                    self.redLineOccupancy[self.trainsRed[key][1] - 1] = 1
                    self._signals.currentBlock = self.trainsRed[key][1]
                    self._signals.signals_trackToTrain[
                        key
                    ].currentBlock = self.trainsRed[key][1]
                self._signals.redLineOccupancy = self.redLineOccupancy

                # check for beacon
                statBeac = ""
                switchBeac = ""
                if newBlock - 1 in self.stations_red:
                    self._signals.beacon = self.stations_red[newBlock - 1]
                    statBeac = self.stations_red[newBlock - 1]
                if newBlock in self._signals.switch_positions_red:
                    switchBeac = "Switch Block " + str(newBlock)

                self._signals.signals_trackToTrain[key].beacon = (
                    statBeac + " " + switchBeac
                )
                self._signals.beacon = (
                    statBeac + " " + switchBeac
                )  # update beacon to include switches

            # print(f'vel: {self._signals.signals_trackToTrain[key].actual_velocity}, auth: {self._signals.signals_trackToTrain[key].authority_fromTrack}, newPeeps {self.trainsRed[key][6]}, {self.trainsRed[key][1]-1 in self.stations_red}')
            if (
                self.trainsRed[key][1] - 1 in self.stations_red
                and self._signals.signals_trackToTrain[key].actual_velocity == 0
                and self._signals.signals_trackToTrain[key].authority_fromTrack == 0
                and self.trainsRed[key][6] == 0
            ):  # update passengers getting on when stopped at a station
                if (
                    self.trainsRed[key][1] == 16
                ):  # check if last station note -1 for indexing
                    self._signals.passenger_count = 0
                    self._signals.signals_trackToTrain[key].passenger_count = 0
                else:
                    # print(f'prev psnger cnt: {self._signals.signals_trackToTrain[key].passenger_count}, newPeeps: {self.trainsRed[key][6]}')
                    newPassengerCount = random.randint(
                        self._signals.signals_trackToTrain[key].passenger_count, 222
                    )  # 222 max passengers on train
                    self.trainsRed[key][6] = (
                        newPassengerCount
                        - self._signals.signals_trackToTrain[key].passenger_count
                    )
                    self._signals.passenger_count = newPassengerCount
                    self._signals.signals_trackToTrain[
                        key
                    ].passenger_count = newPassengerCount
                    self._signals.ticketSales[2] = (
                        self._signals.ticketSales[2] + self.trainsRed[key][6]
                    )  # 2 is index for red line

                    self.stationPeeps_red[self.trainsRed[key][1] - 1] = self.trainsRed[
                        key
                    ][
                        6
                    ]  # update passengers boarding at station
                    # print(f'new psnger cnt: {self._signals.signals_trackToTrain[key].passenger_count}, newPeeps {self.trainsRed[key][6]}')
            elif self.trainsRed[key][1] - 1 not in self.stations_red:  # reset peeps
                self.trainsRed[key][6] = 0  # set newPeeps to 0
            elif (
                self.trainsRed[key][1] - 2 in self.stations_red
            ):  # update people waiting
                self.stationPeeps_red[self.trainsRed[key][1] - 1] = random.randint(
                    self._signals.signals_trackToTrain[key].passenger_count, 222
                )  # update w/ random number to be people waiting

            if (
                self.trainsRed[key][1] == -1 and self._signals.ticketSales[2] > 0
            ):  # if block in yard remove from dict and that train has gone around
                self._signals.signals_trackToTrain.pop(key)
                self.trainsRed.pop(key)

    def getAuthority(self):
        return self._signals.authority_fromWayside

    def updateAuthorityTrainsGreen(self):
        for (
            key
        ) in (
            self.trainsGreen
        ):  # train list values key train num: trackAuth [0], current block[1], prev block[2],distance traveled[3], CTC auth[4]
            authority_str = self.trainsGreen[key][4]
            authorityDistance = 0
            if "yard" in authority_str[1:].lower():
                endBlock = 57  # 57 last block before yard
                authorityDistance = self.greenLine_set[56][
                    1
                ]  # give auth for last block distance
            else:
                endBlock = int(authority_str[1:])
            # print(f'key: {key}, auth: {authority_str} | endblock: {endBlock}\n')
            block = self.trainsGreen[key][1]
            prevBlock = block
            while block != endBlock and block > 0:
                # print(f'green trains: {self.trainsGreen}')
                authorityDistance = (
                    authorityDistance + self.greenLine_set[block - 1][1]
                )  # index 1 is block length
                oldBlock = block
                if block == 100:  # 100 goes to 85
                    block = 85
                elif block == 150:  # 150 to 28
                    block = 28
                elif block == 1:  # 1 to 13
                    block = 13
                elif (
                    block <= 28 or (block >= 77 and block <= 85)
                ) and prevBlock > block:  # 28 -1 or N block: count blocks down
                    block = block - 1
                elif (
                    block in self._signals.switch_positions_green
                ):  # FIXME block 63->62 and 62->63 # if at a switch positon, check switch position for next block
                    if block == self.trainsGreen[key][1]:
                        switchInfo = self.switchNextBlocks_green[
                            block - 1
                        ]  #  left next block, right next block
                        switchPos = self._signals.switch_positions_green[block]
                        if (
                            "yard" in str(switchInfo[switchPos]).lower()
                        ):  # train disappears!
                            block = endBlock  # end loop
                        elif (
                            (block == 77 and switchPos == 1)
                            or (block == 13 and prevBlock == 1)
                            or (block == 28 and prevBlock == 27)
                        ):  # ignore next switch pos if train coming from 76
                            block = block + 1
                        else:
                            # print(f'old block {block}, new block {switchInfo[switchPos]}')
                            block = switchInfo[
                                switchPos
                            ]  # add 1 offset to get correct next block value
                    elif (
                        block == 13 and prevBlock == 1
                    ):  # ignore next switch pos if train coming from 76
                        block = block + 1
                    else:
                        block = endBlock  # give auth up to switch bc switch pos change

                else:
                    block = block + 1

                # if block == prevBlock or block == oldBlock:
                #     print(f'new block: {block}, prevBlock: {prevBlock}, oldBlock: {oldBlock}\n')
                prevBlock = oldBlock

            self.trainsGreen[key][0] = authorityDistance  # update new auth
            self._signals.signals_trackToTrain[
                key
            ].authority_fromTrack = authorityDistance
            self._signals.authority_fromTrack = (
                authorityDistance  # FIXME to set signals to correct class for train
            )
            # self._signals.signals_trackToTrain[key].authority_fromTrack = authorityDistance #FIXME to set signals to correct class for train

    def updateAuthorityTrainsRed(self):
        for (
            key
        ) in (
            self.trainsRed
        ):  # train list values key train num: trackAuth [0], current block[1], prev block[2],distance traveled[3], CTC auth[4]
            authority_str = self.trainsRed[key][4]
            authorityDistance = 0
            if "yard" in authority_str[1:].lower():
                endBlock = 9  # 57 last block before yard
                authorityDistance = self.redLine_set[8][
                    1
                ]  # give auth for last block distance
            else:
                endBlock = int(authority_str[1:])
            # print(f'key: {key}, auth: {authority_str} | endblock: {endBlock}\n')
            block = self.trainsRed[key][1]
            prevBlock = block
            while block != endBlock and block > 0:
                authorityDistance = (
                    authorityDistance + self.redLine_set[block - 1][1]
                )  # index 1 is block length
                oldBlock = block
                if block == 1:  # 1 goes to 16
                    block = 16
                elif block <= 15:  # blocks count down from 15 to 1
                    block = block - 1
                elif (
                    block == 16 and prevBlock == 17
                ):  # 16 goes to 15 if train coming back
                    block = 15
                elif block == 66 and prevBlock == 65:  # 66 to 49
                    block = 48
                elif (block == 48 and prevBlock == 66) or (
                    block > 16 and block <= 48 and prevBlock > block
                ):
                    block = block - 1
                elif block == 16 and prevBlock == 1:
                    block = block + 1
                elif block == 76:
                    block = 27
                else:
                    block = block + 1
                prevBlock = oldBlock
                # print(f'block: {block}')

                # if block == prevBlock or block == oldBlock:
                #     print(f'newblock: {block}, prevBlock: {prevBlock}, oldBlock: {oldBlock}\n')
            # print(f'auth: {authorityDistance}')

            self.trainsRed[key][0] = authorityDistance  # update new auth
            self._signals.signals_trackToTrain[
                key
            ].authority_fromTrack = authorityDistance
            self._signals.authority_fromTrack = (
                authorityDistance  # FIXME to set signals to correct class for train
            )
            # self._signals.signals_trackToTrain[key].authority_fromTrack = authorityDistance #FIXME to set signals to correct class for train

    def setCommandedSpeed(self, speed):
        self.commandedSpeed = speed

    def getCommandedSpeed(self):
        return self._signals.commandedSpeed

    def setLights(self, lights):
        self.lights = lights

    def setCrossings(self, crossings):
        self.crossings = crossings

    def getElevation(self, line, blockNumber):
        if line == "blue":
            return self.blueLine_set[blockNumber][6]
        elif line == "red":
            self.redLine_set[blockNumber][6]
        else:  # green
            self.greenLine_set[blockNumber][6]

    def getGrade(self, line, blockNumber):
        if line == "blue":
            return self.blueLine_set[blockNumber][2]
        elif line == "red":
            self.redLine_set[blockNumber][2]
        else:  # green
            self.greenLine_set[blockNumber][2]

    def getBeacon(self, line, blockNumber):
        # return beacon info for the station
        return ""

    def getAccelLimit(self, line, blockNumber):
        if line == "blue":
            return self.blueAccelLimit
        elif line == "red":
            self.redAccelLimit
        else:  # green
            self.greenAccelLimit

    def setTrackTemp(self, temp):
        if temp <= 35:
            self.heating = "On"
        else:
            self.heating = "Off"

    def launch_main_ui(self):
        from track_model.track_model_ui import TrackModelMainUI

        self.main_ui = TrackModelMainUI(self)

    def launch_test_ui(self):
        from track_model.track_model_test_ui import TrackModelUiTest

        self.test_ui = TrackModelUiTest(self._signals, self)
