# # -*- coding: utf-8 -*-
# """
# Created on Sun Feb 19 12:05:55 2023

# @author: RAYAN
# """

import sys
from TrackControllerSoftware.TrackControllerSoftware import Track_Controller
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from signals.trackcontroller_signals import TrackCTCSignals
from signals.track_signals import TrackSignals

class programmer_UI(QtWidgets.QMainWindow):
    def __init__(self, TrackControllerSoftware: Track_Controller)->None:
        super().__init__()
        self._track_controller = TrackControllerSoftware
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setObjectName("Track Controller Automatic")
        self.resize(500, 500)   
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 1211, 971))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_1 = QtWidgets.QLabel(self.groupBox)
        self.label_1.setObjectName("")
        self.verticalLayout_15.addWidget(self.label_1)
        
        self.combo_line = QtWidgets.QComboBox(self.tab)
        self.combo_line.setObjectName("combo_line")
        self.verticalLayout_15.addWidget(self.combo_line)
        self.combo_line.addItem("Blue Line")
        self.combo_line.addItem("Red Line")
        self.combo_line.addItem("Green Line")
        
        self.combo_line.activated.connect(self.line)

            

        
        self.combo_wayside = QtWidgets.QComboBox(self.tab)
        self.combo_wayside.setObjectName("combo_wayside")
        self.verticalLayout_15.addWidget(self.combo_wayside)


        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_15.addWidget(self.comboBox)

        
        
        
        
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.verticalLayout_15)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.label_auth = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_auth.setFont(font)
        self.label_auth.setObjectName("auth")
        self.horizontalLayout_2.addWidget(self.label_auth)
        self.label_2 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.label_speed = QtWidgets.QLabel(self.tab)
        self.label_speed.setFont(font)
        self.label_speed.setObjectName("Speed")
        self.horizontalLayout_3.addWidget(self.label_speed)
        self.label_4 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_7=QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_occupancy = QtWidgets.QLabel(self.tab)
        self.label_occupancy.setFont(font)
        self.label_occupancy.setObjectName("Occupancy")
        self.horizontalLayout_7.addWidget(self.label_occupancy)
        self.label_bool = QtWidgets.QLabel(self.tab)
        self.label_bool.setFont(font)
        self.label_bool.setObjectName("bool")
        self.horizontalLayout_7.addWidget(self.label_bool)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8= QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_18 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_8.addWidget(self.label_18)
        self.label_cs = QtWidgets.QLabel(self.tab)
        self.label_cs.setFont(font)
        self.label_cs.setObjectName("label_cs")
        self.horizontalLayout_8.addWidget(self.label_cs)
        self.label_19=QtWidgets.QLabel(self.tab)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_8.addWidget(self.label_19)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.verticalLayout_2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setAutoFillBackground(False)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_5.setFont(font)
        self.label_5.setMouseTracking(False)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setIndent(100)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_11.addWidget(self.label_5)
        self.widget = QtWidgets.QWidget(self.groupBox_2)
        self.widget.setObjectName("widget")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setIndent(0)
        self.label_6.setObjectName("label_6")
        self.gridLayout_9.addWidget(self.label_6, 0, 0, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.widget)
        self.radioButton.setEnabled(True)
        self.radioButton.setText("")
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setCheckable(False)
        self.gridLayout_9.addWidget(self.radioButton, 1, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setIndent(0)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_10.addWidget(self.label_8)
        self.radioButton_3 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_3.setText("")
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setCheckable(False)
        self.verticalLayout_10.addWidget(self.radioButton_3)
        self.gridLayout_8.addLayout(self.verticalLayout_10, 0, 1, 1, 1)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setIndent(0)
        self.label_7.setObjectName("label_7")
        self.gridLayout_10.addWidget(self.label_7, 0, 0, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_2.setText("")
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setCheckable(False)
        self.gridLayout_10.addWidget(self.radioButton_2, 1, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_10, 0, 2, 1, 1)
        self.verticalLayout_11.addWidget(self.widget)
        self.verticalLayout_9.addLayout(self.verticalLayout_11)
        self.widget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_9 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.radioButton_4 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_4.setEnabled(True)
        self.radioButton_4.setText("")
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_4.setCheckable(False)
        self.verticalLayout_3.addWidget(self.radioButton_4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_13 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_4.addWidget(self.label_13)
        self.radioButton_5 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_5.setEnabled(True)
        self.radioButton_5.setText("")
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_5.setCheckable(False)
        self.verticalLayout_4.addWidget(self.radioButton_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)
        self.verticalLayout_9.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_10 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_6.addWidget(self.label_10, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_14 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_5.addWidget(self.label_14)
        self.radioButton_6 = QtWidgets.QRadioButton(self.widget_3)
        self.radioButton_6.setEnabled(True)
        self.radioButton_6.setText("")
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_6.setCheckable(False)
        self.verticalLayout_5.addWidget(self.radioButton_6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_15 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_6.addWidget(self.label_15)
        self.radioButton_7 = QtWidgets.QRadioButton(self.widget_3)
        self.radioButton_7.setEnabled(True)
        self.radioButton_7.setText("")
        self.radioButton_7.setObjectName("radioButton_7")
        self.radioButton_7.setCheckable(False)
        self.verticalLayout_6.addWidget(self.radioButton_7)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        self.gridLayout_6.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        self.verticalLayout_9.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_11 = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_7.addWidget(self.label_11, 0, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_16 = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_7.addWidget(self.label_16)
        self.radioButton_8 = QtWidgets.QRadioButton(self.widget_4)
        self.radioButton_8.setEnabled(True)
        self.radioButton_8.setText("")
        self.radioButton_8.setObjectName("radioButton_8")
        self.radioButton_8.setCheckable(False)
        self.verticalLayout_7.addWidget(self.radioButton_8)
        self.horizontalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_17 = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_8.addWidget(self.label_17)
        self.radioButton_9 = QtWidgets.QRadioButton(self.widget_4)
        self.radioButton_9.setEnabled(True)
        self.radioButton_9.setText("")
        self.radioButton_9.setObjectName("radioButton_9")
        self.radioButton_9.setCheckable(False)
        self.verticalLayout_8.addWidget(self.radioButton_9)
        self.horizontalLayout_6.addLayout(self.verticalLayout_8)
        self.gridLayout_7.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)
        self.verticalLayout_9.addWidget(self.widget_4)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setCheckable(False)
        self.verticalLayout_14.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setCheckable(False)
        self.verticalLayout_14.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.setCheckable(False)
        self.verticalLayout_14.addWidget(self.checkBox_4)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.groupBox_3)
        self.tabWidget.addTab(self.tab, "")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tabWidget)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.tabWidget.setCurrentIndex(0)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.line_=-1
        self.block=-1
        self.wayside=-1
        self.b=-1
        self._handler()
        
    def line(self):
        self.combo_wayside.clear()
        self.comboBox.clear()
        self.label_1.clear()
        b1,b2,b3,b4,b5,b6=[],[],[],[],[],[]
        for i in range(1,8):
            b1.append(str(i))
        for i in range(8,16):
            b2.append(str(i))
        for i in range(1,39):
            b3.append(str(i))
        for i in range(39,77):
            b4.append(str(i))
        for i in range(1,76):
            b5.append(str(i))
        for i in range(76,151):
            b6.append(str(i))
        if self.combo_line.currentIndex()==0:
            self.combo_wayside.addItem("Wayside 1",b1)
            self.combo_wayside.addItem("Wayside 2",b2)
        elif self.combo_line.currentIndex()==1:
            self.combo_wayside.addItem("Wayside 1",b3)
            self.combo_wayside.addItem("Wayside 2",b4)
        else:
            self.combo_wayside.addItem("Wayside 1",b5)
            self.combo_wayside.addItem("Wayside 2",b6)
            
        self.combo_wayside.activated.connect(self.clicker)
        
    def clicker(self,index):
        self.comboBox.clear()
        self.label_1.clear()
        self.comboBox.addItems(self.combo_wayside.itemData(index))
        self.comboBox.activated.connect(self.bl)

        
    def bl(self):

        
        self.line_=int(self.combo_line.currentIndex())
        self.wayside = int(self.combo_wayside.currentIndex())
        
        if self.line_==0:
            self.label_1.setText(f'Block {self.wayside*7+self.comboBox.currentIndex()+1}')
            self.block = self.wayside*7+int(self.comboBox.currentIndex())   # self.block used to index lists of lists
            self.b = self.wayside*7+int(self.comboBox.currentIndex())  #self.b used to index lists (241 elements)
        elif self.line_==1:
            self.label_1.setText(f'Block {self.wayside*38+self.comboBox.currentIndex()+1}')
            self.block = self.wayside*38 + int(self.comboBox.currentIndex()) 
            self.b = self.wayside*38 + int(self.comboBox.currentIndex()) +15
        else:
            self.label_1.setText(f'Block {self.wayside*75+self.comboBox.currentIndex()+1}')
            self.block = self.wayside*75 + int(self.comboBox.currentIndex()) 
            self.b = self.wayside*75 + int(self.comboBox.currentIndex()) + 91
            

        

        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Track Controller Automatic"))
        self.groupBox.setTitle(_translate("MainWindow", "Automatic Mode"))
        
        self.label.setText(_translate("MainWindow", "Authority"))
        self.label_2.setText(_translate("MainWindow", "miles"))
        self.label_3.setText(_translate("MainWindow", "Suggested Speed"))
        self.label_4.setText(_translate("MainWindow", "mph"))
        self.label_5.setText(_translate("MainWindow", "Traffic Lights"))
        self.label_6.setText(_translate("MainWindow", "Green"))
        self.label_8.setText(_translate("MainWindow", "Yellow"))
        self.label_7.setText(_translate("MainWindow", "Red"))
        self.label_9.setText(_translate("MainWindow", "Switch Positions"))
        self.label_12.setText(_translate("MainWindow", "Left"))
        self.label_13.setText(_translate("MainWindow", "Right"))
        self.label_10.setText(_translate("MainWindow", "Railway Crossings Lights"))
        self.label_14.setText(_translate("MainWindow", "On"))
        self.label_15.setText(_translate("MainWindow", "Off"))
        self.label_11.setText(_translate("MainWindow", "Railway Crossings Gates"))
        self.label_16.setText(_translate("MainWindow", "Up"))
        self.label_17.setText(_translate("MainWindow", "Down"))
        self.label_18.setText(_translate("MainWindow", "Commanded Speed"))
        self.label_19.setText(_translate("MainWindow", "mph"))
        self.label_occupancy.setText(_translate("MainWindow","Track Occupancy"))
        self.checkBox_2.setText(_translate("MainWindow", "Broken Rail"))
        self.checkBox_3.setText(_translate("MainWindow", "Circuit Failure"))
        self.checkBox_4.setText(_translate("MainWindow", "Power Failure"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "View Input/Output"))


    def _update(self):

     
    
        self.authority_(self._track_controller.get_authority()[self.line_][self.block])
        self.suggested_speed(self._track_controller.get_suggested_speed()[self.line_][self.block])
        
        self.track_occupancy(self._track_controller.get_track_occupancy()[self.b])
        
        self.commanded_speed(self._track_controller.get_commanded_speed()[self.line_][self.block])
        self.broken_rail(self._track_controller.get_broken_rail()[self.b])
        self.circuit_failure(self._track_controller.get_circuit_failure()[self.b])
        self.power_failure(self._track_controller.get_power_failure()[self.b])
        
        self.traffic_lights_green(self._track_controller.get_traffic_lights()[0][self.line_][self.block])
        self.traffic_lights_yellow(self._track_controller.get_traffic_lights()[1][self.line_][self.block])
        self.traffic_lights_red(self._track_controller.get_traffic_lights()[2][self.line_][self.block])
        self.switch_positions(self._track_controller.get_switch_positions()[self.line_][self.block])
        self.crossings(self._track_controller.get_crossings()[self.line_][self.block])

        

    def _handler(self):
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._update)
        self.timer.start()
     

    def authority_(self, aut: int):
        _translate = QtCore.QCoreApplication.translate
        if self._track_controller._track_occupancy[self.b]==True:
            self.label_auth.setText(_translate("MainWindow",aut))
        else:
            self.label_auth.setText(_translate("MainWindow",""))
        
    def suggested_speed(self,sp: int):
        _translate = QtCore.QCoreApplication.translate
        if self._track_controller._track_occupancy[self.b]==True:
            self.label_speed.setText(_translate("MainWindow",str(sp)))
        else:
            self.label_speed.setText(_translate("MainWindow",""))
        
    def track_occupancy(self, track_occ):
        _translate = QtCore.QCoreApplication.translate
        
        if track_occ==False:
             self.label_bool.setText(_translate("MainWindow","No"))
        elif track_occ==True:
            self.label_bool.setText(_translate("MainWindow","Yes"))
        else:
            self.label_bool.setText(_translate("MainWindow",""))
            
    def commanded_speed(self, cs: int):
        _translate = QtCore.QCoreApplication.translate
        if self._track_controller._track_occupancy[self.b]==True:
            self.label_cs.setText(_translate("MainWindow",str(cs)))
        else:
            self.label_cs.setText(_translate("MainWindow",""))
                                
    def broken_rail(self, br_rail: bool):
        if br_rail==True:
            self.checkBox_2.setStyleSheet("QCheckBox::indicator"
               "{"
               "background-color : red;"
               "}")
        else:
            self.checkBox_2.setStyleSheet("QCheckBox::indicator"
               "{"
               "background-color : white;"
               "}")
            
    def circuit_failure(self, circ_failure: bool):
        if circ_failure == True:
            self.checkBox_3.setStyleSheet("QCheckBox::indicator"
                "{"
                "background-color : red;"
                "}")
        else:
            self.checkBox_3.setStyleSheet("QCheckBox::indicator"
                "{"
                "background-color : white;"
                "}")
            
    def power_failure(self, pow_failure: bool):
        if pow_failure == True:
            self.checkBox_4.setStyleSheet("QCheckBox::indicator"
                    "{"
                    "background-color : red;"
                    "}") 
        else: 
            self.checkBox_4.setStyleSheet("QCheckBox::indicator"
                    "{"
                    "background-color : white;"
                    "}") 
            
    def traffic_lights_green(self, tr_lights):
        if tr_lights== True:  # GREEN

            self.radioButton.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : green;"
               "}")
        else:
            self.radioButton.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            
    def traffic_lights_yellow(self, tr_lights):
        if tr_lights == True:
            self.radioButton_3.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : yellow;"
               "}")
        else:
            self.radioButton_3.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            
    def traffic_lights_red(self, tr_lights): 
        if tr_lights == True:
            self.radioButton_2.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : red;"
               "}")

        else: 
            self.radioButton_2.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            
    def switch_positions(self, sw: bool):

        if sw==False:

            self.radioButton_4.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : orange;"
               "}")
            self.radioButton_5.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
        elif sw == True:

            self.radioButton_5.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : orange;"
               "}")
            self.radioButton_4.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            
        else:   

            self.radioButton_5.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            self.radioButton_4.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            
    def crossings(self, val: bool):

        if val==True:

            self.radioButton_6.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : orange;"
               "}")
            self.radioButton_7.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            self.radioButton_8.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : orange;"
               "}")   
            self.radioButton_9.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
        elif val == False:

            self.radioButton_7.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : orange;"
               "}")
            self.radioButton_6.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            
            self.radioButton_8.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")   
            self.radioButton_9.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : orange;"
               "}")
        else: 

            self.radioButton_7.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            self.radioButton_6.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            self.radioButton_9.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
               "}")
            self.radioButton_8.setStyleSheet("QRadioButton::indicator"
               "{"
               "background-color : white;"
                "}") 
    
        
        
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    p = programmer_UI(Track_Controller(TrackCTCSignals(),TrackSignals()))
    sys.exit(app.exec_())
