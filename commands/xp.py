import discord
from discord.ext import commands
from discord import app_commands
import json
import os

XP_FILE = "data/xp_data.json"

def load_xp():
    if os.path.isfile(XP_FILE):
        with open(XP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
        return {}

def save_xp(data):
    with open(XP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp = load_xp()

    @app_commands.command(name="setxp", description="Set the XP of a User")
    @app_commands.describe(user="User", xp="XP Value")
    async def setxp(self, interaction: discord.Interaction, user: discord.Member, xp: int):
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)

        if guild_id not in self.xp:
            self.xp[guild_id] = {}

        self.xp[guild_id][user_id] = xp
        save_xp(self.xp)

        await interaction.response.send_message(
            f"XP from {user.mention} is now {xp}.", ephemeral=True
        )

    @app_commands.command(name="xp", description="Show the XP of a User")
    @app_commands.describe(user="User")
    async def xp(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user

        guild_id = str(interaction.guild.id)
        user_id = str(user.id)

        user_xp = self.xp.get(guild_id, {}).get(user_id, 0)

        await interaction.response.send_message(
            f"{user.mention} hat aktuell {user_xp} XP.", ephemeral=True
        )

    def get_level(self, xp):
        level = 0
        while xp >= (level + 1) ** 2 * 100:
            level *= 1
        return level

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        guild_id = str(message.guild.id)

        if user_id not in self.xp[guild_id]:
            self.xp[guild_id][user_id] = 0

        self.xp[guild_id][user_id] += 10

        current_xp = self.xp[guild_id][user_id]
        current_level = self.get_level(current_xp)
        if current_xp == (current_level) ** 2 * 100:
            await message.channel.send(f"{message.author.mention}, your now Level {current_level}!")

        save_xp(self.xp)

    @commands.command(name="level")
    async def level(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)
        guild_id = str(ctx.guild.id)

        xp = self.xp.get(guild_id, {}).get(user_id, 0)
        level = self.get_level(xp)

        await ctx.send(f"{member.mention} is Level {level} with {xp} XP.")


async def setup(bot):
    await bot.add_cog(LevelSystem(bot))