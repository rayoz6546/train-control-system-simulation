# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TrackModel.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# #uncomment to run from outside dir
from track_model.track_model import TrackModel
from track_model.file_handler import FileHandler

# from TrackModel import TrackModel
# from FileHandler import FileHandler
from signals.track_signals import TrackSignals


class TrackModelMainUI(QWidget):
    def __init__(self, track_model: TrackModel):
        super().__init__()
        self.blueLine_set = {}  # details of blue line
        self.blueSwitches = {}  # details of blue switches
        self.redLine_set = {}
        self.redSwitches = {}
        self.greenLine_set = {}
        self.greenSwitches = {}
        self.trackLayout = QGridLayout()
        self.trackLayoutRed = QGridLayout()
        self.trackLayoutGreen = QGridLayout()
        self.trackLayoutBlue = QGridLayout()
        self.tm = track_model

        # FIXME show ui correct?
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setObjectName("renameDialog")
        self.resize(650, 600)
        self.setMinimumSize(QtCore.QSize(200, 200))
        self.setSizeIncrement(QtCore.QSize(10, 10))
        self.setBaseSize(QtCore.QSize(200, 200))
        self.setStyleSheet(
            "background-color : white ; color: black ;"
        )  # sets background color, then text color
        # self.setStyleSheet("background-color :rgb(255, 204, 255) ; color: rgb(7, 3, 71) ;") #sets background color, then text color
        self.gridLayout_4 = QtWidgets.QGridLayout(self)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.gridLayout_4.addLayout(self.horizontalLayout_11, 0, 0, 3, 2)
        self.tabWidget = QtWidgets.QTabWidget(self)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.tabWidget.setBaseSize(QtCore.QSize(10, 10))
        self.tabWidget.setObjectName("tabWidget")

        # self.tabWidgetRed = QtWidgets.QTabWidget(self)
        # self.tabWidgetRed.setSizePolicy(sizePolicy)
        # self.tabWidgetRed.setMinimumSize(QtCore.QSize(500, 500))
        # self.tabWidgetRed.setBaseSize(QtCore.QSize(10, 10))
        # self.tabWidgetRed.setObjectName("tabWidgetRed")

        self.tab = QtWidgets.QWidget()
        self.tab.setMinimumSize(QtCore.QSize(600, 500))
        self.tab.setObjectName("tab")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.tab)
        self.radioButton.setMinimumSize(QtCore.QSize(10, 10))
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_2.setEnabled(True)
        self.radioButton_2.setAutoExclusive(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.radioButton_2.sizePolicy().hasHeightForWidth()
        )
        self.radioButton_2.setSizePolicy(sizePolicy)
        self.radioButton_2.setBaseSize(QtCore.QSize(0, 0))
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_3.setAutoExclusive(False)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout.addWidget(self.radioButton_3)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setMinimumSize(QtCore.QSize(57, 19))
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.comboBox_3 = QtWidgets.QComboBox(self.tab)
        self.comboBox_3.setObjectName("comboBox_3")
        self.horizontalLayout_16.addWidget(self.comboBox_3)
        self.label_77 = QtWidgets.QLabel(self.tab)
        self.label_77.setObjectName("label_77")
        self.horizontalLayout_16.addWidget(self.label_77)
        self.label_78 = QtWidgets.QLabel(self.tab)
        self.label_78.setObjectName("label_78")
        self.horizontalLayout_16.addWidget(self.label_78)
        self.label_79 = QtWidgets.QLabel(self.tab)
        self.label_79.setObjectName("label_79")
        self.horizontalLayout_16.addWidget(self.label_79)
        self.verticalLayout_2.addLayout(self.horizontalLayout_16)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_13.addWidget(self.label_9)
        self.toolButton = QtWidgets.QToolButton(self.tab)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_13.addWidget(self.toolButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_13, 2, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.label_46 = QtWidgets.QLabel(self.widget)
        self.label_46.setAutoFillBackground(False)
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_34.addWidget(self.label_46)
        self.label_45 = QtWidgets.QLabel(self.widget)
        self.label_45.setObjectName("label_45")
        self.horizontalLayout_34.addWidget(self.label_45)
        self.label_83 = QtWidgets.QLabel(self.widget)
        self.label_83.setObjectName("label_83")
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_38.setObjectName("horizontalLayout_38")
        self.horizontalLayout_38.addWidget(self.label_83)
        self.label_84 = QtWidgets.QLabel(self.widget)
        self.label_84.setObjectName("label_84")
        self.horizontalLayout_38.addWidget(self.label_84)
        self.label_85 = QtWidgets.QLabel(self.widget)
        self.label_85.setObjectName("label_85")
        self.label_86 = QtWidgets.QLabel(self.widget)
        self.label_86.setObjectName("label_86")
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.horizontalLayout_39.addWidget(self.label_85)
        self.horizontalLayout_39.addWidget(self.label_86)
        self.gridLayout_3.addLayout(self.horizontalLayout_34, 4, 0, 1, 1)
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.label_49 = QtWidgets.QLabel(self.widget)
        self.label_49.setAutoFillBackground(False)
        self.label_49.setObjectName("label_49")
        self.horizontalLayout_36.addWidget(self.label_49)
        self.label_50 = QtWidgets.QLabel(self.widget)
        self.label_50.setObjectName("label_50")
        self.horizontalLayout_36.addWidget(self.label_50)
        self.gridLayout_3.addLayout(self.horizontalLayout_36, 5, 0, 1, 1)
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.label_47 = QtWidgets.QLabel(self.widget)
        self.label_47.setAutoFillBackground(False)
        self.label_47.setObjectName("label_47")
        self.horizontalLayout_35.addWidget(self.label_47)
        self.label_48 = QtWidgets.QLabel(self.widget)
        self.label_48.setObjectName("label_48")
        self.horizontalLayout_35.addWidget(self.label_48)
        self.gridLayout_3.addLayout(self.horizontalLayout_35, 6, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_5.addWidget(self.label_14)
        self.label_18 = QtWidgets.QLabel(self.widget)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_5.addWidget(self.label_18)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 7, 0, 1, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_38, 13, 0, 1, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_39, 14, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_6.addWidget(self.label_16)
        self.label_20 = QtWidgets.QLabel(self.widget)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_6.addWidget(self.label_20)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 8, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.label_21 = QtWidgets.QLabel(self.widget)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_7.addWidget(self.label_21)
        self.gridLayout_3.addLayout(self.horizontalLayout_7, 9, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_22 = QtWidgets.QLabel(self.widget)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_8.addWidget(self.label_22)
        self.label_19 = QtWidgets.QLabel(self.widget)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_8.addWidget(self.label_19)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 10, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_24 = QtWidgets.QLabel(self.widget)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_9.addWidget(self.label_24)
        self.label_23 = QtWidgets.QLabel(self.widget)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_9.addWidget(self.label_23)
        self.gridLayout_3.addLayout(self.horizontalLayout_9, 11, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_26 = QtWidgets.QLabel(self.widget)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_10.addWidget(self.label_26)
        self.label_25 = QtWidgets.QLabel(self.widget)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_10.addWidget(self.label_25)
        self.gridLayout_3.addLayout(self.horizontalLayout_10, 12, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 14, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 0, 1, 3, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout_4.addWidget(self.tabWidget, 1, 0, 1, 1)

        powerFailButtons = QButtonGroup(self.verticalLayout)
        powerFailButtons.addButton(self.radioButton)
        powerFailButtons.addButton(self.radioButton_2)
        powerFailButtons.addButton(self.radioButton_3)
        powerFailButtons.setExclusive(True)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.radioButton_3.clicked.connect(self.lineChoiceMain)
        self.radioButton_2.clicked.connect(self.lineChoiceMain)
        self.radioButton.clicked.connect(self.lineChoiceMain)

        self.comboBox.activated.connect(self.updateBlockMain)
        self.toolButton.pressed.connect(self.getFileMain)

        self.clearData()

        # self.comboBox_3.setDisabled(True)
        # self.radioButton_30.setDisabled(True)
        self.handler()

    def update(self):
        self.setFailures()
        self.updateBlockMain()
        self.updateBlockVisual()

    def handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def setFailures(self):
        _translate = (
            QtCore.QCoreApplication.translate
        )  # TODO update for different lines
        currIndex = self.comboBox.currentIndex()  # get current block number
        if currIndex >= 0:
            if self.radioButton_3.isChecked():  # blue
                pfail = self.tm.getPowerFailure_blue()
                circFails = self.tm.getCircuitFailure_blue()
                railFail = self.tm.getBrokenRail_blue()

            elif self.radioButton_2.isChecked():  # green
                pfail = self.tm.getPowerFailure_green()
                circFails = self.tm.getCircuitFailure_green()
                railFail = self.tm.getBrokenRail_green()
            elif self.radioButton.isChecked():  # red
                pfail = self.tm.getPowerFailure_red()
                circFails = self.tm.getCircuitFailure_red()
                railFail = self.tm.getBrokenRail_red()

            if pfail[currIndex] == 1:  # yes failure mode Power failure
                self.label_4.setText(
                    _translate("renameDialog", "Yes")
                )  # update main ui, power failure
            else:
                self.label_4.setText(_translate("renameDialog", "No"))

            if circFails[currIndex] == 1:  # yes circuit failure
                self.label_5.setText(_translate("renameDialog", "Yes"))
            else:
                self.label_5.setText(_translate("renameDialog", "No"))

            if railFail[currIndex] == 1:  # yes broken rail
                self.label_7.setText(_translate("renameDialog", "Yes"))
            else:
                self.label_7.setText(_translate("renameDialog", "No"))

    def lineChoiceMain(self):
        if self.radioButton_3.isChecked():
            self.populateBlue(False)
            self.tm.lineChoice = "blue"
        elif self.radioButton_2.isChecked():  # green
            self.populateGreen()
            self.tm.lineChoice = "green"
        elif self.radioButton.isChecked():  # red
            self.populateRed()
            self.tm.lineChoice = "red"
        else:
            self.clearData()

    def populateBlue(self, test):
        _translate = QtCore.QCoreApplication.translate
        i = 0
        self.blueLine_set = self.tm.getBlueLine()
        self.blueSwitches = self.tm.get_blueSwitches()
        self.comboBox_3.clear()  # clear before populating
        self.comboBox.clear()
        if test == True:
            while i in self.blueLine_set:
                self.comboBox.addItem("")  # main
                self.comboBox.setItemText(
                    i, _translate("renameDialog", "Block " + str(i + 1))
                )
                if i in self.blueSwitches:
                    self.comboBox_3.addItem("Switch " + str(i + 1))
                i = i + 1

        else:
            while i in self.blueLine_set:
                self.comboBox.addItem("")  # main
                self.comboBox.setItemText(
                    i, _translate("renameDialog", "Block " + str(i + 1))
                )
                if i in self.blueSwitches:
                    self.comboBox_3.addItem("Switch " + str(i + 1))
                i = i + 1
            self.setBlockVisual()

    def populateGreen(self):
        _translate = QtCore.QCoreApplication.translate
        i = 0
        self.greenLine_set = self.tm.getGreenLine()
        self.greenSwitches = self.tm.get_greenSwitches()
        self.comboBox_3.clear()  # clear before populating
        self.comboBox.clear()
        while i in self.greenLine_set:
            self.comboBox.addItem("")  # main
            self.comboBox.setItemText(
                i, _translate("renameDialog", "Block " + str(i + 1))
            )
            if i in self.greenSwitches:
                self.comboBox_3.addItem("Switch " + str(i + 1))
            i = i + 1
        self.setBlockVisual()

    def populateRed(self):
        _translate = QtCore.QCoreApplication.translate
        i = 0
        self.redLine_set = self.tm.getRedLine()
        self.redSwitches = self.tm.get_redSwitches()
        self.comboBox_3.clear()  # clear before populating
        self.comboBox.clear()

        while i in self.redLine_set:
            self.comboBox.addItem("")  # main
            self.comboBox.setItemText(
                i, _translate("renameDialog", "Block " + str(i + 1))
            )
            if i in self.redSwitches:
                self.comboBox_3.addItem("Switch " + str(i + 1))
            i = i + 1
        self.setBlockVisual()

    def clearData(self):
        self.comboBox.clear()
        self.comboBox_3.clear()
        self.updateBlockMain(True)

    # can pass test index if test updates and needs to update main too
    def updateBlockMain(self, clearOutputs=False, index=-1):
        """clearOutputs = True if just want to clear"""
        _translate = QtCore.QCoreApplication.translate
        switchPos = ""
        currSwitchIndex = -1
        direction = ""
        # occupancy = 0

        if index < 0:
            currIndex = self.comboBox.currentIndex()
        else:
            currIndex = index
            self.comboBox.setCurrentIndex(index)

        # get block details
        # Block Number [0],Block Length (m)[1],Block Grade (%)[2],Speed Limit (Km/Hr)[3],Infrastructure[4],station side[5],ELEVATION (M)[6],CUMALTIVE ELEVATION (M) [7]
        if clearOutputs == True:
            self.label_45.setText(_translate("renameDialog", "N/A"))  # infrastructure
            self.label_50.setText(_translate("renameDialog", "N/A"))  # station side
            self.label_48.setText(_translate("renameDialog", "N/A"))  # Block Length
            self.label_18.setText(_translate("renameDialog", "N/A"))  # elevation
            self.label_20.setText(_translate("renameDialog", "N/A"))  # Grade
            self.label_21.setText(
                _translate("renameDialog", "N/A")
            )  # Authority, from CTC
            self.label_19.setText(
                _translate("renameDialog", "N/A")
            )  # commanded speed, from CTC
            self.label_23.setText(_translate("renameDialog", "N/A"))  # Speed limit
            self.label_25.setText(
                _translate("renameDialog", "N/A")
            )  # deceleation limit
            self.label_3.setText(_translate("renameDialog", "N/A"))
            self.label_84.setText(_translate("renameDialog", "N/A"))

        elif currIndex >= 0:
            if self.radioButton.isChecked():  # red checked, main
                self.redLine_set = (
                    self.tm.getRedLine()
                )  # TODO update switch display for other lines
                details = self.redLine_set[currIndex]
                self.redSwitches = self.tm.get_redSwitches()
                occupancy = self.tm.redLineOccupancy[currIndex]
                light = self.tm.get_redLineLight(currIndex + 1)
                direction = self.tm.getDirection("r", currIndex)

                switchPos_bool = 0
                if len(self.comboBox_3.currentText()) > 0:
                    switchText = self.comboBox_3.currentText()
                    spaceindex = switchText.index(" ")
                    currSwitchIndex = int(switchText[spaceindex + 1 :])
                if (
                    currSwitchIndex >= 0
                    and currSwitchIndex in self.tm.get_redSwitches()
                ):
                    switchPos_bool = self.tm.get_redSwitch(currSwitchIndex)
                if switchPos_bool:
                    switchPos = "Right"
                else:
                    switchPos = "Left"

            elif self.radioButton_2.isChecked():  # green checked, main
                self.greenLine_set = self.tm.getGreenLine()
                details = self.greenLine_set[currIndex]
                occupancy = self.tm.greenLineOccupancy[currIndex]
                light = self.tm.get_greenLineLight(
                    currIndex + 1
                )  # add 1 to block index to get block number
                direction = self.tm.getDirection("g", currIndex)

                switchPos_bool = 0
                if len(self.comboBox_3.currentText()) > 0:
                    switchText = self.comboBox_3.currentText()
                    spaceindex = switchText.index(" ")
                    currSwitchIndex = int(switchText[spaceindex + 1 :])
                if (
                    currSwitchIndex >= 0
                    and currSwitchIndex in self.tm.get_greenSwitches()
                ):
                    switchPos_bool = self.tm.get_greenSwitch(currSwitchIndex)
                if switchPos_bool:
                    switchPos = "Right"
                else:
                    switchPos = "Left"

            elif self.radioButton_3.isChecked():  # blue checked, main
                self.blueLine_set = self.tm.getBlueLine()
                details = self.blueLine_set[currIndex]
                occupancy = self.tm.blueLineOccupancy[currIndex]

                switchPos_bool = 0
                if currSwitchIndex >= 0:
                    switchPos_bool = self.tm.get_blueSwitch(currSwitchIndex)
                if switchPos_bool:
                    switchPos = "Right"
                else:
                    switchPos = "Left"
            else:
                details = ["", "", "", "", "", "", "", ""]
                switchPos = ""

            passStr = ""
            if occupancy:
                passStr = "Passengers boarding: "
            else:
                passStr = "Passengers waiting: "

            self.label_45.setText(
                _translate(
                    "renameDialog",
                    details[4]
                    + (
                        passStr + str(self.tm.getPassengersBoarding(currIndex))
                        if "STATION" in details[4]
                        else ""
                    ),
                )
            )  # infrastructure
            self.label_50.setText(
                _translate("renameDialog", details[5])
            )  # station side
            self.label_48.setText(
                _translate("renameDialog", str(details[1]) + "miles")
            )  # Block Length
            self.label_18.setText(
                _translate("renameDialog", str(details[6]) + "m")
            )  # elevation
            self.label_20.setText(
                _translate("renameDialog", str(details[2]) + "%")
            )  # Grade
            self.label_21.setText(
                _translate("renameDialog", str(self.tm.getAuthority()))
            )  # Authority, from CTC
            self.label_19.setText(
                _translate("renameDialog", str(self.tm.getCommandedSpeed()))
            )  # commanded speed, from CTC
            self.label_23.setText(
                _translate("renameDialog", str(details[3]) + " mph")
            )  # Speed limit
            self.label_25.setText(
                _translate("renameDialog", "5 mph/s")
            )  # deceleation limit
            self.label_78.setText(
                _translate("renameDialog", switchPos)
            )  # switch position
            self.label_3.setText(
                _translate("renameDialog", "Yes " + direction if occupancy else "No")
            )  # block occupancy
            self.label_84.setText(_translate("renameDialog", light))  # track lightes
            self.label_86.setText(_translate("renameDialog", self.tm.heating))

        # self.comboBox_3.setDisabled(True)
        # self.radioButton_30.setDisabled(True)

    def getFileMain(self):
        # TODO add vars for test and main track layouts
        file = FileHandler()
        lineChoice, lineInfo, switches, switchNextBlocks, stations = file.getFileMain()
        if len(lineChoice) > 0:
            if "blue" in lineChoice:
                self.tm.initialBlueSwitches(switches)
                self.tm.setBlueLine(lineInfo)
                self.tm.switchNextBlocks_blue = switchNextBlocks
                self.tm.stations_blue = stations
            elif "green" in lineChoice:
                self.tm.initialGreenSwitches(switches)
                self.tm.setGreenLine(lineInfo)
                self.tm.switchNextBlocks_green = switchNextBlocks
                self.tm.stations_green = stations
            elif "red" in lineChoice:
                self.tm.initialRedSwitches(switches)
                self.tm.setRedLine(lineInfo)
                self.tm.switchNextBlocks_red = switchNextBlocks
                self.tm.stations_red = stations

    def setBlockVisual(self):
        # TODO update visual for different layouts and clear before setting ui
        # self.trackLayoutRed = QGridLayout()
        widget = QWidget()
        title = ""
        # self.label_87 = QLabel(self)
        # self.label_87.setObjectName("label_87")
        # # adding image to label
        # self.label_87.setPixmap(QtGui.QPixmap("blueLine.png"))
        # #self.setCentralWidget(self.label_87)
        # # Optional, resize label to image size
        # # self.label_87.resize(self.blueLineMap.width(),
        # #                   self.blueLineMap.height())

        # self.trackLayout.addWidget(self.label_87, 1, 1)
        if (
            self.radioButton.isChecked()
            and self.trackLayoutRed.itemAtPosition(4, 4) is None
        ):  # red checked, main
            lineInfo = self.tm.getRedLine()
            title = "Red Line Track"

            for i in range(len(lineInfo)):
                btn = QPushButton(str(i + 1))  # dislay index +1 to start at 1
                # btn.pressed.connect(lambda : self.updateBlockMain(False, i))
                btn.setStyleSheet("background-color : gray")

                self.trackLayoutRed.addWidget(btn, i // 5, i % 5)

            widget.setLayout(self.trackLayoutRed)
            self.tabWidget.addTab(widget, title)
            # self.tabWidgetRed.addTab(widget, title)
            # self.label_87.raise_()
            self.show()

        elif (
            self.radioButton_2.isChecked()
            and self.trackLayoutGreen.itemAtPosition(4, 4) is None
        ):  # green checked, main
            lineInfo = self.tm.getGreenLine()
            title = "Green Line Track"

            for i in range(len(lineInfo)):
                btn = QPushButton(str(i + 1))  # dislay index +1 to start at 1
                # btn.pressed.connect(lambda : self.updateBlockMain(False, i))
                btn.setStyleSheet("background-color : gray")

                self.trackLayoutGreen.addWidget(btn, i // 5, i % 5)

            widget.setLayout(self.trackLayoutGreen)

            self.tabWidget.addTab(widget, title)
            # self.label_87.raise_()
            self.widget.show()
            self.show()
        elif (
            self.radioButton_3.isChecked()
            and self.trackLayoutBlue.itemAtPosition(4, 4) is None
        ):  # blue checked, main
            lineInfo = self.tm.getBlueLine()
            title = "Blue Line Track"

            lineInfo = self.tm.getGreenLine()
            title = "Green Line Track"

            for i in range(len(lineInfo)):
                btn = QPushButton(str(i + 1))  # dislay index +1 to start at 1
                # btn.pressed.connect(lambda : self.updateBlockMain(False, i))
                btn.setStyleSheet("background-color : gray")

                self.trackLayoutBlue.addWidget(btn, i // 5, i % 5)

            widget.setLayout(self.trackLayoutBlue)

            self.tabWidget.addTab(widget, title)
            # self.label_87.raise_()
            self.show()

    def updateBlockVisual(self):
        # TODO incorporate switches
        occupancy = []

        if self.trackLayoutRed.itemAtPosition(4, 4) is not None:  # red , main
            occupancy = self.tm.redLineOccupancy
            for j in range(
                len(occupancy)
            ):  # note getting list of blue line occupancy w/o issue
                trackBlockVisual = self.trackLayoutRed.itemAtPosition(j // 5, j % 5)
                if (occupancy[j] == 1) and (
                    trackBlockVisual != None
                ):  # if block occupied
                    trackBlockVisual.widget().setStyleSheet(
                        "background-color : blue ; color: white ;"
                    )  # sets background color, then text color
                elif trackBlockVisual != None:
                    trackBlockVisual.widget().setStyleSheet(
                        "background-color : gray ; color: black;"
                    )
        if self.trackLayoutGreen.itemAtPosition(4, 4) is not None:  # green , main
            occupancy = self.tm.greenLineOccupancy
            for j in range(
                len(occupancy)
            ):  # note getting list of blue line occupancy w/o issue
                trackBlockVisual = self.trackLayoutGreen.itemAtPosition(j // 5, j % 5)
                if (occupancy[j] == 1) and (
                    trackBlockVisual != None
                ):  # if block occupied
                    trackBlockVisual.widget().setStyleSheet(
                        "background-color : blue; color: white ;"
                    )
                elif trackBlockVisual != None:
                    trackBlockVisual.widget().setStyleSheet(
                        "background-color : gray ; color: black ;"
                    )
        if self.trackLayoutBlue.itemAtPosition(4, 4) is not None:  # blue , main
            occupancy = self.tm.blueLineOccupancy
            for j in range(
                len(occupancy)
            ):  # note getting list of blue line occupancy w/o issue
                trackBlockVisual = self.trackLayoutBlue.itemAtPosition(j // 5, j % 5)
                if (occupancy[j] == 1) and (
                    trackBlockVisual != None
                ):  # if block occupied
                    trackBlockVisual.widget().setStyleSheet(
                        "background-color : blue; color: white ;"
                    )
                elif trackBlockVisual != None:
                    trackBlockVisual.widget().setStyleSheet(
                        "background-color : gray; color: black ;"
                    )

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("renameDialog", "Dialog"))
        self.radioButton.setText(_translate("renameDialog", "Red"))
        self.radioButton_2.setText(_translate("renameDialog", "Green"))
        self.radioButton_3.setText(_translate("renameDialog", "Blue"))
        self.label.setText(_translate("renameDialog", "Block Occupancy"))
        self.label_3.setText(_translate("renameDialog", "Yes"))
        self.label_2.setText(_translate("renameDialog", "Power Failure"))
        self.label_4.setText(_translate("renameDialog", "No"))
        self.label_6.setText(_translate("renameDialog", "Circuit Failure"))
        self.label_5.setText(_translate("renameDialog", "No"))
        self.label_8.setText(_translate("renameDialog", "Broken rail"))
        self.label_7.setText(_translate("renameDialog", "No"))
        self.label_46.setText(_translate("renameDialog", "Infrastructure"))
        self.label_45.setText(_translate("renameDialog", "Switch"))
        self.label_83.setText(_translate("renameDialog", "Track Lights"))
        self.label_84.setText(_translate("renameDialog", "Green"))
        self.label_85.setText(_translate("renameDialog", "Track Heating"))
        self.label_86.setText(_translate("renameDialog", "Off"))
        self.label_49.setText(_translate("renameDialog", "Station Side"))
        self.label_50.setText(_translate("renameDialog", "N/A"))
        self.label_47.setText(_translate("renameDialog", "Block Length"))
        self.label_48.setText(_translate("renameDialog", "20 m"))
        self.label_14.setText(_translate("renameDialog", "Elevation"))
        self.label_18.setText(_translate("renameDialog", "1.5 m"))
        self.label_16.setText(_translate("renameDialog", "Grade"))
        self.label_20.setText(_translate("renameDialog", "10%"))
        self.label_13.setText(_translate("renameDialog", "Authority"))
        self.label_21.setText(_translate("renameDialog", "20 m"))
        self.label_22.setText(_translate("renameDialog", "Commanded Speed"))
        self.label_19.setText(_translate("renameDialog", "40 mph"))
        self.label_24.setText(_translate("renameDialog", "Speed Limit"))
        self.label_23.setText(_translate("renameDialog", "45 mph"))
        self.label_26.setText(_translate("renameDialog", "Acceleration/Decc. Limit"))
        self.label_25.setText(_translate("renameDialog", "5 mph/s"))
        self.label_77.setText(_translate("renameDialog", "Position"))
        self.label_78.setText(_translate("renameDialog", "Left"))
        self.label_9.setText(_translate("renameDialog", "Upload .csv"))
        self.toolButton.setText(_translate("renameDialog", "..."))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab), _translate("renameDialog", "Track Model")
        )


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    renameDialog = QtWidgets.QDialog()

    ui = TrackModelMainUI()
    ui.setupUi(renameDialog)
    renameDialog.show()
    sys.exit(app.exec_())
