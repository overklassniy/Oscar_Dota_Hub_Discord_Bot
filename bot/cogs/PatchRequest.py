import sys

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append('../')
from utils.basic import *
from utils.patchrequest_utils import *


class PatchRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] PatchRequest Cog Loaded')

    patchrequest_command_group = SlashCommandGroup("patchrequest", "Patch Request Commands")

    class RequestModal(discord.ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.add_item(
                discord.ui.InputText(label="Input patch number and letter divided by dot", placeholder='For example: 7.23b', min_length=4,
                                     max_length=5, required=True))

        async def callback(self, ctx: discord.Interaction):
            patch_number = self.children[0].value.lower()
            if is_allowed_patch_string(patch_number) and patch_number < get_rule('STRINGS', 'MAX_PATCH') and is_patch_new(patch_number)[0]:
                embed = discord.Embed(color=discord.Color.yellow())
                embed.set_author(name=str(ctx.user.global_name), icon_url=ctx.user.avatar)
                embed.title = 'A new patch has been requested'
                embed.description = f'Patch: **{patch_number}**'
                embed.set_footer(text='Status: REQUESTED')
                await ctx.respond(embed=embed)
                message = await ctx.original_response()
                print(f'[{get_now()}] {add_requested_patch(message.id, patch_number)}')
            else:
                if not is_allowed_patch_string(patch_number):
                    await ctx.respond('Invalid patch number, please, use only decimal nubmers, dot and correct patch letter.', ephemeral=True)
                elif patch_number >= get_rule('STRINGS', 'MAX_PATCH'):
                    await ctx.respond(
                        f'Invalid patch number, please input a valid patch number, that is older that the {get_rule('STRINGS', 'MAX_PATCH')}.',
                        ephemeral=True)
                elif not is_patch_new(patch_number)[0]:
                    await ctx.respond(is_patch_new(patch_number)[1], ephemeral=True)

    @patchrequest_command_group.command(name="request")
    async def request(self, ctx: discord.ApplicationContext):
        modal = self.RequestModal(title='Patch Request')
        await ctx.send_modal(modal)

    @patchrequest_command_group.command(name="setmaxpatch", description="Set the latest patch that can be requested")
    @option("max_patch", description="The latest patch", required=True)
    async def setmaxpatch(self, ctx: discord.ApplicationContext, max_patch: str):
        write_rule('STRINGS', 'MAX_PATCH', max_patch)
        await ctx.respond(f'Max patch set to {max_patch}', ephemeral=True)
        print(f'[{get_now()}] Set max patch to {max_patch}')

    @patchrequest_command_group.command(name="setdone")
    @option("request_id", description="ID of the message with requested patch", required=True)
    async def setdone(self, ctx: discord.ApplicationContext, request_id: str):
        patch_number = get_requested_patch(request_id)
        print(f'[{get_now()}] {delete_requested_patch(request_id)}')
        print(f'[{get_now()}] {add_ready_patch(patch_number)}')

        message = await ctx.fetch_message(int(request_id))
        embed = message.embeds[0]
        embed.color = discord.Color.green()
        embed.set_footer(text='Status: DONE')

        await message.edit(embed=embed)

        await ctx.respond('Done', ephemeral=True)

    @patchrequest_command_group.command(name="setabandoned")
    @option("request_id", description="ID of the message with requested patch", required=True)
    async def setabandoned(self, ctx: discord.ApplicationContext, request_id: str):
        patch_number = get_requested_patch(request_id)
        print(f'[{get_now()}] {delete_requested_patch(request_id)}')
        print(f'[{get_now()}] {add_abandoned_patch(patch_number)}')

        message = await ctx.fetch_message(int(request_id))
        embed = message.embeds[0]
        embed.color = discord.Color.red()
        embed.set_footer(text='Status: ABANDONED')

        await message.edit(embed=embed)

        await ctx.respond('Done', ephemeral=True)


def setup(bot):
    bot.add_cog(PatchRequest(bot))
