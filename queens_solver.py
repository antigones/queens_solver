from collections import defaultdict
from copy import deepcopy

class QueensSolver:

    def __init__(self, nr_of_queens, color_areas):
        self.nr_of_queens = nr_of_queens
        self.color_areas = color_areas
        self.moves = []

    def build_board(self, placed_queens_positions):
        board = [[0 for _ in range(self.nr_of_queens)] for _ in range(self.nr_of_queens)]
        for positions in placed_queens_positions.values():
            for row,col in positions:
                board[row][col] = 1
        return board
    
    def solve(self):
        placed_queens_positions = defaultdict(list)

        if self.place_queen(col=0,placed_queens_positions=placed_queens_positions) == False:
            return (False,[],[])
        
        board = self.build_board(placed_queens_positions=placed_queens_positions)
        return (True,board,self.moves)
    
    def place_queen(self, col, placed_queens_positions):
        self.moves.append(self.build_board(placed_queens_positions=placed_queens_positions))

        if col >= self.nr_of_queens and all(len(queens) == 1 for queens in placed_queens_positions.values()):
            print('placed_queens_positions',placed_queens_positions)
            return True
        
        for i in range(self.nr_of_queens):
            if self.is_safe(row=i, col=col, placed_queens_positions=placed_queens_positions):
                position_color = self.color_areas[i][col]
                placed_queens_positions[position_color].append((i,col))
                if self.place_queen(col=col + 1, placed_queens_positions=placed_queens_positions) == True:
                    return True
                placed_queens_positions[position_color].remove((i,col))
        return False

    def is_safe(self, row, col, placed_queens_positions):
        if self.two_queens_on_same_color(placed_queens_positions=placed_queens_positions):
            return False
        for i in range(col):
            if any((row,i) in positions for positions in placed_queens_positions.values()):
                return False
        diagonal_neighbours_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diagonal_neighbours_offsets:
            r, c = row + dr, col + dc
            if 0 <= r < self.nr_of_queens and 0 <= c < self.nr_of_queens:
                if any((r,c) in positions for positions in placed_queens_positions.values()):
                    return False
        return True

    def two_queens_on_same_color(self, placed_queens_positions):
        return any(len(positions) > 1 for positions in placed_queens_positions.values())