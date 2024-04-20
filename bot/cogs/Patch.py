import sys

import discord
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append('../')
from utils.basic import *
from utils.patch_utils import *


class Patch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'[{get_now()}] Patch cog loaded')

    patch_commands_group = SlashCommandGroup("patch", "Команды для запроса патчей")

    class RequestModal(discord.ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.add_item(
                discord.ui.InputText(label="Введите номер патча и букву, разделенные точкой", placeholder='Например: 7.23b', min_length=4,
                                     max_length=5, required=True))

        async def callback(self, ctx: discord.Interaction):
            ru_role_id = get_rule('ROLES_IDS', 'RU')
            en_role_id = get_rule('ROLES_IDS', 'EN')
            if ru_role_id in [y.id for y in ctx.author.roles]:
                lang = ru_role_id
            else:
                lang = en_role_id
            patch_number = self.children[0].value.lower()
            if is_allowed_patch_string(patch_number) and patch_number < get_rule('STRINGS', 'MAX_PATCH') and is_patch_new(patch_number, ctx)[0]:
                embed = discord.Embed(color=discord.Color.yellow())
                embed.set_author(name=str(ctx.user.global_name), icon_url=ctx.user.avatar)
                title = 'A new patch has been requested'
                if lang == ru_role_id:
                    title = 'Запрошен новый патч'
                embed.title = title
                desctiption = f'Patch: **{patch_number}**'
                if lang == ru_role_id:
                    desctiption = f'Патч: **{patch_number}**'
                embed.description = desctiption
                footer = 'Status: REQUESTED'
                if lang == ru_role_id:
                    footer = 'Статус: ЗАПРОШЕНО'
                embed.set_footer(text=footer)
                await ctx.respond(embed=embed)
                message = await ctx.original_response()
                print(f'[{get_now()}] {add_requested_patch(message.id, patch_number)}')
            else:
                if not is_allowed_patch_string(patch_number):
                    text1 = 'Invalid patch number, please, use only decimal nubmers, dot and correct patch letter.'
                    if lang == ru_role_id:
                        text1 = 'Неверный номер патча, пожалуйста, используйте только десятичные числа, точку и правильную букву патча.'
                    await ctx.respond(text1, ephemeral=True)
                elif patch_number >= get_rule('STRINGS', 'MAX_PATCH'):
                    text2 = f'Invalid patch number, please input a valid patch number, that is older that the {get_rule('STRINGS', 'MAX_PATCH')}.'
                    if lang == ru_role_id:
                        text2 = f'Неверный номер патча, пожалуйста, введите действительный номер патча, который старше, чем {get_rule('STRINGS', 'MAX_PATCH')}.'
                    await ctx.respond(
                        text2,
                        ephemeral=True)
                elif not is_patch_new(patch_number, ctx)[0]:
                    await ctx.respond(is_patch_new(patch_number, ctx)[1], ephemeral=True)

    @patch_commands_group.command(name="request")
    async def request(self, ctx: discord.ApplicationContext):
        modal = self.RequestModal(title='Patch Request')
        await ctx.send_modal(modal)

    @patch_commands_group.command(name="setmaxpatch", description="Set the latest patch that can be requested")
    @option("max_patch", description="The latest patch", required=True)
    async def setmaxpatch(self, ctx: discord.ApplicationContext, max_patch: str):
        write_rule('STRINGS', 'MAX_PATCH', max_patch)
        await ctx.respond(f'Max patch set to {max_patch}', ephemeral=True)
        print(f'[{get_now()}] Set max patch to {max_patch}')

    @patch_commands_group.command(name="setdone")
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

    @patch_commands_group.command(name="setabandoned")
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
    bot.add_cog(Patch(bot))
