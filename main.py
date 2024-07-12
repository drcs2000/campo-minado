import tkinter as tk
from tkinter import ttk
from game import MinesweeperGame

if __name__ == "__main__":
    root = tk.Tk()
    
    # Aplicando um estilo moderno aos componentes do Tkinter usando ttk.Style()
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=6)  # Estilo para botões
    style.configure("TLabel", font=("Helvetica", 12))  # Estilo para labels
    style.configure("Bomb.TButton", background="red", foreground="white")  # Estilo para botões que representam bombas
    style.configure("Flag.TButton", background="yellow", foreground="black")  # Estilo para botões que representam bandeiras
    style.configure("Revealed.TButton", background="white", foreground="black")  # Estilo para botões revelados
    style.configure("Unrevealed.TButton", background="SystemButtonFace", foreground="black")  # Estilo para botões não revelados
    style.configure("ClickedBomb.TButton", background="darkred", foreground="white")  # Estilo para botão de bomba clicado
    style.configure("Header.TFrame", background="#f0f0f0")  # Estilo para o frame do cabeçalho
    style.configure("Header.TLabel", font=("Helvetica", 14), background="#f0f0f0")  # Estilo para labels no cabeçalho

    game = MinesweeperGame(root)  # Inicializa o jogo
    root.mainloop()  # Inicia o loop principal do Tkinter
