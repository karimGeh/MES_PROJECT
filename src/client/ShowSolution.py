from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets

import matplotlib
from lib.GanttDiagram import GanttDiagram

from lib.sequences import getSequenceWithProperTime

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from lib.FlowJobProblem import FlowJobProblem
from lib.CDS import CDS


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure()
        # self.axes = self.fig.add_subplot()
        super(MplCanvas, self).__init__(self.fig)


class ShowSolution(QWidget):
    def __init__(self, master):
        super(ShowSolution, self).__init__()
        self.master = master

        loadUi("./src/ui/showSolution.ui", self)

        self.mpl_canvas = MplCanvas(self)

        layout = QtWidgets.QVBoxLayout()

        toolbar = NavigationToolbar(self.mpl_canvas, self)

        layout.addWidget(toolbar)
        layout.addWidget(self.mpl_canvas)

        self.chartWidget.setLayout(layout)
        # self.toolbarWidget.setLayout(layout2)

        self.backButton.clicked.connect(self.back)
        self.ganttButton.clicked.connect(self.showGantt)
        self.tfrButton.clicked.connect(self.showTFR)
        self.tarButton.clicked.connect(self.showTAR)

        # variables
        self.solution = None

    def initializeSolution(self):
        flowJobProblem: FlowJobProblem = self.master.flowJobProblem
        problem = self.master.problem

        self.tarButton.setEnabled("preparation" in problem["type"])

        if problem["sequenceSelectionAlgo"] == "CDS Algorithm":
            cds_problem = CDS(flowJobProblem)
            if problem["minimize"] == "Cmax":
                solution = cds_problem.getSolution()
            else:
                solution = cds_problem.getSolutionWithDelay()
        else:
            sequence = getSequenceWithProperTime(flowJobProblem)
            solution = flowJobProblem.generateSolution(sequence)

        self.solution = solution

    def showGantt(self):
        self.initializeSolution()
        self.mpl_canvas.fig.clf()

        ax = self.mpl_canvas.fig.subplots(1)

        gantt = GanttDiagram(self.solution)
        x, y, left, colors = gantt.generateXYChart()

        ax.barh(
            y,
            x,
            left=left,
            color=colors,
        )
        self.sequence_label.setText(
            list(map(lambda i: i + 1, self.solution.sequence)).__repr__()
        )
        if "delay" in self.master.problem["type"]:
            self.ttFrame.setEnabled(True)
            self.tt_label.setText(
                str(self.solution.problem.getTotalTardiness(self.solution))
            )
        else:
            self.ttFrame.setEnabled(False)
            self.tt_label.setText("")

        self.mpl_canvas.fig.canvas.draw()

    def showTFR(self):
        self.initializeSolution()
        self.mpl_canvas.fig.clf()

        ax = self.mpl_canvas.fig.subplots(1)

        ax.bar(
            list(f"m{i+1}" for i in range(self.solution.problem.numberOfMachines)),
            self.solution.getTFR(),
        )

        self.mpl_canvas.fig.canvas.draw()

    def showTAR(self):
        self.initializeSolution()
        self.mpl_canvas.fig.clf()

        ax = self.mpl_canvas.fig.subplots(1)

        ax.bar(
            list(f"m{i+1}" for i in range(self.solution.problem.numberOfMachines)),
            self.solution.getTAR(),
        )

        self.mpl_canvas.fig.canvas.draw()

    def back(self):
        self.master.goTo("defineProblem")
