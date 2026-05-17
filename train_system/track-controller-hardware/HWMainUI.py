import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from Track_Controller_Hardware.TrackControllerHW import Track_Controller
from Track_Controller_Hardware.HWprogrammerUI import programmer_UI
from signals.trackcontroller_signals import TrackCTCSignals
from signals.track_signals import TrackSignals


class ui(QtWidgets.QMainWindow):
    def __init__(self, TrackControllerHW: Track_Controller) -> None:
        super().__init__()
        self._track_controller = TrackControllerHW
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(300, 400)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.formLayout_3 = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout_3.setObjectName("formLayout_3")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
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


        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayout_4 = QtWidgets.QFormLayout(self.groupBox_4)
        self.formLayout_4.setObjectName("formLayout_4")

        # self.toolButton = QtWidgets.QToolButton(self.groupBox_4)
        # self.toolButton.setObjectName("toolButton")
        # self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.toolButton)

        self.toolButton2 = QtWidgets.QToolButton(self.groupBox_4)
        self.toolButton2.setObjectName("toolButton2")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.toolButton2)

        self.toolButton3 = QtWidgets.QToolButton(self.groupBox_4)
        self.toolButton3.setObjectName("toolButton3")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.toolButton3)

        self.gridLayout.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tabWidget)
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.groupBox)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)


        self.retranslateUi()
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.plc_b = ""
        self.plc_g = ""
        self.plc_r = ""
        self.toolButton2.clicked.connect(lambda: self.plc_redline())
        self.toolButton3.clicked.connect(lambda: self.plc_greenline())
        self._handler()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "PLC Control"))
        self.groupBox_4.setTitle(_translate("MainWindow", "PLC scripts"))
        self.toolButton2.setText(_translate("MainWindow", "Upload PLC_redline"))
        self.toolButton3.setText(_translate("MainWindow", "Upload PLC_greenline"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "PLC"))

    def _update(self):
        self._track_controller.voter_greenline(self.plc_g)
        self._track_controller.voter_redline(self.plc_r)
        # self._track_controller.set_rail_status(self.b)
        _translate = QtCore.QCoreApplication.translate

    def _handler(self):

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._update)
        self.timer.start()

    def plc_greenline(self):
        fname2 = QtWidgets.QFileDialog.getOpenFileName(None, "Import PLC", "", "Text Documents (*.txt)")
        self.plc_g = fname2[0]
        print("Point 1")

    def plc_redline(self):
        fname3 = QtWidgets.QFileDialog.getOpenFileName(None, "Import PLC", "", "Text Documents (*.txt)")
        self.plc_r = fname3[0]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Track_Controller(TrackCTCSignals(), TrackSignals())
    t = ui(w)
    p = programmer_UI(w)
    sys.exit(app.exec_())