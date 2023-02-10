import discord
import responses
import connect4

# insert token here
TOKEN = ""

intents = discord.Intents.default()
intents.message_content= True
intents.reactions = True
intents.members = True

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await responses.handle_message(message)

@client.event
async def on_reaction_add(reaction, user):
    pass

client.run(TOKEN)