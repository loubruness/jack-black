import json

# Function to write player data to a JSON file
def write_player_data(file_path, players):
    with open(file_path, 'w') as file:
        json.dump(players, file, indent=4)

# Function to read player data from a JSON file
def read_player_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Example player data
players_data = [
    {"name": "Alice", "balance": 1000},
    {"name": "Bob", "balance": 1500},
    {"name": "Charlie", "balance": 500}
]

# File path
file_path = 'players.json'

# Write data to JSON file
write_player_data(file_path, players_data)

# Read data from JSON file
loaded_players_data = read_player_data(file_path)

# Print loaded data
for player in loaded_players_data:
    print(f"Name: {player['name']}, Balance: {player['balance']}")

for player in loaded_players_data:
    player['balance'] += 100

# Write updated data back to JSON file
write_player_data(file_path, loaded_players_data)