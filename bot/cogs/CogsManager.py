import os
import sys

import discord
from discord import SlashCommandGroup
from discord.ext import commands

sys.path.append('../')
from utils.basic import *


class CogsManager(commands.Cog):
    def __init__(self, bot):
        print(f'[{get_now()}] CogsManager cog loaded')
        self.bot = bot

    CogsManager_command_group = SlashCommandGroup("cogsmanagament", "Cogs Management Commands")

    @CogsManager_command_group.command(name="load")
    async def load(self, ctx: discord.ApplicationContext, extension: str):
        print(f'[{get_now()}] Loaded {extension}')
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.respond(f"Loaded {extension}", ephemeral=True)

    @CogsManager_command_group.command(name="unload")
    async def unload(self, ctx: discord.ApplicationContext, extension: str):
        print(f'[{get_now()}] Unloaded {extension}')
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.respond(f"Unloaded {extension}", ephemeral=True)

    @CogsManager_command_group.command(name="reload")
    async def reload(self, ctx: discord.ApplicationContext, extension: str):
        try:
            self.bot.reload_extension(f'cogs.{extension}')
            print(f'[{get_now()}] Reloaded {extension}')
            await ctx.respond(f"Reloaded {extension}", ephemeral=True)
        except Exception as e:
            await ctx.respond(f"Failed to reload {extension}. {e}", ephemeral=True)

    @CogsManager_command_group.command(name="reload_all")
    async def reload_all(self, ctx: discord.ApplicationContext):
        print(f'[{get_now()}] Reloading all cogs...')
        for file in os.listdir("bot/cogs"):
            if file.endswith(".py") and file != "__init__.py.py":
                self.bot.reload_extension(f'cogs.{file[:-3]}')
                await ctx.respond(f"Reloaded {file[:-3]}", ephemeral=True)


def setup(bot):
    bot.add_cog(CogsManager(bot))
