import sys
from TrackModel.TrackModel import TrackModel
from signals.track_signals import TrackSignals
from TrackModel.TrackModelUi import TrackModelMainUI
from TrackModel.TrackModelTestUi import TrackModelUiTest
from TrackControllerSoftware.TrackControllerSoftware import Track_Controller
from TrackControllerSoftware.programmerUI import programmer_UI
from TrackControllerSoftware.testUI import test_ui
from signals.trackcontroller_signals import TrackCTCSignals
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator


track_signals = TrackSignals()
ctc_signals = TrackCTCSignals()
trc = Track_Controller(ctc_signals,track_signals)
trm = TrackModel(track_signals)



app = QApplication(sys.argv)
testUi = QDialog()
ui3 = TrackModelUiTest(track_signals, trm)
ui3.setupUi(testUi)
testUi.show()

# app2 = QApplication(sys.argv)

renameDialog = QDialog()
ui2 = TrackModelMainUI(trm)
ui2.setupUi(renameDialog)
renameDialog.show()


e2 = programmer_UI(trc)
e3 = test_ui(trc)

sys.exit(app.exec_())

