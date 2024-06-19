from dealer import Dealer
from player import Player


import tkinter as tk
from random import choice, shuffle

# Constantes du jeu
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4

def draw_card(deck):
    return choice(deck)

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        
        self.current_player_index = 0
        self.players = [Player("Joueur 1"), Player("Joueur 2"), Player("Joueur 3"), Player("Joueur 4")]
        self.current_player = self.players[self.current_player_index]
        self.dealer = Dealer()
        self.init_game()

    def init_game(self):
        shuffle(deck)

        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.labels_players = []
        for player in self.players:
            label = tk.Label(self.frame, text=player)
            label.pack()
            self.labels_players.append(label)
        
        self.label_dealer = tk.Label(self.frame, text=f"Dealer: [{self.dealer.get_hand()}, '?']")
        self.label_dealer.pack()

        self.label_bet = tk.Label(self.frame, text=f"{self.current_player.get_name}, placez votre mise:")
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
        
    def next_player(self):
        self.current_player_index = self.current_player_index % len(self.players)
        if self.current_player_index == len(self.players):
            self.current_player= self.dealer
        else:
            self.current_player = self.players[self.current_player_index]

    def place_bet(self):
        try:
            bet = int(self.entry_bet.get())
            if 0 < bet <= self.current_player.get_money:
                self.current_player.set_bet(bet)
                self.labels_players[self.current_player_index].config(text=self.current_player)
                self.entry_bet.delete(0, tk.END)
                self.next_player()
                
                # si le joueur est une insance de Dealer
                if isinstance(self.current_player, Dealer):
                    self.start_turns()
                else:
                    self.label_bet.config(text=f"{self.current_player}, placez votre mise:")
            else:
                self.label_result.config(text="Mise invalide.")
        except ValueError:
            self.label_result.config(text="Veuillez entrer un nombre valide.")

    def start_turns(self):
        self.label_bet.pack_forget()
        self.entry_bet.pack_forget()
        self.button_bet.pack_forget()
        self.label_result.config(text=f"C'est au tour de {self.current_player}.")
        self.button_hit.config(state="normal")
        self.button_stand.config(state="normal")

    def hit(self):
        card = draw_card(deck)
        
        if (self.current_player < 3):
          self.player_hands[self.current_player].append(card)
          total = calculate_hand(self.player_hands[self.current_player])
          self.labels_players[self.current_player].config(text=f"Joueur {self.current_player + 1}: {self.player_hands[self.current_player]} (Total: {total}) - Score: {self.player_scores[self.current_player]}")
        else:
          self.dealer_hand.append(card)
          total = calculate_hand(self.dealer_hand)
          self.label_dealer.config(text=f"Dealer: {self.dealer_hand} (Total: {total})")
          
        if total > 21:
            self.label_result.config(text=f"Joueur {self.current_player + 1} a dépassé 21 et a perdu sa mise.")
            self.end_turn()

    def stand(self):
        self.end_turn()

    def end_turn(self):
        self.current_player += 1
        self.current_player = self.current_player % 4
        if self.current_player == 4:
            self.dealer_turn()
        else:
            self.label_result.config(text=f"C'est au tour du joueur {self.current_player + 1}.")
            self.button_hit.config(state="normal")
            self.button_stand.config(state="normal")

    def dealer_turn(self):
        self.label_dealer.config(text=f"Dealer: {self.dealer_hand} (Total: {calculate_hand(self.dealer_hand)})")
        dealer_total = calculate_hand(self.dealer_hand)
        
        while dealer_total < 17:
            self.dealer_hand.append(draw_card(deck))
            dealer_total = calculate_hand(self.dealer_hand)
            self.label_dealer.config(text=f"Dealer: {self.dealer_hand} (Total: {dealer_total})")

        self.check_winner()

    def check_winner(self):
        dealer_total = calculate_hand(self.dealer_hand)
        results = []
        
        for i in range(4):
            player_total = calculate_hand(self.player_hands[i])
            if player_total > 21:
                results.append(f"Joueur {i + 1} a perdu.")
            elif dealer_total > 21 or player_total > dealer_total:
                self.player_scores[i] += self.player_bets[i] * 2
                results.append(f"Joueur {i + 1} a gagné.")
            elif player_total < dealer_total:
                results.append(f"Joueur {i + 1} a perdu.")
            else:
                self.player_scores[i] += self.player_bets[i]
                results.append(f"Joueur {i + 1} a fait un match nul.")
            
            self.labels_players[i].config(text=f"Joueur {i + 1}: {self.player_hands[i]} (Total: {player_total}) - Score: {self.player_scores[i]}")
        
        self.label_result.config(text="\n".join(results))
        self.reset_game()

    def reset_game(self):
        self.current_player = 0
        self.player_bets = [0, 0, 0, 0]
        self.frame.destroy()
        self.init_game()

# Initialisation de l'application Tkinter
root = tk.Tk()
game = BlackjackGame(root)
root.mainloop()
