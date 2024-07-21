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
        self.__timer_label = None  # Inicializa o rótulo do timer como None
        self.__timer_running = False  # Indica se o timer está ativo
        self.__timer_counter = 0  # Contador do timer
        self.__number_colors = {  # Dicionário de cores para os números
            1: "blue",
            2: "green",
            3: "red",
            4: "purple",
            5: "maroon",
            6: "turquoise",
            7: "black",
            8: "gray"
        }
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

        self.__flags_label = ttk.Label(self.__header_frame, text=f"Bombas: {self.__bombs - self.__flags_placed}", style="Header.TLabel")
        self.__flags_label.pack(side="left")

        self.__timer_label = ttk.Label(self.__header_frame, text="Tempo: 000", style="Header.TLabel")
        self.__timer_label.pack(side="right")

    def update_header(self):
        # Atualiza as informações no cabeçalho
        self.__flags_label.config(text=f"Bombas: {self.__bombs - self.__flags_placed}")

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
        self.show_instructions()

    def show_instructions(self):
        # Mostra as instruções do jogo em um modal
        instructions = tk.Toplevel(self.master)
        instructions.title("Instruções")
        instructions.resizable(False, False)

        instruction_text = (
            "Bem-vindo ao Campo Minado!\n\n"
            "Objetivo:\n"
            "Revele todas as células que não contêm bombas.\n\n"
            "Como jogar:\n"
            "1. Clique com o botão esquerdo para revelar uma célula.\n"
            "2. Clique com o botão direito para colocar/remover uma bandeira.\n\n"
            "Boa sorte!"
        )

        ttk.Label(instructions, text=instruction_text, font=("Helvetica", 16), justify="center").pack(pady=10)
        ttk.Button(instructions, text="Iniciar", command=lambda: [self.start_game(), instructions.destroy()]).pack(pady=5)

        self.center_window(instructions)

    def start_game(self):
        # Inicia o jogo
        self.reset_game()

    def reset_game(self):
        # Reinicia o jogo com o novo tabuleiro e contadores
        self.__flags_placed = 0
        self.__board = Board(self.__size, self.__size, self.__bombs)
        self.create_widgets()
        self.update_header()
        self.reset_timer()

    def create_widgets(self):
        # Cria os widgets do jogo, incluindo o cabeçalho e os botões das células
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_header()

        self.__frame = ttk.Frame(self.master, padding="10")
        self.__frame.pack()

        for row in range(self.__size):
            for col in range(self.__size):
                button = tk.Button(self.__frame, width=4, height=2, command=lambda row=row, col=col: self.on_button_click(row, col))
                button.bind("<Button-3>", lambda e, row=row, col=col: self.on_right_click(row, col))
                button.grid(row=row, column=col, padx=1, pady=1)
                self.__board.grid[row][col].button = button

        self.center_window(self.master)

    def toggle_flag_mode(self):
        # Alterna o modo de bandeira
        self.__is_flag_mode = not self.__is_flag_mode

    def on_button_click(self, row, col):
        # Lida com o clique do botão esquerdo do mouse em uma célula
        if not self.__timer_running:
            self.start_timer()

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
                    self.stop_timer()
                    self.game_over(True)
        self.update_header()

    def on_right_click(self, row, col):
        # Lida com o clique do botão direito do mouse em uma célula
        self.__board.toggle_flag(row, col)
        if self.__board.grid[row][col].is_flagged:
            self.__flags_placed += 1
            self.__board.grid[row][col].button.config(bg="yellow")
        else:
            self.__flags_placed -= 1
            self.__board.grid[row][col].button.config(bg="SystemButtonFace")
        self.update_buttons()
        self.update_header()

    def update_buttons(self):
        # Atualiza o estado dos botões de acordo com o estado das células
        for row in range(self.__size):
            for col in range(self.__size):
                cell = self.__board.grid[row][col]
                if cell.is_revealed:
                    if cell.is_bomb:
                        cell.button.config(bg="red")
                    else:
                        cell.button.config(
                            text="" if cell.bomb_count == 0 else str(cell.bomb_count),
                            fg=self.__number_colors.get(cell.bomb_count, "black"),
                            bg="lightgrey"
                        )
                elif cell.is_flagged:
                    cell.button.config(bg="yellow")
                else:
                    cell.button.config(text="", bg="SystemButtonFace")

    def reveal_all_bombs(self, clicked_row, clicked_col):
        # Revela todas as bombas no tabuleiro
        for row in range(self.__size):
            for col in range(self.__size):
                cell = self.__board.grid[row][col]
                if cell.is_bomb:
                    cell.button.config(bg="red")
        self.stop_timer()
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

    def start_timer(self):
        # Inicia o timer do jogo
        self.__timer_running = True
        self.update_timer()

    def stop_timer(self):
        # Para o timer do jogo
        self.__timer_running = False

    def reset_timer(self):
        # Reseta o timer do jogo
        self.__timer_counter = 0
        self.__timer_label.config(text="Tempo: 000")

    def update_timer(self):
        # Atualiza o timer do jogo
        if self.__timer_running:
            self.__timer_counter += 1
            self.__timer_label.config(text=f"Tempo: {self.__timer_counter:03d}")
            self.master.after(1000, self.update_timer)
