import discord
import aiosqlite
import datetime
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def footer_text(self, ctx):
        return f"?{ctx.command} ▪ Executed by {ctx.author}"
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"✅ **Banned** {member.mention} | Reason: {reason}\n{self.footer_text(ctx)}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"✅ **Kicked** {member.mention} | Reason: {reason}\n{self.footer_text(ctx)}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🧹 Deleted {amount} messages.\n{self.footer_text(ctx)}")
        await msg.delete(delay=3)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="No reason"):
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"🔇 **Muted** {member.mention} for {minutes} mins | Reason: {reason}\n{self.footer_text(ctx)}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):
        timestamp = str(datetime.datetime.now())
        async with aiosqlite.connect("bot.db") as db:
            await db.execute("INSERT INTO warnings VALUES (?, ?, ?, ?, ?)", 
                             (member.id, ctx.guild.id, reason, ctx.author.id, timestamp))
            await db.commit()
        await ctx.send(f"⚠️ **Warned** {member.mention} | Reason: {reason}\n{self.footer_text(ctx)}")

    @commands.command()
    async def warnings(self, ctx, member: discord.Member):
        async with aiosqlite.connect("bot.db") as db:
            cursor = await db.execute("SELECT reason, moderator_id FROM warnings WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id))
            rows = await cursor.fetchall()
        
        if not rows:
            return await ctx.send(f"{member.name} has no warnings.")
        
        embed = discord.Embed(title=f"Warnings for {member.name}", color=discord.Color.orange())
        for idx, row in enumerate(rows, 1):
            embed.add_field(name=f"Warn #{idx}", value=f"Reason: {row[0]}\nMod: <@{row[1]}>\n{self.footer_text(ctx)}", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned **{user.name}**\n{self.footer_text(ctx)}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"⏲️ Slowmode set to **{seconds}** seconds.\n{self.footer_text(ctx)}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"🔒 Channel locked.\n{self.footer_text(ctx)}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"🔓 Channel unlocked.\n{self.footer_text(ctx)}")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, name: str):
        await member.edit(nick=name)
        await ctx.send(f"✅ Changed nickname for {member.mention}\n{self.footer_text(ctx)}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        """Re-creates the channel to clear all history."""
        pos = ctx.channel.position
        new_channel = await ctx.channel.clone(reason="Nuke command")
        await ctx.channel.delete()
        await new_channel.edit(position=pos)
        await new_channel.send(f"☢️ **Channel Nuked.**\n{self.footer_text(ctx)}", delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))