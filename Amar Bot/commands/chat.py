import os
import json
import asyncio
import textwrap
from discord import app_commands, Interaction
from discord.ext import commands
from llama_setup import llm
from .personality import load_personality


MAX_TOKENS = 2000
MAX_WORDS = 1000
MAX_CONTEXT_TURNS = 20
MAX_DISCORD_MESSAGE_LEN = 2000

CHAT_MEMORY_DIR = "chat_memory"
MEMORY_STATUS_DIR = "memory_status"
PERSONALITY_DIR = "personality"

# Ensure folders exist
os.makedirs(CHAT_MEMORY_DIR, exist_ok=True)
os.makedirs(MEMORY_STATUS_DIR, exist_ok=True)
os.makedirs(PERSONALITY_DIR, exist_ok=True)

# Paths for files in the new folders
TOGGLE_FILE = os.path.join(MEMORY_STATUS_DIR, "memory_status.json")

def load_user_memory(user_id):
    path = os.path.join(CHAT_MEMORY_DIR, f"user_{user_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_user_memory(user_id, history):
    path = os.path.join(CHAT_MEMORY_DIR, f"user_{user_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def load_memory_toggle(user_id):
    if not os.path.exists(TOGGLE_FILE):
        return True
    with open(TOGGLE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(user_id), True)

def save_memory_toggle(user_id, status):
    # optional, if you have a function to save memory toggle
    if os.path.exists(TOGGLE_FILE):
        with open(TOGGLE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    data[str(user_id)] = status
    with open(TOGGLE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def build_prompt(history, user_input, memory_enabled):
    if not memory_enabled or not history:
        return f"User: {user_input}\nAI:"
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

    # Load memory toggle
    memory_enabled = load_memory_toggle(user_id)
    history = load_user_memory(user_id) if memory_enabled else []

    # Build prompt + personality
    personality_data = load_personality()
    personality = personality_data.get(str(user_id), "default")
    style_instructions = {
        "friendly": "Respond in a friendly and casual tone.",
        "formal": "Respond formally, like a professional assistant.",
        "sarcastic": "Respond with a sarcastic tone.",
        "motivational": "Respond in a motivating and uplifting style.",
        "technical": "Respond with precise, technical explanations.",
        "default": "Respond normally."
    }
    style = style_instructions.get(personality, style_instructions["default"])
    prompt = f"{style}\n\n" + build_prompt(history, message, memory_enabled)


    try:
        response = await asyncio.to_thread(llm, prompt, max_tokens=MAX_TOKENS, stop=["User:", "\nAI:"])
        ai_reply = response["choices"][0]["text"].strip()
    except Exception as e:
        await interaction.followup.send(f"**Error generating AI response:** {str(e)}")
        return

    # Trim long replies
    words = ai_reply.split()
    if len(words) > MAX_WORDS:
        ai_reply = " ".join(words[:MAX_WORDS]) + "..."

    # Save memory only if enabled
    if memory_enabled:
        history.append({"user": message, "ai": ai_reply})
        save_user_memory(user_id, history)

    # Send in chunks
    prefix_len = len("**AI (continued):** ")
    max_chunk_len = MAX_DISCORD_MESSAGE_LEN - prefix_len
    chunks = textwrap.wrap(ai_reply, width=max_chunk_len)

    for i, chunk in enumerate(chunks):
        prefix = "**AI (continued):** " if i > 0 else "**AI:** "
        safe_chunk = chunk[:MAX_DISCORD_MESSAGE_LEN - len(prefix)]
        await interaction.followup.send(f"{prefix}{safe_chunk}")

    print(f"Sending chunk {i + 1}/{len(chunks)} (length={len(chunk)})")

def setup(bot: commands.Bot):
    bot.tree.add_command(chat)
