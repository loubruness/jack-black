class Person:
    # SRP: La classe Person a une seule responsabilité : gérer les cartes d'une personne (joueur ou dealer).
    def __init__(self, name=''):
        self.name = name
        self.hand = []

    def take_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def calculate_hand(self):
        # SRP: La méthode calculate_hand est responsable du calcul de la valeur des cartes.
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
    # OCP: La classe Dealer est une extension de Person et ajoute de nouvelles fonctionnalités sans modifier Person.
    def __init__(self):
        super().__init__('Dealer')
        self.visible = False

    def __str__(self):
        # SRP: La méthode __str__ est responsable de la représentation sous forme de chaîne de caractères.
        if self.visible:
            return f"Dealer: {self.hand} (Total: {self.calculate_hand()})"
        return f"Dealer: [{self.hand[0]}, '?'] (Total: ?)"

    def __repr__(self):
        # SRP: La méthode __repr__ utilise la méthode __str__ pour représenter l'objet.
        return self.__str__()

class Player(Person):
    # OCP: La classe Player est une extension de Person et ajoute de nouvelles fonctionnalités sans modifier Person.
    def __init__(self, name, money=50, nb_games=1, nb_wins=0, nb_losses=0):
        super().__init__(name)
        self.money = money
        self.bet = 0
        self.nb_games = nb_games
        self.nb_wins = nb_wins
        self.nb_losses = nb_losses

    def set_bet(self, new_bet):
        # SRP: La méthode set_bet est responsable de la gestion des paris du joueur.
        self.bet = new_bet
        self.money -= new_bet

    def __str__(self):
        # SRP: La méthode __str__ est responsable de la représentation sous forme de chaîne de caractères.
        return f"{self.name}: {self.hand} (Total: {self.calculate_hand()}) - Money: {self.money} - Bet: {self.bet}"

    def __repr__(self):
        # SRP: La méthode __repr__ utilise la méthode __str__ pour représenter l'objet.
        return self.__str__()
