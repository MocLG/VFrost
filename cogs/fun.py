import discord
import random
import aiohttp
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_footer(self, ctx):
        """Standard footer for all embeds."""
        return f"?{ctx.command} ▪ Executed by {ctx.author.display_name}"

    async def send_embed(self, ctx, description, color=discord.Color.blue()):
        """Helper to send a uniform embed response."""
        embed = discord.Embed(description=description, color=color)
        embed.set_footer(text=self.get_footer(ctx))
        return await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx, dice: str = "1d6"):
        """Rolls dice in XdX format."""
        try:
            rolls, limit = map(int, dice.split('d'))
            if rolls > 20: return await self.send_embed(ctx, "❌ Keep it under 20 dice to save my RAM!", discord.Color.red())
            
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await self.send_embed(ctx, f"🎲 **Dice Results:** {result}", discord.Color.purple())
        except Exception:
            await self.send_embed(ctx, "❌ Format must be **XdX** (e.g., 1d20 or 2d6).", discord.Color.red())

    @commands.command()
    async def coinflip(self, ctx):
        """Flips a coin."""
        side = random.choice(['Heads', 'Tails'])
        await self.send_embed(ctx, f"🪙 The coin landed on: **{side}**", discord.Color.gold())
    
    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question: str):
        """Ask the magic 8-ball a question."""
        responses = ["Yes.", "No.", "Maybe.", "Ask again later.", "Definitely!", "Unlikely."]
        answer = random.choice(responses)
        
        embed = discord.Embed(title="🎱 Magic 8-Ball", color=discord.Color.dark_magenta())
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=f"**{answer}**", inline=False)
        embed.set_footer(text=self.get_footer(ctx))
        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        """Fetches a random meme from Reddit."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as response:
                if response.status != 200:
                    return await self.send_embed(ctx, "❌ Failed to fetch a meme. Try again later.", discord.Color.red())
                
                data = await response.json()
                embed = discord.Embed(title=data['title'], url=data['postLink'], color=discord.Color.random())
                embed.set_image(url=data['url'])
                
                # Combined footer: Meme data + Execution info
                footer_info = f"👍 {data['ups']} | r/{data['subreddit']} | {self.get_footer(ctx)}"
                embed.set_footer(text=footer_info)
                await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        """Slaps a member."""
        await self.send_embed(ctx, f"✋ {ctx.author.mention} slapped {member.mention}!", discord.Color.dark_red())

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        """Hugs a member."""
        await self.send_embed(ctx, f"🫂 {ctx.author.mention} gave {member.mention} a warm hug!", discord.Color.teal())

async def setup(bot):
    await bot.add_cog(Fun(bot))