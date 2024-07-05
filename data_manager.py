import json

class DataManager:
    @staticmethod
    def read_player_data(file_path):
        # SRP: Responsible for reading player data from a file.
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Return an empty list if the file is not found

    @staticmethod
    def write_player_data(file_path, players):
        # SRP: Responsible for writing player data to a file.
        with open(file_path, 'w') as file:
            json.dump(players, file, indent=4)

# SRP: DataManager class separates concerns by providing methods specifically for reading and writing player data, adhering to the Single Responsibility Principle.
# OCP: The DataManager class is open for extension. If additional data management functionality is needed, new methods can be added without modifying existing read and write methods.
# DIP: DataManager class depends on abstractions (file I/O and JSON serialization provided by Python's standard library) rather than concrete implementations, adhering to the Dependency Inversion Principle.
