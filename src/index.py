import sys
from PyQt5.QtWidgets import QApplication

from App import App

import resources


app = QApplication(sys.argv)
widget = App()
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
