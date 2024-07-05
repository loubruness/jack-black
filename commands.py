from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class HitCommand(Command):
    def __init__(self, player, deck):
        self.player = player
        self.deck = deck

    def execute(self):
        card = self.deck.draw_card()
        self.player.take_card(card)
        return card

class StandCommand(Command):
    def __init__(self, game):
        self.game = game

    def execute(self):
        self.game.end_turn()
