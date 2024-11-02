class QueensSolver:

    def __init__(self, nr_of_queens, areas):
        self.nr_of_queens = nr_of_queens
        self.areas = areas
        self.board = [[0 for _ in range(nr_of_queens)] for row in range(nr_of_queens)]
    
    
    def solve(self):
        if self.place_queen(col=0) == False:
            print("Solution does not exist")
            return False
        self.printSolution()
        return True
    
    def place_queen(self, col):
        if self.two_queens_on_same_color():
            return False   
        if col >= self.nr_of_queens:
            return True
        for i in range(self.nr_of_queens):
            if self.is_safe(row=i, col=col):
                self.board[i][col] = 1
                if self.place_queen(col=col + 1) == True:
                    return True
                self.board[i][col] = 0
        return False

    def printSolution(self):
        for i in range(self.nr_of_queens):
            for j in range(self.nr_of_queens):
                if self.board[i][j] == 1:
                    print(self.areas[i][j],end=" ")
                else:
                    print(".",end=" ")
            print()

    def find_queens(self): 
        queens_positions = [] 
        for i in range(len(self.board)): 
            for j in range(len(self.board)): 
                if self.board[i][j] == 1: 
                    queens_positions.append((i, j)) 
        return queens_positions

    def are_on_same_color(self, pos1, pos2):
        row1, col1 = pos1 
        row2, col2 = pos2
        return self.areas[row1][col1] == self.areas[row2][col2]

    def is_safe(self, row, col):

        for i in range(col):
            if self.board[row][i] == 1:
                return False

        left_diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in left_diagonal_directions: 
            r, c = row + dr, col + dc 
            if 0 <= r < self.nr_of_queens and 0 <= c < self.nr_of_queens:
                if self.board[r][c] == 1:
                    return False

        return True

    def two_queens_on_same_color(self):
        queen_pos = self.find_queens()
        for pos1 in queen_pos:
            for pos2 in queen_pos:
                if pos1 != pos2:
                    if self.are_on_same_color(pos1,pos2):
                        return True
        return False