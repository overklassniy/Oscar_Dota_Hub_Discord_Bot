import json
import re

import aiohttp
import discord
from discord.ext import commands
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
    author_id = ctx.author.id
    channel_id = ctx.channel.id
    channel_description = f"Channel: <#{channel_id}>\n"
    if isinstance(error, commands.NoPrivateMessage):
        channel_description = f"Channel (DM): `{channel_id}`\n"
    command = ctx.command
    embed = discord.Embed(
        title="An error has occurred!",
        description=f"User: <@{author_id}>\n" +
                    channel_description +
                    f"Command: `{command}`\n" +
                    f"Error: `{str(error)}`",
        color=0xff0000
    )
    embed.set_footer(text=f'Time: {time}')
    print(f'[{time}] Sending error message')
    await channel.send(embed=embed)


def is_discord_link_allowed(url: str, server_id: int) -> bool:
    match = re.match(r"https?://(?:www\.)?discord(?:app)?\.com/channels/(\d+)/(\d+)/(\d+)", url)
    if match:
        return match.group(1) == str(server_id)
    return False


async def is_invite_to_target_server(url: str, server_id: int) -> bool:
    match = re.match(r"(https?://)?(www\.)?(discord\.(gg|com/invite)/([a-zA-Z0-9]+))", url)
    if match:
        invite_code = match.group(5)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v10/invites/{invite_code}") as resp:
                if resp.status == 200:
                    invite_data = await resp.json()
                    if invite_data["guild"]["id"] == str(server_id):
                        return True
    return False
