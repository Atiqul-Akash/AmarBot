import os
import json
from discord import app_commands, Interaction, Embed
from discord.ext import commands
from discord.ui import View, Button
from discord import ButtonStyle


PERSONALITY_DIR = "personality"
PERSONALITY_FILE = os.path.join(PERSONALITY_DIR, "personality.json")

os.makedirs(PERSONALITY_DIR, exist_ok=True)

def load_personality():
    if os.path.exists(PERSONALITY_FILE):
        with open(PERSONALITY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_personality(data):
    with open(PERSONALITY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Custom Button subclass with callback
class PersonalityButton(Button):
    def __init__(self, style_key, label, user_id):
        super().__init__(label=label, style=ButtonStyle.primary, custom_id=style_key)
        self.user_id = user_id
        self.style_key = style_key

    async def callback(self, interaction: Interaction):
        data = load_personality()
        data[str(self.user_id)] = self.style_key
        save_personality(data)

        embed = Embed(
            title="🧠 Personality Changed!",
            description=f"Your AI will now respond in **{self.label}** style.",
            color=0x00BFFF
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# View containing all personality buttons
class PersonalityView(View):
    def __init__(self, user_id):
        super().__init__(timeout=120)
        self.user_id = user_id

        personalities = {
            "friendly": "Friendly 😊",
            "formal": "Formal 🧐",
            "sarcastic": "Sarcastic 😏",
            "motivational": "Motivational 💪",
            "technical": "Technical 🧠",
            "default": "Default Normal"
        }

        for key, label in personalities.items():
            self.add_item(PersonalityButton(key, label, user_id))

@app_commands.command(name="personality", description="View and set your AI's personality style")
async def personality(interaction: Interaction):
    user_id = str(interaction.user.id)
    data = load_personality()
    current = data.get(user_id, "default")

    personalities = {
        "friendly": "Friendly 😊",
        "formal": "Formal 🧐",
        "sarcastic": "Sarcastic 😏",
        "motivational": "Motivational 💪",
        "technical": "Technical 🧠",
        "default": "Default Normal"
    }

    current_name = personalities.get(current, "Default Normal")

    embed = Embed(
        title="🧠 Your Current AI Personality",
        description=f"**{current_name}**",
        color=0x00BFFF
    )
    await interaction.response.send_message(embed=embed, view=PersonalityView(interaction.user.id), ephemeral=True)

def setup(bot: commands.Bot):
    bot.tree.add_command(personality)
