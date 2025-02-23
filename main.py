from solver_utils import print_solution

BOARD_COLORS_1 = [
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

board = 1
method = "binary"

if board == 1:

    BOARD_COLORS = BOARD_COLORS_1
    N = len(BOARD_COLORS)
    if method == "integer":
        from GeneticSolverInteger import GeneticSolver as Solver
        solver = Solver(seed=577781055, crossover_proba=1/N, pop_size=600, mutate_proba=1.0/N, generations=400, use_elitism=True, color_areas=BOARD_COLORS, nr_of_queens=N)
    elif method == "binary":
        from GeneticSolverBinary import GeneticSolver as Solver
        solver = Solver(seed=666317534, crossover_proba=0.9, pop_size=1000, mutate_proba=0.2, generations=200, use_elitism=False, mate="twopoint", color_areas=BOARD_COLORS, nr_of_queens=N)
    else:
        from CPlexSolver import CPlexSolver as Solver
        solver = Solver(color_areas=BOARD_COLORS, nr_of_queens=N)

elif board == 2:

    BOARD_COLORS = BOARD_COLORS_2
    N = len(BOARD_COLORS)
    if method == "integer":
        from GeneticSolverInteger import GeneticSolver as Solver
        solver = Solver(seed=32748968, crossover_proba=1.0/N, pop_size=200, mutate_proba=1.0/N, generations=300, use_elitism=True, color_areas=BOARD_COLORS, nr_of_queens=N)
    elif method == "binary":
        from GeneticSolverBinary import GeneticSolver as Solver
        solver = Solver(seed=473065221, crossover_proba=0.9, pop_size=200, mutate_proba=0.3, generations=100, use_elitism=False, mate="onepoint", color_areas=BOARD_COLORS, nr_of_queens=N)
    else:
        from CPlexSolver import CPlexSolver as Solver
        solver = Solver(color_areas=BOARD_COLORS, nr_of_queens=N)

else:

    BOARD_COLORS = BOARD_COLORS_3
    N = len(BOARD_COLORS)
    if method == "integer":
        from GeneticSolverInteger import GeneticSolver as Solver
        solver = Solver(seed=460212636, crossover_proba=1.0/N, pop_size=400, mutate_proba=1.0/N, generations=100, use_elitism=True, color_areas=BOARD_COLORS, nr_of_queens=N)
    elif method == "binary":
        from GeneticSolverBinary import GeneticSolver as Solver
        solver = Solver(seed=618414986, crossover_proba=0.9, pop_size=1000, mutate_proba=0.2, generations=50, use_elitism=True, mate="twopoint", color_areas=BOARD_COLORS, nr_of_queens=N)
    else:
        from CPlexSolver import CPlexSolver as Solver
        solver = Solver(color_areas=BOARD_COLORS, nr_of_queens=N)


if __name__ == '__main__':
    could_solve, solution, _ = solver.solve()
    print_solution(board=solution, nr_of_queens=N, color_areas=BOARD_COLORS)
    if not could_solve:
        print('Could not solve')
