import sys

import discord
from discord.ext import commands

sys.path.append("..")
from utils.basic import *
from utils.discord_basic import *

administration_roles = get_rule('ROLES_IDS', 'ADMINISTRATION')


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Tools cog loaded')

    @commands.command()
    async def move(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        if not is_privileged(ctx, administration_roles):
            print(f'[{get_now()}] No permission to perform MOVE command for {ctx.author.name} ({ctx.author.id})')
            await ctx.respond('You do not have permission to perform this command', ephemeral=True)
            return

        if ctx.message.reference is not None:
            replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
            embed = discord.Embed(description=replied_message.content, color=discord.Color.blurple())
            embed.set_author(name=replied_message.author.name, icon_url=replied_message.author.avatar)
            await channel.send(embed=embed)
            await replied_message.delete()
            await ctx.message.delete()
        else:
            message = await ctx.send('You must reply to the message to move it.')
            await message.delete(delay=5)


def setup(bot):
    bot.add_cog(Tools(bot))
