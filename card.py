import random

class Deck:

    # Singleton design pattern
    _instance = None
    
    def __new__(cls, nb_decks=1):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(nb_decks)
        return cls._instance
    
    def __init__(self, nb_decks=1):
        self.nb_decks = nb_decks
        self.num_card = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.color_card = ['♠', '♣', '♦', '♥']
        self.cards = [card + color for card in self.num_card for color in self.color_card for _ in range(self.nb_decks)]
        random.shuffle(self.cards)
        
    def draw_card(self):
        if not self.cards:
            raise ValueError("No more cards in the deck.")
        return self.cards.pop()
