import re
import sys

import discord
from discord.ext import commands

sys.path.append("..")  # Include the parent directory in the system path to access other modules.
from cogs.Tasks import *  # Import all tasks from the Tasks cog.
from utils.basic import *  # Import utilities such as configuration fetching.
from utils.listeners_utils import *  # Import utilities specifically tailored for listeners.

# Fetch a boolean value indicating if the bot is in testing mode.
testing = get_rule('BOOLEANS', 'TESTING')


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store an instance of the bot.
        print(f'[{get_now()}] Listeners cog loaded')  # Log the initialization of the Listeners cog.

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # This listener triggers when a reaction is added to any message.
        channel_id = payload.channel_id
        user = payload.member
        message_id = payload.message_id
        channels = get_rule('CHANNELS_IDS', 'SEARCH')
        if testing:
            channels = get_rule('CHANNELS_IDS', 'TEST')
        if channel_id not in channels:
            return  # Ignore reactions in channels that are not designated for listening.

        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            if str(reaction) != get_rule('STRINGS', 'DAGON_EMOJI'):
                date = get_now(need_date_only=True)
                time = get_now(need_date=False)
                if str(user) != 'overklassniy#0':
                    reaction_data = {
                        "username": str(user.global_name),
                        "user_id": user.id,
                        "emoji": str(reaction),
                        "date": date,
                        "time": time
                    }
                    write_deleted_reactions(channel.name, reaction_data)
                reactions_channel = self.bot.get_channel(get_rule('CHANNELS_IDS', 'REACTIONS_DELETED_LOG'))
                embedVar = discord.Embed(
                    title="Reaction deleted",
                    description=f'Channel: <#{channel_id}>\n' +
                                f'Channel ID: {channel_id}\n' +
                                f'User: `{str(user)}`\n' +
                                f'User ID: `{user.id}`\n' +
                                f'Reaction: `{str(reaction)}`\n' +
                                f'Date: `{date}`\n' +
                                f'Time: `{time}`',
                    color=0xcc0000
                )
                print(f'[{get_now()}] Sending deleted reaction data')
                await reactions_channel.send(embed=embedVar)
                print(f'[{get_now()}] Removed reaction {str(reaction)} from channel {str(channel)}')
                await reaction.remove(user)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        # This listener handles incoming messages to restrict them to commands only in specific channels.
        channel_id = message.channel.id
        if channel_id in get_rule('CHANNELS_IDS', 'COMMANDS_ONLY_CHANNELS') and not testing:
            if message.type != discord.MessageType.application_command:
                print(f'[{get_now()}] Deleted message "{message.content}" from channel {message.channel.name}')
                await message.delete()
                return

        admin_id = get_rule('INTEGERS', 'ADMINISTRATOR_ID')
        if message.author.id == admin_id:
            return

        urls = re.findall(r'(https?://[^\s]+|www\.[^\s]+|[^\s]+\.[a-z]{2,})', message.content)
        if urls:
            server_id = get_rule('INTEGERS', 'GUILD_ID')
            for url in urls:
                domain_match = re.findall(r'https?://(?:www\.)?([^/]+)', url)
                if not domain_match:
                    domain_match = re.findall(r'www\.(.*)', url)
                    if not domain_match:
                        domain_match = re.findall(r'([^\s]+\.[a-z]{2,})', url)

                domain = domain_match[0].lower()

                if domain not in get_rule('STRINGS', 'WHITELIST_DOMAINS') and not is_discord_link_allowed(url, server_id):
                    if re.match(r"(https?://)?(www\.)?(discord\.(gg|com/invite)/([a-zA-Z0-9]+))", url):
                        if await is_invite_to_target_server(url, server_id):
                            continue
                    print(f'[{get_now()}] Deleted message "{message.content}" from channel {message.channel.name}')
                    await message.delete()
                    return

    @commands.Cog.listener()
    async def on_ready(self):
        # Log in notification and start scheduled tasks.
        print(f'[{get_now()}] Logged in as {self.bot.user.name}')
        Tasks.change_status.start(self)
        Tasks.clear_search_channels.start(self)
        Tasks.auto_search.start(self)
        Tasks.check_dagons.start(self)
        Tasks.clear_daily_stats.start(self)
        if not testing:
            Tasks.send_log_updates.start(self)
        if not testing and get_rule('BOOLEANS', 'SEND_START_STATE'):
            await send_start_state(self)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ApplicationContext, error):
        # Handle generic command errors.
        if isinstance(error, commands.errors.NoPrivateMessage):
            await handle_error(self, ctx, error)
            message = await ctx.send('This command cannot be used in private messages.')
            await message.delete(delay=5)
            raise error
        if not testing and get_rule('BOOLEANS', 'SEND_ERRORS'):
            await handle_error(self, ctx, error)
            message = await ctx.send('An error occurred. Please try again.')
            await message.delete(delay=5)
        else:
            raise error

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        # Handle errors specific to slash commands, providing user feedback on missing roles.
        if isinstance(error, commands.errors.MissingAnyRole) or isinstance(error, commands.errors.MissingRole):
            roles_ids = list(map(int, re.findall(r'\d+', str(error))))
            roles = ' / '.join(f'<@&{role_id}>' for role_id in roles_ids)
            await handle_error(self, ctx, error)
            await ctx.respond(f'You are missing the role: {roles}', ephemeral=True)
            raise error
        if isinstance(error, commands.errors.NoPrivateMessage):
            await handle_error(self, ctx, error)
            await ctx.respond('This command cannot be used in private messages.', ephemeral=True)
            raise error
        if not testing and get_rule('BOOLEANS', 'SEND_ERRORS'):
            await handle_error(self, ctx, error)
            message = await ctx.send('An error occurred. Please try again.')
            await message.delete(delay=5)
        else:
            await handle_error(self, ctx, error)
            raise error


def setup(bot):
    bot.add_cog(Listeners(bot))
