import random
from cell import Cell

class Board:
    def __init__(self, num_rows, num_columns, num_mines):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_mines = num_mines
        self.cells = [[Cell() for _ in range(num_columns)] for _ in range(num_rows)]
        self.initialize_board()

    def initialize_board(self):
        self.place_mines()
        self.calculate_adjacency()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.num_rows - 1)
            col = random.randint(0, self.num_columns - 1)
            if not self.cells[row][col].is_mine:
                self.cells[row][col].is_mine = True
                mines_placed += 1

    def calculate_adjacency(self):
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                self.cells[row][col].calculate_adjacent_mines(self, row, col)

    def reveal_cell(self, row, col):
        if not self.cells[row][col].is_revealed:
            self.cells[row][col].reveal()

    def toggle_flag(self, row, col):
        self.cells[row][col].flag()

    def is_mine(self, row, col):
        return self.cells[row][col].is_mine
