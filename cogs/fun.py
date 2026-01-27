import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, dice: str = "1d6"):
        try:
            rolls, limit = map(int, dice.split('d'))
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(f"🎲 Result: {result}")
        except:
            await ctx.send("Format must be XdX (e.g. 1d20)")

    @commands.command()
    async def coinflip(self, ctx):
        await ctx.send(f"🪙 It's **{random.choice(['Heads', 'Tails'])}**!")

async def setup(bot):
    await bot.add_cog(Fun(bot))