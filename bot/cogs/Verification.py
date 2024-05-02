import asyncio
import random
import sys

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append("..")  # Include the parent directory in the system path for importing modules.
from utils.basic import *  # Import basic utility functions and constants.
from utils.verification_utils import *  # Import verification-specific utilities.
from utils.steam_opendota import *  # Import utilities related to Steam and OpenDota APIs.

unverified_role_id = get_rule('ROLES_IDS', 'UNVERIFIED')  # Fetch the role ID for unverified users.


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store an instance of the bot.
        print(f'[{get_now()}] Verification cog loaded')  # Log the loading of the Verification cog.

    verification_commands_group = SlashCommandGroup("verification", "Commands for user verification", guild_only=True)

    @verification_commands_group.command(name='verify', description="Command for user verification")
    @commands.has_role(unverified_role_id)  # Restrict this command to users with the 'unverified' role.
    @option("steam_url", description="Enter your Steam profile URL", required=True)
    async def verify(self, ctx: discord.ApplicationContext, steam_url: str):
        # Handle the verification process.
        ru_role_id = get_rule('ROLES_IDS', 'RU')
        en_role_id = get_rule('ROLES_IDS', 'EN')
        lang = ru_role_id if ru_role_id in [y.id for y in ctx.author.roles] else en_role_id

        verify_channel = get_rule('CHANNELS_IDS', 'VERIFY')
        message_if_wrong_channel = f'This command only available at <#{verify_channel}>!' if lang == en_role_id else f'Эта команда доступна только в канале <#{verify_channel}>!'
        if ctx.channel_id != verify_channel:
            # Ensure the command is used in the designated verification channel.
            print(f'[{get_now()}] Wrong channel for verification: {ctx.channel_id} ({ctx.channel.name})')
            await ctx.respond(content=message_if_wrong_channel, ephemeral=True)
            return

        await ctx.response.defer()
        await asyncio.sleep(2)  # Artificial delay to simulate processing time.
        passphrase = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(16))  # Generate a random passphrase.
        print(f'[{get_now()}] Sending "verification initiated" log')
        await log_verification_attempt(self, ctx, steam_url, passphrase)  # Log the verification attempt.

        if not uri_validator(steam_url):
            # Validate the Steam URL format.
            message_invalid_url = 'Invalid Steam profile URL.' if lang == en_role_id else 'Неверная ссылка на Ваш профиль Steam.'
            print(f'[{get_now()}] Wrong steam profile URL: {steam_url}')
            message = await ctx.respond(content=message_invalid_url)
            await message.delete(delay=5)
            return

        try:
            # Send verification instructions via a private message.
            print(f'[{get_now()}] Sending verification instructions to {ctx.author.name} ({ctx.author.id})')
            await send_verification_instructions(ctx, steam_url, passphrase)
        except discord.Forbidden:
            # Handle the case where the bot is unable to send a private message due to user privacy settings.
            message_dm_error = 'I was unable to send you a private message. Please check your privacy settings and try again.' if lang == en_role_id else 'Я не смог отправить Вам личное сообщение. Пожалуйста, проверьте Ваши настройки конфиденциальности и попробуйте еще раз.'
            print(f"[{get_now()}] Couldn't send DM for verification")
            message = await ctx.respond(content=message_dm_error)
            await message.delete(delay=5)


def setup(bot):
    bot.add_cog(Verification(bot))
