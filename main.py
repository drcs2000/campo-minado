import tkinter as tk
from tkinter import ttk
from game import MinesweeperGame

if __name__ == "__main__":
    root = tk.Tk()
    
    # Applying a modern style
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=6)
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("Bomb.TButton", background="red", foreground="white")
    style.configure("Flag.TButton", background="yellow", foreground="black")
    style.configure("Revealed.TButton", background="white", foreground="black")
    style.configure("Unrevealed.TButton", background="SystemButtonFace", foreground="black")
    style.configure("ClickedBomb.TButton", background="darkred", foreground="white")
    style.configure("Header.TFrame", background="#f0f0f0")
    style.configure("Header.TLabel", font=("Helvetica", 14), background="#f0f0f0")

    game = MinesweeperGame(root)
    root.mainloop()
