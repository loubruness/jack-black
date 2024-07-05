from person import Player
from person import Dealer

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name, money=50, nb_games=1, nb_wins=0, nb_losses=0):
        # SRP: The create_player method is responsible for creating instances of players or dealers.
        if player_type == "dealer":
            return Dealer()
        elif player_type == "human":
            return Player(name, money, nb_games, nb_wins, nb_losses)
        else:
            # SRP: Error handling is also a responsibility of this method.
            raise ValueError(f"Unknown player type: {player_type}")

# DIP: The create_player method adheres to the Dependency Inversion Principle by creating instances of Dealer or Player based on the provided parameters without the rest of the code depending directly on the creation of these instances.
# OCP: The create_player method is open for extension. To add a new player type, simply add a new condition for that type in this method without modifying other parts of the code.
