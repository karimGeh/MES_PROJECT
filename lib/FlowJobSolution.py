from lib import FlowJobProblem


class FlowJobSolution:
    def __init__(self, problem, sequence: list[int], CArray: list[list[int]]) -> None:
        self.problem: FlowJobProblem.FlowJobProblem = problem
        self.sequence = sequence
        self.CArray = CArray

    def getCMax(self):
        return self.CArray[self.problem.numberOfMachines - 1][self.sequence[-1]]
