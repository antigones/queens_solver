from queens_solver import QueensSolver
from anim_utils import print_solution
import urwid

frame = 0

def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

def refresh(_loop, _data):
    if _data == len(moves):
        return
    outputTxt = print_solution(board=moves[_data],nr_of_queens=N,color_areas=BOARD_COLORS)
    
    txt.set_text(outputTxt)
    _data += 1
    loop.set_alarm_in(0.2, refresh, _data)

N = 10

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

solver = QueensSolver(nr_of_queens=N,color_areas=BOARD_COLORS)
could_solve, solution, moves = solver.solve()

if could_solve:
    moves = moves[5000:]
    outputTxt = print_solution(board=moves[frame],nr_of_queens=N,color_areas=BOARD_COLORS)

    txt = urwid.Text(outputTxt)
    fill = urwid.Filler(txt, 'top')

    loop = urwid.MainLoop(fill, unhandled_input=unhandled_input)
    frame += 1
    loop.set_alarm_in(1, refresh, frame)
    loop.run()