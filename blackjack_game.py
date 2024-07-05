from card import Deck
from person import Player, Dealer
from data_manager import DataManager
from player_factory import PlayerFactory
from commands import HitCommand, StandCommand

class BlackjackGame:    # Create a BlackjackGame class to respect the MVC design pattern
    def __init__(self, file_path): # Initialize the BlackjackGame class with the file_path, and loaded_players attributes
        self.file_path = file_path
        self.loaded_players = DataManager.read_player_data(self.file_path)
        self.init_game()
    
    def init_game(self): # Initialize the game with the default values
        self.jackpot = 10000   
        self.nb_players = 0
        self.players = []
        self.current_player = 0
        self.deck = Deck(4)
        self.state = "start_game"   # State of the game that permits to the UI to know what to display
        self.result = ""    # Result of the game that is displayed in the UI
        
    def start_game(self):   # Start the game and set the state to "set_players"
        self.result = f"Entrez le nombre de joueurs."
        self.state="set_players"
        
    def set_nb_players(self, nb_players):   # Set the number of players in the game(check if it is a good value), and set the state to "set_names"
        try:
            self.nb_players = int(nb_players)
            self.current_player = 0
            self.players = []
            self.state="set_names"
            self.result = f"Entrez le nom du joueur {self.current_player + 1}."
        except ValueError:
            self.result = "Veuillez entrer un nombre valide."

    def add_player(self, player_name):  # Add a player to the game, load the player data if it exists, and set the state to "init_playing"
        player_data = next((player for player in self.loaded_players if player["name"] == player_name), None)
        if player_data:
            player = PlayerFactory.create_player("human", player_data["name"], player_data["money"], player_data["nb_games"], player_data["nb_wins"], player_data["nb_losses"])
            if player.money == 0:
                player.money = 50
                print(f"{player.name} a reçu 50€ pour rejouer.")
        else:
            player = PlayerFactory.create_player("human", player_name)
            self.loaded_players.append({"id": len(self.loaded_players) + 1, "name": player_name, "money": player.money, "nb_games": player.nb_games, "nb_wins": player.nb_wins, "nb_losses": player.nb_losses})
        self.players.append(player)
        self.current_player += 1
        if self.current_player < self.nb_players:
            self.result = f"Entrez le nom du joueur {self.current_player + 1}."
        else:
            self.state="init_playing"

    def init_playing(self):  # Add a Dealer to the game and give two cards to each player, set the state to "place_bet"
        self.players.append(PlayerFactory.create_player("dealer", "Dealer"))
        for player in self.players:
            player.hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.current_player = 0
        self.player = self.players[self.current_player]
        self.state="place_bet"
        self.result = f"{self.player.name}, placez votre mise."

    def place_bet(self, bet):   # Place a bet for the current player, and set the state to "start_turns" if all players have placed their bets
        try:
            bet = int(bet)
            if 0 < bet <= self.player.money:
                self.player.set_bet(bet)
                self.jackpot += bet
                self.next_player()

                if isinstance(self.player, Dealer):
                    self.next_player()
                    self.state="start_turns"
                else:
                    self.result = f"{self.player.name}, placez votre mise."
            else:
                self.result = "Mise invalide."
        except ValueError:
            self.result ="Veuillez entrer un nombre valide."        

    def next_player(self):  # Set the next player as the current player
        self.current_player += 1
        self.current_player %= len(self.players)
        self.player = self.players[self.current_player]

    def start_turns(self):  # Start the turns of the players, and set the state to "player_turn"
        self.state="player_turn"
        self.player_turn()

    def player_turn(self):  # Start the turn of the current player and set the state to "end_playing" if the current player is the dealer
        if isinstance(self.player, Dealer):
            self.dealer_turn()
        else:
            self.result = f"C'est au tour de {self.player.name}."

    def hit(self):  # Execute the HitCommand and check if the player has a blackjack or has exceeded 21
        command = HitCommand(self.player, self.deck)
        card = command.execute()
        if self.player.calculate_hand() == 21:
            self.result = f"{self.player.name} a fait un blackjack."
            self.end_turn()
        elif self.player.calculate_hand() > 21:
            self.result = f"{self.player.name} a dépassé 21 et a perdu sa mise."
            self.end_turn()

    def stand(self):    # Execute the StandCommand and end the turn of the current player
        command = StandCommand(self)
        command.execute()

    def end_turn(self): # End the turn of the current player and start the turn of the next player
        self.next_player()
        self.player_turn()

    def dealer_turn(self):  # Start the turn of the dealer and set the state to "end_playing"
        dealer = self.players[-1]
        while dealer.calculate_hand() < 17:
            command = HitCommand(dealer, self.deck)
            command.execute()
        dealer.visible = True
        self.check_winner()
        self.save_updated_player_data()
        self.state="end_playing"
        
    def check_winner(self): # Check the winner of the game and update the player data
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

    def save_updated_player_data(self): # Save the updated player data in the file
        for player in self.players:
            if isinstance(player, Player):
                player_data = next((p for p in self.loaded_players if p["name"] == player.name), None)
                if player_data:
                    player_data["money"] = player.money
                    player_data["nb_games"] = player.nb_games
                    player_data["nb_wins"] = player.nb_wins
                    player_data["nb_losses"] = player.nb_losses
        DataManager.write_player_data(self.file_path, self.loaded_players)
        
    def restart(self): # Restart the game
        self.init_game()

        
    
