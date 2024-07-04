import tkinter as tk
from person import Dealer

class UIManager:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.frame = tk.Frame(self.root)
        self.init_ui()

    def init_ui(self):
        self.clear_frame()
        self.choose_nb_players()

    def choose_nb_players(self):
        self.clear_frame()
        self.label_nb_players = tk.Label(self.frame, text="Combien de joueurs voulez-vous ajouter?")
        self.label_nb_players.pack()

        self.entry_nb_players = tk.Entry(self.frame)
        self.entry_nb_players.pack()

        self.button_nb_players = tk.Button(self.frame, text="Valider", command=self.get_nb_players)
        self.button_nb_players.pack()

    def get_nb_players(self):
        nb_players = int(self.entry_nb_players.get())
        self.game.set_nb_players(nb_players)
        self.clear_frame()
        self.get_player_name()

    def get_player_name(self):        
        self.label_name = tk.Label(self.frame, text=f"Quel est le nom du joueur {self.game.current_player + 1}?")
        self.label_name.pack()

        self.entry_name = tk.Entry(self.frame)
        self.entry_name.pack()

        self.button_name = tk.Button(self.frame, text="Submit", command=self.save_player_name)
        self.button_name.pack()

    def save_player_name(self):
        player_name = self.entry_name.get()
        self.game.add_player(player_name)
        if self.game.current_player >= self.game.nb_players:
            self.clear_frame()
            self.init_game_ui()
        else:
            self.label_name.config(text=f"Quel est le nom du joueur {self.game.current_player + 1}?")
            self.entry_name.delete(0, tk.END)
            
    def get_player_bet(self):
        self.instruction = " , placez votre mise:"
        
        self.entry_bet = tk.Entry(self.frame)
        self.entry_bet.pack()

        self.button_bet = tk.Button(self.frame, text="Submit", command=self.save_player_bet)
        self.button_bet.pack()
        
        self.update_ui()
        
    def save_player_bet(self):
        bet = int(self.entry_bet.get())
        self.game.place_bet(bet)
        if isinstance(self.game.player, Dealer):
            self.label_instruction.destroy()
            self.entry_bet.destroy()
            self.start_turns()
        else:
            self.update_ui()
            self.entry_bet.delete(0, tk.END)
        
    def get_instruction(self):
        return {self.game.player.name} + self.instruction
            
    def start_turns(self):     
        self.instruction = " , à votre tour."   
        
        self.button_hit = tk.Button(self.frame, text="Hit", command=self.hit)
        self.button_hit.pack()
        
        self.button_stand = tk.Button(self.frame, text="Stand", command=self.stand)
        self.button_stand.pack()
        
        
        self.update_ui()
        

    def init_game_ui(self):
        self.clear_frame()
        self.game.init_game()
        self.labels_players = []
        self.instruction=''
        for player in self.game.players:
            label = tk.Label(self.frame, text=player)
            label.pack()
            self.labels_players.append(label)
            
        self.label_instruction = tk.Label(self.frame, text=self.get_instruction)
        self.label_instruction.pack()
        
        self.get_player_bet()

    def place_bet(self):
        bet = int(self.entry_bet.get())
        self.game.place_bet(bet)
        self.update_ui()

    def hit(self):
        self.game.hit()
        self.update_ui()

    def stand(self):
        self.game.stand()
        self.update_ui()

    def update_ui(self):
        for i, player in enumerate(self.game.players):
            self.labels_players[i].config(text=player)
        self.label_instruction.config(text=self.instruction)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
