import sys

import discord
from discord import SlashCommandGroup
from discord.ext import commands

sys.path.append("..")  # Modify the system path to include the parent directory for module access.
from utils.basic import *  # Import utilities from basic.py which includes functions like get_rule().


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store an instance of the bot.
        print(f'[{get_now()}] Help cog loaded')  # Log the initialization of the Fun cog.

    # Group of slash commands under the 'help' category.
    help_commands_group = SlashCommandGroup("help", "Help commands")

    @help_commands_group.command(name='about', description="Get information about the bot.")
    async def about(self, ctx: discord.ApplicationContext):
        await ctx.respond(content='Sorry, "help" module is not implemented yet.', ephemeral=True)
        print(f'[{get_now()}] "/help about" used by {ctx.author.display_name} ({ctx.author.id}) in {ctx.channel.name} ({ctx.channel.id})')


# Function to add this cog to the bot.
def setup(bot):
    bot.add_cog(Help(bot))
