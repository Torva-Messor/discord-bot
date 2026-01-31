from discord import ButtonStyle, Interaction
import discord.ui as ui
from pathlib import Path

from main import Bot
from plugin_loader import Plugin, find_plugins

class PluginSection(ui.Section):
    def __init__(self, bot: Bot, plugin: Plugin) -> None:
        self.bot = bot
        self.plugin = plugin
        plugin_name = plugin.module_path.split('.')[-2]

        reload_btn = ui.Button(label="Reload", style=ButtonStyle.gray)
        
        reload_btn.callback = self.reload_callback

        super().__init__(
            ui.TextDisplay(plugin_name), 
            accessory=reload_btn
        )

    async def reload_callback(self, interaction: Interaction):
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
            *[PluginSection(bot=self.bot, plugin=plugin) for plugin in plugins],
            ui.Separator(),

            ui.TextDisplay(f"-# count: {len(plugins)}")
        )
        
        
        self.add_item(self.container)

    