from enum import member

import discord
from discord.ext import commands
from discord import  app_commands
import logging

log = logging.getLogger(__name__)

warns = {}

class Warn(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Warn a user.")
    @app_commands.describe(member="The User u want to warn", reason="Provide a reason.")
    async def warn(self, interaction: discord.Interaction, member: discord.member, reason: str):
        log.info(f"{interaction.user} warned {member.mention}")
        guild_id = interaction.guild.id
        user_id = member.id

        if guild_id not in warns:
            warns[guild_id] = {}
        if user_id not in warns[guild_id]:
            warns[guild_id][user_id] = []

        warns[guild_id][user_id].append(reason)

        await interaction.response.send_message(
            f"{member.mention} got warned. By: {interaction.user.mention}. \n Reason: {reason}", ephemeral=True
        )
    @app_commands.command(name="warnings", description="Warns from a User.")
    @app_commands.describe(member="The User Warns u want to see")
    async def list_warns(self, interaction: discord.Interaction, member: discord.member, reason: str):
        guild_id = interaction.guild,id
        user_id = member.id

        user_warns = warns.get(guild_id, {}).get(user_id, [])

        if not user_warns:
            await interaction.response.send_message(f"{member.mention} has not warns.", ephemeral=True)
        else:
            formatted = "\n".join(f"{i+1}. {w}" for i, w in enumerate(user_warns))
            await interaction.response.send_message(
                f"{member.mention} hat **{len(user_warns)}** Verwarnung(en):\n```{formatted}```",
                ephemeral=True
            )
    @app_commands.command(name="warnclear", description="Delete all warns from a user")
    @app_commands.describe(member="User")
    async def clear_warns(self, interaction: discord.Interaction, member : discord.member, reason: str):
        log.info(f"{interaction.user} cleared warns from {member.mention}")
        guild_id = interaction.guild_id
        user_id = member.id

        if guild_id in warns and user_id in warns[guild_id]:
            del warns[guild_id][user_id]
            await interaction.response.send_message(f"The Warns from {member.mention} got cleared.")
        else:
            await interaction.response.send_message(f"{member.mention} has no warns.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Warn(bot))