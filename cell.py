class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_bomb = False  # Inicializa a célula como não sendo uma bomba
        self.is_revealed = False  # Inicializa a célula como não revelada
        self.is_flagged = False  # Inicializa a célula como não marcada com bandeira
        self.bomb_count = 0  # Inicializa a contagem de bombas adjacentes como zero

    def reveal(self):
        self.is_revealed = True  # Revela a célula, alterando seu estado para revelado

    def toggle_flag(self):
        self.is_flagged = not self.is_flagged  # Alterna o estado da bandeira na célula
