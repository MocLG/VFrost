import discord
from discord.ext import commands

# SET THIS TO YOUR CHANNEL ID
LOG_CHANNEL_ID = 1337449724470497362

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_log_footer(self, user):
        """Standard footer for logs to keep style consistent."""
        # This shows the user who triggered the event and your bot's identity
        return f"User ID: {user.id} ▪ Logged by GeminiBot"

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return
            
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            return

        embed = discord.Embed(
            description=f"🗑️ **Message deleted in** {message.channel.mention}", 
            color=discord.Color.orange(),
            timestamp=message.created_at
        )
        embed.set_author(name=f"{message.author.display_name} ({message.author})", icon_url=message.author.display_avatar.url)
        
        # Handling empty messages (like images or embeds)
        content = message.content if message.content else "*No text content (likely an image or embed)*"
        embed.add_field(name="Content", value=content, inline=False)
        
        embed.set_footer(text=self.get_log_footer(message.author))
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content or not before.guild:
            return
            
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            return

        embed = discord.Embed(
            description=f"📝 **Message edited in** {before.channel.mention}", 
            color=discord.Color.blue(),
            timestamp=after.edited_at or discord.utils.utcnow()
        )
        embed.set_author(name=f"{before.author.display_name} ({before.author})", icon_url=before.author.display_avatar.url)
        
        # Truncate content if it's too long for an embed field (prevents crashes)
        before_content = (before.content[:1021] + '...') if len(before.content) > 1024 else before.content
        after_content = (after.content[:1021] + '...') if len(after.content) > 1024 else after.content

        embed.add_field(name="Before", value=before_content or "*Empty*", inline=False)
        embed.add_field(name="After", value=after_content or "*Empty*", inline=False)
        
        embed.set_footer(text=self.get_log_footer(before.author))
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))