import connect4

game_handler = connect4.GameHandler();

async def handle_message(message):
    message_content = message.content.lower()

    # tests if the message is a bot command
    if message_content[0] != "!":
        return

    # isolates the specific command from the rest of the message
    command = ""
    for let in message_content:
        if let != " ":
            command += let
        else: break
    message_content = message_content[len(command):]


    bot_message = ""

    if command == "!help":
        bot_message = "Start a game of Connect 4 with \"!challenge @[player]\"!"

    elif command == "!challenge":
        mentions = message.mentions
        if len(mentions) != 1:
            bot_message = "You must mention one user to start a challenge."
        else:
            challenged_user = mentions[0]
            await game_handler.handle_challenge(message.author, challenged_user, message.channel)

    if bot_message != "":
        await message.channel.send(bot_message)

async def handle_reaction(reaction, user):
    await game_handler.handle_reaction(reaction, user)