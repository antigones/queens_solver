from queens_solver import QueensSolver
from solver_utils import print_solution


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

BOARD_COLORS = [
    [0,0,0,0,1,1,2,2,2],
    [0,0,0,0,1,3,3,2,2],
    [0,0,0,0,1,3,4,2,2],
    [0,0,0,0,1,3,4,4,2],
    [0,0,0,0,0,0,0,0,0],
    [5,6,6,6,7,0,0,0,0],
    [5,6,6,7,7,0,0,0,0],
    [5,5,5,8,7,0,0,0,0],
    [5,8,8,8,7,0,0,0,0]
    ]

N = len(BOARD_COLORS)

if __name__ == '__main__':
    solver = QueensSolver(nr_of_queens=N,color_areas=BOARD_COLORS)
    could_solve, solution, _ = solver.solve()
    if could_solve:
        print_solution(board=solution,nr_of_queens=N,color_areas=BOARD_COLORS)
    else:
        print('Could not solve')
