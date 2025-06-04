import os
import json
from discord import app_commands, Interaction, Embed
from discord.ext import commands
from llama_setup import llm

MEMORY_DIR = "chat_memory"
MAX_TOKENS = 1000

def load_user_memory(user_id):
    path = os.path.join(MEMORY_DIR, f"user_{user_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def build_summary_prompt(history):
    if not history:
        return "There is no conversation history to summarize."

    full_convo = ""
    for entry in history[-20:]:
        full_convo += f"User: {entry['user']}\nAI: {entry['ai']}\n"

    prompt = (
        f"Here is a conversation between a user and an AI assistant:\n\n"
        f"{full_convo}\n\n"
        "Summarize this conversation in a short paragraph:"
    )
    return prompt

@app_commands.command(name="summary", description="Summarize your past conversation with the AI")
async def summary(interaction: Interaction):
    await interaction.response.defer()
    user_id = interaction.user.id
    history = load_user_memory(user_id)

    if not history:
        embed = Embed(
            title="❗ No Chat History",
            description="You don't have any conversation history to summarize.",
            color=0xE74C3C  # Red
        )
        embed.set_footer(text="/summary • No data")
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    prompt = build_summary_prompt(history)
    response = llm(prompt, max_tokens=MAX_TOKENS, stop=["User:", "\nAI:"])
    summary_text = response["choices"][0]["text"].strip()

    if not summary_text:
        summary_text = "⚠️ Sorry, I couldn't generate a summary this time."

    embed = Embed(
        title="📋 Conversation Summary",
        description=summary_text,
        color=0x3498DB  # Blue
    )
    embed.set_footer(text="/summary • AI-generated")
    await interaction.followup.send(embed=embed)

def setup(bot: commands.Bot):
    bot.tree.add_command(summary)
