from lib import FlowJobProblem
from lib.sequences import getSigmaJohnson


class CDS:
    def __init__(self, problem: FlowJobProblem.FlowJobProblem) -> None:
        self.problem = problem
        self.solution = None

    def getSolution(self):
        optimalSequence = getSigmaJohnson(*self.generateTwoVirtualMachines(1))
        optimalTime = self.problem.getCMax(optimalSequence)

        for k in range(2, len(self.problem.jobsMatrix)):
            johnsonsSequence = getSigmaJohnson(*self.generateTwoVirtualMachines(k))
            time = self.problem.getCMax(johnsonsSequence)

            if time < optimalTime:
                optimalTime = time
                optimalSequence = johnsonsSequence

        # self.solution = {
        #     "sequence": optimalSequence,
        #     "C_max": optimalTime
        # }

        return self.problem.generateSolution(optimalSequence)

    def getSolutionWithDelay(self):
        optimalSequence = getSigmaJohnson(*self.generateTwoVirtualMachines(1))
        solution = self.problem.generateSolution(optimalSequence)
        TotalTardiness = self.problem.getTotalTardiness(solution)

        for k in range(2, len(self.problem.jobsMatrix)):
            johnsonsSequence = getSigmaJohnson(*self.generateTwoVirtualMachines(k))
            solution = self.problem.generateSolution(johnsonsSequence)
            newTotalTardiness = self.problem.getTotalTardiness(solution)

            if newTotalTardiness < TotalTardiness:
                TotalTardiness = newTotalTardiness
                optimalSequence = johnsonsSequence

        # self.solution = {
        #     "sequence": optimalSequence,
        #     "C_max": self.problem.getCMax(johnsonsSequence),
        #     "TotalTardiness": TotalTardiness
        # }

        return solution

    def generateTwoVirtualMachines(self, k: int):
        firstKMachines = zip(*self.problem.jobsMatrix[0:k])
        lastKMachines = zip(*self.problem.jobsMatrix[-k:])

        virtualMachineOne = [sum(v) for v in firstKMachines]
        virtualMachineTwo = [sum(v) for v in lastKMachines]

        return [virtualMachineOne, virtualMachineTwo]
