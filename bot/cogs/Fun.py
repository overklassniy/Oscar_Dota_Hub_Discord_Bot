import sys
from random import randint, choice

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append("..")  # Modify the system path to include the parent directory for module access.
from utils.basic import *  # Import utilities from basic.py which includes functions like get_rule().
from utils.fun_utils import *  # Import utilities from fun_utils.py which includes functions like get_rule().


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
        text = f'{ctx.author.mention} gets a random number ({number1} - {number2}): {random_number}'
        # If the user has the Russian role, respond in Russian.
        if ru_role_id in [y.id for y in ctx.author.roles]:
            text = f'{ctx.author.mention} получает случайное число ({number1} - {number2}): **{random_number}**'
        print(f'[{get_now()}] {text}')  # Log the action.
        await ctx.response.send_message(content=text)  # Send the message to the channel.

    # Slash command to simulate flipping a coin.
    @fun_commands_group.command(name='flip', description="Flip a coin.")
    async def flip(self, ctx: discord.ApplicationContext):
        ru_role_id = get_rule('ROLES_IDS', 'RU')  # Get the ID for Russian role.
        coin_sides = ['***РЕШКА***', '***ОРЁЛ***']  # Options for coin sides in Russian for authenticity.
        random_side = choice(coin_sides)  # Randomly choose between the two sides.
        text = f'{ctx.author.mention} flips a coin: {random_side}'
        # Customize the response for users with the Russian role.
        if ru_role_id in [y.id for y in ctx.author.roles]:
            text = f'{ctx.author.mention} подбрасывает монетку: {random_side}'
        print(f'[{get_now()}] {text}')  # Log the action.
        await ctx.response.send_message(content=text)  # Send the response.

    @fun_commands_group.command(name='tip', description="Tip a member.")
    async def tip(self, ctx: discord.ApplicationContext,
                  member: discord.Option(discord.SlashCommandOptionType.mentionable, name="member", description="Member to tip.", required=True)):
        ru_role_id = get_rule('ROLES_IDS', 'RU')
        if not isinstance(member, discord.Member):
            incorrect_member_text = 'Incorrect member.'
            print(f'[{get_now()}] {incorrect_member_text} Type: {type(member)}')
            if ru_role_id in [y.id for y in ctx.author.roles]:
                incorrect_member_text = 'Неправильный участник'
            await ctx.respond(incorrect_member_text, ephemeral=True)
            return

        if member.id == ctx.author.id:
            not_yourself_text = 'You can\'t tip yourself.'
            print(f'[{get_now()}] {ctx.author.id} tried to tip himself.')
            if ru_role_id in [y.id for y in ctx.author.roles]:
                not_yourself_text = 'Вы не можете поблагодарить себя.'
            await ctx.respond(not_yourself_text, ephemeral=True)
            return

        if member.bot:
            not_bot_text = 'You can\'t tip bots.'
            print(f'[{get_now()}] {ctx.author.id} tried to tip bot: {member}.')
            if ru_role_id in [y.id for y in ctx.author.roles]:
                not_bot_text = 'Вы не можете поблагодарить бота.'
            await ctx.respond(not_bot_text, ephemeral=True)
            return

        name_1 = ctx.author.global_name
        rgb_color_1 = ctx.author.color.to_rgb()[::-1] + tuple([255])
        avatar_url_1 = ctx.author.avatar.url
        avatar_url256_1 = avatar_url_1[:-13] + 'png?size=256'
        id1 = ctx.author.id

        name_2 = member.global_name
        rgb_color_2 = member.color.to_rgb()[::-1] + tuple([255])
        avatar_url_2 = member.avatar.url
        avatar_url256_2 = avatar_url_2[:-13] + 'png?size=256'
        id2 = member.id

        avatar_path_1 = download_image(avatar_url256_1, f'temp/avatar_{id1}.png')
        avatar_path_2 = download_image(avatar_url256_2, f'temp/avatar_{id2}.png')
        tip_path = f'temp/tip_{id1}_{id2}.png'

        resize_image_if_small(avatar_path_1)
        resize_image_if_small(avatar_path_2)

        create_tip_image(name_1=name_1, name_2=name_2, avatar_path_1=avatar_path_1, avatar_path_2=avatar_path_2, text_color_1=rgb_color_1,
                         text_color_2=rgb_color_2, output_path=tip_path)

        text = f'{ctx.author.mention} TIPPED {member.mention}!'
        print(f'[{get_now()}] ')
        if ru_role_id in [y.id for y in member.roles]:
            text = f'{ctx.author.mention} ХВАЛИТ {member.mention}!'
        await ctx.respond(content=text, file=discord.File(tip_path, 'tip.png'))


# Function to add this cog to the bot.
def setup(bot):
    bot.add_cog(Fun(bot))
