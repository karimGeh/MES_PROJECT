from typing import List
from lib import FlowJobProblem


class FlowJobSolution:
    def __init__(self, problem, sequence: List[int], CArray: List[List[int]]) -> None:
        self.problem: FlowJobProblem.FlowJobProblem = problem
        self.sequence = sequence
        self.CArray = CArray

    def getCMax(self):
        return self.CArray[self.problem.numberOfMachines - 1][self.sequence[-1]]

    def getC(self, job, machine):
        return self.CArray[machine][job]

    def __repr__(self) -> str:
        return "\n".join(
            [
                f"sequence:{list(map(lambda i:i+1,self.sequence))}",
                "solution array :",
                (
                    "".ljust(5)
                    + ",".join(
                        map(
                            lambda e: ("j" + str(e + 1)).rjust(6),
                            range(self.problem.numberOfJobs),
                        )
                    )
                ),
                *[
                    (
                        f"M{j +1} :".ljust(5)
                        + ",".join(map(lambda e: str(e).rjust(6), machine))
                    )
                    for j, machine in enumerate(self.CArray)
                ],
            ]
        )
