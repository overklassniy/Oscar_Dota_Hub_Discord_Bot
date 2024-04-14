import sys
from random import choice

from discord import SlashCommandGroup, option
from discord.ext import commands
from discord.utils import get

sys.path.append("..")
from utils.basic import *
from utils.search_utils import *


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Search cog loaded')

    search_commands_group = SlashCommandGroup("search", "Search related commands")

    @search_commands_group.command(name="search")
    @option("image")
    async def search(self, ctx, image=0):
        guild = ctx.guild
        channel = ctx.channel
        if channel.id not in get_rule("CHANNELS_IDS", 'SEARCH_CHANNELS'):
            await ctx.respond('Please, select a channel in #Search category', ephemeral=True)
            print(f'[{get_now()}] Wrong channel ID for /search: {channel.id} ({channel.name})')
            return
        search_channels_roles = get_rule('ROLES', 'SEARCH_CHANNELS_ROLES')
        role_id = search_channels_roles[str(channel.id)]
        role = get(guild.roles, id=role_id)
        search_images = get_rule('IMAGES', 'SEARCH')
        image_url = search_images[image - 1] if image else choice(search_images)
        message = await generate_search_message(image_url=image_url, role=role)
        await ctx.send(**message)
        await ctx.respond('Done', ephemeral=True)
        print(f'[{get_now()}] Search message sent to {ctx.channel.name}')


def setup(bot):
    bot.add_cog(Search(bot))
