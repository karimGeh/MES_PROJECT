from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget


class WelcomeScreen(QWidget):
    def __init__(self, master):
        super(WelcomeScreen, self).__init__()
        self.master = master

        loadUi("./src/ui/landingPage.ui", self)

        # connect buttons
        self.startButton.clicked.connect(self.start)

    def start(self):
        self.master.goTo("defineProblem")
