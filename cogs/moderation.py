import discord
import aiosqlite
import datetime
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_footer(self, ctx):
        """Helper to generate the standard footer text."""
        return f"?{ctx.command} ▪ Executed by {ctx.author.display_name}"

    async def send_embed(self, ctx, description, color=discord.Color.blue()):
        """Helper to send a uniform embed response."""
        embed = discord.Embed(description=description, color=color)
        embed.set_footer(text=self.get_footer(ctx))
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await self.send_embed(ctx, f"✅ **Banned** {member.mention} | **Reason:** {reason}", discord.Color.red())

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await self.send_embed(ctx, f"✅ **Kicked** {member.mention} | **Reason:** {reason}", discord.Color.orange())

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(description=f"🧹 Deleted **{amount}** messages.", color=discord.Color.purple())
        embed.set_footer(text=self.get_footer(ctx))
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=3)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="No reason"):
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await self.send_embed(ctx, f"🔇 **Muted** {member.mention} for **{minutes}m** | **Reason:** {reason}", discord.Color.light_grey())

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):
        timestamp = str(datetime.datetime.now())
        async with aiosqlite.connect("bot.db") as db:
            await db.execute("INSERT INTO warnings VALUES (?, ?, ?, ?, ?)", 
                             (member.id, ctx.guild.id, reason, ctx.author.id, timestamp))
            await db.commit()
        await self.send_embed(ctx, f"⚠️ **Warned** {member.mention} | **Reason:** {reason}", discord.Color.gold())

    @commands.command()
    async def warnings(self, ctx, member: discord.Member):
        async with aiosqlite.connect("bot.db") as db:
            cursor = await db.execute("SELECT reason, moderator_id FROM warnings WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id))
            rows = await cursor.fetchall()
        
        if not rows:
            return await self.send_embed(ctx, f"✅ {member.display_name} has no warnings.", discord.Color.green())
        
        embed = discord.Embed(title=f"Warnings for {member.display_name}", color=discord.Color.orange())
        for idx, row in enumerate(rows, 1):
            embed.add_field(name=f"Warn #{idx}", value=f"**Reason:** {row[0]}\n**Mod:** <@{row[1]}>", inline=False)
        
        embed.set_footer(text=self.get_footer(ctx))
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await self.send_embed(ctx, f"✅ Unbanned **{user.name}**", discord.Color.green())

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await self.send_embed(ctx, f"⏲️ Slowmode set to **{seconds}** seconds.", discord.Color.blue())

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await self.send_embed(ctx, "🔒 Channel locked.", discord.Color.dark_red())

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await self.send_embed(ctx, "🔓 Channel unlocked.", discord.Color.dark_green())

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, name: str):
        await member.edit(nick=name)
        await self.send_embed(ctx, f"✅ Changed nickname for {member.mention} to **{name}**", discord.Color.blue())

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        pos = ctx.channel.position
        new_channel = await ctx.channel.clone(reason="Nuke command")
        await ctx.channel.delete()
        await new_channel.edit(position=pos)
        
        embed = discord.Embed(description="☢️ **Channel Nuked.**", color=discord.Color.red())
        embed.set_footer(text=self.get_footer(ctx))
        await new_channel.send(embed=embed, delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))