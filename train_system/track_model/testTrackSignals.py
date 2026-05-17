import sys
from TrackModel import TrackModel
from signals.track_signals import TrackSignals
from TrackModelUi import TrackModelMainUI
from TrackModelTestUi import TrackModelUiTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator


track_signals = TrackSignals()
trm = TrackModel(track_signals)


app3 = QApplication(sys.argv)
testUi = QDialog()
ui3 = TrackModelUiTest(track_signals, trm)
ui3.setupUi(testUi)
testUi.show()

app2 = QApplication(sys.argv)
renameDialog = QDialog()
ui2 = TrackModelMainUI(trm)
ui2.setupUi(renameDialog)
renameDialog.show()

sys.exit(app2.exec_())

# TO DO: copy update and handler functions into the main UI and instantiate main UI here

# TO DO: copy update and handler functions into the main UI and instantiate main UI here