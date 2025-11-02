"""
This script initializes and starts a Discord bot using discord.py
(with application commands support).
It loads environment variables, sets up intents,
and logs all received messages to the console.
Environment Variables Required:
- TOKEN: The bot token from Discord Developer Portal.
- APP_ID: The application ID of the bot.
- GUILD_ID: ID of a guild to scope slash command sync.

The main extension loaded:
- plugins.status.main   (must exist in the project structure)
Libraries Used:
- discord.py (commands extension + app commands)
- python-dotenv for loading .env
"""

import time
from discord.ext import commands
from discord.message import Message
from discord import Intents, Object
from dotenv import load_dotenv
from os import environ
import asyncio

# Load environment variables from .env file
load_dotenv()

# Enable message content intent (required for bots to read messages)
intents = Intents.default()
intents.message_content = True


class Bot(commands.Bot):
    """
    Custom Bot class extending discord.ext.commands.Bot.
    Adds:
    - launch_time tracking
    - custom logging of every received message
    - automatic on_ready sync of slash commands to a specific guild
    """
    
    launch_time: float = time.time()  # Timestamp when bot starts

    async def on_message(self, message: Message) -> None:
        """
        Triggered for every message the bot can see.
        Logs the author and content to the terminal.
        Ensures command processing by calling super().
        """
        print(f"{message.author}: {message.content}")
        # self.user check to make typechecker happy
        if self.user and message.author.id == self.user.id:
            return
        await super().on_message(message)

    async def on_ready(self) -> None:
        """
        Called once the bot is fully logged into Discord.
        Attempts to sync slash commands to a specific guild.
        """
        print(f"Logged in as {self.user}")

        guild_id = environ.get("GUILD_ID")
        if guild_id:
            await self.tree.sync(guild=Object(guild_id))
            print("Slash command tree synced to specific guild")


async def main():
    """
    Creates the bot instance, loads an extension, and starts the bot.
    Uses asyncio.run() when script is run directly.
    """
    app_id = environ.get("APP_ID")
    if not app_id:
        raise ValueError("Missing APP_ID environment variable")

    bot = Bot(
        intents=intents,
        command_prefix="!",
        application_id=int(app_id)
    )

    token = environ.get("TOKEN")
    if not token:
        raise ValueError("Missing TOKEN environment variable")

    # Load status plugin (must exist in project)
    await bot.load_extension("plugins.status.main")
    print("Loaded extension: plugins.status.main")

    # Start the bot session
    await bot.start(token=token)


if __name__ == "__main__":
    # Execute the main bot function asynchronously
    asyncio.run(main())
