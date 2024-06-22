import asyncio

import discord
from discord.ui import View
from utils.steam_opendota import *


async def generate_search_message(image_url: str, role: discord.Role) -> dict:
    embed = discord.Embed(
        title=":bangbang: СТАВИМ 10 ДАГОНОВ И НАЧИНАЕМ ИГРУ :bangbang:",
        color=role.color
    )
    embed.set_image(url=image_url)
    return {'content': role.mention, 'embed': embed}


async def check_ip_provided(ctx: discord.ApplicationContext, ip: str) -> bool:
    ru_role_id = get_rule('ROLES_IDS', 'RU')
    text = "You didn't specify the IP!"
    if ru_role_id in [y.id for y in ctx.author.roles]:
        text = 'Вы не указали IP!'
    if ip is None:
        message = await ctx.send(content=text)
        await message.delete(delay=5)
        print(f'[{get_now()}] No IP provided!')
        return False
    return True


def format_usernames_with_mmr(users_dict: dict):
    return '\n'.join([f'{user.global_name} [{get_mmr_from_discord(str(user.id))}]: {mark}' for user, mark in users_dict.items()])


async def send_ready_embed(ctx: discord.ApplicationContext, users, users_dict: dict):
    description = f'Игроков готово:\n\n0 / {len(users)}\n\n{format_usernames_with_mmr(users_dict)}'
    embed = discord.Embed(
        title='Монитор готовности',
        description=description,
        color=discord.Color.gold()
    )
    print(f'[{get_now()}] Sending ready monitor')
    return await ctx.send(embed=embed)


async def notify_users(users, reminder_embed, connect_embed, view: discord.ui.View):
    forbidden_users = []
    for user in users:
        if not user.bot:
            try:
                await user.send(embeds=[reminder_embed, connect_embed], view=view)
            except discord.Forbidden:
                forbidden_users.append(f'<@{user.id}>')
    return forbidden_users


class AcceptButton(View):
    def __init__(self, users, users_dict, ready_message):
        super().__init__()
        self.users = users
        self.users_dict = users_dict
        self.ready_message = ready_message
        self.ready_now = 0
        self.lock = asyncio.Lock()

    @discord.ui.button(label='Я готов', style=discord.ButtonStyle.green)
    async def accept_game(self, button, interaction):
        async with self.lock:
            if self.users_dict[interaction.user] == '✅':
                await interaction.response.send_message('Вы уже приняли участие.', ephemeral=True)
                return

            self.ready_now += 1
            self.users_dict[interaction.user] = '✅'
            description = f'Игроков готово:\n{self.ready_now} / {len(self.users)}\n\n{format_usernames_with_mmr(self.users_dict)}'
            embed = discord.Embed(
                title='Монитор готовности',
                description=description,
                color=discord.Color.green()
            )
            await self.ready_message.edit(embed=embed)
            await interaction.response.edit_message(view=None)


def create_embeds(message, ip: str):
    message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
    reminder_embed = discord.Embed(
        title='Ваша игра найдена!',
        description=f'Вы нашли игру в Dota Hub!\n{message_link}',
        color=discord.Color.gold(),
        url=message_link
    )
    connect_embed = discord.Embed(
        title=f'connect {ip}',
        description='Пожалуйста, нажмите кнопку ниже, для подтверждения и подключитесь к игре!',
        color=discord.Color.green()
    )
    return reminder_embed, connect_embed


async def handle_forbidden_users(search, ctx: discord.ApplicationContext, forbidden_users):
    channel_id = get_rule('CHANNELS_IDS', 'FORBIDDEN_USERS')
    forbidden_users_channel = search.bot.get_channel(channel_id)
    description = f"Couldn't send a message to the following people: {', '.join(forbidden_users)}"
    embed = discord.Embed(title='Error sending the readiness message', description=description)
    await forbidden_users_channel.send(embed=embed)
    print(f'[{get_now()}] {description}')
    await ctx.send(content=description)
