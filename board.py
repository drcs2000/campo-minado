import random
from cell import Cell

class Board:
    def __init__(self, rows, cols, bombs):
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        # Cria uma grade (grid) de células
        self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.place_bombs()  # Coloca as bombas no tabuleiro
        self.calculate_bomb_counts()  # Calcula a contagem de bombas adjacentes para cada célula

    def place_bombs(self):
        placed_bombs = 0
        # Coloca bombas aleatoriamente no tabuleiro até alcançar o número desejado
        while placed_bombs < self.bombs:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            cell = self.grid[row][col]
            if not cell.is_bomb:
                cell.is_bomb = True
                placed_bombs += 1

    def calculate_bomb_counts(self):
        # Calcula quantas bombas adjacentes cada célula possui
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col].is_bomb:
                    self.grid[row][col].bomb_count = self.count_adjacent_bombs(row, col)

    def count_adjacent_bombs(self, row, col):
        count = 0
        # Conta as bombas nas células adjacentes
        for r in range(max(0, row-1), min(self.rows, row+2)):
            for c in range(max(0, col-1), min(self.cols, col+2)):
                if (r, c) != (row, col) and self.grid[r][c].is_bomb:
                    count += 1
        return count

    def reveal_cell(self, row, col):
        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.reveal()  # Revela a célula
        if cell.bomb_count == 0:
            # Se a célula não tem bombas adjacentes, revela as células adjacentes
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if (r, c) != (row, col):
                        self.reveal_cell(r, c)

    def toggle_flag(self, row, col):
        cell = self.grid[row][col]
        if not cell.is_revealed:
            cell.toggle_flag()  # Marca ou desmarca a célula com uma bandeira
