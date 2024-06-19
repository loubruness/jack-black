import tkinter as tk
from random import choice, shuffle

from person import Player, Dealer

# Constantes du jeu
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4

def draw_card(deck):
    return choice(deck)
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.init_game()

    def init_game(self):
        self.select_players()
        shuffle(deck)

        for player in self.players:
            player.hand = [draw_card(deck), draw_card(deck)]

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.labels_players = []
        for player in self.players:
            label = tk.Label(self.frame, text=player)
            label.pack()
            self.labels_players.append(label)

        self.label_bet = tk.Label(self.frame, text=f"{self.player.name}, placez votre mise:")
        self.label_bet.pack()
        
        self.entry_bet = tk.Entry(self.frame)
        self.entry_bet.pack()
        
        self.button_bet = tk.Button(self.frame, text="Placer mise", command=self.place_bet)
        self.button_bet.pack()

        self.button_hit = tk.Button(self.frame, text="Hit", command=self.hit, state="disabled")
        self.button_hit.pack()

        self.button_stand = tk.Button(self.frame, text="Stand", command=self.stand, state="disabled")
        self.button_stand.pack()
        
        self.label_result = tk.Label(self.frame, text="")
        self.label_result.pack()
        
    def select_players(self):
        self.players = [Player(f"Joueur {i + 1}") for i in range(4)]
        self.players.append(Dealer())
        self.current_player = 0
        self.player = self.players[self.current_player]

    def place_bet(self):
        try:
            bet = int(self.entry_bet.get())
            if 0 < bet <= self.player.money:
                self.player.set_bet(bet)
                self.labels_players[self.current_player].config(text=self.player)
                self.entry_bet.delete(0, tk.END)
                self.next_player()

                if isinstance(self.player, Dealer):
                    self.next_player()
                    self.start_turns()
                else:
                    self.label_bet.config(text=f"{self.player.name}, placez votre mise:")
            else:
                self.label_result.config(text="Mise invalide.")
        except ValueError:
            self.label_result.config(text="Veuillez entrer un nombre valide.")
            
    def next_player(self):
        self.current_player += 1
        self.current_player = self.current_player % 5
        self.player = self.players[self.current_player]

    def start_turns(self):
        self.label_bet.pack_forget()
        self.entry_bet.pack_forget()
        self.button_bet.pack_forget()
        self.label_result.config(text=f"C'est au tour de {self.player.name}.")
        self.button_hit.config(state="normal")
        self.button_stand.config(state="normal")

    def hit(self):
        card = draw_card(deck)
        self.player.take_card(card)
        self.labels_players[self.current_player].config(text=self.player)
        
        if self.player.calculate_hand() == 21:
            self.label_result.config(text=f"{self.player.name} a fait un blackjack.")
            self.end_turn()
          
        if self.player.calculate_hand() > 21:
            self.label_result.config(text=f"{self.player.name} a dépassé 21 et a perdu sa mise.")
            self.end_turn()

    def stand(self):
        self.end_turn()

    def end_turn(self):
        self.next_player()
        if isinstance(self.player, Dealer):
            self.dealer_turn()
        else:
            self.label_result.config(text=f"C'est au tour de {self.player.name}.")
            self.button_hit.config(state="normal")
            self.button_stand.config(state="normal")

    def dealer_turn(self):
        self.players[-1].visible = True
        self.labels_players[-1].config(text=self.players[-1])
        while self.players[-1].calculate_hand() < 17:
            self.players[-1].take_card(draw_card(deck))
            self.labels_players[-1].config(text=self.players[-1])

        self.check_winner()

    def check_winner(self):
        results = []
        i = 0
        for player in self.players:
            if isinstance(player, Dealer):
                continue
            if player.calculate_hand() > 21:
                results.append(f"{player.name} a perdu.")
            elif self.players[-1].calculate_hand() > 21 or player.calculate_hand() > self.players[-1].calculate_hand():
                player.win
                results.append(f"{player.name} a gagné.")
            elif player.calculate_hand() < self.players[-1].calculate_hand():
                player.lose
                results.append(f"{player.name} a perdu.")
            else:
                player.equality
                results.append(f"{player.name} a fait un match nul.")
            
            self.labels_players[i].config(text=player)
            i += 1
        
        self.label_result.config(text="\n".join(results))

        self.button_hit.config(state="disabled")
        self.button_stand.config(state="disabled")
        self.button_restart = tk.Button(self.frame, text="Recommencer", command=self.reset_game)
        self.button_restart.pack()


    def reset_game(self):
        self.current_player = 0
        for player in self.players:
            player.clear_hand()
        self.frame.destroy()
        self.init_game()

# Initialisation de l'application Tkinter
root = tk.Tk()
game = BlackjackGame(root)
root.mainloop()