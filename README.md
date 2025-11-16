# Discord Bot

A Discord bot built using discord.py with support for slash commands and prefix commands.

Includes a status command that shows latency, uptime, and memory usage.

---

## Requirements

- Python 3.10 or newer
- A Discord bot token and application ID

Install packages:

    pip install -r requirements.txt

---

## Setup

Create a `.env` file:

    TOKEN=your_bot_token_here
    APP_ID=your_application_id_here
    GUILD_ID=your_guild_id_here

`GUILD_ID` makes slash commands update faster but is optional.

---

## Run

    python main.py

---

---

## License

MIT License
