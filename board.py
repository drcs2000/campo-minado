import random
from cell import Cell

class Board:
    def __init__(self, rows, cols, bombs):
        self.__rows = rows  # Número de linhas do tabuleiro
        self.__cols = cols  # Número de colunas do tabuleiro
        self.__bombs = bombs  # Número de bombas no tabuleiro
        # Cria uma grade (grid) de células
        self.__grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.__place_bombs()  # Coloca as bombas no tabuleiro
        self.__calculate_bomb_counts()  # Calcula a contagem de bombas adjacentes para cada célula

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    @property
    def bombs(self):
        return self.__bombs

    @property
    def grid(self):
        return self.__grid

    def __place_bombs(self):
        # Coloca bombas aleatoriamente no tabuleiro até alcançar o número desejado
        placed_bombs = 0
        while placed_bombs < self.__bombs:
            row = random.randint(0, self.__rows - 1)
            col = random.randint(0, self.__cols - 1)
            cell = self.__grid[row][col]
            if not cell.is_bomb:
                cell.is_bomb = True
                placed_bombs += 1

    def __calculate_bomb_counts(self):
        # Calcula quantas bombas adjacentes cada célula possui
        for row in range(self.__rows):
            for col in range(self.__cols):
                if not self.__grid[row][col].is_bomb:
                    self.__grid[row][col].bomb_count = self.__count_adjacent_bombs(row, col)

    def __count_adjacent_bombs(self, row, col):
        count = 0
        # Conta as bombas nas células adjacentes
        for r in range(max(0, row-1), min(self.__rows, row+2)):
            for c in range(max(0, col-1), min(self.__cols, col+2)):
                if (r, c) != (row, col) and self.__grid[r][c].is_bomb:
                    count += 1
        return count

    def reveal_cell(self, row, col):
        # Revela a célula e, se não tiver bombas adjacentes, revela as células adjacentes
        cell = self.__grid[row][col]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.reveal()
        if cell.bomb_count == 0:
            for r in range(max(0, row-1), min(self.__rows, row+2)):
                for c in range(max(0, col-1), min(self.__cols, col+2)):
                    if (r, c) != (row, col):
                        self.reveal_cell(r, c)

    def toggle_flag(self, row, col):
        # Alterna a bandeira na célula especificada
        cell = self.__grid[row][col]
        if not cell.is_revealed:
            cell.toggle_flag()
