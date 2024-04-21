import json

import discord
from utils.basic import *


def get_deleted_reactions() -> dict:
    deleted_reactions = json.load(open(get_rule('PATHS', 'DELETED_REACTIONS'), 'r'))
    # TODO: сделать вывод в формате списка, собрав все удаленные реакции из всех каналов в один (не забыв указать канал из которого забирался) и отсортировав по возрастанию где null (None) идут самыми ранними
    return deleted_reactions


def write_deleted_reactions(channel_name: str, data: dict):
    deleted_reactions = json.load(open(get_rule('PATHS', 'DELETED_REACTIONS'), 'r'))
    if channel_name not in deleted_reactions.keys():
        deleted_reactions[channel_name] = []
    deleted_reactions[channel_name].append(data)
    json.dump(deleted_reactions, open(get_rule('PATHS', 'DELETED_REACTIONS'), 'w'))
    return f'Wrote a new deleted reaction to {channel_name}'


async def send_start_state(listeners):
    channel = listeners.bot.get_channel(get_rule('CHANNELS_IDS', 'STATE'))
    embed = discord.Embed(
        title="The bot is running",
        description=f'Date: `{get_now(need_date_only=True)}`\n' +
                    f'Time: `{get_now(need_date=False)}`',
        color=0x1f8b4c
    )
    print(f'[{get_now()}] Sending start state')
    await channel.send(embed=embed)


async def handle_error(listeners, ctx: discord.ApplicationContext, error):
    time = get_now()
    channel = listeners.bot.get_channel(get_rule('CHANNELS_IDS', 'ERRORS'))
    embed = discord.Embed(
        title="An error has occurred!",
        description=f"User: <@{ctx.author.id}>\n" +
                    f"Channel: <#{ctx.channel.id}>\n" +
                    f"Command: `{ctx.command}`\n" +
                    f"Error: `{str(error)}`",
        color=0xff0000
    )
    embed.set_footer(text=f'Time: {time}')
    print(f'[{time}] Sending error message')
    await channel.send(embed=embed)
    print(error)
    message = await ctx.send('An error occurred. Please try again.')
    await message.delete(delay=5)
