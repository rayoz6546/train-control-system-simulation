import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from Track_Controller_Hardware.TestHWlauncher import Launcher

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
e = Launcher()
sys.exit(app.exec_())