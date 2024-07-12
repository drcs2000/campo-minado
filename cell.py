class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self):
        self.is_revealed = True

    def flag(self):
        self.is_flagged = not self.is_flagged

    def calculate_adjacent_mines(self, board, row, col):
        self.adjacent_mines = sum([board.is_mine(r, c)
                                   for r in range(row-1, row+2)
                                   for c in range(col-1, col+2)
                                   if 0 <= r < board.num_rows and 0 <= c < board.num_columns])
