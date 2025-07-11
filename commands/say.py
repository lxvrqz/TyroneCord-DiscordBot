import discord
from discord import app_commands
from discord.ext import commands
import logging

log = logging.getLogger(__name__)

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="say", description="Let the bot say smth")
    @app_commands.describe(message="The Text, that the bot should say")
    async def say(self, interaction: discord.Interaction, message: str):
        log.info(f"{interaction.user} hat /say genutzt: {message}")
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Say(bot))