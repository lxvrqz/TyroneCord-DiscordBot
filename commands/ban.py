import discord
from discord import app_commands
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban a user from the server.")
    @app_commands.describe(member="The member to be banned.", reason="The reason for the ban.")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You don't have permission to ban.", ephemeral=True)
            return
        await member.ban(reason=reason)
        await interaction.response.send_message(
            f"{member.mention} was banned by {interaction.user.mention}.\n**Reason: {reason}**"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            synced = await self.bot.tree.sync()
            print(f"commands synced: {len(synced)}")
        except Exception as e:
            print(f"smth is wrong: {e}")

async def setup(bot):
    await bot.add_cog(Ban(bot))
