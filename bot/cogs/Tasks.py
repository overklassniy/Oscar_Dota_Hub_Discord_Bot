import sys
from copy import copy
from itertools import cycle

import discord
from discord.ext import commands, tasks

sys.path.append("..")
from utils.basic import *
from utils.tasks_utils import *

status = cycle(copy(get_rule('STRINGS', 'STATUS')))


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Tasks cog loaded')

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(status)))

    @tasks.loop(seconds=55)
    async def clear_search_channels(self):
        search_channels = get_rule('CHANNELS_IDS', 'SEARCH')
        for channel in search_channels:
            await clear_channel(self, channel)

    @tasks.loop(seconds=55)
    async def auto_search(self):
        search_channels = get_rule('CHANNELS_IDS', 'SEARCH')
        for channel in search_channels:
            await send_search(self, channel)

    @tasks.loop(seconds=180)
    async def check_dagons(self):
        search_channels = get_rule('CHANNELS_IDS', 'SEARCH')
        for c in search_channels:
            channel = self.bot.get_channel(c)
            messagef = await channel.history(limit=1).flatten()
            message_id = messagef[0].id
            message = await channel.fetch_message(message_id)
            total_reactions = sum(reaction.count for reaction in message.reactions)
            if total_reactions >= 6:
                embed = discord.Embed(
                    title=f"{total_reactions} dagons!",
                    description=f'Channel: {channel.mention}\n' +
                                f'Time: `{get_now()}`',
                    color=0x1f8b4c
                )
                dagons_channel = self.bot.get_channel(get_rule('CHANNELS_IDS', 'DAGONS_NOTIFICATION'))
                await dagons_channel.send(message.jump_url, embed=embed)


def setup(bot):
    bot.add_cog(Tasks(bot))
