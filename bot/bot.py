import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import utils.logger as logger
from utils.basic import *

logger.install()
load_dotenv()


class Oscar(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def close(self):
        print(f'[{get_now()}] Closing bot...')
        await super().close()


intents = discord.Intents.all()
bot = Oscar(command_prefix="~", intents=intents)

for file in os.listdir("bot/cogs"):
    if file.endswith(".py") and file != "__init__.py.py":
        bot.load_extension(f'cogs.{file[:-3]}')

discord_token = os.getenv('DISCORD_TOKEN_OSCAR')
if get_rule('BOOLEANS', 'TESTING'):
    discord_token = os.getenv('DISCORD_TOKEN_TEST')
bot.run(discord_token)
