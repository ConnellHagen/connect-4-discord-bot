import random
from enum import Enum

class GamePiece(Enum):
    NoPiece = 0
    Yellow = 1
    Red = 2

class PlayerColor(Enum):
    Yellow = 0
    Red = 1

class Connect4Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.turn = random.choice(list(PlayerColor)) # Chooses a random starting player
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

    async def send_game_message(self, channel):
        message_content = ""
        if(self.turn == PlayerColor.Red):
            message_content += f":red_circle: Red: {self.player1.mention}\n:white_circle: Yellow: {self.player2.mention}\n"
        else:
            message_content += f":white_circle: Red: @{self.player1.mention}\n:yellow_circle: Yellow: @{self.player2.mention}\n"
        message_content += self.to_grid();

        message = await channel.send(message_content)
        id = message.id
        return id

class GameHandler:
    def __init__(self):
        self.id_game_dict = {}

    async def handle_challenge(self, player1, player2, channel):
        # send message about initiating new game
        await self.add_game(player1, player2, channel)
    
    async def add_game(self, player1, player2, channel):
        new_game = Connect4Game(player1, player2)
        message_id = await new_game.send_game_message(channel);
        self.id_game_dict[message_id] = new_game