import sys
from train_controller.train_controller import TrainController
from train_model.train_model import TrainModel
from signals.train_signals import TrainSignals
from signals.track_signals import TrackSignals
from train_controller.test_ui import TestUI
from train_model.main_ui import Ui_MainUI

# from TrackModel.TrackModelUi import Ui_renameDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator

app = QApplication(sys.argv)
train_signals = TrainSignals()
tc = TrainController(train_signals, True)
tc.launch_driver_ui()
tc.launch_engineer_ui()
controllerUI = TestUI(tc)

# app2 = QApplication(sys.argv)
# renameDialog = QDialog()
# ui2 = Ui_renameDialog(trm)
# ui2.setupUi(renameDialog)
# renameDialog.show()

sys.exit(app.exec_())
