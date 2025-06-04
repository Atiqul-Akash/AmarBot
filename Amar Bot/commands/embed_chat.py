import os
import json
import asyncio
import textwrap
from discord import app_commands, Interaction, Embed
from discord.ext import commands
from llama_setup import llm

MAX_TOKENS = 2000
MAX_WORDS = 1000  # New limit on words
MAX_CONTEXT_TURNS = 20
MAX_DISCORD_MESSAGE_LEN = 2000
EMBED_MAX_DESC_LEN = 1900  # Safe max embed description length
MEMORY_DIR = "chat_memory"

os.makedirs(MEMORY_DIR, exist_ok=True)

def load_user_memory(user_id):
    path = os.path.join(MEMORY_DIR, f"user_{user_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_user_memory(user_id, history):
    path = os.path.join(MEMORY_DIR, f"user_{user_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def build_prompt(history, user_input):
    prompt = ""
    for message in history[-MAX_CONTEXT_TURNS:]:
        prompt += f"User: {message['user']}\nAI: {message['ai']}\n"
    prompt += f"User: {user_input}\nAI:"
    return prompt

@app_commands.command(name="embedchat", description="Chat with your personal AI assistant")
@app_commands.describe(message="Your message to the AI")
async def embed_chat(interaction: Interaction, message: str):
    await interaction.response.defer()
    user_id = interaction.user.id
    history = load_user_memory(user_id)

    prompt = build_prompt(history, message)

    try:
        # Run LLM in background thread
        response = await asyncio.to_thread(llm, prompt, max_tokens=MAX_TOKENS, stop=["User:", "\nAI:"])
        ai_reply = response["choices"][0]["text"].strip()
    except Exception as e:
        await interaction.followup.send(f"**Error generating AI response:** {str(e)}")
        return

    # Limit to max 1000 words
    words = ai_reply.split()
    if len(words) > MAX_WORDS:
        ai_reply = " ".join(words[:MAX_WORDS]) + "..."

    # Save to memory
    history.append({"user": message, "ai": ai_reply})
    save_user_memory(user_id, history)

    # Split into chunks for embed descriptions
    chunks = textwrap.wrap(ai_reply, width=EMBED_MAX_DESC_LEN)

    for i, chunk in enumerate(chunks):
        embed = Embed(
            title="🤖 AI Assistant",
            description=chunk,
            color=0x1ABC9C
        )
        footer_text = f"Page {i+1}/{len(chunks)} • Response from /chat"
        embed.set_footer(text=footer_text)

        await interaction.followup.send(embed=embed)

# === ADD TO TREE ON IMPORT ===
def setup(bot: commands.Bot):
    bot.tree.add_command(embed_chat)
