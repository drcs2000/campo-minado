import tkinter as tk
from tkinter import ttk
from game import MinesweeperGame

if __name__ == "__main__":
    root = tk.Tk()
    
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=6)
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("Header.TFrame", background="#f0f0f0")
    style.configure("Header.TLabel", font=("Helvetica", 14), background="#f0f0f0")

    game = MinesweeperGame(root)
    root.mainloop()
