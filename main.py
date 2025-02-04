from queens_solver import QueensSolver
from solver_utils import print_solution
from GeneticSolverBinary import GeneticSolver
# from GeneticSolverInteger import GeneticSolver
from CPlexSolver import CPlexSolver

# Non Risolvibile
# BOARD_COLORS = [
#     [0,1,1,1,1,1,1,1,1,2],
#     [0,0,1,1,1,1,1,3,2,2],
#     [4,0,0,5,1,1,3,3,2,9],
#     [4,4,0,5,5,1,3,7,2,9],
#     [4,4,6,6,5,1,7,7,2,9],
#     [4,4,4,6,5,1,7,8,8,9],
#     [4,4,4,6,5,1,7,8,9,9],
#     [4,4,4,6,6,1,8,8,9,9],
#     [4,4,4,4,6,1,8,9,9,9],
#     [4,4,4,4,4,9,9,9,9,9]
#     ]

BOARD_COLORS = [
    [0,1,1,1,1,1,2,2],
    [1,1,1,3,3,3,2,2],
    [1,1,3,3,3,3,3,3],
    [1,3,3,3,4,4,4,3],
    [5,5,5,5,6,6,4,3],
    [5,5,5,5,6,7,7,7],
    [5,5,5,5,6,7,7,7],
    [5,5,5,5,6,7,7,7],
    ]

N = len(BOARD_COLORS)

if __name__ == '__main__':
    solver = CPlexSolver(color_areas=BOARD_COLORS, nr_of_queens=N, area_version=True)
    # solver = QueensSolver(nr_of_queens=N,color_areas=BOARD_COLORS)
    # solver = GeneticSolver(nr_of_queens=N, color_areas=BOARD_COLORS)
    could_solve, solution, _ = solver.solve()
    print_solution(board=solution, nr_of_queens=N, color_areas=BOARD_COLORS)
    if not could_solve:
        print('Could not solve')
