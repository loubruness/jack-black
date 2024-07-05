from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        # SRP: Defines a single responsibility method for execution of commands.
        pass

class HitCommand(Command):
    def __init__(self, player, deck):
        # SRP: Handles the command to hit a player with a card from a deck.
        self.player = player
        self.deck = deck

    def execute(self):
        # SRP: Executes the command by drawing a card and giving it to the player.
        card = self.deck.draw_card()
        self.player.take_card(card)
        return card

class StandCommand(Command):
    def __init__(self, game):
        # SRP: Handles the command to stand in the game.
        self.game = game

    def execute(self):
        # SRP: Executes the command to end the turn in the game.
        self.game.end_turn()

# OCP: The Command, HitCommand, and StandCommand classes are open for extension. You can create new commands by subclassing Command without modifying existing code.
# LSP: Instances of HitCommand and StandCommand can be substituted where Command is expected, ensuring compatibility with the Command interface.
# ISP: Command interface segregates the responsibility of executing commands, allowing concrete implementations like HitCommand and StandCommand to focus solely on their specific actions.
# DIP: The Command, HitCommand, and StandCommand classes depend on abstractions (Command and ABC module) rather than concrete implementations, adhering to the Dependency Inversion Principle.
