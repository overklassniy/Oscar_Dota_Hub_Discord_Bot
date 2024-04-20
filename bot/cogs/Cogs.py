import os
import sys

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append('../')
from utils.basic import *


class Cogs(commands.Cog):
    def __init__(self, bot):
        print(f'[{get_now()}] Cogs cog loaded')
        self.bot = bot

    cogs_commands_group = SlashCommandGroup("cogs", "Cogs Management Commands")

    @cogs_commands_group.command(name="load")
    @option(name="extension", description="Cog extension to load", required=True)
    async def load(self, ctx: discord.ApplicationContext, extension: str):
        extension = extension.lower().capitalize()
        print(f'[{get_now()}] Loaded {extension}')
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.respond(f"Loaded {extension}", ephemeral=True)

    @cogs_commands_group.command(name="unload")
    @option(name="extension", description="Cog extension to load", required=True)
    async def unload(self, ctx: discord.ApplicationContext, extension: str):
        extension = extension.lower().capitalize()
        print(f'[{get_now()}] Unloaded {extension}')
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.respond(f"Unloaded {extension}", ephemeral=True)

    @cogs_commands_group.command(name="reload")
    @option(name="extension", description="Cog extension to load", required=True)
    async def reload(self, ctx: discord.ApplicationContext, extension: str):
        extension = extension.lower().capitalize()
        try:
            self.bot.reload_extension(f'cogs.{extension}')
            print(f'[{get_now()}] Reloaded {extension}')
            await ctx.respond(f"Reloaded {extension}", ephemeral=True)
        except Exception as e:
            print(f"[{get_now()}] Failed to reload {extension}. {e}")
            await ctx.respond(f"Failed to reload {extension}. {e}", ephemeral=True)

    @cogs_commands_group.command(name="reload_all")
    async def reload_all(self, ctx: discord.ApplicationContext):
        print(f'[{get_now()}] Reloading all cogs...')
        for file in os.listdir("bot/cogs"):
            if file.endswith(".py") and file != "__init__.py":
                self.bot.reload_extension(f'cogs.{file[:-3]}')
                await ctx.respond(f"Reloaded {file[:-3]}", ephemeral=True)


def setup(bot):
    bot.add_cog(Cogs(bot))
