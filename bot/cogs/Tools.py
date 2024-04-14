import sys

import discord
from discord.ext import commands

sys.path.append("..")
from utils.basic import *


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Tools cog loaded')

    @commands.command()
    async def move(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        if ctx.message.reference is not None:
            replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
            embed = discord.Embed(description=replied_message.content, color=discord.Color.blurple())
            embed.set_author(name=replied_message.author.name, icon_url=replied_message.author.avatar)
            await channel.send(embed=embed)  # Move the message with the avatar and sender's name
            await replied_message.delete()  # Delete the original message
            await ctx.message.delete()  # Delete the /move command
        else:
            await ctx.send('You must reply to the message to move it.')


def setup(bot):
    bot.add_cog(Tools(bot))
