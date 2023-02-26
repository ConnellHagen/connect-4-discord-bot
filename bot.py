import discord
import responses

# insert token here
TOKEN = ""

intents = discord.Intents.default()
intents.message_content= True
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
    if user == client.user:
        return
    await responses.handle_reaction(reaction, user)

client.run(TOKEN)