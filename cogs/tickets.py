import discord
from discord.ext import commands
import asyncio

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Persistent view

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green, custom_id="ticket_button", emoji="📩")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
        await channel.send(f"Welcome {interaction.user.mention}, staff will be with you shortly. Use `?close` to end this ticket.")
        await interaction.response.send_message(f"Ticket created at {channel.mention}", ephemeral=True)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_tickets(self, ctx):
        embed = discord.Embed(title="Support Tickets", description="Click the button below to open a ticket.", color=discord.Color.blue())
        await ctx.send(embed=embed, view=TicketView())

    @commands.command()
    async def close(self, ctx):
        if "ticket-" in ctx.channel.name:
            await ctx.send("Closing ticket in 5 seconds...")
            await asyncio.sleep(5)
            await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))