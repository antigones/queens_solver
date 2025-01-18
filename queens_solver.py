from collections import defaultdict
from copy import deepcopy

class QueensSolver:

    def __init__(self, nr_of_queens, color_areas):
        self.nr_of_queens = nr_of_queens
        self.color_areas = color_areas
        self.board = [[0 for _ in range(nr_of_queens)] for _ in range(nr_of_queens)]
        self.moves = []
    
    def solve(self):
        placed_queens_positions = defaultdict(list)
        if self.place_queen(col=0,placed_queens_positions=placed_queens_positions) == False:
            return (False,[],[])
        return (True,self.board,self.moves)
    
    def place_queen(self, col, placed_queens_positions):
        self.moves.append(deepcopy(self.board))
        if self.two_queens_on_same_color(placed_queens_positions=placed_queens_positions):
            return False   
        if col >= self.nr_of_queens:
            return True
        
        for i in range(self.nr_of_queens):
            if self.is_safe(row=i, col=col):
                self.board[i][col] = 1
                position_color = self.color_areas[i][col]
                placed_queens_positions[position_color].append((i,col))
                
                if self.place_queen(col=col + 1, placed_queens_positions=placed_queens_positions) == True:
                    return True
                self.board[i][col] = 0
                placed_queens_positions[position_color].remove((i,col))
        return False

    def are_on_same_color(self, pos1, pos2):
        row1, col1 = pos1 
        row2, col2 = pos2
        return self.color_areas[row1][col1] == self.color_areas[row2][col2]

    def is_safe(self, row, col):
        for i in range(col):
            if self.board[row][i] == 1:
                return False
        diagonal_neighbours_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diagonal_neighbours_offsets: 
            r, c = row + dr, col + dc 
            if 0 <= r < self.nr_of_queens and 0 <= c < self.nr_of_queens:
                if self.board[r][c] == 1:
                    return False
        return True

    def two_queens_on_same_color(self, placed_queens_positions):
        
        # use collections.Counter to count queens on area
        return any(len(value) > 1 for value in placed_queens_positions.values())
        """
        queen_pos = placed_queens_positions
        for pos1 in queen_pos:
            for pos2 in queen_pos:
                if pos1 != pos2:
                    if self.are_on_same_color(pos1,pos2):
                        return True
        return False
        """