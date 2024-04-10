import sys
from random import randint, choice

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append("..")
from utils.basic import *


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Fun cog loaded')

    fun_command_group = SlashCommandGroup("fun", "Commands for fun")

    @fun_command_group.command(name='roll', description="Команда /roll из Dota 2")
    @option("number1", description="Введите минимальное число", required=False)
    @option("number2", description="Введите максимальное число", required=False)
    async def roll(self, ctx: discord.ApplicationContext, number1: int, number2: int):
        if not number1:
            number1 = 1
        if number1 < 0:
            number1 = 1
        if number1 > 999999:
            number1 = 999999
        if not number2:
            number2 = 100
        if number2 < 0:
            number2 = 1
        if number2 > 999999:
            number2 = 999999
        if number1 > number2:
            number1 = number2
        if number2 < number1:
            number2 = number1

        random_number = randint(number1, number2)
        print(f'[{get_now()}] {ctx.author} получает случайное число ({number1} - {number2}): {random_number}')
        await ctx.response.send_message(content=f'{ctx.author} получает случайное число ({number1} - {number2}): {random_number}')

    @fun_command_group.command(name='flip', description="Команда /flip из Dota 2")
    async def flip(self, ctx: discord.ApplicationContext):
        coin_sides = ['***РЕШКА***', '***ОРЁЛ***']
        random_side = choice(coin_sides)
        print(f'[{get_now()}] {ctx.author} подбрасывает монетку: {random_side}')
        await ctx.response.send_message(content=f'{ctx.author} подбрасывает монетку: {random_side}')


def setup(bot):
    bot.add_cog(Fun(bot))
