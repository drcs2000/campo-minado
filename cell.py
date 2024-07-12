class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_bomb = False
        self.is_revealed = False
        self.is_flagged = False
        self.bomb_count = 0

    def reveal(self):
        self.is_revealed = True

    def toggle_flag(self):
        self.is_flagged = not self.is_flagged
