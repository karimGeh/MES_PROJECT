from lib import FlowJobProblem


def getSigmaJohnson(MachineOne: list[int], MachineTwo: list[int]):
    jobs = [[i, j] for i, j in zip(MachineOne, MachineTwo)]

    U = [k for k, u in enumerate(jobs) if u[0] <= u[1]]
    V = [k for k, v in enumerate(jobs) if v[0] > v[1]]

    U = list(sorted(U, key=lambda k: MachineOne[k]))
    V = list(sorted(V, key=lambda k: MachineTwo[k], reverse=True))

    return U + V  # Sigma Johnson


def getSequenceWithProperTime(problem: FlowJobProblem.FlowJobProblem):
    TP_list = [0 for _ in "0" * problem.numberOfJobs]
    defaultSequence = list(range(problem.numberOfJobs))

    for i in range(problem.numberOfJobs):
        TP_list[i] = sum(
            [
                problem.getTimeOfJobOnMachine(defaultSequence[i], k)
                + problem.getPreparationTimeOfJob(
                    defaultSequence[i], defaultSequence[i], k
                )
                for k in range(problem.numberOfMachines)
            ]
        )

    listOfJobs = [{"index": i, "TP": TP_list[i]} for i in range(problem.numberOfJobs)]

    bestSeq = [
        k["index"]
        for k in sorted(listOfJobs, key=lambda element: element["TP"], reverse=True)
    ]

    return bestSeq
