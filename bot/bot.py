import discord
from discord.ext import commands
from dotenv import load_dotenv

import utils.logger as logger
from utils.basic import *

logger.install()
load_dotenv()

testing = get_rule('BOOLEANS', 'TESTING')


class Oscar(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def close(self):
        print(f'[{get_now()}] Closing bot...')
        await super().close()


intents = discord.Intents.all()
prefix = get_rule('PREFIXES', 'DEFAULT')
if testing:
    prefix = get_rule('PREFIXES', 'TESTING')
bot = Oscar(command_prefix=prefix, intents=intents)

for file in os.listdir(get_rule('PATHS', 'COGS')):
    if file.endswith(".py") and file != "__init__.py":
        bot.load_extension(f'cogs.{file[:-3]}')

discord_token = os.getenv('DISCORD_TOKEN_OSCAR')
if testing:
    discord_token = os.getenv('DISCORD_TOKEN_TEST')
bot.run(discord_token)
