# Discord Bot

A Discord bot built using discord.py with support for slash commands and prefix commands.

Includes a status command that shows latency, uptime, and memory usage.

---

## Requirements
- uv package manager
- A Discord bot token
- App ID(BOT ID)
- GUILD ID
## Optional features
- google api key
Install packages:

    uv sync

---

## Setup

Create a `.env` file:

    TOKEN=your_bot_token_here
    APP_ID=your_application_id_here
    GUILD_ID=your_guild_id_here
    YOUTUBE_API_KEY="YOUR_GOOGLE_API_KEY_HERE
    DISCORD_MOD_ROLE_ID= role ID of moderators role
    DISCORD_ADMIN_ROLE_ID= role ID that has permission to add moderators
    MOD_DB_FILE="mod_database.json

---

## Run

    uv run main.py

---

---

## License

MIT License
