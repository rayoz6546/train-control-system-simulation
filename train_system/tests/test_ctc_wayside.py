import sys
from CTC.CTC import CTC
from CTC.Train import Train
from TrackControllerSoftware.TrackControllerSoftware import Track_Controller
from signals.trackcontroller_signals import TrackCTCSignals
from signals.track_signals import TrackSignals
from TrackControllerSoftware.programmerUI import programmer_UI
from TrackControllerSoftware.UI import ui
#from TrackControllerSoftware.testUI import test_ui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator
from CTC.mainUI import mainUI
from CTC.testUI import testUI

signal = TrackCTCSignals()
tr_signals = TrackSignals()
ctc = CTC(signal)
tc = Track_Controller(signal,tr_signals)

app = QApplication(sys.argv)
#e = testUI(ctc)
e1 = mainUI(ctc)

e2 = programmer_UI(tc)
e3 = ui(tc)
#e3 = test_ui(tc)
sys.exit(app.exec_())