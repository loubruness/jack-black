import tkinter as tk
from blackjack_game import BlackjackGame
from ui_manager import UIManager

# Initialize the Tkinter application
file_path = 'players.json'
root = tk.Tk()
game = BlackjackGame(file_path)
ui_manager = UIManager(root, game)
root.mainloop()
