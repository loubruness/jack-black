import tkinter as tk
from random import choice, shuffle

# Constantes du jeu
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4

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
        
        self.player_scores = [50, 50, 50, 50]
        self.player_bets = [0, 0, 0, 0]
        self.current_player = 0
        self.init_game()

    def init_game(self):
        shuffle(deck)
        self.dealer_hand = [draw_card(deck), draw_card(deck)]
        self.player_hands = [[draw_card(deck), draw_card(deck)] for _ in range(4)]

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.labels_players = []
        for i in range(4):
            label = tk.Label(self.frame, text=f"Joueur {i + 1}: {self.player_hands[i]} (Total: {calculate_hand(self.player_hands[i])}) - Score: {self.player_scores[i]}")
            label.pack()
            self.labels_players.append(label)
        
        self.label_dealer = tk.Label(self.frame, text=f"Dealer: [{self.dealer_hand[0]}, '?']")
        self.label_dealer.pack()

        self.label_bet = tk.Label(self.frame, text=f"Joueur {self.current_player + 1}, placez votre mise:")
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

    def place_bet(self):
        try:
            bet = int(self.entry_bet.get())
            if 0 < bet <= self.player_scores[self.current_player]:
                self.player_bets[self.current_player] = bet
                self.player_scores[self.current_player] -= bet
                self.labels_players[self.current_player].config(text=f"Joueur {self.current_player + 1}: {self.player_hands[self.current_player]} (Total: {calculate_hand(self.player_hands[self.current_player])}) - Score: {self.player_scores[self.current_player]}")
                self.entry_bet.delete(0, tk.END)
                self.current_player += 1

                if self.current_player == 4:
                    self.start_turns()
                else:
                    self.label_bet.config(text=f"Joueur {self.current_player + 1}, placez votre mise:")
            else:
                self.label_result.config(text="Mise invalide.")
        except ValueError:
            self.label_result.config(text="Veuillez entrer un nombre valide.")

    def start_turns(self):
        self.label_bet.pack_forget()
        self.entry_bet.pack_forget()
        self.button_bet.pack_forget()
        self.label_result.config(text=f"C'est au tour du joueur {self.current_player + 1}.")
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
