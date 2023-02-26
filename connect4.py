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
                    string_of_grid += ":yellow_square:"
                elif self.gameboard[h][w] == GamePiece.Red:
                    string_of_grid += ":red_square:"
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

        emojis = ["{}\ufe0f\u20e3".format(num) for num in range(1, 8)]
        for emoji in emojis:
            await message.add_reaction(emoji)

        return id
    
    async def send_win_message(self, channel):
        pass
    
    def is_legal_move(self, column):
        return self.gameboard[0][column] == GamePiece.NoPiece
    
    def make_move(self, column):
        for i in range(0, 6)[::-1]:
            if(self.gameboard[i][column] == GamePiece.NoPiece):
                self.gameboard[i][column] = self.turn_to_piece()
                break

    def switch_turns(self):
        if self.turn != PlayerColor.Red:
            self.turn = PlayerColor.Red
        else:
            self.turn = PlayerColor.Yellow

    def test_for_win(self):
        return False

    def turn_to_piece(self):
        if(self.turn == PlayerColor.Yellow):
            return GamePiece.Yellow
        else:
            return GamePiece.Red
    
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

            # if the person reacting to a game is not the person who is taking a turn, the reaction is removed
            if player_turn != user:
                await reaction.message.remove_reaction(reaction.emoji, user)
                return 
            
            emoji = str(reaction.emoji)
            number_selected = 0

            if(emoji == "1\ufe0f\u20e3"):
                number_selected = 1
            elif(emoji == "2\ufe0f\u20e3"):
                number_selected = 2
            elif(emoji == "3\ufe0f\u20e3"):
                number_selected = 3
            elif(emoji == "4\ufe0f\u20e3"):
                number_selected = 4
            elif(emoji == "5\ufe0f\u20e3"):
                number_selected = 5
            elif(emoji == "6\ufe0f\u20e3"):
                number_selected = 6
            elif(emoji == "7\ufe0f\u20e3"):
                number_selected = 7
            else: # undo reaction if the reaction is not one of the 7 valid commands
                await reaction.message.remove_reaction(reaction.emoji, user)
                return
        
            # undo reaction if the move made is illegal
            if(not reacted_game.is_legal_move(number_selected - 1)):
                await reaction.message.remove_reaction(reaction.emoji, user)
                return
                        

            del self.id_game_dict[reaction.message.id]
            await reaction.message.delete()
            reacted_game.make_move(number_selected - 1)

            # if the game has been won by the move, then this will end the game
            if(reacted_game.test_for_win()):
                reacted_game.send_win_message()
                return
                        
            reacted_game.switch_turns()
            message_id = await reacted_game.send_game_message(reaction.message.channel)
            self.id_game_dict[message_id] = reacted_game
                

        # exception is thrown when a message not containing a game is reacted to
        # nothing will happen since the reaction must have been added to a non-game message
        except Exception as excep:
            pass