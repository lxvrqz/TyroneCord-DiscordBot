import discord
from discord.ext import commands
from discord import app_commands

class UserInfo(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="Show infos about a User")
    @app_commands.describe(user="User u want to see")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user

        embed = discord.Embed(title=f"Userinfo: {user}", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Name", value=str(user), inline=True)
        embed.add_field(name="Account createt", value=user.created_at.strftime("%d.%m.%Y %H:%M"), inline=False)
        embed.add_field(name="Joined Server",
                    value=user.joined_at.strftime("%d.%m.%Y %H:%M") if user.joined_at else "Error", inline=False)
        embed.add_field(name="Bot", value=str(user.bot), inline=True)
        embed.add_field(name="Top Role", value=user.top_role.mention, inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(UserInfo(Bot))