from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QWidget

import pandas as pd

from lib.FlowJobProblem import FlowJobProblem


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
        self.minimize = "Cmax"
        self.problem = {
            "jobsMatrix": [],
            "jobsDelayArray": [],
            "preparationMatrix": [],
            "type": "normal",
            "sequenceSelectionAlgo": self.sequenceSelectionAlgo,
            "minimize": self.minimize,
        }

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
        self.processing_time_error_label.setText("")
        self.processing_time_file_name.setText(file)
        self.processingTimeFile = file

    def updateDelayFileName(self, file):
        self.delay_error_label.setText("")
        self.delay_file_name.setText(file)
        self.delayFile = file

    def updatePreparationFileName(self, file):
        self.preparation_error_label.setText("")
        self.preparation_file_name.setText(file)
        self.preparationFile = file

    def handleDelayChange(self):
        self.delay_error_label.setText("")
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
        self.preparation_error_label.setText("")
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
        self.problem["sequenceSelectionAlgo"] = self.sequenceSelectionAlgo

    def handleMinimizationChange(self):
        isCmax = self.CmaxRadioButton.isChecked()
        self.minimize = "Cmax" if isCmax else "TT"
        self.problem["minimize"] = self.minimize

    def readAndValidateProcessingTimeFile(self):
        show_error = self.processing_time_error_label.setText
        show_error("")

        try:
            jobsMatrix = pd.read_excel(self.processingTimeFile).values.tolist()

        except Exception as e:
            show_error("Couldn't read file")
            return False

        if len(jobsMatrix) < 2:
            show_error("A Flow Job Problem should have at least two machines")
            return False

        if len(jobsMatrix[0]) < 2:
            show_error("All machines should have at least two jobs")
            return False

        if any(len(machine) != len(jobsMatrix[0]) for machine in jobsMatrix):
            show_error(
                "All machines in a flow job problem should have the same number of jobs"
            )
            return False

        if any(not isinstance(v, int) for v in sum(jobsMatrix, [])):
            show_error(
                "all values in this excel file should be intigers except first row"
            )
            return False

        self.problem["jobsMatrix"] = jobsMatrix
        return True

    def readAndValidateDelayFile(self):
        show_error = self.delay_error_label.setText
        show_error("")

        try:
            jobsDelayArray = pd.read_excel(self.delayFile).values.tolist()[0]
        except Exception as e:
            show_error("Couldn't read file")
            return False

        if any(not isinstance(v, int) for v in jobsDelayArray):
            show_error(
                "all values in this excel file should be intigers except first row"
            )
            return False

        if len(jobsDelayArray) != len(self.problem["jobsMatrix"][0]):
            show_error(
                "File should have {} columns (same number of jobs specified in processing time file)".format(
                    len(self.problem["jobsMatrix"][0])
                )
            )
            return False

        self.problem["jobsDelayArray"] = jobsDelayArray
        return True

    def readAndValidatePreparationFile(self):
        show_error = self.preparation_error_label.setText
        show_error("")

        try:
            excelFile = pd.ExcelFile(self.preparationFile)
        except Exception as e:
            show_error("Couldn't read file")
            return False

        if len(excelFile.sheet_names) != len(self.problem["jobsMatrix"]):
            show_error(
                "Excel File should have {} worksheet (same number of machines specified in processing time file)".format(
                    len(self.problem["jobsMatrix"])
                )
            )
            return False

        preparationMatrix = []
        for sheet in excelFile.sheet_names:
            preparationMatrix.append(excelFile.parse(sheet).values.tolist())

        numberOfJobs = len(self.problem["jobsMatrix"][0])

        if any(
            len(machinePreparationMatrix) != numberOfJobs
            or any(
                len(element) != numberOfJobs
                or any(not isinstance(i, int) for i in element)
                for element in machinePreparationMatrix
            )
            for machinePreparationMatrix in preparationMatrix
        ):
            show_error(
                "Every sheet should be exactly an n by n matrix where n is the number of jobs"
            )
            return False

        self.problem["preparationMatrix"] = preparationMatrix
        return True

    def nextFunc(self):
        isDelayChecked = self.delayCheckBox.isChecked()
        isPreparationChecked = self.preparationCheckBox.isChecked()

        # if processingFile do not exist
        if not self.processingTimeFile:
            # show error processing time required
            return self.processing_time_error_label.setText(
                "Processing Time File is required."
            )
        # else read and validate the file
        else:
            done = self.readAndValidateProcessingTimeFile()
            if not done:
                return

        # if delay is checked and delayFile do not exist
        if isDelayChecked and not self.delayFile:
            # show error delay file required
            return self.delay_error_label.setText("Delay File is required.")
        # else read and validate delay file
        elif isDelayChecked:
            done = self.readAndValidateDelayFile()
            if not done:
                return

        # if preparation is checked and preparationFile do not exist
        if isPreparationChecked and not self.preparationFile:
            # show error preparation file required
            return self.preparation_error_label.setText("Preparation File is required.")
        # else read and validate preparation file
        elif isPreparationChecked:
            done = self.readAndValidatePreparationFile()
            if not done:
                return

        typeOfProblem = ["normal", "delay", "preparation", "delay_and_preparation"][
            isDelayChecked + isPreparationChecked * 2
        ]

        flowJobProblem = FlowJobProblem(
            jobsMatrix=self.problem["jobsMatrix"],
            jobsDelayArray=self.problem["jobsDelayArray"],
            preparationMatrix=self.problem["preparationMatrix"],
            type=typeOfProblem,
        )

        self.problem["type"] = typeOfProblem
        self.problem["sequenceSelectionAlgo"] = self.sequenceSelectionAlgo
        self.problem["minimize"] = self.minimize

        self.master.flowJobProblem = flowJobProblem
        self.master.problem = self.problem
        self.master.goTo("showSolution")
        self.master.pages["showSolution"].innerWidget.showGantt()
