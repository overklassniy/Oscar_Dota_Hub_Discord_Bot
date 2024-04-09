import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.basic import *

load_dotenv()


class Oscar(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)


intents = discord.Intents.all()
bot = Oscar(command_prefix="!", intents=intents)


async def send_start_state():
    channel = bot.get_channel(get_rule('CHANNELS_IDS', 'STATE_CHANNEL_ID'))
    embed = discord.Embed(
        title="The bot is running",
        description=f'Time: `{get_now()}`',
        color=0x1f8b4c
    )
    await channel.send(embed=embed)


@bot.event
async def on_ready():
    print(f'[{get_now()}] Logged in as {bot.user.name}')
    if get_rule('BOOLEANS', 'SEND_START_STATE'):
        await send_start_state()


for file in os.listdir("bot/cogs"):
    if file.endswith(".py") and file != "__init__.py.py":
        bot.load_extension(f'cogs.{file[:-3]}')

discord_token = os.getenv('DISCORD_TOKEN_OSCAR')
if get_rule('BOOLEANS', 'TESTING'):
    discord_token = os.getenv('DISCORD_TOKEN_TEST')
bot.run(discord_token)
