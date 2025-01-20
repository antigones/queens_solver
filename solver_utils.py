from sty import bg

def print_solution(board, nr_of_queens, color_areas):
    bg_colors = [bg(200+(i*10)) for i in range(nr_of_queens)]
    for i in range(nr_of_queens):
        for j in range(nr_of_queens):
            if board[i][j] == 1:
                print(bg_colors[color_areas[i][j]]+'👑 '+bg.rs,end='')
            else:
                print(bg_colors[color_areas[i][j]]+' . '+bg.rs,end='')
        print()