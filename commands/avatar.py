import discord
from discord import app_commands
from discord.ext import commands
import logging

log = logging.getLogger(__name__)

class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Show the avatar of a user.")
    @app_commands.describe(user="The user whose avatar should be displayed")
    async def avatar(self, interaction: discord.Interaction, user: discord.User):
        log.info(f"{interaction.user} used /avatar: {user or interaction.user}")
        embed = discord.Embed(
            title=f"Avatar from {user.display_name}",
            color= discord.Color.purple()
        )
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text="DEV lxvrqz | Tyrone")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Avatar(bot))