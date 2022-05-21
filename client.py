import discord
from discord.ext import commands

import Message
from Storage import Storage

TOKEN = ""
PREFIX = "!"

cogs = [Message]

client = commands.Bot(command_prefix=PREFIX)
client.remove_command("help")

for i in range(len(cogs)):
    cogs[i].setup(client, PREFIX)

#@client.event
#async def on_message(message):
#    if Storage().checking.checking_server_channel(message.guild.id, message.channel.id):

@client.event
async def on_ready():
    print(f"[ LOGIN ]: {client.user}")

client.run(TOKEN)