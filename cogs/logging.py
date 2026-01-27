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
        
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
            embed.add_field(name="User", value=message.author.mention)
            embed.add_field(name="Content", value=message.content or "[Content not cached]")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content: return

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            embed = discord.Embed(title="Message Edited", color=discord.Color.blue())
            embed.add_field(name="User", value=before.author.mention)
            embed.add_field(name="Before", value=before.content or "[Not cached]", inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))