from PyQt5 import QtGui, QtWidgets

# !
from utils.InnerWidget import InnerWidget

# ! widgets
from client.WelcomeScreen import WelcomeScreen
from client.DefineProblem import DefineProblem
from client.ShowSolution import ShowSolution


# class App(QtWidgets.QStackedWidget):
class App(QtWidgets.QStackedWidget):
    def __init__(self) -> None:
        super(App, self).__init__()

        self.pages = {
            "welcomeScreen": InnerWidget(self, WelcomeScreen),
            "defineProblem": InnerWidget(self, DefineProblem),
            "showSolution": InnerWidget(self, ShowSolution),
        }

        for value in self.pages.values():
            self.addWidget(value.innerWidget)

        self.setWindowTitle("Flow Job Optimization Software")
        self.setFixedHeight(700)
        self.setFixedWidth(1000)
        self.setCurrentIndex(self.pages["welcomeScreen"].index)

    def goTo(self, page):
        if page not in self.pages:
            raise Exception("page not found")

        self.setCurrentIndex(self.pages[page].index)
