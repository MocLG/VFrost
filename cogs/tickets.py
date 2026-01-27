import discord
from discord.ext import commands
import asyncio

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Persistent view for 128MB stability

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green, custom_id="ticket_button", emoji="📩")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        
        # Permissions setup
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # Create channel using display_name for cleaner look
        channel = await guild.create_text_channel(f"ticket-{interaction.user.display_name}", overwrites=overwrites)
        
        # Ticket Welcome Embed
        embed = discord.Embed(
            title="Ticket Opened",
            description=f"Hello {interaction.user.mention},\nStaff will be with you shortly.\n\nUse `?close` to end this session.",
            color=discord.Color.green()
        )
        # Using interaction for footer since ctx isn't available here
        embed.set_footer(text=f"Ticket System ▪ Created by {interaction.user.display_name}")
        
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Ticket created at {channel.mention}", ephemeral=True)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_footer(self, ctx):
        """Standard footer using display_name for 'MocLG' branding."""
        return f"?{ctx.command} ▪ Executed by {ctx.author.display_name}"

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_tickets(self, ctx):
        """Sends the persistent button to open tickets."""
        embed = discord.Embed(
            title="🎫 Support System", 
            description="Need help? Click the button below to open a private support ticket.", 
            color=discord.Color.blue()
        )
        embed.set_footer(text=self.get_footer(ctx))
        # We pass the view here
        await ctx.send(embed=embed, view=TicketView())

    @commands.command()
    async def close(self, ctx):
        """Closes the ticket channel."""
        if "ticket-" in ctx.channel.name:
            embed = discord.Embed(
                description="🔒 **Closing ticket in 5 seconds...**",
                color=discord.Color.red()
            )
            embed.set_footer(text=self.get_footer(ctx))
            await ctx.send(embed=embed)
            
            await asyncio.sleep(5)
            await ctx.channel.delete()
        else:
            # Error if used outside a ticket channel
            error_embed = discord.Embed(
                description="❌ This command can only be used in a ticket channel.",
                color=discord.Color.red()
            )
            error_embed.set_footer(text=self.get_footer(ctx))
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Tickets(bot))