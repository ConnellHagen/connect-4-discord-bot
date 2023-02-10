import random
from enum import Enum

class GamePiece(Enum):
    NoPiece = 0
    Yellow = 1
    Red = 2

class Connect4Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.gameboard = [[GamePiece.NoPiece for w in range(7)] for h in range(6)]

    def to_grid(self):
        string_of_grid = "";
        for h in range(6):
            for w in range(7):
                if self.gameboard[h][w] == GamePiece.NoPiece:
                    string_of_grid += ":white_large_square:"
                elif self.gameboard[h][w] == GamePiece.Yellow:
                    string_of_grid += ":yellow_circle:"
                elif self.gameboard[h][w] == GamePiece.Red:
                    string_of_grid += ":red_circle:"
                if (w == 6 and h != 5):
                    string_of_grid += "\n"

        return string_of_grid

class GameHandler:
    def __init__(self):
        # holds game IDs as keys, and `Connect4Game` objects as values
        self.game_list = {}
        self.id_list = []

    async def handle_challenge(self, player1, player2):
        self.id_list.append(self.add_game(player1, player2))
    
    def add_game(self, player1, player2):
        id = generate_id()
        self.game_list[id] = Connect4Game(player1, player2)
        return id

    def retrieve_game(self, id):
        return self.game_list.get(id, None)

    def get_id_list(self):
        return self.id_list


VALUES = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
def generate_id():
    id = ""
    for i in range(20):
        id += VALUES[random.randint(0, 61)]
    return id