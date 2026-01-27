import discord
from discord.ext import commands
import time
import datetime

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
    
    def footer_text(self, ctx):
        return f"?{ctx.command} ▪ Executed by {ctx.author}"

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! `{round(self.bot.latency * 1000)}ms`\n{self.footer_text(ctx)}")

    @commands.command()
    async def uptime(self, ctx):
        current_time = time.time()
        uptime_seconds = int(round(current_time - self.start_time))
        uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
        await ctx.send(f"🚀 Uptime: `{uptime_str}`\n{self.footer_text(ctx)}")

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.blue())
        embed.add_field(name="Owner", value=guild.owner.mention)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%b %d, %Y"))
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        execution_line = f"\n{self.footer_text(ctx)}"        
        await ctx.send(content=execution_line, embed=embed)
        

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"User Info: {member.name}", color=member.color)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%b %d, %Y"))
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%b %d, %Y"))
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"{member.display_avatar.url}\n{self.footer_text(ctx)}")

async def setup(bot):
    await bot.add_cog(Utility(bot))