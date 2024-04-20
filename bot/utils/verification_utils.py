import sys

import discord
from discord.ui import Button, View

sys.path.append("..")
from utils.basic import *
from utils.steam_opendota import *


async def log_verification_attempt(verification, ctx: discord.ApplicationContext, steam_url: str, passphrase: str):
    verify_log_channel = verification.bot.get_channel(get_rule('CHANNELS_IDS', 'VERIFY_LOG'))
    embed = discord.Embed(
        title="Verification process initiated",
        description=f'User: <@{ctx.author.id}>\n' +
                    f'User_ID: `{ctx.author.id}`\n' +
                    f'Steam: `{steam_url}`\n' +
                    f'Passphrase: `{passphrase}`',
        color=0xd6f11d
    )
    embed.set_footer(text=f'Time: {get_now()}')
    await verify_log_channel.send(embed=embed)


async def send_verification_instructions(ctx: discord.ApplicationContext, steam_url: str, passphrase: str):
    ru_role_id = get_rule('ROLES_IDS', 'RU')
    en_role_id = get_rule('ROLES_IDS', 'EN')
    if ru_role_id in [y.id for y in ctx.author.roles]:
        lang = ru_role_id
    else:
        lang = en_role_id
    embed_info, embed_profile, embed_howto = create_verification_embeds(steam_url, passphrase, lang)
    button_done = create_verification_button(ctx, passphrase, steam_url)
    first_message = await ctx.author.send(embeds=[embed_info, embed_profile, embed_howto], view=View(button_done, timeout=None))
    verify_channel_message_text = 'Please, check your DM for verification instructions.'
    if lang == ru_role_id:
        verify_channel_message_text = 'Пожалуйста, проверьте ЛИЧНЫЕ СООБЩЕНИЯ для дальнейших инструкций'
    verify_channel_message = await ctx.followup.send(content=verify_channel_message_text)
    await verify_channel_message.delete(delay=5)


def create_verification_embeds(steam_url: str, passphrase: str, lang: int, state: int = 0):
    ru_role_id = get_rule('ROLES_IDS', 'RU')
    en_role_id = get_rule('ROLES_IDS', 'EN')
    if state == 0:
        embed_info = ''
        embed_profile = ''
        embed_howto = ''
        if lang == ru_role_id:
            embed_info = discord.Embed(
                title="Верификация Steam",
                description="Здравствуйте, Вы начали верификацию своего профиля Steam. Нам нужны данные о Вашем аккаунте ради получения ранга Dota 2. **Пожалуйста, убедитесь, что у Вас включена __общедоступная история матчей__ и отключен __анонимный режим__ в настройках Dota 2 (Настройки -> Сообщество).**",
                color=0xd6f11d
            )
            embed_profile = discord.Embed(
                title="Ваш профиль",
                description=f"Настоящее имя: `{get_realname(steam_url)}`\n" +
                            f'Ваш профиль Steam: {steam_url}',
                color=0xd6f11d
            )
            embed_howto = discord.Embed(
                title="Как верифицировать?",
                description=f'Добавьте в свое **настоящее имя** следующий текст: `{passphrase}`. **ВЫ СМОЖЕТЕ УБРАТЬ ЕГО ПОСЛЕ ВЕРИФИКАЦИИ**. После этого нажмите на кнопку "Я сменил имя".',
                color=0xd6f11d
            )
        if lang == en_role_id:
            embed_info = discord.Embed(
                title="Steam verification",
                description="Hello, you have started the verification of your Steam profile. We need data about your account to obtain a Dota 2 rank. **Please make sure that you have the __public match history__ enabled and __anonymous mode__ disabled in the Dota 2 settings (Settings -> Community).**",
                color=0xd6f11d
            )
            embed_profile = discord.Embed(
                title="Your Steam profile",
                description=f"Real name: `{get_realname(steam_url)}`\n" +
                            f'Your Steam profile: {steam_url}',
                color=0xd6f11d
            )
            embed_howto = discord.Embed(
                title="How to verify?",
                description=f'Add the following text to your **real name**: `{passphrase}`. **YOU WILL BE ABLE TO REMOVE IT AFTER VERIFICATION**. After that, click the “I changed my name” button.',
                color=0xd6f11d
            )
        embed_info.set_image(url='https://cdn.discordapp.com/attachments/1072851627171647529/1135631936967159808/image.png')
        embed_howto.set_image(url='https://media.discordapp.net/attachments/1072851627171647529/1151931126995234856/image.png')
        embed_profile.set_thumbnail(url=get_avatar(steam_url))
        return embed_info, embed_profile, embed_howto
    if state == 1:
        if lang == ru_role_id:
            embed_success = discord.Embed(
                title='Успешная верификация',
                description=f"Вы успешно верифицировали аккаунт. Вы можете убрать `{passphrase}` из своего **настоящего имени**.",
                color=0x49bd17
            )
            embed_profile_2 = discord.Embed(
                title=get_nickname(steam_url),
                description=f"Настоящее имя: `{get_realname(steam_url)}`\n" +
                            f'Ваш профиль Steam: {steam_url}',
                color=0x49bd17
            )
            embed_profile_2.set_thumbnail(url=get_avatar(steam_url))
            return embed_success, embed_profile_2
        if lang == en_role_id:
            embed_success = discord.Embed(
                title='Verification succeed',
                description=f"You have successfully verified your account. You can remove `{passphrase}` from your **real name**.",
                color=0x49bd17
            )
            embed_profile_2 = discord.Embed(
                title=get_nickname(steam_url),
                description=f"Real name: `{get_realname(steam_url)}`\n" +
                            f'Your Steam profile: {steam_url}',
                color=0x49bd17
            )
            embed_profile_2.set_thumbnail(url=get_avatar(steam_url))
            return embed_success, embed_profile_2
    if state == 2:
        if lang == ru_role_id:
            embed_deny = discord.Embed(
                title='Неудачная верификация',
                description="Вы не сменили имя!",
                color=0xbc202c
            )
            embed_profile_2 = discord.Embed(
                title=get_nickname(steam_url),
                description=f"Настоящее имя: `{get_realname(steam_url)}`\n" +
                            f"Ваш профиль Steam: {steam_url}",
                color=0xbc202c
            )
            embed_profile_2.set_thumbnail(url=get_avatar(steam_url))
            return embed_deny, embed_profile_2
        if lang == en_role_id:
            embed_deny = discord.Embed(
                title='Verification failed',
                description="You haven't changed real name!",
                color=0xbc202c
            )
            embed_profile_2 = discord.Embed(
                title=get_nickname(steam_url),
                description=f"Real name: `{get_realname(steam_url)}`\n" +
                            f"Your Steam profile: {steam_url}",
                color=0xbc202c
            )
            embed_profile_2.set_thumbnail(url=get_avatar(steam_url))
            return embed_deny, embed_profile_2


