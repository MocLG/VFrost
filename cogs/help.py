import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Bot Help Menu", color=discord.Color.green())
        
        embed.add_field(name="🛡️ Moderation", value="`?ban`, `?kick`, `?mute`, `?warn`, `?warnings`, `?purge`")
        embed.add_field(name="📈 Levels", value="`?rank`, `?leaderboard` (Auto-XP enabled)")
        embed.add_field(name="🎫 Tickets", value="`?setup_tickets`, `?close`")
        embed.add_field(name="🎮 Fun", value="`?roll`, `?coinflip`")
        
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))