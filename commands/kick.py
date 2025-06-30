import discord
from discord import app_commands
from discord.ext import commands
import logging

log = logging.getLogger(__name__)


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a user from the server.")
    @app_commands.describe(member="The member to be kicked.", reason="The reason for the kick.")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        log.info(f"{interaction.user} used /kick: {member}. Reason: {reason}")
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You don't have permission to kick members.", ephemeral=True)
            return
        await member.kick(reason=reason)
        await interaction.response.send_message(
            f"{member.mention} was kicked by {interaction.user.mention}.\n**Reason: {reason}**"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            synced = await self.bot.tree.sync()
            print(f"commands synced: {len(synced)}")
        except Exception as e:
            print(f"smth is wrong: {e}")

async def setup(bot):
    await bot.add_cog(Kick(bot))
