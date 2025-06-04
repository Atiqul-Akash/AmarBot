# 🤖 AmarBot

**AmarBot** is a modern, multipurpose Discord bot that brings AI-powered conversation, moderation tools, utility features, and more — all in one sleek package.

---

## ✨ Features

- 💬 **AI Chat Assistant** — Chat with an intelligent LLM-powered assistant using `/chat`
- 🧠 **Memory & Summarization** — Personalized conversation memory with `/summary`
- 🧹 **Chat Reset** — Reset your chat history with `/resetchat`
- 📶 **Ping Utility** — Check real-time latency using `/ping`
- 🛠️ **Modular Design** — Easy to extend with new commands and features
- 🎮 **Fun & Games** — Coming soon!

---

## 📁 Project Structure
AmarBot/
│
├── bot.py # Main bot launcher
├── llama_setup.py # LLM setup logic
│
├── commands/ # Slash command modules
│ ├── init.py # Loads all command modules
│ ├── chat.py # /chat command with memory
│ ├── ping.py # /ping command
│ ├── reset_chat.py # /resetchat command
│ └── summary.py # /summary command
│
├── chat_memory/ # Stores user memory in JSON files
│
├── .env (optional) # For storing secrets like bot token
├── requirements.txt # Python dependencies
└── README.md # This file

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AmarBot.git
cd AmarBot
```
###2. Install dependencies
```bash
 pip install -r requirements.txt
```
###3. Set your bot token
Option 1 (unsafe):
Edit bot.py and paste your token directly.

Option 2 (recommended):
Create a .env file or set an environment variable:

```bash
DISCORD_BOT_TOKEN=your_token_here
```
Then load it in bot.py:
```bash
import os
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
```
###4. Run the bot
```bash
python bot.py
```

🧠 Powered By
llama-cpp-python — Local LLM backend

Discord.py v2 (Slash Commands)

Python 3.10+


🛠️ Roadmap
 AI Chat via /chat

 Latency check via /ping

 Reset user chat memory via /resetchat

 Conversation summarization via /summary

 Moderation commands (ban, kick, etc.)

 Fun mini-games

 Web dashboard (future)

 Multi-language support

🤝 Contributing
Contributions are welcome! Feel free to fork the project and submit a pull request. For major changes, please open an issue first.

📄 License
This project is licensed under the MIT License — do what you want with it, just give credit.

🌐 Creator
Made with ❤️ by Atiqul Islam Akash
📍 Bangladesh
GitHub: @Atiqul-Akash

