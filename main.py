from queens_solver import QueensSolver
from solver_utils import print_solution
from GeneticSolverBinary import GeneticSolver
# from GeneticSolverInteger import GeneticSolver
from CPlexSolver import CPlexSolver

# 1 su slide
# CPLEX OK
# GA BINARY KO
# GA INTEGER OK (seed = 577781055, crossover_proba = 1.0 / self.n_queens, pop_size = 600, mutate_proba = 1.0 / self.n_queens, generations = 400, use_elitism = True)
BOARD_COLORS = [
    [0,1,1,1,1,1,1,1,1,2],
    [0,0,1,1,1,1,1,3,2,2],
    [4,0,0,5,1,1,3,3,2,9],
    [4,4,0,5,5,1,3,7,2,9],
    [4,4,6,6,5,1,7,7,2,9],
    [4,4,4,6,5,1,7,8,8,9],
    [4,4,4,6,5,1,7,8,9,9],
    [4,4,4,6,6,1,8,8,9,9],
    [4,4,4,4,6,1,8,9,9,9],
    [4,4,4,4,4,9,9,9,9,9]
    ]

# 2 su slide:
# CPLEX OK
# GA BINARY OK (seed = 473065221, crossover_proba = 0.9, pop_size = 200, mutate_proba = 0.3, generations = 100, use_elitism = False, mate = self.__cxOnePointCustom, mutate = __randMutateCustom)
# GA INTEGER OK (seed = 32748968, crossover_proba = 1.0 / self.n_queens, pop_size = 200, mutate_proba = 1.0 / self.n_queens, generations = 300, use_elitism = True)
BOARD_COLORS_2 = [
    [0,0,0,0,1,1,2,2,2],
    [0,0,0,0,1,3,3,2,2],
    [0,0,0,0,1,3,4,2,2],
    [0,0,0,0,1,3,4,4,2],
    [0,0,0,0,0,0,0,0,0],
    [5,6,6,6,7,0,0,0,0],
    [5,6,6,7,7,0,0,0,0],
    [5,5,5,8,7,0,0,0,0],
    [5,8,8,8,7,0,0,0,0],
    ]

# 3 su slide:
# CPLEX OK
# GA KO
# GA INTEGER OK (seed = 460212636, crossover_proba = 1.0 / self.n_queens, pop_size = 400, mutate_proba = 1.0 / self.n_queens, generations = 100, use_elitism = True)
BOARD_COLORS_3 = [
    [0,1,2,2,2,2,2,2,3,3],
    [1,1,1,2,2,2,4,2,3,3],
    [2,1,2,2,2,2,4,2,3,3],
    [2,2,2,2,4,4,4,4,4,5],
    [2,2,2,2,2,2,4,5,5,5],
    [2,2,2,2,6,6,4,6,6,5],
    [2,7,2,2,6,6,6,6,8,5],
    [7,7,7,6,6,6,6,8,8,8],
    [9,7,9,9,6,6,6,6,8,6],
    [9,9,9,6,6,6,6,6,6,6]
    ]

# Ultima su LinkedIn
LAST_LINKEDIN = [
    [0,1,1,1,1,1,2,2],
    [1,1,1,3,3,3,2,2],
    [1,1,3,3,3,3,3,3],
    [1,3,3,3,4,4,4,3],
    [5,5,5,5,6,6,4,3],
    [5,5,5,5,6,7,7,7],
    [5,5,5,5,6,7,7,7],
    [5,5,5,5,6,7,7,7],
    ]

BOARD_COLORS = BOARD_COLORS
N = len(BOARD_COLORS)

if __name__ == '__main__':
    # solver = CPlexSolver(color_areas=BOARD_COLORS, nr_of_queens=N)
    # solver = QueensSolver(nr_of_queens=N,color_areas=BOARD_COLORS)
    solver = GeneticSolver(nr_of_queens=N, color_areas=BOARD_COLORS)
    could_solve, solution, _ = solver.solve()
    print_solution(board=solution, nr_of_queens=N, color_areas=BOARD_COLORS)
    if not could_solve:
        print('Could not solve')
