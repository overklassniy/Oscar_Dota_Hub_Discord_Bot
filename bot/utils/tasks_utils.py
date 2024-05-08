import datetime
from random import choice

import discord
from utils.basic import *


async def clear_channel(tasks, channel_id: int):
    channel = tasks.bot.get_channel(channel_id)
    now = datetime.datetime.now()
    if all([
        now.hour == 9,
        now.minute in {0, 1, 2},
        not await is_channel_empty(channel),
    ]):
        await clear(channel)


async def is_channel_empty(channel: discord.TextChannel) -> bool:
    messages = await channel.history(limit=1).flatten()
    return not bool(messages)


async def clear(channel: discord.TextChannel):
    messages = []
    async for message in channel.history(limit=None):
        messages.append(message)
    await channel.delete_messages(messages)


async def send_search(tasks, channel_id: int):
    search_images = get_rule('IMAGES_URLS', 'SEARCH')
    channel = tasks.bot.get_channel(channel_id)
    now = datetime.datetime.now()
    if all([
        now.hour == 11,
        now.minute in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
        await is_channel_empty(channel),
    ]):
        image_url = choice(search_images)
        guild_id = get_rule('INTEGERS', 'GUILD_ID')
        search_channels_roles = get_rule('ROLES_IDS', 'SEARCH_CHANNELS_ROLES_IDS')
        role = tasks.bot.get_guild(guild_id).get_role(search_channels_roles[str(channel_id)])
        message = await generate_search_message(image_url=image_url, role=role)
        await channel.send(**message)


async def generate_search_message(image_url: str, role: discord.Role):
    embed = discord.Embed(
        title=":bangbang: СТАВИМ 10 ДАГОНОВ И НАЧИНАЕМ ИГРУ :bangbang:",
        color=role.color
    )
    embed.set_image(url=image_url)
    return {'content': role.mention, 'embed': embed}


def read_new_log_lines(file_path: str, last_position: int) -> tuple:
    with open(file_path, 'r', encoding='utf-8') as file:
        file.seek(last_position)
        new_lines = file.readlines()
        last_position = file.tell()
    return new_lines, last_position


def reset_daily_tips():
    now = datetime.datetime.now()
    if all([now.hour == 9, now.minute in {0, 1, 2}]):
        stats = get_stats()
        for member_id in list(stats.keys()):
            stats[member_id]['TIPS_USED_TODAY'] = 0
            stats[member_id]['TIPS_RECEIVED_TODAY'] = 0
        write_stats(stats)