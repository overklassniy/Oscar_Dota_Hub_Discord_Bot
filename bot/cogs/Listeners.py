import sys

import discord
from discord.ext import commands

sys.path.append("..")
from cogs.Tasks import *
from utils.basic import *
from utils.listeners_utils import *

testing = get_rule('BOOLEANS', 'TESTING')


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Listeners cog loaded')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        user = payload.member
        message_id = payload.message_id
        channels = get_rule('CHANNELS_IDS', 'SEARCH')
        if get_rule('BOOLEANS', 'TESTING'):
            channels = get_rule('CHANNELS_IDS', 'TEST')
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
                                f'Channel ID: {channel_id}\n' +
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        channel_id = message.channel.id
        if not channel_id:
            return
        commands_only_channels = get_rule('CHANNELS_IDS', 'COMMANDS_ONLY_CHANNELS')
        if channel_id in commands_only_channels and not testing:
            if message.type != discord.MessageType.application_command:
                print(f'[{get_now()}] Deleted message "{str(message.content)}" from channel {str(message.channel.name)}')
                await message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[{get_now()}] Logged in as {self.bot.user.name}')

        Tasks.change_status.start(self)
        Tasks.auto_search.start(self)
        Tasks.check_dagons.start(self)

        if not testing and get_rule('BOOLEANS', 'SEND_START_STATE'):
            await send_start_state()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ApplicationContext, error):
        if not testing and get_rule('BOOLEANS', 'SEND_ERRORS'):
            await handle_error(self, ctx, error)
        else:
            raise error

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        if not testing and get_rule('BOOLEANS', 'SEND_ERRORS'):
            await handle_error(self, ctx, error)
        else:
            raise error


def setup(bot):
    bot.add_cog(Listeners(bot))
