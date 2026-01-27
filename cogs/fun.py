import discord
import random
import aiohttp
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def footer_text(self, ctx):
        return f"?{ctx.command} ▪ Executed by {ctx.author}"

    @commands.command()
    async def roll(self, ctx, dice: str = "1d6"):
        try:
            rolls, limit = map(int, dice.split('d'))
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(f"🎲 Result: {result}\n{self.footer_text(ctx)}")
        except:
            await ctx.send(f"Format must be XdX (e.g. 1d20)\n{self.footer_text(ctx)}")

    @commands.command()
    async def coinflip(self, ctx):
        await ctx.send(f"🪙 It's **{random.choice(['Heads', 'Tails'])}**!\n{self.footer_text(ctx)}")
    
    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question):
        responses = ["Yes.", "No.", "Maybe.", "Ask again later.", "Definitely!", "Unlikely."]
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {random.choice(responses)}\n{self.footer_text(ctx)}")

    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as response:
                data = await response.json()
                embed = discord.Embed(title=data['title'], url=data['postLink'], color=discord.Color.random())
                embed.set_image(url=data['url'])
                embed.set_footer(text=f"👍 {data['ups']} | Subreddit: r/{data['subreddit']}")
                await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        await ctx.send(f"✋ {ctx.author.mention} slapped {member.mention}!\n{self.footer_text(ctx)}")

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        await ctx.send(f"🫂 {ctx.author.mention} gave {member.mention} a big hug!\n{self.footer_text(ctx)}")

async def setup(bot):
    await bot.add_cog(Fun(bot))