import discord
import aiosqlite
import random
from discord.ext import commands

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    def get_ratelimit(self, message):
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        # Rate limit check (prevent spam XP)
        if self.get_ratelimit(message):
            return

        xp_gain = random.randint(15, 25)

        async with aiosqlite.connect("bot.db") as db:
            cursor = await db.execute("SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?", (message.author.id, message.guild.id))
            row = await cursor.fetchone()

            if row is None:
                await db.execute("INSERT INTO levels VALUES (?, ?, ?, ?)", (message.author.id, message.guild.id, xp_gain, 0))
                await db.commit()
            else:
                current_xp, current_level = row
                new_xp = current_xp + xp_gain
                new_level = int(new_xp ** 0.5 / 10) # Simple calc

                await db.execute("UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?", (new_xp, new_level, message.author.id, message.guild.id))
                await db.commit()

                if new_level > current_level:
                    await message.channel.send(f"🎉 {message.author.mention} reached **Level {new_level}**!")

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        async with aiosqlite.connect("bot.db") as db:
            cursor = await db.execute("SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id))
            row = await cursor.fetchone()

        if row:
            embed = discord.Embed(title=f"Rank: {member.name}", color=discord.Color.blue())
            embed.add_field(name="Level", value=str(row[1]))
            embed.add_field(name="XP", value=str(row[0]))
            await ctx.send(embed=embed)
        else:
            await ctx.send("User is not ranked yet.")

async def setup(bot):
    await bot.add_cog(Levels(bot))