# Connect 4 Bot

## About
Connect 4 certainly is one of the games of all time. And now you can play it in your Discord server with your friends using this bot. 

The rules are simple:

1. Players take turns dropping pieces down columns in the game board.

2. If a player gets 4 of their pieces in a row, they win. If the board fills up with no lines of 4, the game is a draw. Examples:

<p float = "left">
    <img src = "https://user-images.githubusercontent.com/72321241/221975114-8605321e-5d6d-4173-aa29-e56ce7a87d07.png" width = 45% >
    <img src = "https://user-images.githubusercontent.com/72321241/221975115-469be18c-b017-495b-a81d-c44ae01ccc2e.PNG" width = 45% >
</p>

## Usage

### Hosting the bot yourself:

Go to the Discord Developer Portal (https://discord.com/developers/applications) and create a new application. Create a bot, and copy its token. Paste the token into the `Token = ""` quotes in `bot.py`. Lastly, execute the code with `python3 bot.py`. If the token is correct, any server that the bot you created is a member of will now have a working connect 4 bot

### Adding the official bot to your server (not recommended; going to be offline):

Click the following link, Discord will walk you through hosting my official bot on your server: https://discord.com/api/oauth2/authorize?client_id=1069375140577677323&permissions=274878113856&scope=bot
.

## Other Information
To get a list of all commands the bot can use, say "!help" in the chat and it will respond with them.

To challenge a player, use "!challenge @[player]" in order to start a game.
