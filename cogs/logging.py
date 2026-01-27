import discord
from discord.ext import commands

# SET THIS TO YOUR CHANNEL ID
LOG_CHANNEL_ID = 1337449724470497362


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot: return
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(description=f"🗑️ **Message deleted in** {message.channel.mention}", color=discord.Color.orange())
            embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
            embed.add_field(name="Content", value=message.content or "No text content")
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content: return
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(description=f"📝 **Message edited in** {before.channel.mention}", color=discord.Color.blue())
            embed.set_author(name=before.author, icon_url=before.author.display_avatar.url)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))