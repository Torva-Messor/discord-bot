import asyncio
from typing import Any
from discord import ButtonStyle, Emoji, Interaction, PartialEmoji
import discord.ui as ui
from pathlib import Path

from main import Bot
from plugin_loader import Plugin, find_plugins

class PluginButton(ui.Button):
    def __init__(self, bot: Bot, plugin: Plugin, *,custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None):
        self.bot = bot
        self.plugin = plugin
        super().__init__(style=ButtonStyle.gray, label="Reload", disabled=False, custom_id=custom_id, url=url, emoji=emoji, row=row)
    async def callback(self, interaction: Interaction) -> Any:
        # Defer interaction to prevent timeout
        await interaction.response.defer(ephemeral=True)
        
        try:

            await self.bot.reload_extension(self.plugin.module_path)
            
            self.style = ButtonStyle.green
            self.disabled = True

            if self.view and interaction.message:
                await interaction.message.edit(view=self.view)
            
    
            await asyncio.sleep(2.0)
            
            self.style = ButtonStyle.gray
            self.disabled = False
        except Exception as e:
            # ERROR: Change to Red/"Error"
            self.style = ButtonStyle.red
            self.disabled = True
            await interaction.followup.send(
                content=f"❌ Error reloading `{self.plugin.module_path}`:\n```py\n{e}\n```",
                ephemeral=True
            )    
        # State Reset        
        self.emoji = None
        self.disabled = False
        if self.view and interaction and interaction.message:
            await interaction.message.edit(view=self.view)
    
class PluginSection(ui.Section):
    def __init__(self, bot: Bot, plugin: Plugin, id: int) -> None:
        self.bot = bot
        self.id = id
        self.plugin = plugin
        plugin_name = plugin.module_path.split('.')[-2]

        reload_btn = PluginButton(self.bot, self.plugin, custom_id=f"reload-{self.id}")

        super().__init__(
            ui.TextDisplay(plugin_name), 
            accessory=reload_btn
        )

    async def reload_callback(self, interaction: Interaction, button: ui.Button):
        try:
            await interaction.response.send_message(
                f"Reloading plugin: {self.plugin.module_path}...", 
                ephemeral=True
            )
            
            
            await self.bot.reload_extension(self.plugin.module_path)
            
            await interaction.followup.send(
                content=f"Plugin `{self.plugin.module_path}` reloaded", 
                ephemeral=True
            )
        
        except Exception as e: 
            await interaction.followup.send(str(e))

class PluginView(ui.LayoutView):
    def __init__(self, bot: Bot, *, timeout: float | None = 60.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        plugins = find_plugins(base_dir=Path('plugins').absolute().resolve())
        
        self.container = ui.Container(
            ui.TextDisplay("### Plugins"),
            ui.Separator(),
            *[PluginSection(bot=self.bot, plugin=plugin, id=id) for id,plugin in enumerate(plugins)],
            ui.Separator(),

            ui.TextDisplay(f"-# count: {len(plugins)}")
        )
        
        
        self.add_item(self.container)

    