import sys
from train_controller.train_controller import TrainController
from TrackModel.TrackModel import TrackModel
from train_model.train_model import TrainModel
from signals.train_signals import TrainSignals
from signals.track_signals import TrackSignals
from train_controller.driver_ui import DriverUI
from train_model.main_ui import Ui_MainUI
# from TrackModel.TrackModelUi import Ui_renameDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator

train_signals = TrainSignals()
track_signals = TrackSignals()
tc = TrainController(train_signals)
tm = TrainModel(train_signals, track_signals)
trm = TrackModel(track_signals)

app = QApplication(sys.argv)
main_ui = QMainWindow()
ui = Ui_MainUI(tm)
ui.setupUi(main_ui)
main_ui.show()

controllerUI = DriverUI(tc)

# app2 = QApplication(sys.argv)
# renameDialog = QDialog()
# ui2 = Ui_renameDialog(trm)
# ui2.setupUi(renameDialog)
# renameDialog.show()

sys.exit(app.exec_())
