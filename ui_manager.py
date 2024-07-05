import tkinter as tk
from person import Dealer

class UIManager:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.frame = tk.Frame(self.root)
        self.reload_ui()
        
    def reload_ui(self):
        if self.game.state == "start_game":
            self.init_ui()
        else:    
            self.label_result.config(text=self.game.result)
            
            if self.game.state == "set_players":
                self.choose_nb_players()
            elif self.game.state == "set_names":
                self.get_player_name()
            elif self.game.state == "init_playing":
                self.init_playing_ui()
            elif self.game.state == "place_bet":
                self.get_player_bet()
            elif self.game.state == "start_turns":
                self.start_turns()
            elif self.game.state == "player_turn":
                self.player_turn()
            elif self.game.state == "end_playing":
                self.end_playing()
            else :
                print(self.game.state+" Error: Unknown state")
                self.clear_frame()
        
    def init_ui(self):
        self.clear_frame()
        self.label_result = tk.Label(self.frame)
        self.label_result.pack()
        
        self.entry = tk.Entry(self.frame)
        self.entry.pack()
        
        self.button_submit = tk.Button(self.frame, text="Valider")
        self.button_submit.pack()
        
        self.game.start_game()
        self.reload_ui()
        
    def choose_nb_players(self):
        self.entry.delete(0, tk.END)
        
        self.entry.unbind("<Return>")
        self.entry.bind("<Return>", self.get_nb_players)
        
        self.button_submit.config(command=self.get_nb_players)


    def get_nb_players(self,event=None):
        nb_players = int(self.entry.get())
        self.game.set_nb_players(nb_players)
        self.reload_ui()

    def get_player_name(self):        
        self.entry.delete(0, tk.END)
        
        self.entry.unbind("<Return>")
        self.entry.bind("<Return>", self.save_player_name)
        
        self.button_submit.config(command=self.save_player_name)

    def save_player_name(self,event=None):
        player_name = self.entry.get()
        self.game.add_player(player_name)
        self.reload_ui()
 

    def init_playing_ui(self):
        self.clear_frame()
        self.game.init_playing()
        self.labels_players = []
        for player in self.game.players:
            label = tk.Label(self.frame, text=player)
            label.pack()
            self.labels_players.append(label)
            
        self.label_result = tk.Label(self.frame, text=self.game.result)
        self.label_result.pack()
        
        self.entry = tk.Entry(self.frame)
        self.entry.bind("<Return>", self.save_player_bet)
        self.entry.pack()

        self.button_submit = tk.Button(self.frame, text="Submit", command=self.save_player_bet)
        self.button_submit.pack()
        
        self.reload_ui()
    
    def get_player_bet(self):
        self.entry.delete(0, tk.END)
        
        self.entry.unbind("<Return>")
        self.entry.bind("<Return>", self.save_player_bet)
        
        self.button_submit.config(command=self.save_player_bet)
        
        self.update_ui()
            
    def save_player_bet(self,event=None):
        bet = int(self.entry.get())
        self.game.place_bet(bet)
        self.reload_ui()       
        
    def place_bet(self):
        bet = int(self.entry.get())
        self.game.place_bet(bet)
        self.reload_ui()
    
    def start_turns(self):  
        self.button_hit = tk.Button(self.frame, text="Hit", command=self.hit)
        self.button_hit.pack()
        
        self.button_stand = tk.Button(self.frame, text="Stand", command=self.stand)
        self.button_stand.pack()
        
        self.button_submit.destroy()
        self.entry.destroy()
        
        self.game.start_turns()
        self.reload_ui()
    
    def player_turn(self):
        self.update_ui()
        
    def hit(self):
        self.game.hit()
        self.reload_ui()

    def stand(self):
        self.game.stand()
        self.reload_ui()
    
    def end_playing(self):
        self.button_hit.destroy()
        self.button_stand.destroy()
        
        self.button_restart = tk.Button(self.frame, text="Restart", command=self.restart)
        self.button_restart.pack()
        self.update_ui()
    
    def restart(self):
        self.game.restart()
        self.reload_ui()

    def update_ui(self):
        for i, player in enumerate(self.game.players):
            self.labels_players[i].config(text=player)
        self.label_result.config(text=self.game.result)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
