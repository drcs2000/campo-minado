import tkinter as tk
from tkinter import ttk
from board import Board

class MinesweeperGame:
    def __init__(self, master):
        self.master = master  # Janela principal do Tkinter
        self.master.title("Campo Minado")
        self.__size = 8  # Tamanho inicial do tabuleiro
        self.__bombs = 10  # Número inicial de bombas
        self.__flags_placed = 0  # Contador de bandeiras colocadas
        self.__board = Board(self.__size, self.__size, self.__bombs)  # Inicializa o tabuleiro
        self.__is_flag_mode = False  # Indica se o modo de bandeira está ativo
        self.__header_frame = None  # Inicializa o cabeçalho como None
        self.create_menu()  # Cria o menu do jogo
        self.show_start_menu()  # Mostra o menu inicial

    def __del__(self):
        print("MinesweeperGame foi destruído")  # Destrutor

    def center_window(self, window):
        # Centraliza a janela na tela
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f'+{x}+{y}')

    def create_menu(self):
        # Cria o menu do jogo com opções de dificuldade e modo bandeira
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
        # Cria o cabeçalho com contagem de bandeiras e campos restantes
        self.__header_frame = ttk.Frame(self.master, padding="10", style="Header.TFrame")
        self.__header_frame.pack(side="top", fill="x")

        self.__flags_label = ttk.Label(self.__header_frame, text=f"Bandeiras: {self.__flags_placed}", style="Header.TLabel")
        self.__flags_label.pack(side="left")

        self.__remaining_label = ttk.Label(self.__header_frame, text=f"Campos restantes: {self.__size * self.__size - self.__bombs}", style="Header.TLabel")
        self.__remaining_label.pack(side="right")

    def update_header(self):
        # Atualiza as informações no cabeçalho
        self.__flags_label.config(text=f"Bandeiras: {self.__flags_placed}")
        remaining_cells = sum(1 for row in self.__board.grid for cell in row if not cell.is_revealed)
        self.__remaining_label.config(text=f"Campos restantes: {remaining_cells - self.__bombs}")

    def show_start_menu(self):
        # Mostra o menu inicial para escolher a dificuldade do jogo
        if self.__header_frame:
            self.__header_frame.destroy()
            self.__header_frame = None

        for widget in self.master.winfo_children():
            if widget != self.__header_frame:
                widget.destroy()

        frame = ttk.Frame(self.master, padding="20")
        frame.pack(pady=20)

        ttk.Label(frame, text="Escolha a Dificuldade", font=("Helvetica", 16)).pack(pady=10)
        ttk.Button(frame, text="Fácil", command=lambda: self.set_difficulty("easy")).pack(fill="x", pady=5)
        ttk.Button(frame, text="Médio", command=lambda: self.set_difficulty("medium")).pack(fill="x", pady=5)
        ttk.Button(frame, text="Difícil", command=lambda: self.set_difficulty("hard")).pack(fill="x", pady=5)

        self.center_window(self.master)

    def set_difficulty(self, level):
        # Define a dificuldade do jogo e reinicia o jogo
        if level == "easy":
            self.__size = 8
            self.__bombs = 10
        elif level == "medium":
            self.__size = 12
            self.__bombs = 20
        elif level == "hard":
            self.__size = 16
            self.__bombs = 40
        self.reset_game()

    def reset_game(self):
        # Reinicia o jogo com o novo tabuleiro e contadores
        self.__flags_placed = 0
        self.__board = Board(self.__size, self.__size, self.__bombs)
        self.create_widgets()
        self.update_header()

    def create_widgets(self):
        # Cria os widgets do jogo, incluindo o cabeçalho e os botões das células
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_header()

        self.__frame = ttk.Frame(self.master, padding="10")
        self.__frame.pack()

        for row in range(self.__size):
            for col in range(self.__size):
                button = ttk.Button(self.__frame, width=4, command=lambda row=row, col=col: self.on_button_click(row, col))
                button.bind("<Button-3>", lambda e, row=row, col=col: self.on_right_click(row, col))
                button.grid(row=row, column=col, padx=2, pady=2)
                self.__board.grid[row][col].button = button

        self.center_window(self.master)

    def toggle_flag_mode(self):
        self.__is_flag_mode = not self.__is_flag_mode  # Alterna o modo de bandeira

    def on_button_click(self, row, col):
        # Lida com o clique do botão esquerdo do mouse em uma célula
        if self.__is_flag_mode:
            self.on_right_click(row, col)
        else:
            cell = self.__board.grid[row][col]
            if cell.is_bomb:
                self.reveal_all_bombs(row, col)
            else:
                self.__board.reveal_cell(row, col)
                self.update_buttons()
                if self.check_win():
                    self.game_over(True)
        self.update_header()

    def on_right_click(self, row, col):
        # Lida com o clique do botão direito do mouse em uma célula
        self.__board.toggle_flag(row, col)
        if self.__board.grid[row][col].is_flagged:
            self.__flags_placed += 1
        else:
            self.__flags_placed -= 1
        self.update_buttons()
        self.update_header()

    def update_buttons(self):
        # Atualiza o estado dos botões de acordo com o estado das células
        for row in range(self.__size):
            for col in range(self.__size):
                cell = self.__board.grid[row][col]
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
        # Revela todas as bombas no tabuleiro
        for row in range(self.__size):
            for col in range(self.__size):
                cell = self.__board.grid[row][col]
                if cell.is_bomb:
                    if row == clicked_row and col == clicked_col:
                        cell.button.config(text="M", style="ClickedBomb.TButton")
                    else:
                        cell.button.config(text="B", style="Bomb.TButton")
        self.game_over(False)

    def check_win(self):
        # Verifica se todas as células não-bomba foram reveladas
        for row in range(self.__size):
            for col in range(self.__size):
                cell = self.__board.grid[row][col]
                if not cell.is_revealed and not cell.is_bomb:
                    return False
        return True

    def game_over(self, win):
        # Exibe a janela de "Game Over" com a mensagem apropriada
        self.show_game_over_dialog(win)

    def show_game_over_dialog(self, win):
        # Cria a janela de "Game Over" com opções de reiniciar ou sair
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
        # Reinicia o jogo fechando a janela de "Game Over" e voltando ao menu inicial
        dialog.destroy()
        self.show_start_menu()
