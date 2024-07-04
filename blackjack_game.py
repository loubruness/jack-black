from card import Deck
from person import Player, Dealer
from data_manager import DataManager
from player_factory import PlayerFactory
from commands import HitCommand, StandCommand

class BlackjackGame:
    def __init__(self, file_path):
        self.jackpot = 10000
        self.file_path = file_path
        self.loaded_players = DataManager.read_player_data(self.file_path)
        self.init_game()
    
    def init_game(self):
        self.nb_players = 0
        self.players = []
        self.current_player = 0
        self.deck = Deck()
        self.nb_players = 0
        self.state = "start_game"
        self.result = ""
        
    def start_game(self):
        self.result = f"Entrez le nombre de joueurs."
        self.state="set_players"
        
    def set_nb_players(self, nb_players):
        self.nb_players = nb_players
        self.current_player = 0
        self.players = []
        self.state="set_names"
        self.result = f"Entrez le nom du joueur {self.current_player + 1}."

    def add_player(self, player_name):
        player_data = next((player for player in self.loaded_players if player["name"] == player_name), None)
        if player_data:
            player = PlayerFactory.create_player("human", player_data["name"], player_data["money"], player_data["nb_games"], player_data["nb_wins"], player_data["nb_losses"])
        else:
            player = PlayerFactory.create_player("human", player_name)
            self.loaded_players.append({"id": len(self.loaded_players) + 1, "name": player_name, "money": player.money, "nb_games": player.nb_games, "nb_wins": player.nb_wins, "nb_losses": player.nb_losses})
        self.players.append(player)
        self.current_player += 1
        if self.current_player < self.nb_players:
            self.result = f"Entrez le nom du joueur {self.current_player + 1}."
        else:
            self.state="init_party"

    def init_party(self):
        self.players.append(PlayerFactory.create_player("dealer", "Dealer"))
        for player in self.players:
            player.hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.current_player = 0
        self.player = self.players[self.current_player]
        self.state="place_bet"
        self.result = f"{self.player.name}, placez votre mise."

    def place_bet(self, bet):
        self.player.set_bet(bet)
        self.jackpot += bet
        self.next_player()
        self.result = f"{self.player.name}, placez votre mise."
        if isinstance(self.player, Dealer):
            self.next_player()
            self.state="start_turns"
            

    def next_player(self):
        self.current_player += 1
        self.current_player %= len(self.players)
        self.player = self.players[self.current_player]

    def start_turns(self):
        self.state="player_turn"
        self.player_turn()

    def player_turn(self):
        if isinstance(self.player, Dealer):
            self.dealer_turn()
        else:
            self.result = f"C'est au tour de {self.player.name}."

    def hit(self):
        command = HitCommand(self.player, self.deck)
        card = command.execute()
        if self.player.calculate_hand() == 21:
            self.result = f"{self.player.name} a fait un blackjack."
            self.end_turn()
        elif self.player.calculate_hand() > 21:
            self.result = f"{self.player.name} a dépassé 21 et a perdu sa mise."
            self.end_turn()

    def stand(self):
        command = StandCommand(self)
        command.execute()

    def end_turn(self):
        self.next_player()
        self.player_turn()

    def dealer_turn(self):
        dealer = self.players[-1]
        dealer.visible = True
        while dealer.calculate_hand() < 17:
            dealer.take_card(self.deck.draw_card())
        self.check_winner()
        self.state="end_party"

    def check_winner(self):
        results = []
        dealer_hand = self.players[-1].calculate_hand()
        for player in self.players[:-1]:
            player.nb_games += 1
            player_hand = player.calculate_hand()
            if player_hand > 21 or (player_hand < dealer_hand and dealer_hand <= 21):
                results.append(f"{player.name} a perdu.")
                player.nb_losses += 1
            elif dealer_hand > 21 or player_hand > dealer_hand:
                results.append(f"{player.name} a gagné.")
                player.nb_wins += 1
                self.jackpot -= player.bet * 2
                player.money += player.bet * 2
            else:
                results.append(f"{player.name} a fait un match nul.")
                self.jackpot -= player.bet
                player.money += player.bet
            player.bet = 0
            
        self.result = "\n".join(results)
        self.save_updated_player_data()

    def save_updated_player_data(self):
        for player in self.players:
            if isinstance(player, Player):
                player_data = next((p for p in self.loaded_players if p["name"] == player.name), None)
                if player_data:
                    player_data["money"] = player.money
                    player_data["nb_games"] = player.nb_games
                    player_data["nb_wins"] = player.nb_wins
                    player_data["nb_losses"] = player.nb_losses
        DataManager.write_player_data(self.file_path, self.loaded_players)
        
    def restart(self):
        self.init_game()

        
    
