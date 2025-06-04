import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import discord
from discord.ext import commands
from commands import setup as load_all_commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    try:
        load_all_commands(bot)
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

bot.run("YOUR_TOKEN_HERE")
