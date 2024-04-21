import os
import sys

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append('../')  # Ensure the utils module can be found by adjusting the system path.
from utils.basic import *  # Import all utilities from basic.py, usually functions or constants.

# Retrieve the first two administration roles from the configuration or database.
administration_roles = get_rule('ROLES_IDS', 'ADMINISTRATION')[:2]


class Cogs(commands.Cog):
    def __init__(self, bot):
        print(f'[{get_now()}] Cogs cog loaded')  # Log when the Cogs.md cog is fully loaded.
        self.bot = bot  # Store the bot instance within the class for further use.

    # Create a group for slash commands related to cog management.
    cogs_commands_group = SlashCommandGroup("cogs", "Cogs.md Management Commands")

    # Slash command to load a specific cog.
    @cogs_commands_group.command(name="load", description="Load a specific cog")
    @commands.has_any_role(*administration_roles)  # Restrict command to users with administration roles.
    @option(name="extension", description="Cog extension to load", required=True)
    async def load(self, ctx: discord.ApplicationContext, extension: str):
        extension = extension.lower().capitalize()  # Format the extension name properly.
        print(f'[{get_now()}] Loaded {extension}')  # Log the loading action.
        self.bot.load_extension(f'cogs.{extension}')  # Load the specified extension.
        await ctx.respond(f"Loaded {extension}", ephemeral=True)  # Respond to the user privately.

    # Slash command to unload a specific cog.
    @cogs_commands_group.command(name="unload", description="Unload a specific cog")
    @commands.has_any_role(*administration_roles)
    @option(name="extension", description="Cog extension to unload", required=True)
    async def unload(self, ctx: discord.ApplicationContext, extension: str):
        extension = extension.lower().capitalize()
        print(f'[{get_now()}] Unloaded {extension}')
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.respond(f"Unloaded {extension}", ephemeral=True)

    # Slash command to reload a specific cog.
    @cogs_commands_group.command(name="reload", description="Reload a specific cog")
    @commands.has_any_role(*administration_roles)
    @option(name="extension", description="Cog extension to reload", required=True)
    async def reload(self, ctx: discord.ApplicationContext, extension: str):
        extension = extension.lower().capitalize()
        try:
            self.bot.reload_extension(f'cogs.{extension}')
            print(f'[{get_now()}] Reloaded {extension}')
            await ctx.respond(f"Reloaded {extension}", ephemeral=True)
        except Exception as e:
            print(f"[{get_now()}] Failed to reload {extension}. {e}")
            await ctx.respond(f"Failed to reload {extension}. {e}", ephemeral=True)

    # Slash command to reload all cogs.
    @cogs_commands_group.command(name="reload_all", description="Reload all cogs")
    @commands.has_any_role(*administration_roles)
    async def reload_all(self, ctx: discord.ApplicationContext):
        print(f'[{get_now()}] Reloading all cogs...')
        for file in os.listdir(get_rule('PATHS', 'COGS')):
            if file.endswith(".py") and file != "__init__.py":
                self.bot.reload_extension(f'cogs.{file[:-3]}')
                await ctx.respond(f"Reloaded {file[:-3]}", ephemeral=True)


# Register this cog with the bot.
def setup(bot):
    bot.add_cog(Cogs(bot))
