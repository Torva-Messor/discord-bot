from discord import Embed, Interaction
from main import Bot
from discord.ext import commands
from discord import app_commands
class Dev(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.hybrid_command(
        name = 'sync',
        guild_only=True
    )
    async def sync(self, ctx: commands.Context[Bot]): 
        "Syncs the bot's command tree in the current guild"
        message = await ctx.reply(f"Syncingcommands to this guild...")

        if ctx.guild is None:
            await ctx.send("This command must be used in a server.")
            return
        
        await ctx.defer()
        self.bot.tree.copy_global_to(guild=ctx.guild)
        spec = await self.bot.tree.sync(guild = ctx.guild)
        if message:
            await message.edit(content=f"Synced {len(spec)} commands to this guild.")
        else:
            await ctx.reply(f"Synced {len(spec)} commands to this guild.")

    @commands.hybrid_group(name='plugin')
    async def plugin(self, ctx: commands.Context[Bot]):
        if ctx.invoked_subcommand is None:
            pass

    @plugin.command('list')
    async def plugins_list(self, ctx: commands.Context[Bot]):
        embed = Embed(title="Plugin List")
        for index, key in enumerate(self.bot.extensions.keys()):
            plugin_name = key.split('.')[-2]
            embed.add_field(name=str(index + 1), value=plugin_name, inline=index % 3 == 0 if False else True)
        await ctx.reply(embeds=[embed])

    async def plugin_autocomplete(self, interaction: Interaction, current: str):
        choices = []
        for key in self.bot.extensions.keys():
            display_name = key.split('.')[-2] 
            if current.lower() in display_name.lower():
                choices.append(app_commands.Choice(name=display_name, value=key))
        
        # Return only the first 25 [Discord limit]
        return choices[:25]

    @plugin.command('reload')
    @app_commands.autocomplete(plugin=plugin_autocomplete)
    async def plugin_reload(self, ctx: commands.Context[Bot], plugin: str):
        try:
            await self.bot.reload_extension(plugin)
            await ctx.reply(f'Plugin `{plugin}` reloaded')
        except Exception as e:
            await ctx.reply(str(e))

async def setup(bot: Bot):
    """
    Required async setup function to load the Dev cog when the extension is initialized.
    """
    await bot.add_cog(Dev(bot))