def create_verification_button(ctx: discord.ApplicationContext, passphrase: str, steam_url: str):
    ru_role_id = get_rule('ROLES_IDS', 'RU')
    en_role_id = get_rule('ROLES_IDS', 'EN')
    label = 'I changed real name!'
    if ru_role_id in [y.id for y in ctx.author.roles]:
        label = 'Я сменил имя!'
    button_done = Button(style=discord.ButtonStyle.success, label=label)

    async def button_callback(button_interaction):
        if passphrase in get_realname(steam_url):
            users_dict = get_users()
            users_dict[str(button_interaction.user.id)] = str(steamurl_to_steamid64(steam_url))
            write_users(users_dict)
            print(f'[{get_now()}] Wrote "{button_interaction.user.id}": "{steamurl_to_steamid64(steam_url)}" to users.json')

            verified_role = discord.utils.get(ctx.guild.roles, id=get_rule('ROLES_IDS', 'VERIFIED'))
            unverified_role = discord.utils.get(ctx.guild.roles, id=get_rule('ROLES_IDS', 'UNVERIFIED'))
            member = ctx.guild.get_member(button_interaction.user.id)
            print(f'[{get_now()}] Added "Verified" role to {ctx.author.name} ({ctx.author.id}).')
            await member.add_roles(verified_role)
            print(f'[{get_now()}] Removed "Not verified" role from {ctx.author.name} ({ctx.author.id}).')
            await member.remove_roles(unverified_role)
            lang = en_role_id
            if ru_role_id in [y.id for y in ctx.author.roles]:
                lang = ru_role_id
            print(f'[{get_now()}] Sending verification status: succeed')
            await button_interaction.user.send(embeds=create_verification_embeds(steam_url, passphrase, lang, state=1))
            print(f'[{get_now()}] Disabling button from DM instructions')
            try:
                await button_interaction.response.edit_message(view=None)
            except Exception as e:
                print(str(e))
        else:
            lang = en_role_id
            if ru_role_id in [y.id for y in ctx.author.roles]:
                lang = ru_role_id
            print(f'[{get_now()}] Sending verification status: failed')
            await button_interaction.user.send(embeds=create_verification_embeds(steam_url, passphrase, lang, state=2))

    button_done.callback = button_callback
    return button_done
