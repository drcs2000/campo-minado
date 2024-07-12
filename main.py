import tkinter as tk
from game import Game

class MinesweeperApp:
    def __init__(self, root, num_rows=10, num_columns=10, num_mines=10):
        self.root = root
        self.game = Game(num_rows, num_columns, num_mines)
        self.game.start_game()
        self.create_widgets()

    def create_widgets(self):
        for row in range(self.game.board.num_rows):
            for col in range(self.game.board.num_columns):
                button = tk.Button(self.root, width=2, height=1,
                                   command=lambda r=row, c=col: self.reveal_cell(r, c))
                button.grid(row=row, column=col)

    def reveal_cell(self, row, col):
        cell = self.game.board.cells[row][col]
        if cell.is_mine:
            self.game.end_game(False)
            self.update_button(row, col, "M", "red")
        else:
            cell.reveal()
            self.update_button(row, col, cell.adjacent_mines, "white")
            if self.game.check_win_condition():
                self.game.end_game(True)

    def update_button(self, row, col, text, color):
        button = self.root.grid_slaves(row=row, column=col)[0]
        button.config(text=text, bg=color)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Campo Minado")
    app = MinesweeperApp(root)
    root.mainloop()
