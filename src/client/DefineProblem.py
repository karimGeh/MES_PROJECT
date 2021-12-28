from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QWidget


class DefineProblem(QWidget):
    def __init__(self, master):
        super(DefineProblem, self).__init__()
        self.master = master

        loadUi("./src/ui/defineProblem.ui", self)

        # connect buttons
        self.nextButton.clicked.connect(self.nextFunc)
        self.backButton.clicked.connect(self.back)
        self.processingTimeFileButton.clicked.connect(self.getProcessingTimeFile)
        self.delayFileButton.clicked.connect(self.getDelayFile)
        self.preparationFileButton.clicked.connect(self.getPreparationFile)

        self.delayCheckBox.stateChanged.connect(self.handleDelayChange)
        self.preparationCheckBox.stateChanged.connect(self.handlePreparationChange)

        self.availableSelectionAlgorithms = ["CDS Algorithm", "Proper Time of Job"]

        for algo in self.availableSelectionAlgorithms:
            self.selectionAlgoSelect.addItem(algo)

        self.selectionAlgoSelect.setCurrentIndex(0)
        self.selectionAlgoSelect.currentTextChanged.connect(
            self.handleSelectionAlgoChange
        )

        self.CmaxRadioButton.setChecked(True)
        self.CmaxRadioButton.toggled.connect(self.handleMinimizationChange)

        # local variables
        self.processingTimeFile = ""
        self.delayFile = ""
        self.preparationFile = ""
        self.sequenceSelectionAlgo = self.selectionAlgoSelect.currentText()
        self.minimizationAlgo = "Cmax"

    def back(self):
        self.master.goTo("welcomeScreen")

    def getProcessingTimeFile(self):
        file, *_ = QFileDialog.getOpenFileName(
            self, "Select file", filter="Excel file (*.xlsx *.xls)"
        )
        self.updateProcessingTimeFileName(file)

    def getDelayFile(self):
        file, *_ = QFileDialog.getOpenFileName(
            self, "Select file", filter="Excel file (*.xlsx *.xls)"
        )
        self.updateDelayFileName(file)

    def getPreparationFile(self):
        file, *_ = QFileDialog.getOpenFileName(
            self, "Select file", filter="Excel file (*.xlsx *.xls)"
        )
        self.updatePreparationFileName(file)

    def updateProcessingTimeFileName(self, file):
        self.processing_time_file_name.setText(file)
        self.processingTimeFile = file

    def updateDelayFileName(self, file):
        self.delay_file_name.setText(file)
        self.delayFile = file

    def updatePreparationFileName(self, file):
        self.preparation_file_name.setText(file)
        self.preparationFile = file

    def handleDelayChange(self):
        isProperTimeAlgo = self.selectionAlgoSelect.currentIndex() == 1
        isChecked = self.delayCheckBox.isChecked()
        self.delayFrame.setEnabled(isChecked)

        self.CDSFrame.setEnabled(isChecked and not isProperTimeAlgo)
        if isChecked == True:
            return

        # if delay is turned off
        self.CmaxRadioButton.setChecked(True)
        self.updateDelayFileName("")

    def handlePreparationChange(self):
        isChecked = self.preparationCheckBox.isChecked()

        self.preparationFrame.setEnabled(isChecked)
        self.sequenceSelectionAlgoFrame.setEnabled(isChecked)

        if isChecked == True:
            return

        # if preparation is turned off
        self.selectionAlgoSelect.setCurrentIndex(0)
        self.updatePreparationFileName("")

    def handleSelectionAlgoChange(self):
        isDelayChecked = self.delayCheckBox.isChecked()
        isProperTimeAlgo = self.selectionAlgoSelect.currentIndex() == 1

        self.CDSFrame.setEnabled(isDelayChecked and not isProperTimeAlgo)

        self.sequenceSelectionAlgo = self.selectionAlgoSelect.currentText()

    def handleMinimizationChange(self):
        isCmax = self.CmaxRadioButton.isChecked()
        self.minimizationAlgo = "Cmax" if isCmax == True else "TT"

    def nextFunc(self):
        # Todo: process and validate files
        print(self.processingTimeFile)
        print(self.delayFile)
        print(self.preparationFile)
        print(self.sequenceSelectionAlgo)
        print(self.minimizationAlgo)
