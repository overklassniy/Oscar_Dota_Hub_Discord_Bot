import asyncio
import random
import sys

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append("..")
from utils.basic import *
from utils.verification_utils import *
from utils.steam_opendota import *


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Verification cog loaded')

    fun_commands_group = SlashCommandGroup("verification", "Команды для верификации")

    @fun_commands_group.command(name='verify', description="Команда для верификации")
    @option("steam_url", description="Введите URL своего профиля в Steam", required=True)
    async def verify(self, ctx: discord.ApplicationContext, steam_url: str):
        ru_role_id = get_rule('ROLES_IDS', 'RU')
        en_role_id = get_rule('ROLES_IDS', 'EN')
        lang = en_role_id
        if ru_role_id in [y.id for y in ctx.author.roles]:
            lang = ru_role_id

        verify_channel = get_rule('CHANNELS_IDS', 'VERIFY')
        text = f'This command only available at <#{verify_channel}>!'
        if lang == ru_role_id:
            text = f'Эта команда доступна только в канале <#{verify_channel}>!'
        if ctx.channel_id != verify_channel:
            print(f'[{get_now()}] Wrong channel for verification: {ctx.channel_id} ({ctx.channel.name})')
            await ctx.respond(content=text, ephemeral=True)
            return

        await ctx.response.defer()
        await asyncio.sleep(2)
        passphrase = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(16))
        print(f'[{get_now()}] Sending "verification initiated" log')
        await log_verification_attempt(self, ctx, steam_url, passphrase)

        if not uri_validator(steam_url):
            text = 'Invalid Steam profile URL.'
            if ru_role_id in [y.id for y in ctx.author.roles]:
                text = 'Неверная ссылка на Ваш профиль Steam.'
            print(f'[{get_now()}] Wrong steam profile URL: {steam_url}')
            message = await ctx.respond(content=text)
            await message.delete(delay=5)
            return

        try:
            print(f'[{get_now()}] Sending verification instructions to {ctx.author.name} ({ctx.author.id})')
            await send_verification_instructions(ctx, steam_url, passphrase)
        except discord.Forbidden:
            text = 'I was unable to send you a private message. Please check your privacy settings and try again.'
            if lang == ru_role_id:
                text = 'Я не смог отправить Вам личное сообщение. Пожалуйста, проверьте Ваши настройки конфиденциальности и попробуйте еще раз.'
            print(f"[{get_now()}] Couldn't send DM for verification")
            message = await ctx.respond(content=text)
            await message.delete(delay=5)


def setup(bot):
    bot.add_cog(Verification(bot))
