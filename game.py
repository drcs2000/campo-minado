import tkinter as tk
from tkinter import ttk
from board import Board

class MinesweeperGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Campo Minado")
        self.size = 8
        self.bombs = 10
        self.flags_placed = 0
        self.board = Board(self.size, self.size, self.bombs)
        self.is_flag_mode = False
        self.header_frame = None  # Inicializa como None
        self.create_menu()
        self.show_start_menu()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f'+{x}+{y}')

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Fácil", command=lambda: self.set_difficulty("easy"))
        game_menu.add_command(label="Médio", command=lambda: self.set_difficulty("medium"))
        game_menu.add_command(label="Difícil", command=lambda: self.set_difficulty("hard"))
        game_menu.add_separator()
        game_menu.add_command(label="Sair", command=self.master.quit)

        flag_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modo", menu=flag_menu)
        flag_menu.add_command(label="Colocar/Remover Bandeira", command=self.toggle_flag_mode)

    def create_header(self):
        self.header_frame = ttk.Frame(self.master, padding="10", style="Header.TFrame")
        self.header_frame.pack(side="top", fill="x")

        self.flags_label = ttk.Label(self.header_frame, text=f"Bandeiras: {self.flags_placed}", style="Header.TLabel")
        self.flags_label.pack(side="left")

        self.remaining_label = ttk.Label(self.header_frame, text=f"Campos restantes: {self.size * self.size - self.bombs}", style="Header.TLabel")
        self.remaining_label.pack(side="right")

    def update_header(self):
        self.flags_label.config(text=f"Bandeiras: {self.flags_placed}")
        remaining_cells = sum(1 for row in self.board.grid for cell in row if not cell.is_revealed)
        self.remaining_label.config(text=f"Campos restantes: {remaining_cells - self.bombs}")

    def show_start_menu(self):
        for widget in self.master.winfo_children():
            if widget != self.header_frame:
                widget.destroy()

        frame = ttk.Frame(self.master, padding="20")
        frame.pack(pady=20)

        ttk.Label(frame, text="Escolha a Dificuldade", font=("Helvetica", 16)).pack(pady=10)
        ttk.Button(frame, text="Fácil", command=lambda: self.set_difficulty("easy")).pack(fill="x", pady=5)
        ttk.Button(frame, text="Médio", command=lambda: self.set_difficulty("medium")).pack(fill="x", pady=5)
        ttk.Button(frame, text="Difícil", command=lambda: self.set_difficulty("hard")).pack(fill="x", pady=5)

        self.center_window(self.master)

    def set_difficulty(self, level):
        if level == "easy":
            self.size = 8
            self.bombs = 10
        elif level == "medium":
            self.size = 12
            self.bombs = 20
        elif level == "hard":
            self.size = 16
            self.bombs = 40
        self.reset_game()

    def reset_game(self):
        self.flags_placed = 0
        self.board = Board(self.size, self.size, self.bombs)
        self.create_widgets()
        self.update_header()

    def create_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_header()

        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack()

        for row in range(self.size):
            for col in range(self.size):
                button = ttk.Button(self.frame, width=4, command=lambda row=row, col=col: self.on_button_click(row, col))
                button.bind("<Button-3>", lambda e, row=row, col=col: self.on_right_click(row, col))
                button.grid(row=row, column=col, padx=2, pady=2)
                self.board.grid[row][col].button = button

        self.center_window(self.master)

    def toggle_flag_mode(self):
        self.is_flag_mode = not self.is_flag_mode

    def on_button_click(self, row, col):
        if self.is_flag_mode:
            self.on_right_click(row, col)
        else:
            cell = self.board.grid[row][col]
            if cell.is_bomb:
                self.reveal_all_bombs(row, col)
            else:
                self.board.reveal_cell(row, col)
                self.update_buttons()
                if self.check_win():
                    self.game_over(True)
        self.update_header()

    def on_right_click(self, row, col):
        self.board.toggle_flag(row, col)
        if self.board.grid[row][col].is_flagged:
            self.flags_placed += 1
        else:
            self.flags_placed -= 1
        self.update_buttons()
        self.update_header()

    def update_buttons(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board.grid[row][col]
                if cell.is_revealed:
                    if cell.is_bomb:
                        cell.button.config(text="B", style="Bomb.TButton")
                    else:
                        cell.button.config(text=str(cell.bomb_count), style="Revealed.TButton")
                elif cell.is_flagged:
                    cell.button.config(text="F", style="Flag.TButton")
                else:
                    cell.button.config(text="", style="Unrevealed.TButton")

    def reveal_all_bombs(self, clicked_row, clicked_col):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board.grid[row][col]
                if cell.is_bomb:
                    if row == clicked_row and col == clicked_col:
                        cell.button.config(text="M", style="ClickedBomb.TButton")
                    else:
                        cell.button.config(text="B", style="Bomb.TButton")
        self.game_over(False)

    def check_win(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board.grid[row][col]
                if not cell.is_revealed and not cell.is_bomb:
                    return False
        return True

    def game_over(self, win):
        self.show_game_over_dialog(win)

    def show_game_over_dialog(self, win):
        dialog = tk.Toplevel(self.master)
        dialog.title("Game Over")
        dialog.resizable(False, False)
        
        message = "Você ganhou!" if win else "Você acertou uma bomba!"
        color = "green" if win else "red"

        ttk.Label(dialog, text=message, font=("Helvetica", 14), foreground=color).pack(pady=20)
        
        ttk.Button(dialog, text="Reiniciar", command=lambda: self.restart_game(dialog)).pack(side="left", padx=20, pady=10)
        ttk.Button(dialog, text="Sair", command=self.master.quit).pack(side="right", padx=20, pady=10)
        
        self.center_window(dialog)
        
    def restart_game(self, dialog):
        dialog.destroy()
        self.show_start_menu()
