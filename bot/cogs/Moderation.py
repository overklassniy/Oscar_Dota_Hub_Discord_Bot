import sys

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append("..")  # Modify the system path to include the parent directory for module access.
from utils.basic import *  # Import utilities from basic.py which includes functions like get_rule().

administration_roles = get_rule('ROLES_IDS', 'ADMINISTRATION')


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store an instance of the bot.
        print(f'[{get_now()}] Moderation cog loaded')  # Log the initialization of the Fun cog.

    # Group of slash commands under the 'moderation' category.
    moderation_commands_group = SlashCommandGroup("moderation", "Moderation commands", guild_only=True)

    @moderation_commands_group.command(name='blacklist_url_add', description="Add URL to URLS blacklist.")
    @commands.has_any_role(*administration_roles)
    @option(name="url", description="URL to add into blacklist", required=True)
    async def blacklist_url_add(self, ctx: discord.ApplicationContext, url: str):
        blacklist_urls = get_rule('STRINGS', 'BLACKLIST_URLS')
        blacklist_urls.append(url)
        write_rule('STRINGS', 'BLACKLIST_URLS', blacklist_urls)
        await ctx.respond(f'"{url}" added to URLs blacklist', ephemeral=True)
        print(f'{get_now()} {ctx.author.id} ({ctx.author.name}) added "{url}" to URLs blacklist')


# Function to add this cog to the bot.
def setup(bot):
    bot.add_cog(Moderation(bot))
