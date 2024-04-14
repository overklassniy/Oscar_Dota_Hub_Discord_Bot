import discord


async def generate_search_message(image_url: str, role: discord.Role):
    embed = discord.Embed(
        title=":bangbang: СТАВИМ 10 ДАГОНОВ И НАЧИНАЕМ ИГРУ :bangbang:",
        color=role.color
    )
    embed.set_image(url=image_url)
    return {'content': role.mention, 'embed': embed}
