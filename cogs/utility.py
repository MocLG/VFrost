import discord
from discord.ext import commands
import time
import datetime

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
    
    def get_footer(self, ctx):
        """Standard footer using display_name for 'MocLG' branding."""
        return f"?{ctx.command} ▪ Executed by {ctx.author.display_name}"

    async def send_embed(self, ctx, description, color=discord.Color.blue()):
        """Helper to send a uniform embed response."""
        embed = discord.Embed(description=description, color=color)
        embed.set_footer(text=self.get_footer(ctx))
        return await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Shows the bot's latency."""
        latency = round(self.bot.latency * 1000)
        await self.send_embed(ctx, f"🏓 **Pong!** Delay: `{latency}ms`", discord.Color.green())

    @commands.command()
    async def uptime(self, ctx):
        """Displays how long the bot has been running."""
        uptime_seconds = int(round(time.time() - self.start_time))
        uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
        
        embed = discord.Embed(title="🚀 Bot Status", color=discord.Color.blue())
        embed.add_field(name="Uptime", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="Platform", value="Android (NetHunter)", inline=True)
        embed.set_footer(text=self.get_footer(ctx))
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        """Detailed information about the current server."""
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.blue())
        
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Member Count", value=f"`{guild.member_count}`", inline=True)
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%b %d, %Y"), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        embed.set_footer(text=self.get_footer(ctx))
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Detailed information about a specific user."""
        member = member or ctx.author
        
        embed = discord.Embed(title=f"User Info: {member.display_name}", color=member.color)
        embed.add_field(name="Global Name", value=f"`{member}`", inline=True)
        embed.add_field(name="ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%b %d, %Y"), inline=False)
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%b %d, %Y"), inline=False)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=self.get_footer(ctx))
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """Shows a user's profile picture."""
        member = member or ctx.author
        embed = discord.Embed(title=f"Avatar: {member.display_name}", color=discord.Color.random())
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=self.get_footer(ctx))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))