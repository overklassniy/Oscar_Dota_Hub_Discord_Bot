import sys
from random import choice

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands
from discord.utils import get

sys.path.append("..")
from utils.basic import *
from utils.discord_basic import *
from utils.search_utils import *

administration_roles = get_rule('ROLES_IDS', 'ADMINISTRATION')


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Search cog loaded')

    search_commands_group = SlashCommandGroup("search", "Search related commands")

    @search_commands_group.command(name="search", description="Send search message")
    @commands.has_any_role(*administration_roles)
    @option("image", description="Image number attached to message")
    async def search(self, ctx: discord.ApplicationContext, image: int = 0):
        guild = ctx.guild
        channel = ctx.channel
        if channel.id not in get_rule("CHANNELS_IDS", 'SEARCH'):
            await ctx.respond('Please, select a channel in #Search category', ephemeral=True)
            print(f'[{get_now()}] Wrong channel ID for /search: {channel.id} ({channel.name})')
            return
        search_channels_roles = get_rule('ROLES_IDS', 'SEARCH_CHANNELS_ROLES_IDS')
        role_id = search_channels_roles[str(channel.id)]
        role = get(guild.roles, id=role_id)
        search_images = get_rule('IMAGES_URLS', 'SEARCH')
        if image > len(search_images) or image < 0:
            await ctx.respond(f'Wrong image number, please use a number from 1 to {len(search_images)}', ephemeral=True)
            print(f'[{get_now()}] Wrong image number for /search: {image}')
            return
        image_url = search_images[image - 1] if image else choice(search_images)
        message = await generate_search_message(image_url=image_url, role=role)
        await ctx.send(**message)
        await ctx.respond('Done', ephemeral=True)
        print(f'[{get_now()}] Search message sent to {ctx.channel.name}')

    @commands.command()
    async def gather(self, ctx: discord.ApplicationContext, ip: str = None):
        if not is_privileged(ctx, administration_roles):
            print(f'[{get_now()}] No permission to perform GATHER command for {ctx.author.name} ({ctx.author.id})')
            await ctx.respond('You do not have permission to perform this command', ephemeral=True)
            return

        replied_message = ctx.message.reference
        if not await check_ip_provided(ctx, ip):
            return

        await ctx.message.delete()
        message = await ctx.fetch_message(replied_message.message_id)
        target_emoji = get_rule('STRINGS', 'DAGON_EMOJI')
        users = []
        for reaction in message.reactions:
            if str(reaction) == target_emoji:
                async for user in reaction.users():
                    users.append(user)
        users = list(set(users))
        users_dict = {user: '❌' for user in users}

        ready_message = await send_ready_embed(ctx, users, users_dict)
        view = AcceptButton(users, users_dict, ready_message)

        reminder_embed, connect_embed = create_embeds(message, ip)
        forbidden_users = await notify_users(users, reminder_embed, connect_embed, view)

        if forbidden_users:
            await handle_forbidden_users(self, ctx, forbidden_users)


def setup(bot):
    bot.add_cog(Search(bot))
