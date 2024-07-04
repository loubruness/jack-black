import json

class DataManager:
    @staticmethod
    def read_player_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def write_player_data(file_path, players):
        with open(file_path, 'w') as file:
            json.dump(players, file, indent=4)
