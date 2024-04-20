import datetime
import sys

import discord
import numpy as np
import pandas as pd
from discord import SlashCommandGroup, option
from discord.ext import commands

sys.path.append('../')
from utils.basic import *
from utils.patch_utils import *

administration_roles = get_rule('ROLES_IDS', 'ADMINISTRATION')[:2]


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

    @patch_commands_group.command(name="request", description="Запросить патч")
    async def request(self, ctx: discord.ApplicationContext):
        request_channel_id = get_rule('CHANNELS_IDS', 'PATCH_REQUEST')
        if ctx.channel_id != request_channel_id:
            print(f'[{get_now()}] {ctx.author.name} ({ctx.author.id}) tried to /request in channel: {ctx.channel_id}')
            await ctx.respond(f'Please, use /request in <#{request_channel_id}> channel.', ephemeral=True)
            return

        modal = self.RequestModal(title='Patch Request')
        await ctx.send_modal(modal)

    @patch_commands_group.command(name="setmaxpatch", description="Set the latest patch that can be requested")
    @commands.has_any_role(*administration_roles)
    @option("max_patch", description="The latest patch number", required=True)
    async def setmaxpatch(self, ctx: discord.ApplicationContext, max_patch: str):
        write_rule('STRINGS', 'MAX_PATCH', max_patch)
        await ctx.respond(f'Max patch set to {max_patch}', ephemeral=True)
        print(f'[{get_now()}] Set max patch to {max_patch}')

    @patch_commands_group.command(name="setdone", description="Set the patch request status: DONE")
    @commands.has_any_role(*administration_roles)
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

    @patch_commands_group.command(name="setabandoned", description="Set the patch request status: ABANDONED")
    @commands.has_any_role(*administration_roles)
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

    @patch_commands_group.command(name="create_script", description="Create a SteamCMD patch download script")
    @commands.has_any_role(*administration_roles)
    @option('date', description="The date of the patch from SteamDB", required=True)
    @option('number', description="The number / name of the patch from SteamDB", required=False)
    async def create_script(self, ctx: discord.ApplicationContext, date: str, number: str = 'UNKNOWN'):
        auto_steamcmd_scripts = get_rule('CHANNELS_IDS', 'AUTO_STEAMCMD_SCRIPTS')

        if ctx.channel_id not in [auto_steamcmd_scripts] + get_rule('CHANNELS_IDS', 'TEST'):
            print(f'[{get_now()}] {ctx.author.name} ({ctx.author.id}) tried to /create_script in channel: {ctx.channel_id}')
            await ctx.respond(f'Please, use /create_script in <#{auto_steamcmd_scripts}> channel.', ephemeral=True)
            return

        ru_role_id = get_rule('ROLES_IDS', 'RU')
        tdate = date.replace('\t', ' ')
        max_timestamp = datetime.datetime.strptime(tdate, "%d %B %Y %a %H:%M").replace(tzinfo=datetime.timezone.utc).timestamp()
        pre_manifests = pd.read_pickle('data/manifests.pkl')
        pre_manifests['TimeDiff'] = max_timestamp - pre_manifests['Timestamp']
        pre_manifests.loc[pre_manifests['TimeDiff'] < 0, 'TimeDiff'] = np.nan
        pre_manifests = pre_manifests.dropna()
        idx = pre_manifests.groupby('DepotID')['TimeDiff'].idxmin()
        manifests = pre_manifests.loc[idx]
        depot_manifest_dict = manifests.groupby('DepotID')['ManifestID'].apply(list).to_dict()
        script = create_script(depot_manifest_dict, max_timestamp)
        print(f'[{get_now()}] Created script for {number} ({tdate})')
        script_name = f'temp/steamcmdscript_dota{number}.txt'
        fscript = open(script_name, 'w', encoding='utf-8')
        fscript.write(f'// {number}\n// {tdate}\n\n{script}\n')
        fscript.close()
        text = f'# {number}\n> Created by <@{get_rule('INTEGERS', 'OSCAR_ID')}>. Please check the correctness of the script.'
        if ru_role_id in [y.id for y in ctx.author.roles]:
            text = f"# {number}\n> Сделан <@{get_rule('INTEGERS', 'OSCAR_ID')}>'ом. Пожалуйста, проверяйте правильность скрипта."
        await ctx.respond(content=text, file=discord.File(script_name))
        print(f'[{get_now()}] Sent script for {number} ({tdate})')


def setup(bot):
    bot.add_cog(Patch(bot))
