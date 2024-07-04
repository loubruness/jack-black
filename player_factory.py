from person import Player
from person import Dealer

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name, money=50, nb_games=1, nb_wins=0, nb_losses=0):
        if player_type == "dealer":
            return Dealer()
        elif player_type == "human":
            return Player(name, money, nb_games, nb_wins, nb_losses)
        else:
            raise ValueError(f"Unknown player type: {player_type}")