import discord
import aiosqlite
import random
import asyncio
from discord.ext import commands

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # cooldown mapping: 1 message per 60 seconds per member
        self._cd = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
    
    def footer_text(self, ctx):
        return f"?{ctx.command} ▪ Executed by {ctx.author}"

    def get_ratelimit(self, message: discord.Message):
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bots and DMs
        if message.author.bot or not message.guild:
            return

        # Check for cooldown to prevent XP spamming
        ratelimit = self.get_ratelimit(message)
        if ratelimit:
            return

        xp_gain = random.randint(15, 25)

        async with aiosqlite.connect("bot.db") as db:
            # Check if user exists in the DB
            cursor = await db.execute(
                "SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?", 
                (message.author.id, message.guild.id)
            )
            row = await cursor.fetchone()

            if row is None:
                # New user entry
                await db.execute(
                    "INSERT INTO levels (user_id, guild_id, xp, level) VALUES (?, ?, ?, ?)", 
                    (message.author.id, message.guild.id, xp_gain, 0)
                )
                await db.commit()
            else:
                current_xp, current_level = row
                new_xp = current_xp + xp_gain
                # Formula: level = sqrt(xp) / 10
                new_level = int(new_xp ** 0.5 / 10)

                await db.execute(
                    "UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?", 
                    (new_xp, new_level, message.author.id, message.guild.id)
                )
                await db.commit()

                # Level up notification
                if new_level > current_level:
                    embed = discord.Embed(
                        description=f"🎊 {message.author.mention} has reached **Level {new_level}**!",
                        color=discord.Color.green()
                    )
                    await message.channel.send(embed=embed)

    @commands.command(name="rank", aliases=["lvl"])
    async def rank(self, ctx, member: discord.Member = None):
        """Check your current level and XP."""
        member = member or ctx.author
        async with aiosqlite.connect("bot.db") as db:
            cursor = await db.execute(
                "SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?", 
                (member.id, ctx.guild.id)
            )
            row = await cursor.fetchone()

        if row:
            xp, level = row
            next_lvl_xp = int(((level + 1) * 10) ** 2)
            xp_needed = next_lvl_xp - xp

            embed = discord.Embed(title=f"⭐ {member.display_name}'s Rank", color=discord.Color.blue())
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(name="Level", value=f"**{level}**", inline=True)
            embed.add_field(name="Total XP", value=f"**{xp}**", inline=True)
            embed.set_footer(text=f"{xp_needed} XP until Level {level + 1}\n{self.footer_text(ctx)}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"This user hasn't earned any XP yet!\n{self.footer_text(ctx)}")

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        """Displays the top 10 players in the server."""
        async with aiosqlite.connect("bot.db") as db:
            # We let SQLite handle the sorting to save RAM
            cursor = await db.execute("""
                SELECT user_id, xp, level FROM levels 
                WHERE guild_id = ? 
                ORDER BY xp DESC LIMIT 10
            """, (ctx.guild.id,))
            rows = await cursor.fetchall()

        if not rows:
            return await ctx.send(f"No one has earned XP in this server yet.\n{self.footer_text(ctx)}")

        embed = discord.Embed(title=f"🏆 {ctx.guild.name} Leaderboard", color=discord.Color.gold())
        
        description = ""
        for index, (user_id, xp, level) in enumerate(rows, start=1):
            # Attempt to get user from cache; if not found, show ID to save memory
            member = ctx.guild.get_member(user_id)
            name = member.display_name if member else f"User {user_id}"
            description += f"**{index}. {name}** — Lvl {level} ({xp} XP)\n"
        embed.description = description
        execution_line = f"\n{self.footer_text(ctx)}"
        
        await ctx.send(content=execution_line, embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))
