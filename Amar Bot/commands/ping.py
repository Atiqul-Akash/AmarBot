from discord import app_commands, Interaction, Embed
from discord.ext import commands
import datetime

@app_commands.command(name="ping", description="Check the bot's latency")
async def ping(interaction: Interaction):
    latency_ms = round(interaction.client.latency * 1000)
    now = datetime.datetime.utcnow()
    unix_timestamp = int(now.timestamp())

    embed = Embed(
        title="🏓 Pong!",
        description=f"**Latency:** `{latency_ms}ms`",
        color=0x00BFFF
    )
    embed.set_footer(text="Bot Status • /ping")

    await interaction.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.tree.add_command(ping)
