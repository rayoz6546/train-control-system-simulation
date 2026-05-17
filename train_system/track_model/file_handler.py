from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class FileHandler:
    def __init__(self):
        filename = ""
        data = {}

    # get track info for each block/line and switch info and return
    def getFileMain(self):
        file, check = QFileDialog.getOpenFileName(
            None, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv)"
        )
        if check:
            # TODO can be just one function?
            # TODO add beacon ifno
            fr = open(file, "r")
            lineInfo = {}
            switches = {}
            switchNextBlocks = {}
            stations = {}
            i = 0
            # note list: Block Number [0],Block Length (m) [1],Block Grade (%) [2],Speed Limit (Km/Hr)[3],Infrastructure [4],station side [5], ELEVATION (M) [6],CUMALTIVE ELEVATION (M) [7]
            lineChoice = fr.readline()
            for line in fr:
                line = line.strip("\n")
                curr = line.split(",")
                station = None
                # convert from meters to miles (1 km = 0.621371 miles)
                curr[1] = float(curr[1]) * (0.621371 / 1000)
                curr[3] = float(curr[3]) * 0.621371
                curr[2] = float(curr[2])
                curr[6] = float(curr[6]) * 3.28084  # convert elev from m to ft
                if ";" in curr[4] and ("Switch" in curr[4] or "SWITCH" in curr[4]):
                    if "|" in curr[4]:
                        curr[4], station = curr[4].split("|")
                    if "YARD" in curr[4]:
                        switchInfo = curr[4][
                            curr[4].index("(") + 1 : curr[4].index(")")
                        ]
                        switchInfo = switchInfo.replace(")", "")
                        left, right = switchInfo.split("-")
                        nextBlock = []
                        nextBlock.append(left if "Y" in left else int(left))
                        nextBlock.append(right if "Y" in right else int(right))
                        switchNextBlocks[i] = nextBlock
                        switches[i] = "Left"
                    else:
                        startIndex = curr[4].index("S")
                        switchInfo = curr[4][startIndex + 7 :]
                        switchInfo = switchInfo.split(" ")[0].strip(")")
                        switchInfo = switchInfo.split(";")
                        nextBlock = []
                        nextBlock.append(int(switchInfo[0].split("-")[1]))
                        nextBlock.append(int(switchInfo[1].split("-")[1]))
                        switchNextBlocks[i] = nextBlock
                        switches[i] = "Left"
                if "STATION" in curr[4] or station is not None:
                    if station is None:
                        stations[i] = curr[4]
                    else:
                        stations[i] = station
                lineInfo[i] = curr

                i = i + 1
            fr.close()

            return lineChoice, lineInfo, switches, switchNextBlocks, stations

    def getFileTest(self, file):    
        # TODO can be just one function?
        # TODO add beacon ifno
        fr = open(file, "r")
        lineInfo = {}
        switches = {}
        switchNextBlocks = {}
        stations = {}
        i = 0
        # note list: Block Number [0],Block Length (m) [1],Block Grade (%) [2],Speed Limit (Km/Hr)[3],Infrastructure [4],station side [5], ELEVATION (M) [6],CUMALTIVE ELEVATION (M) [7]
        lineChoice = fr.readline()
        for line in fr:
            line = line.strip("\n")
            curr = line.split(",")
            station = None
            # convert from meters to miles (1 km = 0.621371 miles)
            curr[1] = float(curr[1]) * (0.621371 / 1000)
            curr[3] = float(curr[3]) * 0.621371
            curr[2] = float(curr[2])
            curr[6] = float(curr[6]) * 3.28084  # convert elev from m to ft
            if ";" in curr[4] and ("Switch" in curr[4] or "SWITCH" in curr[4]):
                if "|" in curr[4]:
                    curr[4], station = curr[4].split("|")
                if "YARD" in curr[4]:
                    switchInfo = curr[4][
                        curr[4].index("(") + 1 : curr[4].index(")")
                    ]
                    switchInfo = switchInfo.replace(")", "")
                    left, right = switchInfo.split("-")
                    nextBlock = []
                    nextBlock.append(left if "Y" in left else int(left))
                    nextBlock.append(right if "Y" in right else int(right))
                    switchNextBlocks[i] = nextBlock
                    switches[i] = "Left"
                else:
                    startIndex = curr[4].index("S")
                    switchInfo = curr[4][startIndex + 7 :]
                    switchInfo = switchInfo.split(" ")[0].strip(")")
                    switchInfo = switchInfo.split(";")
                    nextBlock = []
                    nextBlock.append(int(switchInfo[0].split("-")[1]))
                    nextBlock.append(int(switchInfo[1].split("-")[1]))
                    switchNextBlocks[i] = nextBlock
                    switches[i] = "Left"
            if "STATION" in curr[4] or station is not None:
                if station is None:
                    stations[i] = curr[4]
                else:
                    stations[i] = station
            lineInfo[i] = curr

            i = i + 1
        fr.close()

        return lineChoice, lineInfo, switches, switchNextBlocks, stations