import asyncio
import sys
from copy import copy
from itertools import cycle

import discord
from discord.ext import commands, tasks

sys.path.append("..")  # Include the parent directory in the system path to access other modules.
from utils.basic import *  # Import basic utility functions and constants.
from utils.tasks_utils import *  # Import utilities specific to task handling.

# Define a cycling iterator for the bot status updates.
status = cycle(copy(get_rule('STRINGS', 'STATUS')))

last_file_position = 0


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Reference to the Discord bot instance.
        print(f'[{get_now()}] Tasks cog loaded')  # Log the loading of the Tasks cog.

    @tasks.loop(seconds=10)
    async def change_status(self):
        # Periodically change the bot's presence based on predefined statuses.
        await self.bot.change_presence(activity=discord.Game(next(status)))

    @tasks.loop(seconds=55)
    async def clear_search_channels(self):
        # Periodically clear messages in designated search channels.
        search_channels = get_rule('CHANNELS_IDS', 'SEARCH')
        for channel in search_channels:
            await clear_channel(self, channel)

    @tasks.loop(seconds=55)
    async def auto_search(self):
        # Automatically send search prompts in search channels at set intervals.
        search_channels = get_rule('CHANNELS_IDS', 'SEARCH')
        for channel in search_channels:
            await send_search(self, channel)

    @tasks.loop(seconds=600)
    async def check_dagons(self):
        # Check for messages in search channels that have reached a threshold number of reactions.
        search_channels = get_rule('CHANNELS_IDS', 'SEARCH')
        for c in search_channels:
            channel = self.bot.get_channel(c)
            messagef = await channel.history(limit=1).flatten()  # Retrieve the last message in the channel.
            if not messagef:
                return
            message_id = messagef[0].id
            message = await channel.fetch_message(message_id)
            total_reactions = sum(reaction.count for reaction in message.reactions)  # Sum all reactions on the message.
            if total_reactions >= get_rule('INTEGERS', 'DAGONS_FOR_NOTIFY'):
                # Send a notification if the total number of reactions reaches a threshold.
                embed = discord.Embed(
                    title=f"{total_reactions} dagons!",
                    description=f'Channel: {channel.mention}\n' +
                                f'Time: `{get_now()}`',
                    color=0x1f8b4c
                )
                dagons_channel = self.bot.get_channel(get_rule('CHANNELS_IDS', 'DAGONS_NOTIFICATION'))
                await dagons_channel.send(message.jump_url, embed=embed)  # Send an embed with the message link.

    @tasks.loop(seconds=180)
    async def send_log_updates(self):
        global last_file_position
        channel = self.bot.get_channel(get_rule('CHANNELS_IDS', 'CONSOLE'))
        if channel:  # Проверяем, что канал существует
            new_lines, last_file_position = read_new_log_lines(get_latest_log_file(), last_file_position)
            if new_lines:  # Если есть новые строки, отправляем их в канал
                # Объединяем строки и разделяем сообщение по символу переноса строки
                full_message = ''.join(new_lines)
                messages = full_message.split('\n')
                message_chunk = ''
                for line in messages:
                    if len(message_chunk) + len(line) + 1 > 1990:
                        await channel.send(f"```prolog\n{message_chunk}\n```")
                        message_chunk = ''
                        await asyncio.sleep(15)  # Пауза в 15 секунд
                    message_chunk += line + '\n'
                if message_chunk:
                    await channel.send(f"```prolog\n{message_chunk}\n```")

    @tasks.loop(seconds=55)
    async def clear_daily_stats(self):
        reset_daily_tips()


def setup(bot):
    bot.add_cog(Tasks(bot))
