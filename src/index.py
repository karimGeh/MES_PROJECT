import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from App import App

import resources


app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("src/favicon.png"))

widget = App()
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
