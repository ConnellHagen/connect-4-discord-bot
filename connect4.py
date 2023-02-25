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
        string_of_grid += ":black_large_square:" * 9
        string_of_grid += "\n"
        string_of_grid += ":black_large_square:"
        string_of_grid += ":one::two::three::four::five::six::seven:"
        string_of_grid += ":black_large_square:\n"
        for h in range(6):
            string_of_grid += ":black_large_square:"
            for w in range(7):
                if self.gameboard[h][w] == GamePiece.NoPiece:
                    string_of_grid += ":white_large_square:"
                elif self.gameboard[h][w] == GamePiece.Yellow:
                    string_of_grid += ":yellow_circle:"
                elif self.gameboard[h][w] == GamePiece.Red:
                    string_of_grid += ":red_circle:"
            string_of_grid += ":black_large_square:\n"
        string_of_grid += ":black_large_square:" * 9

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
    
    def get_turn(self):
        return self.turn
    
    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

class GameHandler:
    def __init__(self):
        self.id_game_dict = {}

    async def handle_challenge(self, player1, player2, channel):
        # note to self: send message about initiating new game
        await self.add_game(player1, player2, channel)
    
    async def add_game(self, player1, player2, channel):
        new_game = Connect4Game(player1, player2)
        message_id = await new_game.send_game_message(channel);
        self.id_game_dict[message_id] = new_game
    
    async def handle_reaction(self, reaction, user):
        try:
            reacted_game = self.id_game_dict[reaction.message.id]

            player_turn = user;
            if(reacted_game.get_turn() == PlayerColor.Red):
                player_turn = reacted_game.get_player1()
            else:
                player_turn = reacted_game.get_player2()

            if player_turn == user:
                print("take action!!")
                # Note to self: insert code here for transferring the emoji to action in the game being taken
            # if the person reacting to a game is not the person who is taking a turn, the reaction is removed
            else:
                await reaction.message.remove_reaction(reaction.emoji, user)

        # Exception is thrown when a message not containing a game is reacted to
        # Nothing will happen since the reaction must have been added to a non-game message
        except Exception as excep:
            pass
                