import discord
import aiosqlite
import datetime
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"✅ **Banned** {member.mention} | Reason: {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"✅ **Kicked** {member.mention} | Reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🧹 Deleted {amount} messages.")
        await msg.delete(delay=3)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="No reason"):
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🔇 **Muted** {member.mention} for {minutes} mins | Reason: {reason}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):
        timestamp = str(datetime.datetime.now())
        async with aiosqlite.connect("bot.db") as db:
            await db.execute("INSERT INTO warnings VALUES (?, ?, ?, ?, ?)", 
                             (member.id, ctx.guild.id, reason, ctx.author.id, timestamp))
            await db.commit()
        await ctx.send(f"⚠️ **Warned** {member.mention} | Reason: {reason}")

    @commands.command()
    async def warnings(self, ctx, member: discord.Member):
        async with aiosqlite.connect("bot.db") as db:
            cursor = await db.execute("SELECT reason, moderator_id FROM warnings WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id))
            rows = await cursor.fetchall()
        
        if not rows:
            return await ctx.send(f"{member.name} has no warnings.")
        
        embed = discord.Embed(title=f"Warnings for {member.name}", color=discord.Color.orange())
        for idx, row in enumerate(rows, 1):
            embed.add_field(name=f"Warn #{idx}", value=f"Reason: {row[0]}\nMod: <@{row[1]}>", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))