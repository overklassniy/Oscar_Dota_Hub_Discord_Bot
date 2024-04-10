import sys

import discord
from discord.ext import commands

sys.path.append("..")
from utils.basic import *
from utils.listeners_utils import *


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Listeners cog loaded')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        user = payload.member
        message_id = payload.message_id
        channels = get_rule('CHANNELS_IDS', 'SEARCH_CHANNELS')
        if get_rule('BOOLEANS', 'TESTING'):
            channels = get_rule('CHANNELS_IDS', 'TESTING_CHANNELS')
        if channel_id not in channels:
            return
        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            if str(reaction) != get_rule('STRINGS', 'DAGON_EMOJI'):
                date = get_now(need_date_only=True)
                time = get_now(need_date=False)
                if str(user) != 'overklassniy#0':
                    reaction_data = {
                        "username": str(user.global_name),
                        "user_id": user.id,
                        "emoji": str(reaction),
                        "date": date,
                        "time": time
                    }
                    write_deleted_reactions(channel.name, reaction_data)
                reactions_channel = self.bot.get_channel(get_rule('CHANNELS_IDS', 'REACTIONS_DELETED_LOG'))
                embedVar = discord.Embed(
                    title="Reaction deleted",
                    description=f'Channel: <#{channel_id}>\n' +
                                f'Channel ID: {channel_id}' +
                                f'User: `{str(user)}`\n' +
                                f'User ID: `{user.id}`\n' +
                                f'Reaction: `{str(reaction)}`\n' +
                                f'Date: `{date}`\n' +
                                f'Time: `{time}`',
                    color=0xcc0000
                )
                print(f'[{get_now()}] Sending deleted reaction data')
                await reactions_channel.send(embed=embedVar)
                print(f'[{get_now()}] Removed reaction {str(reaction)} from channel {str(channel)}')
                await reaction.remove(user)

    async def send_start_state(self):
        channel = self.bot.get_channel(get_rule('CHANNELS_IDS', 'STATE_CHANNEL_ID'))
        embed = discord.Embed(
            title="The bot is running",
            description=f'Date: {get_now(need_date_only=True)}' +
                        f'Time: `{get_now(need_date=False)}`',
            color=0x1f8b4c
        )
        print(f'[{get_now()}] Sending start state')
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[{get_now()}] Logged in as {self.bot.user.name}')
        if get_rule('BOOLEANS', 'SEND_START_STATE'):
            await send_start_state()


def setup(bot):
    bot.add_cog(Listeners(bot))
