from lib.CDS import CDS
from lib.FlowJobProblem import FlowJobProblem
from lib.sequences import getSequenceWithProperTime


Author = """
  Created by :  Karim Gehad
  On         :  22/12/2021

  email      :  karimgehad@outlook.com
  github     :  https://github.com/karimGeh
  linkedIn   :  https://www.linkedin.com/in/karim-gehad
"""
print(Author)


jobsMatrix = [
    # 0  1  2  3  4
    [5, 5, 3, 6, 7],  # machine 1
    [2, 4, 5, 5, 3],  # machine 2
    [3, 2, 5, 4, 2],  # machine 3
]

jobsDelayArray = [10, 15, 12, 8, 13]

preparationMatrix = [
    [
        [2, 2, 3, 2, 1],
        [2, 3, 2, 3, 3],
        [3, 2, 3, 4, 2],
        [1, 3, 2, 3, 2],
        [3, 4, 2, 3, 1],
    ],
    [
        [3, 1, 3, 2, 1],
        [3, 3, 2, 3, 3],
        [3, 2, 3, 4, 2],
        [2, 1, 2, 4, 2],
        [2, 3, 2, 3, 2],
    ],
    [
        [2, 3, 1, 2, 3],
        [1, 2, 3, 3, 3],
        [4, 3, 2, 3, 1],
        [3, 2, 2, 1, 2],
        [3, 2, 3, 4, 2],
    ],
]

problem1 = FlowJobProblem(
    jobsMatrix,
    jobsDelayArray=jobsDelayArray,
    preparationMatrix=preparationMatrix,
    type="delay_and_preparation",
)

# CDS_solution = CDS(problem1)

# print(CDS_solution.getSolution())
# solution = problem1.generateSolution([3, 2, 1, 0, 4])
# print(solution)
# print(CDS(problem1).getSolution())
# print(CDS(problem1).getSolutionWithDelay())
solution = problem1.generateSolution(getSequenceWithProperTime(problem1))
print(solution)
