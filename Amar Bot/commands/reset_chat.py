import os
from discord import app_commands, Interaction, Embed
from discord.ext import commands

MEMORY_DIR = "chat_memory"

@app_commands.command(name="resetchat", description="Reset your chat memory with the AI")
async def reset_chat(interaction: Interaction):
    user_id = interaction.user.id
    file_path = os.path.join(MEMORY_DIR, f"user_{user_id}.json")

    if os.path.exists(file_path):
        os.remove(file_path)
        embed = Embed(
            title="✅ Chat Memory Reset",
            description="Your chat history with the AI has been successfully cleared.",
            color=0x2ECC71  # Green
        )
        embed.set_footer(text="/resetchat • Memory cleared")
    else:
        embed = Embed(
            title="ℹ️ No Memory Found",
            description="You don’t have any chat history to reset.",
            color=0x3498DB  # Blue
        )
        embed.set_footer(text="/resetchat • No memory")

    await interaction.response.send_message(embed=embed, ephemeral=True)

# === ADD TO TREE ON IMPORT ===
def setup(bot: commands.Bot):
    bot.tree.add_command(reset_chat)
