from typing import List
from lib import FlowJobSolution
import matplotlib.pyplot as plt


class GanttDiagram:
    def __init__(self, solution: FlowJobSolution.FlowJobSolution) -> None:
        self.problem = solution.problem
        self.solution = solution
        self.sequence = solution.sequence

    def getJobMetaData(self, job: int, machine: int) -> dict:
        timeOnMachine = self.problem.getTimeOfJobOnMachine(job, machine)
        return {
            "timeOnMachine": timeOnMachine,
            "startTime": self.solution.getC(job, machine) - timeOnMachine,
            "finishTime": self.solution.getC(job, machine),
        }

    def generateNrandomColors(self, n: int) -> List[str]:
        f = plt.cm.get_cmap("hsv", n)
        return [f(i) for i in range(n)]

    def generateXYChart(self):
        colors = self.generateNrandomColors(self.problem.numberOfJobs)
        y = []
        x = []
        startTime = []
        for machineIndex in range(self.problem.numberOfMachines):
            jobs = self.sequence
            timeOnFirstMachine = [
                self.getJobMetaData(i, machineIndex)["timeOnMachine"] for i in jobs
            ]
            startTimeOnFirstMachine = [
                self.getJobMetaData(i, machineIndex)["startTime"] for i in jobs
            ]
            y = [self.problem.numberOfMachines - machineIndex] * len(jobs) + y
            x = timeOnFirstMachine + x
            startTime = startTimeOnFirstMachine + startTime

        return [x, y, startTime, colors]
