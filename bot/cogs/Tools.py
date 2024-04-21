import sys

import discord
from discord.ext import commands

sys.path.append("..")  # Adds the parent directory to the system path to ensure imports from utils work.
from utils.basic import *  # Import basic utility functions and constants.
from utils.discord_basic import *  # Import Discord-specific utility functions.

administration_roles = get_rule('ROLES_IDS', 'ADMINISTRATION')  # Fetch the role IDs that have administration privileges.


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store an instance of the bot within the cog for later use.
        print(f'[{get_now()}] Tools cog loaded')  # Log the loading of the Tools cog.

    @commands.command()
    async def move(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        # The move command is used to relocate a message to another channel within the server.
        if not await is_privileged(ctx, administration_roles):
            # Check if the user has the required privileges to execute the command.
            print(f'[{get_now()}] No permission to perform MOVE command for {ctx.author.name} ({ctx.author.id})')
            await ctx.respond('You do not have permission to perform this command', ephemeral=True)
            return

        if ctx.message.reference is not None:
            # Check if the move command was invoked in response to another message.
            replied_message = await ctx.fetch_message(ctx.message.reference.message_id)  # Fetch the referenced message.
            embed = discord.Embed(description=replied_message.content, color=discord.Color.blurple())
            # Create an embed containing the content of the original message.
            embed.set_author(name=replied_message.author.name, icon_url=replied_message.author.avatar)
            # Set the author of the embed to be the author of the original message.
            await channel.send(embed=embed)  # Send the embed to the specified channel.
            await replied_message.delete()  # Delete the original message after moving it.
            await ctx.message.delete()  # Delete the command message to clean up the channel.
        else:
            # If the move command was not used in response to another message, inform the user of the correct usage.
            message = await ctx.send('You must reply to the message to move it.')
            await message.delete(delay=5)  # Delete the informative message after a short delay.


def setup(bot):
    bot.add_cog(Tools(bot))
