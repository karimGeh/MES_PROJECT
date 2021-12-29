from typing import List
from lib import FlowJobProblem


class FlowJobSolution:
    def __init__(self, problem, sequence: List[int], CArray: List[List[int]]) -> None:
        self.problem: FlowJobProblem.FlowJobProblem = problem
        self.sequence = sequence
        self.CArray = CArray

    def getCMax(self) -> int:
        return self.CArray[self.problem.numberOfMachines - 1][self.sequence[-1]]

    def getC(self, job, machine) -> int:
        return self.CArray[machine][job]

    def getTFR(self) -> int:
        machines = []

        for machine in range(self.problem.numberOfMachines):
            machines.append(
                sum(
                    self.problem.getTimeOfJobOnMachine(j, machine)
                    for j in range(self.problem.numberOfJobs)
                )
                / self.getCMax()
            )

        return machines

    def getTAR(self):
        machines = []

        for machine in range(self.problem.numberOfMachines):
            machines.append(
                (
                    self.getCMax()
                    - sum(
                        self.problem.getTimeOfJobOnMachine(j, machine)
                        for j in range(self.problem.numberOfJobs)
                    )
                    - self.problem.getPreparationTimeOfJob(
                        self.sequence[0], self.sequence[0], machine
                    )
                    - sum(
                        self.problem.getPreparationTimeOfJob(
                            self.sequence[j], self.sequence[j - 1], machine
                        )
                        for j in range(1, self.problem.numberOfJobs)
                    )
                )
                / self.getCMax()
            )

        return machines

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
