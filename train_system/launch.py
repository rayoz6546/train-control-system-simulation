import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from signals.launcher import Launcher

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
e = Launcher()
sys.exit(app.exec_())
