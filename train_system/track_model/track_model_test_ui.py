import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from signals.track_signals import TrackSignals

# #uncomment to run from outside dir
from track_model.track_model import TrackModel
from track_model.file_handler import FileHandler

# from TrackModel import TrackModel
# from FileHandler import FileHandler


class TrackModelUiTest(QMainWindow):
    def __init__(self, signals: TrackSignals, track_model: TrackModel) -> None:
        super().__init__()
        self._signals = signals
        self.blueLine_set = {}  # details of blue line
        self.blueSwitches = {}  # details of blue switches, TODO read info from csv
        self.redLine_set = {}
        self.redSwitches = {}
        self.greenLine_set = {}
        self.greenSwitches = {}
        self.tm = track_model

        # FIXME show ui correct?
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setObjectName("renameDialog")
        self.resize(500, 500)
        self.setMinimumSize(QtCore.QSize(200, 200))
        self.setSizeIncrement(QtCore.QSize(10, 10))
        self.setBaseSize(QtCore.QSize(200, 200))
        self.setStyleSheet(
            "background-color : white ; color: black ;"
        )  # sets background color, then text color
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
        self.tab = QtWidgets.QWidget()
        self.tab.setMinimumSize(QtCore.QSize(576, 100))
        self.tab.setObjectName("tab_2")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setMinimumSize(QtCore.QSize(100, 100))
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_4.setMinimumSize(QtCore.QSize(10, 10))
        self.radioButton_4.setAutoExclusive(False)
        self.radioButton_4.setObjectName("radioButton_4")
        self.verticalLayout_3.addWidget(self.radioButton_4)
        self.radioButton_6 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_6.setAutoExclusive(False)
        self.radioButton_6.setObjectName("radioButton_6")
        self.verticalLayout_3.addWidget(self.radioButton_6)
        self.radioButton_5 = QtWidgets.QRadioButton(self.tab_2)  # test
        self.radioButton_5.setAutoExclusive(False)
        self.radioButton_5.setObjectName("radioButton_5")
        self.verticalLayout_3.addWidget(self.radioButton_5)
        self.verticalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_2.setObjectName("comboBox_2")
        self.verticalLayout_5.addWidget(self.comboBox_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.comboBox_7 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_7.setObjectName("comboBox_7")
        self.verticalLayout_4.addWidget(self.comboBox_7)
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.label_80 = QtWidgets.QLabel(self.tab_2)
        self.label_80.setObjectName("label_80")
        self.horizontalLayout_33.addWidget(self.label_80)
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.label_81 = QtWidgets.QLabel(self.tab_2)
        self.label_81.setObjectName("label_81")
        self.horizontalLayout_37.addWidget(self.label_81)
        self.label_82 = QtWidgets.QLabel(self.tab_2)
        self.label_82.setObjectName("label_82")
        self.horizontalLayout_37.addWidget(self.label_82)

        self.label_83 = QtWidgets.QLabel(self.tab_2)
        self.label_83.setObjectName("label_83")
        self.label_84 = QtWidgets.QLineEdit(self.tab_2)
        self.label_84.setEnabled(True)
        self.label_84.setGeometry(QtCore.QRect(20, 50, 81, 31))
        self.label_84.setObjectName("label_84")
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_38.setObjectName("horizontalLayout_38")
        self.horizontalLayout_38.addWidget(self.label_83)
        self.horizontalLayout_38.addWidget(self.label_84)

        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.radioButton_30 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_30.setAutoExclusive(False)
        self.radioButton_30.setObjectName("radioButton_30")
        self.horizontalLayout_31.addWidget(self.radioButton_30)
        self.radioButton_29 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_29.setCheckable(True)
        self.radioButton_29.setAutoExclusive(False)
        self.radioButton_29.setObjectName("radioButton_29")
        self.horizontalLayout_31.addWidget(self.radioButton_29)
        self.horizontalLayout_32.addLayout(self.horizontalLayout_31)
        self.horizontalLayout_33.addLayout(self.horizontalLayout_32)
        self.verticalLayout_4.addLayout(self.horizontalLayout_33)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.tab_2)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_10 = QtWidgets.QLabel(self.widget_2)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_21.addWidget(self.label_10)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setContentsMargins(5, -1, -1, 5)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.radioButton_7 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_7.setAutoExclusive(False)
        self.radioButton_7.setObjectName("radioButton_7")
        self.horizontalLayout_17.addWidget(self.radioButton_7)
        self.radioButton_8 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_8.setAutoExclusive(False)
        self.radioButton_8.setChecked(True)
        self.radioButton_8.setObjectName("radioButton_8")
        self.horizontalLayout_17.addWidget(self.radioButton_8)
        blockOcc = QButtonGroup(self.horizontalLayout_17)
        blockOcc.addButton(self.radioButton_8)
        blockOcc.addButton(self.radioButton_7)
        blockOcc.setExclusive(True)
        self.horizontalLayout_21.addLayout(self.horizontalLayout_17)
        self.gridLayout_5.addLayout(self.horizontalLayout_21, 0, 0, 1, 1)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label_11 = QtWidgets.QLabel(self.widget_2)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_22.addWidget(self.label_11)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.radioButton_10 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_10.setAutoExclusive(False)
        self.radioButton_10.setObjectName("radioButton_10")
        self.horizontalLayout_18.addWidget(self.radioButton_10)
        self.radioButton_9 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_9.setAutoExclusive(False)
        self.radioButton_9.setChecked(True)
        self.radioButton_9.setObjectName("radioButton_9")
        self.horizontalLayout_18.addWidget(self.radioButton_9)
        self.horizontalLayout_22.addLayout(self.horizontalLayout_18)
        self.gridLayout_5.addLayout(self.horizontalLayout_22, 1, 0, 1, 1)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.label_15 = QtWidgets.QLabel(self.widget_2)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_23.addWidget(self.label_15)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.radioButton_12 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_12.setAutoExclusive(False)
        self.radioButton_12.setObjectName("radioButton_12")
        self.horizontalLayout_19.addWidget(self.radioButton_12)
        self.radioButton_11 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_11.setAutoExclusive(False)
        self.radioButton_11.setChecked(True)
        self.radioButton_11.setObjectName("radioButton_11")
        self.horizontalLayout_19.addWidget(self.radioButton_11)
        self.horizontalLayout_23.addLayout(self.horizontalLayout_19)
        self.gridLayout_5.addLayout(self.horizontalLayout_23, 2, 0, 1, 1)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_17 = QtWidgets.QLabel(self.widget_2)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_24.addWidget(self.label_17)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.radioButton_14 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_14.setAutoExclusive(False)
        self.radioButton_14.setObjectName("radioButton_14")
        self.horizontalLayout_20.addWidget(self.radioButton_14)
        self.radioButton_13 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_13.setAutoExclusive(False)
        self.radioButton_13.setChecked(True)
        self.radioButton_13.setObjectName("radioButton_13")
        self.horizontalLayout_20.addWidget(self.radioButton_13)
        self.horizontalLayout_24.addLayout(self.horizontalLayout_20)
        self.gridLayout_5.addLayout(self.horizontalLayout_24, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 0, 1, 1, 2)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_41 = QtWidgets.QLabel(self.tab_2)
        self.label_41.setObjectName("label_41")
        self.horizontalLayout_14.addWidget(self.label_41)
        self.label_42 = QtWidgets.QLabel(self.tab_2)
        self.label_42.setObjectName("label_42")
        self.horizontalLayout_14.addWidget(self.label_42)
        self.verticalLayout_7.addLayout(self.horizontalLayout_14)
        self.verticalLayout_7.addLayout(self.horizontalLayout_37)
        self.verticalLayout_7.addLayout(self.horizontalLayout_38)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_39 = QtWidgets.QLabel(self.tab_2)
        self.label_39.setObjectName("label_39")
        self.horizontalLayout_12.addWidget(self.label_39)
        self.label_40 = QtWidgets.QLabel(self.tab_2)
        self.label_40.setObjectName("label_40")
        self.horizontalLayout_12.addWidget(self.label_40)
        self.verticalLayout_7.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_43 = QtWidgets.QLabel(self.tab_2)
        self.label_43.setObjectName("label_43")
        self.horizontalLayout_15.addWidget(self.label_43)
        self.label_44 = QtWidgets.QLabel(self.tab_2)
        self.label_44.setObjectName("label_44")
        self.horizontalLayout_15.addWidget(self.label_44)
        self.verticalLayout_7.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_28 = QtWidgets.QLabel(self.tab_2)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_25.addWidget(self.label_28)
        self.label_35 = QtWidgets.QLabel(self.tab_2)
        self.label_35.setObjectName("label_35")
        self.horizontalLayout_25.addWidget(self.label_35)
        self.verticalLayout_7.addLayout(self.horizontalLayout_25)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_37 = QtWidgets.QLabel(self.tab_2)
        self.label_37.setObjectName("label_37")
        self.horizontalLayout_27.addWidget(self.label_37)
        self.label_36 = QtWidgets.QLineEdit(self.tab_2)
        self.label_36.setEnabled(True)
        self.label_36.setGeometry(QtCore.QRect(20, 50, 81, 31))
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_27.addWidget(self.label_36)

        self.verticalLayout_7.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_29 = QtWidgets.QLabel(self.tab_2)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_26.addWidget(self.label_29)
        self.label_30 = QtWidgets.QLabel(self.tab_2)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_26.addWidget(self.label_30)
        self.verticalLayout_7.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_33 = QtWidgets.QLabel(self.tab_2)
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_28.addWidget(self.label_33)
        self.label_31 = QtWidgets.QLabel(self.tab_2)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_28.addWidget(self.label_31)
        self.verticalLayout_7.addLayout(self.horizontalLayout_28)
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.label_38 = QtWidgets.QLabel(self.tab_2)
        self.label_38.setObjectName("label_38")
        self.horizontalLayout_29.addWidget(self.label_38)
        self.label_32 = QtWidgets.QLabel(self.tab_2)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_29.addWidget(self.label_32)
        self.verticalLayout_7.addLayout(self.horizontalLayout_29)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_34 = QtWidgets.QLabel(self.tab_2)
        self.label_34.setObjectName("label_34")
        self.horizontalLayout_30.addWidget(self.label_34)
        self.label_27 = QtWidgets.QLabel(self.tab_2)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_30.addWidget(self.label_27)
        self.verticalLayout_7.addLayout(self.horizontalLayout_30)
        self.gridLayout.addLayout(self.verticalLayout_7, 1, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 2, 0, 1, 1)
        self.toolButton_2 = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout.addWidget(self.toolButton_2, 2, 1, 1, 1)
        self.buttonBox_2 = QtWidgets.QDialogButtonBox(self.tab_2)
        self.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_2.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox_2.setObjectName("buttonBox_2")
        self.gridLayout.addWidget(self.buttonBox_2, 2, 2, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_4.addWidget(self.tabWidget, 1, 0, 1, 1)

        lineChoice = QButtonGroup(self.horizontalLayout_17)
        lineChoice.addButton(self.radioButton_4)
        lineChoice.addButton(self.radioButton_5)
        lineChoice.addButton(self.radioButton_6)
        lineChoice.setExclusive(True)

        switchChoice = QButtonGroup(self.horizontalLayout_31)
        switchChoice.addButton(self.radioButton_30)
        switchChoice.addButton(self.radioButton_29)
        switchChoice.setExclusive(True)

        powerFailButtons = QButtonGroup(self.horizontalLayout_18)
        powerFailButtons.addButton(self.radioButton_10)
        powerFailButtons.addButton(self.radioButton_9)
        powerFailButtons.setExclusive(True)

        circuitFailButtons = QButtonGroup(self.horizontalLayout_23)
        circuitFailButtons.addButton(self.radioButton_12)
        circuitFailButtons.addButton(self.radioButton_11)
        circuitFailButtons.setExclusive(True)

        brokenRailButtons = QButtonGroup(self.horizontalLayout_24)
        brokenRailButtons.addButton(self.radioButton_14)
        brokenRailButtons.addButton(self.radioButton_13)
        brokenRailButtons.setExclusive(True)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("renameDialog", "Dialog"))
        self.radioButton_4.setText(_translate("renameDialog", "Red"))
        self.radioButton_6.setText(_translate("renameDialog", "Green"))
        self.radioButton_5.setText(_translate("renameDialog", "Blue"))
        self.label_80.setText(_translate("renameDialog", "Position"))
        self.radioButton_30.setText(_translate("renameDialog", "Left"))
        self.radioButton_29.setText(_translate("renameDialog", "Right"))
        self.label_10.setText(_translate("renameDialog", "Block Occupancy"))
        self.radioButton_7.setText(_translate("renameDialog", "Yes"))
        self.radioButton_8.setText(_translate("renameDialog", "No"))
        self.label_11.setText(_translate("renameDialog", "Power Failure"))
        self.radioButton_10.setText(_translate("renameDialog", "Yes"))
        self.radioButton_9.setText(_translate("renameDialog", "No"))
        self.label_15.setText(_translate("renameDialog", "Circuit Failure"))
        self.radioButton_12.setText(_translate("renameDialog", "Yes"))
        self.radioButton_11.setText(_translate("renameDialog", "No"))
        self.label_17.setText(_translate("renameDialog", "Broken rail"))
        self.radioButton_14.setText(_translate("renameDialog", "Yes"))
        self.radioButton_13.setText(_translate("renameDialog", "No"))
        self.label_41.setText(_translate("renameDialog", "Block Length"))
        self.label_42.setText(_translate("renameDialog", "60 m"))
        self.label_39.setText(_translate("renameDialog", "Infrastructure:"))  # test
        self.label_40.setText(_translate("renameDialog", "Switch"))
        self.label_43.setText(_translate("renameDialog", "Station Side"))
        self.label_44.setText(_translate("renameDialog", "Left"))
        self.label_28.setText(_translate("renameDialog", "Elevation"))
        self.label_35.setText(_translate("renameDialog", "1.5 m"))
        self.label_37.setText(_translate("renameDialog", "Authority"))
        # self.label_36.setText(_translate("renameDialog", "20 m"))
        self.label_29.setText(_translate("renameDialog", "Grade"))
        self.label_30.setText(_translate("renameDialog", "10%"))
        self.label_33.setText(_translate("renameDialog", "Commanded Speed"))
        self.label_31.setText(_translate("renameDialog", "40 mph"))
        self.label_38.setText(_translate("renameDialog", "Speed Limit"))
        self.label_32.setText(_translate("renameDialog", "45 mph"))
        self.label_34.setText(_translate("renameDialog", "Acceleration/Decc. Limit"))
        self.label_27.setText(_translate("renameDialog", "5 mph/s"))
        self.label_12.setText(_translate("renameDialog", "Upload .csv"))
        self.toolButton_2.setText(_translate("renameDialog", "..."))
        self.label_81.setText(_translate("renameDialog", "Track Lights"))
        self.label_82.setText(_translate("renameDialog", "Green"))
        self.label_83.setText(_translate("renameDialog", "Set Track Temperature"))

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            _translate("renameDialog", "Test Track Model"),
        )

        self.label_36.textChanged.connect(self.getAuthority)
        self.label_84.textChanged.connect(self.setTrackTemp)
        self.toolButton_2.pressed.connect(self.getFileTest)
        self.comboBox_2.activated.connect(self.updateBlockTest)

        # when line selected populate with details
        self.radioButton_5.clicked.connect(self.lineChoice)
        self.radioButton_6.clicked.connect(self.lineChoice)
        self.radioButton_4.clicked.connect(self.lineChoice)

        # test ui button for switch positions
        self.radioButton_29.clicked.connect(self.updateSwitches)  # TODO update
        self.radioButton_30.clicked.connect(self.updateSwitches)

        self.radioButton_7.clicked.connect(self.blockOccupied)  # block Occupancy Yes
        self.radioButton_8.clicked.connect(self.blockOccupied)  # block Occupancy No

        # set failure modes
        self.radioButton_10.clicked.connect(
            self.failure
        )  # yes failure mode Power failure
        self.radioButton_12.clicked.connect(self.failure)  # yes circuit failure
        self.radioButton_14.clicked.connect(self.failure)  # yes broken rail
        self.radioButton_11.clicked.connect(
            self.failure
        )  # yes failure mode Power failure
        self.radioButton_13.clicked.connect(self.failure)  # yes circuit failure
        self.radioButton_9.clicked.connect(self.failure)  # yes broken rail

    def getAuthority(self):
        if len(self.label_36.text()) > 0:
            self._signals.authority = int(self.label_36.text())
        # else:
        #     self._signals.authority = 0 #if nothing entered default to 0

    def setTrackTemp(self):
        if len(self.label_84.text()) > 0:
            self.tm.setTrackTemp(int(self.label_84.text()))
        else:
            self.tm.setTrackTemp(40)  # if nothing entered default to 40

    def getFileTest(self):
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

    def lineChoice(self):  # populates with line info of selected line
        if self.radioButton_5.isChecked():  # blue line
            self.populateBlue(True)
        elif self.radioButton_4.isChecked():  # red line
            self.populateRed(True)
        elif self.radioButton_6.isChecked():  # green line
            self.populateGreen(True)
        else:
            self.clearData()

    def updateBlockTest(
        self, clearOutputs=False
    ):  # TODO update so failure modes are updated on display
        _translate = QtCore.QCoreApplication.translate
        currIndex = self.comboBox_2.currentIndex()
        if clearOutputs == True:
            self.label_42.setText(_translate("renameDialog", "N/A"))  # infrastructure
            self.label_40.setText(_translate("renameDialog", "N/A"))  # station side
            self.label_44.setText(_translate("renameDialog", "N/A"))  # Block Length
            self.label_35.setText(_translate("renameDialog", "N/A"))  # elevation
            self.label_30.setText(_translate("renameDialog", "0"))  # Grade
            self.label_36.setText(
                _translate("renameDialog", "0")
            )  # Authority, from CTC
            self.label_31.setText(
                _translate("renameDialog", "N/A")
            )  # commanded speed, from CTC
            self.label_32.setText(_translate("renameDialog", "N/A"))  # Speed limit
            self.label_27.setText(
                _translate("renameDialog", "N/A")
            )  # deceleation limit
        else:
            # get block details
            # Block Number [0],Block Length (m)[1],Block Grade (%)[2],Speed Limit (Km/Hr)[3],Infrastructure[4],station side[5],ELEVATION (M)[6],CUMALTIVE ELEVATION (M) [7]

            if self.radioButton_4.isChecked():  # red checked, test
                details = self._signals.redLine_set[currIndex]

            elif self.radioButton_6.isChecked():  # green checked
                details = self._signals.greenLine_set[currIndex]

            elif self.radioButton_5.isChecked():  # blue checked
                details = self._signals.blueLine_set[currIndex]

            self.label_42.setText(
                _translate("renameDialog", str(details[1]) + "m")
            )  # block length
            self.label_40.setText(
                _translate("renameDialog", details[4])
            )  # infrastructure
            self.label_44.setText(
                _translate("renameDialog", details[5])
            )  # station side

            self.label_35.setText(
                _translate("renameDialog", str(details[6]) + "m")
            )  # elevation
            self.label_36.setText(
                _translate("renameDialog", "0")
            )  # authority, from CTC
            self.label_30.setText(
                _translate("renameDialog", str(details[2]) + "%")
            )  # Grade
            self.label_31.setText(
                _translate("renameDialog", "50 mph")
            )  # Commanded speed
            self.label_32.setText(
                _translate("renameDialog", str(details[3]) + " mph")
            )  # Speed Limit
            self.label_27.setText(
                _translate("renameDialog", "8 mph/s")
            )  # Accel/decc limit

    def populateBlue(self, test):
        self.comboBox_2.clear()  # clear before populating new line
        self.comboBox_7.clear()
        _translate = QtCore.QCoreApplication.translate
        i = 0
        self.blueLine_set = self._signals.blueLine_set
        self.blueSwitches = self._signals.blueSwitches_set
        while i in self.blueLine_set:
            self.comboBox_2.addItem("")  # test
            self.comboBox_2.setItemText(
                i, _translate("renameDialog", "Block " + str(i + 1))
            )
            if i in self.blueSwitches:
                self.comboBox_7.addItem("Switch " + str(i + 1))
            i = i + 1

    def populateRed(self, test):
        self.comboBox_2.clear()  # clear before populating new line
        self.comboBox_7.clear()
        _translate = QtCore.QCoreApplication.translate
        i = 0
        self.redLine_set = self._signals.redLine_set
        self.redSwitches = self._signals.redSwitches_set
        while i in self.redLine_set:
            self.comboBox_2.addItem("")  # test
            self.comboBox_2.setItemText(
                i, _translate("renameDialog", "Block " + str(i + 1))
            )
            if i in self.redSwitches:
                self.comboBox_7.addItem("Switch " + str(i + 1))
            i = i + 1

    def populateGreen(self, test):
        self.comboBox_2.clear()  # clear before populating new line
        self.comboBox_7.clear()
        _translate = QtCore.QCoreApplication.translate
        i = 0
        self.greenLine_set = self._signals.greenLine_set
        self.greenSwitches = self._signals.greenSwitches_set
        while i in self.greenLine_set:
            self.comboBox_2.addItem("")  # test
            self.comboBox_2.setItemText(
                i, _translate("renameDialog", "Block " + str(i + 1))
            )
            if i in self.greenSwitches:
                self.comboBox_7.addItem("Switch " + str(i + 1))
            i = i + 1

    def updateSwitches(self):
        """1 = right, 0 = left"""
        _translate = QtCore.QCoreApplication.translate
        currentSwitch = self.comboBox_7.currentIndex()
        switchPos_bool = self.radioButton_29.isChecked() == True  # right checked

        if self.radioButton_4.isChecked():  # red
            self._signals.redSwitches_set[currentSwitch] = switchPos_bool
        elif self.radioButton_5.isChecked():  # blue
            self._signals.blueSwitches_set[currentSwitch] = switchPos_bool
        else:  # green
            self._signals.greenSwitches_set[currentSwitch] = switchPos_bool

    def failure(self):  # test UI update then updates trackmodel -> updates signals
        currIndex = self.comboBox_2.currentIndex()  # get index of chosen block

        if self.radioButton_5.isChecked():  # blue line
            self.tm.setPowerFailure_blue(currIndex, self.radioButton_10.isChecked())
            self.tm.setCircuitFailure_blue(currIndex, self.radioButton_12.isChecked())
            self.tm.setBrokenRail_blue(currIndex, self.radioButton_14.isChecked())

        elif self.radioButton_6.isChecked():  # green line
            self.tm.setPowerFailure_green(currIndex, self.radioButton_10.isChecked())
            self.tm.setCircuitFailure_green(currIndex, self.radioButton_12.isChecked())
            self.tm.setBrokenRail_green(currIndex, self.radioButton_14.isChecked())

        elif self.radioButton_4.isChecked():  # red line
            self.tm.setPowerFailure_red(currIndex, self.radioButton_10.isChecked())
            self.tm.setCircuitFailure_red(currIndex, self.radioButton_12.isChecked())
            self.tm.setBrokenRail_red(currIndex, self.radioButton_14.isChecked())

    def blockOccupied(self):
        currIndex = self.comboBox_2.currentIndex()  # get index of chosen block
        if self.radioButton_5.isChecked():  # blue line
            self.tm.setOccupancy("blue", currIndex, self.radioButton_7.isChecked())

        elif self.radioButton_6.isChecked():  # green line
            self.tm.setOccupancy(
                line="green",
                blockNumber=currIndex,
                occupied=self.radioButton_7.isChecked(),
            )

        elif self.radioButton_4.isChecked():  # red line
            self.tm.setOccupancy("red", currIndex, self.radioButton_7.isChecked())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    renameDialog = QtWidgets.QDialog()
    ui = TrackModelUiTest()
    ui.setupUi(renameDialog)
    renameDialog.show()
    sys.exit(app.exec_())
