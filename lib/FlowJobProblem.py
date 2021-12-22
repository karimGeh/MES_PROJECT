"""
this file define the class of Flow Job Problem

"""
from lib import FlowJobSolution

OBJECT_OF_AVAILABLE_TYPES = {
    "normal": 0,
    "delay": 1,
    "preparation": 2,
    "delay_and_preparation": 3
}


def raiseError(message: str):
    raise RuntimeError(message)


class FlowJobProblem:
    def __init__(
        self,
        jobsMatrix: list[list[int]],
        jobsDelayArray: list[int] = [],
        preparationMatrix: list[list[int]] = [],
        type: str = "normal"
    ) -> None:
        #!
        #! default validation - start
        if type not in OBJECT_OF_AVAILABLE_TYPES:
            return raiseError("Type of problem do not exist,\n Available types are:" +
                              list(OBJECT_OF_AVAILABLE_TYPES.keys()).__repr__())
        if len(jobsMatrix) < 2:
            return raiseError("A Flow Job Problem should have at least two machines")

        if len(jobsMatrix[0]) < 2:
            return raiseError("All machines should have at least two jobs")

        if any(len(machine) != len(jobsMatrix[0]) for machine in jobsMatrix):
            return raiseError("All machines in a flow job problem should have the same number of jobs")
        #! default validation - end
        #!

        self.type = OBJECT_OF_AVAILABLE_TYPES[type]

        self.jobsMatrix = jobsMatrix
        self.jobsDelayArray = jobsDelayArray
        self.preparationMatrix = preparationMatrix

        self.numberOfMachines = len(jobsMatrix)
        self.numberOfJobs = len(jobsMatrix[0])

        #!
        #! related type validation - start
        """
        if self.type == OBJECT_OF_AVAILABLE_TYPES["normal"]:
            "do nothing"
        """

        if(
            self.type == OBJECT_OF_AVAILABLE_TYPES["delay"] or
            self.type == OBJECT_OF_AVAILABLE_TYPES["delay_and_preparation"]
        ):
            # check if length of delay array == number of jobs we have
            if len(self.jobsDelayArray) != self.numberOfJobs:
                return raiseError("length of delay array should be the same as number of jobs")
            "else do nothing"

        if (
            self.type == OBJECT_OF_AVAILABLE_TYPES["preparation"] or
            self.type == OBJECT_OF_AVAILABLE_TYPES["delay_and_preparation"]
        ):
            # check if the length of preparation matrix is the same as number of machines
            if len(self.preparationMatrix) != self.numberOfMachines:
                return raiseError("length of preparation matrix should be the same as number of machines")

            # check if all preparation element is an n by n matrix where n is number of jobs
            elif any(
                    len(machinePreparationMatrix) != self.numberOfJobs or
                    any(
                        len(element) != self.numberOfJobs
                        for element in machinePreparationMatrix
                    )
                    for machinePreparationMatrix in preparationMatrix
            ):
                return raiseError("the preparation matrix should have m 2d-array, where m is the number of machines, each 2d-array is n by n matrix, where n is the number of jobs we have")

            "else do nothing"
        #! related type validation - end
        #!

        self.solutions: list[FlowJobSolution.FlowJobSolution] = []

    def getTimeOfJobOnMachine(
        self, job: int, machine: int
    ) -> int:
        return self.jobsMatrix[machine][job]

    def getPreparationTimeOfJob(
        self, job: int, previous_job: int, machine: int
    ):
        return self.preparationMatrix[machine][previous_job][job]

    def normalModel(self, jobIndex, machineIndex, sequence, CArray):
        if jobIndex == 0 and machineIndex == 0:
            return self.getTimeOfJobOnMachine(
                sequence[jobIndex], machineIndex)

        if jobIndex == 0:
            return (
                self.getC(0, machineIndex - 1, sequence, CArray)[0]
                + self.getTimeOfJobOnMachine(sequence[jobIndex], machineIndex)
            )

        if machineIndex == 0:
            return (
                self.getC(sequence[jobIndex - 1], 0, sequence, CArray)[0]
                + self.getTimeOfJobOnMachine(sequence[jobIndex], machineIndex)
            )

        return (
            max(
                self.getC(sequence[jobIndex - 1],
                          machineIndex, sequence, CArray)[0],
                self.getC(jobIndex, machineIndex - 1, sequence, CArray)[0],
            )
            + self.getTimeOfJobOnMachine(sequence[jobIndex], machineIndex)
        )

    def preparationModel(self, jobIndex, machineIndex, sequence, CArray):
        if jobIndex == 0 and machineIndex == 0:
            return (
                self.getTimeOfJobOnMachine(sequence[jobIndex], machineIndex)
                + self.getPreparationTimeOfJob(
                    sequence[jobIndex], sequence[jobIndex], machineIndex
                )
            )

        if jobIndex == 0:
            return (
                max(
                    self.getC(0, machineIndex - 1, sequence, CArray)[0],
                    self.getPreparationTimeOfJob(
                        sequence[jobIndex], sequence[jobIndex], machineIndex),
                )
                + self.getTimeOfJobOnMachine(sequence[jobIndex], machineIndex)
            )

        if machineIndex == 0:
            return (
                self.getC(jobIndex - 1, 0, sequence, CArray)[0]
                + self.getPreparationTimeOfJob(
                    sequence[jobIndex], sequence[jobIndex - 1], machineIndex
                )
                + self.getTimeOfJobOnMachine(sequence[jobIndex], machineIndex)
            )

        return (
            max(
                self.getC(jobIndex, machineIndex - 1, sequence, CArray)[0],
                self.getC(jobIndex - 1, machineIndex, sequence, CArray)[0]
                + self.getPreparationTimeOfJob(
                    sequence[jobIndex], sequence[jobIndex - 1], machineIndex
                ),
            )
            + self.getTimeOfJobOnMachine(sequence[jobIndex], machineIndex)
        )

    def getC(self, jobIndex, machineIndex, sequence, CArray):
        for solution in self.solutions:
            if solution.sequence == sequence:
                CArray = solution.CArray

        if CArray[machineIndex][sequence[jobIndex]] >= 0:
            COfJob = CArray[machineIndex][sequence[jobIndex]]
            return [COfJob, CArray]

        if(
            self.type == OBJECT_OF_AVAILABLE_TYPES["preparation"] or
            self.type == OBJECT_OF_AVAILABLE_TYPES["delay_and_preparation"]
        ):
            COfJob = self.preparationModel(
                jobIndex, machineIndex, sequence, CArray)
        else:
            COfJob = self.normalModel(jobIndex, machineIndex, sequence, CArray)

        CArray[machineIndex][sequence[jobIndex]] = COfJob

        return [COfJob, CArray]

    def getCMax(self, sequence: list[int]):
        if not sequence or len(sequence) != self.numberOfJobs:
            raiseError("sequence should be of length number of jobs")

        for solution in self.solutions:
            if solution.sequence == sequence:
                return solution.getCMax()

        solution = self.generateSolution(sequence)

        return solution.getCMax()

    def generateSolution(self, sequence: list[int]) -> FlowJobSolution.FlowJobSolution:
        CArray = [
            [-1 for _ in range(self.numberOfJobs)]
            for _ in range(self.numberOfMachines)
        ]

        _, CArray = self.getC(self.numberOfJobs - 1,
                              self.numberOfMachines - 1, sequence, CArray)

        solution = FlowJobSolution.FlowJobSolution(self, sequence, CArray)
        self.solutions.append(solution)

        return solution
