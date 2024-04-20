import discord


async def is_privileged(ctx: discord.ApplicationContext, roles_ids: list) -> bool:
    return any(
        discord.utils.get(ctx.author.roles, id=role_ids)
        for role_ids in roles_ids
    )
