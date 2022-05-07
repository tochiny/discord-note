import discord
from discord.ext import commands

import Message

TOKEN = ""
PREFIX = "!"

cogs = [Message]

bot = commands.Bot(command_prefix=PREFIX)

for i in range(len(cogs)):
    cogs[i].setup(bot)

@bot.event
async def on_ready():
    print(f"[ LOGIN ]: {bot.user}")

bot.run(TOKEN)
