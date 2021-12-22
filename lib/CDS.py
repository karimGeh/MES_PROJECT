from lib import FlowJobProblem
from lib.SigmaJohnson import getSigmaJohnson


class CDS:
    def __init__(self, problem: FlowJobProblem.FlowJobProblem) -> None:
        self.problem = problem
        self.solution = None

    def getSolution(self):
        if self.solution:
            return self.solution

        optimalSequence = getSigmaJohnson(*self.generateTwoVirtualMachines(1))
        optimalTime = self.problem.getCMax(optimalSequence)

        for k in range(2, len(self.problem.jobsMatrix)):
            johnsonsSequence = getSigmaJohnson(
                *self.generateTwoVirtualMachines(k)
            )
            time = self.problem.getCMax(johnsonsSequence)

            if time < optimalTime:
                optimalTime = time
                optimalSequence = johnsonsSequence

        self.solution = {
            "sequence": optimalSequence,
            "C_max": optimalTime
        }

        return self.solution

    def generateTwoVirtualMachines(self, k: int):
        firstKMachines = zip(*self.problem.jobsMatrix[0:k])
        lastKMachines = zip(*self.problem.jobsMatrix[-k:])

        virtualMachineOne = [sum(v) for v in firstKMachines]
        virtualMachineTwo = [sum(v) for v in lastKMachines]

        return [virtualMachineOne, virtualMachineTwo]
