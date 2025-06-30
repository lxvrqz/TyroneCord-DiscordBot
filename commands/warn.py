import json
import os
import discord
from discord.ext import commands
from discord import app_commands, Member
import logging

log = logging.getLogger(__name__)

WARN_FILE = "warns.json"

def load_warns():
    if os.path.isfile(WARN_FILE):
        with open(WARN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_warns(data):
    with open(WARN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

warns = load_warns()

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Warn a user.")
    @app_commands.describe(user="The user you want to warn", reason="Reason for the warning")
    async def warn(self, interaction: discord.Interaction, user: Member, reason: str):
        log.info(f"{interaction.user} warned {user}")
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)

        if guild_id not in warns:
            warns[guild_id] = {}
        if user_id not in warns[guild_id]:
            warns[guild_id][user_id] = []

        warns[guild_id][user_id].append(reason)
        save_warns(warns)

        await interaction.response.send_message(
            f"{user.mention} got warned by {interaction.user.mention}. \n**Reason: {reason}**", ephemeral=True
        )

    @app_commands.command(name="warnings", description="Check warnings of a user.")
    @app_commands.describe(user="User whose warnings you want to see")
    async def list_warns(self, interaction: discord.Interaction, user: Member):
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)

        user_warns = warns.get(guild_id, {}).get(user_id, [])

        if not user_warns:
            await interaction.response.send_message(f"{user.mention} has no warnings.", ephemeral=True)
        else:
            formatted = "\n".join(f"{i+1}. {w}" for i, w in enumerate(user_warns))
            await interaction.response.send_message(
                f"{user.mention} has **{len(user_warns)}** warning(s):\n```{formatted}```",
                ephemeral=True
            )

    @app_commands.command(name="warnclear", description="Clear all warnings from a user.")
    @app_commands.describe(user="User to clear warnings from")
    async def clear_warns(self, interaction: discord.Interaction, user: Member):
        log.info(f"{interaction.user} cleared warnings from {user}")
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)

        if guild_id in warns and user_id in warns[guild_id]:
            del warns[guild_id][user_id]
            save_warns(warns)
            await interaction.response.send_message(f"Warnings from {user.mention} have been cleared.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} has no warnings.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Warn(bot))
