class Person:
    name=''
    def __init__(self):
        self.hand = []
      
    def take_card(self, card):
        self.hand.append(card)
      
    def clear_hand(self):
        self.hand = []
      
    def calculate_hand(self):
        total = 0
        aces = 0
        for card in self.hand:
            if card[0] in ['J', 'Q', 'K']:
                total += 10
            elif card[0] == 'A':
                aces += 1
                total += 11
            else:
                total += int(card[:-1])
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

class Dealer(Person):
    def __init__(self):
        super().__init__()
        self.visible = False
        self.name = 'Dealer'
        
    def start_turn(self,game):
        self.visible = True
        while self.calculate_hand() < 17:
            self.take_card(game.deck.draw_card())
        self.check_winner(game)
        
    def check_winner(self,game):
        results = []
        hand = self.calculate_hand()
        for player in game.players[:-1]:
            player.nb_games += 1
            player_hand = player.calculate_hand()
            if player_hand > 21 or (player_hand < hand and hand <= 21):
                results.append(f"{player.name} a perdu.")
                player.nb_losses += 1
            elif hand > 21 or player_hand > hand:
                results.append(f"{player.name} a gagné.")
                player.nb_wins += 1
                game.jackpot -= player.bet * 2
                player.money += player.bet * 2
            else:
                results.append(f"{player.name} a fait un match nul.")
                game.jackpot -= player.bet
                player.money += player.bet
            player.bet = 0
        game.result = "\n".join(results)
  
        
    def __str__(self):
        if self.visible:
            return f"Dealer: {self.hand} (Total: {self.calculate_hand()})"
        return f"Dealer: [{self.hand[0]}, '?'] (Total: ?)"
    
    def __repr__(self):
        return self.__str__()
  
class Player(Person):
    def __init__(self, name, money=50, nb_games=1, nb_wins=0, nb_losses=0):
        super().__init__()
        self.name = name
        self.money = money
        self.bet = 0
        self.nb_games = nb_games
        self.nb_wins = nb_wins
        self.nb_losses = nb_losses
    
    def set_bet(self, new_bet):
        self.bet = new_bet
        self.money -= new_bet
  
    def __str__(self):
        return f"{self.name}: {self.hand} (Total: {self.calculate_hand()}) - Money: {self.money} - Bet: {self.bet}"
  
    def __repr__(self):
        return self.__str__()
