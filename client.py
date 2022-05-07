import discord
from discord.ext import commands

import Message

TOKEN = "OTY3MDQ5NTM2ODA5ODc3NTA0.GOHIn1.l2iNI15MeeInOIUM9WTjlhBpghliALOjddInvc"
PREFIX = "!"

cogs = [Message]

bot = commands.Bot(command_prefix=PREFIX)

for i in range(len(cogs)):
    cogs[i].setup(bot)

@bot.event
async def on_ready():
    print(f"[ LOGIN ]: {bot.user}")

bot.run(TOKEN)