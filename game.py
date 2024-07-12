from board import Board

class Game:
    def __init__(self, num_rows, num_columns, num_mines):
        self.board = Board(num_rows, num_columns, num_mines)
        self.game_over = False
        self.game_won = False

    def start_game(self):
        self.board.initialize_board()

    def check_win_condition(self):
        for row in self.board.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        self.game_won = True
        return True

    def end_game(self, won):
        self.game_over = True
        self.game_won = won
