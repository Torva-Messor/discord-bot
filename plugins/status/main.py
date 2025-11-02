"""
Provides a hybrid (slash + prefix) command to display the bot's current status,
including latency, uptime, and memory usage.

Dependencies:
- psutil for memory usage statistics
- main.Bot to access launch_time attribute
"""

import time
from datetime import datetime, timedelta, UTC
import psutil
import os

from discord import Embed, Color
from discord.ext import commands
from main import Bot


class Status(commands.Cog):
    """
    A commands.Cog module that adds a bot status command.
    Displays latency, uptime, and memory usage in an embed.
    """

    def __init__(self, bot: Bot):
        """
        Stores a reference to the bot instance.

        Parameters:
        - bot (Bot): The main bot instance from main.py
        """
        self.bot = bot

    @commands.hybrid_command(
        name="status",
        description="Displays the bot's current runtime and performance details.",
        help="Displays uptime, ping, and memory usage."
    )
    async def status(self, ctx: commands.Context[commands.Bot]):
        """
        Sends an embed to the channel with bot performance metrics.
        Uses hybrid_command so it works as both a slash and prefix command.

        Parameters:
        - ctx: Command invocation context with author and channel information
        """
        # Calculate uptime since the bot launch time stored in main.Bot
        uptime_seconds = int(time.time() - self.bot.launch_time)
        uptime_str = str(timedelta(seconds=uptime_seconds))

        # Process memory usage in megabytes
        memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

        # Build the embed response
        embed = Embed(
            title="Bot Status",
            color=Color.blurple(),
            timestamp=datetime.now(UTC)
        )

        # Bot latency converted to milliseconds
        embed.add_field(name="Ping", value=f"{self.bot.latency * 1000:.0f} ms")
        embed.add_field(name="Uptime", value=uptime_str)
        embed.add_field(name="Memory Usage", value=f"{memory_usage:.1f} MB")

        embed.set_footer(text=f"Requested by {ctx.author.display_name}")

        await ctx.send(embed=embed)


async def setup(bot: Bot):
    """
    Required async setup function to load the Status cog when the extension is initialized.
    """
    await bot.add_cog(Status(bot))
