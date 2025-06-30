import discord
from discord.ext import commands
from discord import app_commands

class OpenTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎫")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category_name = "Open-Tickets"
        category = discord.utils.get(guild.categories, name=category_name)
        if category is None:
            category = await guild.create_category(category_name)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
        }

        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category, overwrites=overwrites)

        # Close button view
        close_view = CloseTicketButton()

        await channel.send(f"Hello {interaction.user.mention}, \nYour ticket will be done shortly.", view=close_view)
        await interaction.response.send_message(f"Ticket-{interaction.user.mention} createt!", ephemeral=True)


class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        if channel.name.startswith("ticket-"):
            await interaction.response.send_message("Ticket will close.", ephemeral=True)
            await channel.delete()
        else:
            await interaction.response.send_message("Error", ephemeral=True)


class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket", description="Create a ticket emble")
    async def ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Support Ticket",
            description="Click on the button to create a ticket.",
            color=discord.Color.blurple()
        )
        view = OpenTicketButton()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(TicketSystem(bot))
