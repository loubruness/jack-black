import tkinter as tk
from random import choice, shuffle
import json
import json

from person import Player, Dealer

# Constants for the game
# Constants for the game
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4

file_path = 'players.json'

def read_player_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_player_data(file_path, players):
    with open(file_path, 'w') as file:
        json.dump(players, file, indent=4)

def draw_card(deck):
    return choice(deck)

def calculate_hand(hand):
    total = 0
    aces = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            total += 10
        elif card == 'A':
            aces += 1
            total += 11
        else:
            total += card
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.jackpot = 10000
        self.players = []
        self.current_player = 0
        self.frame = tk.Frame(self.root)
        self.loaded_players = read_player_data(file_path)
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
        self.nb_players = int(self.entry_nb_players.get())
        self.current_player = 0
        self.players = []
        self.get_player_name()

    def get_player_name(self):
        self.clear_frame()
        self.label_name = tk.Label(self.frame, text=f"Quel est le nom du joueur {self.current_player + 1}?")
        self.label_name.pack()

        self.entry_name = tk.Entry(self.frame)
        self.entry_name.pack()

        self.button_name = tk.Button(self.frame, text="Submit", command=self.save_player_name)
        self.button_name.pack()

    def save_player_name(self):
        player_name = self.entry_name.get()
        player_data = next((player for player in self.loaded_players if player["name"] == player_name), None)

        if player_data:
            player = Player(player_data["name"], player_data["money"])
            print(f"Loaded existing player: {player_name} with {player_data['money']} money.")
        else:
            player = Player(player_name)
            self.loaded_players.append({"id": len(self.loaded_players) + 1, "name": player_name, "money": player.money})
            print(f"Created new player: {player_name}.")

        self.players.append(player)
        self.current_player += 1
        if self.current_player < self.nb_players:
            self.get_player_name()
        else:
            self.init_game()

    def init_game(self):
        self.select_players()
        shuffle(deck)

        for player in self.players:
            player.hand = [draw_card(deck), draw_card(deck)]

        self.clear_frame()

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
        

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()
        self.frame = tk.Frame(self.root)
        self.frame.pack()

    def select_players(self):
        self.players.append(Dealer())
        self.current_player = 0
        self.player = self.players[self.current_player]

    def place_bet(self):
        try:
            bet = int(self.entry_bet.get())
            if 0 < bet <= self.player.money:
                self.player.set_bet(bet)
                self.jackpot += bet
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
        self.current_player = self.current_player % (len(self.players))
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
        winners = []
        dealer_hand = self.players[-1].calculate_hand()
        i = 0
        
        for player in self.players[:-1]:
            player_hand = player.calculate_hand()
            if player_hand > 21 or (player_hand < dealer_hand and dealer_hand <= 21):
                results.append(f"{player.name} a perdu.")
            elif dealer_hand > 21 or player_hand > dealer_hand:
                winners.append(player)
                results.append(f"{player.name} a gagné.")
            else:
                winners.append(player)
                results.append(f"{player.name} a fait un match nul.")
                            
            self.labels_players[i].config(text=player)
            i += 1
        
        if winners:
            for winner in winners:
                if self.jackpot == 0:
                    results.append(f"{winner.name} you ruined us all ! You took the last of the jackpot !")
                else:
                    if winner.calculate_hand() == 21:
                        jackpot_share = winner.bet*1.5
                        self.jackpot -= jackpot_share
                    if winner.calculate_hand() < 21:
                        jackpot_share = winner.bet*2
                        self.jackpot -= jackpot_share
                    if winner.calculate_hand() == dealer_hand:
                        jackpot_share = winner.bet
                        self.jackpot -= jackpot_share
                
                winner.money += jackpot_share
                results.append(f"{winner.name} receives {jackpot_share:.2f} from the jackpot.")
                self.labels_players[self.players.index(winner)].config(text=winner)
        else:
            results.append("None of you got lucky huh ? Better luck next time !")
            
            
        self.label_result.config(text="\n".join(results))

        self.button_hit.config(state="disabled")
        self.button_stand.config(state="disabled")
        self.button_restart = tk.Button(self.frame, text="Recommencer", command=self.reset_game)
        self.button_restart.pack()        

        self.save_updated_player_data()

    def save_updated_player_data(self):
        for player in self.players:
            if isinstance(player, Player):
                player_data = next((p for p in self.loaded_players if p["name"] == player.name), None)
                if player_data:
                    player_data["money"] = player.money
        write_player_data(file_path, self.loaded_players)

    def reset_game(self):
        self.current_player = 0
        for player in self.players:
            player.clear_hand()
        self.clear_frame()
        self.choose_nb_players()

# Initialize the Tkinter application
root = tk.Tk()
game = BlackjackGame(root)
root.mainloop()
