import os
import json
import asyncio
import textwrap
from discord import app_commands, Interaction
from discord.ext import commands
from llama_setup import llm

MAX_TOKENS = 2000
MAX_WORDS = 1000  # New limit on words
MAX_CONTEXT_TURNS = 20
MAX_DISCORD_MESSAGE_LEN = 2000
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

@app_commands.command(name="chat", description="Chat with your personal AI assistant")
@app_commands.describe(message="Your message to the AI")
async def chat(interaction: Interaction, message: str):
    await interaction.response.defer()
    user_id = interaction.user.id
    history = load_user_memory(user_id)

    prompt = build_prompt(history, message)

    try:
        # Run LLM in a background thread to avoid blocking
        response = await asyncio.to_thread(llm, prompt, max_tokens=MAX_TOKENS, stop=["User:", "\nAI:"])
        ai_reply = response["choices"][0]["text"].strip()
    except Exception as e:
        await interaction.followup.send(f"**Error generating AI response:** {str(e)}")
        return

    # Trim to max 1000 words
    words = ai_reply.split()
    if len(words) > MAX_WORDS:
        ai_reply = " ".join(words[:MAX_WORDS]) + "..."

    # Save to memory
    history.append({"user": message, "ai": ai_reply})
    save_user_memory(user_id, history)

    # Split into safe chunks
    prefix_len = len("**AI (continued):** ")
    max_chunk_len = MAX_DISCORD_MESSAGE_LEN - prefix_len
    chunks = textwrap.wrap(ai_reply, width=max_chunk_len)

    for i, chunk in enumerate(chunks):
        prefix = "**AI (continued):** " if i > 0 else "**AI:** "
        safe_chunk = chunk[:MAX_DISCORD_MESSAGE_LEN - len(prefix)]
        await interaction.followup.send(f"{prefix}{safe_chunk}")

    print(f"Sending chunk {i + 1}/{len(chunks)} (length={len(chunk)})")


# === ADD TO TREE ON IMPORT ===
def setup(bot: commands.Bot):
    bot.tree.add_command(chat)
