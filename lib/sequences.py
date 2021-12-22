def getSigmaJohnson(MachineOne: list[int], MachineTwo: list[int]):
    jobs = [[i, j] for i, j in zip(MachineOne, MachineTwo)]

    U = [k for k, u in enumerate(jobs) if u[0] <= u[1]]
    V = [k for k, v in enumerate(jobs) if v[0] > v[1]]

    U = list(sorted(U, key=lambda k: MachineOne[k]))
    V = list(sorted(V, key=lambda k: MachineTwo[k], reverse=True))

    return U + V  # Sigma Johnson
