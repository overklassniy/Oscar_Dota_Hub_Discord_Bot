import sys
from random import randint, choice

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append("..")  # Modify the system path to include the parent directory for module access.
from utils.basic import *  # Import utilities from basic.py which includes functions like get_rule().


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store an instance of the bot.
        print(f'[{get_now()}] Fun cog loaded')  # Log the initialization of the Fun cog.

    # Group of slash commands under the 'fun' category.
    fun_commands_group = SlashCommandGroup("fun", "Commands for fun")

    # Slash command to simulate a dice roll, reminiscent of the /roll command in Dota 2.
    @fun_commands_group.command(name='roll', description="Roll a random number within a range.")
    @option("number1", description="Minimum number", required=False)  # First number, defaults to None.
    @option("number2", description="Maximum number", required=False)  # Second number, defaults to None.
    async def roll(self, ctx: discord.ApplicationContext, number1: int, number2: int):
        ru_role_id = get_rule('ROLES_IDS', 'RU')  # Get the ID for Russian role to customize the response.
        # Set defaults and validate the provided numbers to ensure they're within logical limits.
        if not number1:
            number1 = 1
        if number1 < 0 or number1 > 999999:
            number1 = max(1, min(number1, 999999))
        if not number2:
            number2 = 100
        if number2 < 0 or number2 > 999999:
            number2 = max(1, min(number2, 999999))
        # Ensure the minimum is not greater than the maximum.
        if number1 > number2:
            number1, number2 = number2, number1

        random_number = randint(number1, number2)  # Generate a random number in the range.
        text = f'{ctx.author} gets a random number ({number1} - {number2}): {random_number}'
        # If the user has the Russian role, respond in Russian.
        if ru_role_id in [y.id for y in ctx.author.roles]:
            text = f'{ctx.author} получает случайное число ({number1} - {number2}): {random_number}'
        print(f'[{get_now()}] {text}')  # Log the action.
        await ctx.response.send_message(content=text)  # Send the message to the channel.

    # Slash command to simulate flipping a coin.
    @fun_commands_group.command(name='flip', description="Flip a coin.")
    async def flip(self, ctx: discord.ApplicationContext):
        ru_role_id = get_rule('ROLES_IDS', 'RU')  # Get the ID for Russian role.
        coin_sides = ['***РЕШКА***', '***ОРЁЛ***']  # Options for coin sides in Russian for authenticity.
        random_side = choice(coin_sides)  # Randomly choose between the two sides.
        text = f'{ctx.author} flips a coin: {random_side}'
        # Customize the response for users with the Russian role.
        if ru_role_id in [y.id for y in ctx.author.roles]:
            text = f'{ctx.author} подбрасывает монетку: {random_side}'
        print(f'[{get_now()}] {text}')  # Log the action.
        await ctx.response.send_message(content=text)  # Send the response.


# Function to add this cog to the bot.
def setup(bot):
    bot.add_cog(Fun(bot))
