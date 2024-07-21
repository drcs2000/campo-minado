class Cell:
    def __init__(self, row, col, is_bomb=False):
        self.__row = row  # Linha da célula
        self.__col = col  # Coluna da célula
        self.__is_bomb = is_bomb  # Indica se a célula é uma bomba
        self.__is_revealed = False  # Indica se a célula foi revelada
        self.__is_flagged = False  # Indica se a célula está marcada com uma bandeira
        self.__bomb_count = 0  # Contagem de bombas adjacentes

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

    @property
    def is_bomb(self):
        return self.__is_bomb

    @is_bomb.setter
    def is_bomb(self, value):
        self.__is_bomb = value

    @property
    def is_revealed(self):
        return self.__is_revealed

    @property
    def is_flagged(self):
        return self.__is_flagged

    @property
    def bomb_count(self):
        return self.__bomb_count

    @bomb_count.setter
    def bomb_count(self, value):
        self.__bomb_count = value

    def reveal(self):
        self.__is_revealed = True  # Revela a célula, alterando seu estado para revelado

    def toggle_flag(self):
        self.__is_flagged = not self.__is_flagged  # Alterna o estado da bandeira na célula
