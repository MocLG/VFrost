import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_footer(self, ctx):
        """Standard footer using display_name for 'MocLG' branding."""
        return f"?{ctx.command} ▪ Executed by {ctx.author.display_name}"

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Displays the bot's help menu."""
        
        # Creating the Embed
        embed = discord.Embed(
            title="Bot Help Menu",
            description="Use the prefix `?` before any command.",
            color=discord.Color.blue()
        )

        # 🛡️ Moderation Section
        mod_commands = (
            "* `?ban <member> [reason]`: Bans a member.\n"
            "* `?kick <member> [reason]`: Kicks a member.\n"
            "* `?unban <user_id>`: Unbans a user via ID.\n"
            "* `?mute <member> <minutes> [reason]`: Times out a member.\n"
            "* `?warn <member> [reason]`: Issues a logged warning.\n"
            "* `?warnings <member>`: Displays warning history.\n"
            "* `?purge <amount>`: Deletes recent messages.\n"
            "* `?slowmode <seconds>`: Sets channel cooldown.\n"
            "* `?lock`: Prevents messages in the channel.\n"
            "* `?unlock`: Re-enables messaging.\n"
            "* `?nick <member> <new_name>`: Changes nickname.\n"
            "* `?nuke`: Deletes and re-creates the channel."
        )
        embed.add_field(name="🛡️ Moderation", value=mod_commands, inline=False)

        # 📈 Levels Section
        level_commands = (
            "* `?rank [member]` (Aliases: ?lvl): Shows level/XP progress.\n"
            "* `?leaderboard` (Aliases: ?lb): Displays top 10 users."
        )
        embed.add_field(name="📈 Levels", value=level_commands, inline=False)

        # 🎫 Tickets Section
        ticket_commands = (
            "* `?setup_tickets`: Create a ticket system (Admin only).\n"
            "* `?close`: Closes the current ticket channel."
        )
        embed.add_field(name="🎫 Tickets", value=ticket_commands, inline=False)

        # 🎮 Fun Section
        fun_commands = (
            "* `?roll [XdX]`: Rolls dice (e.g., 2d20).\n"
            "* `?coinflip`: Flips a coin (Heads/Tails).\n"
            "* `?8ball <question>`: Magic 8-ball response.\n"
            "* `?meme`: Random meme from Reddit.\n"
            "* `?slap <member>`: Fun slap interaction.\n"
            "* `?hug <member>`: Fun hug interaction."
        )
        embed.add_field(name="🎮 Fun", value=fun_commands, inline=False)

        # 🛠️ Utility Section
        util_commands = (
            "* `?ping`: Shows the bot's current latency.\n"
            "* `?uptime`: Displays bot runtime and platform.\n"
            "* `?serverinfo`: Detailed server information.\n"
            "* `?userinfo [member]`: Detailed user information.\n"
            "* `?avatar [member]`: Shows user's profile picture."
        )
        embed.add_field(name="🛠️ Utility", value=util_commands, inline=False)

        # ❓ General Section
        embed.add_field(name="❓ General", value="* `?help`: Displays this menu.", inline=False)

        # Final Touch: Consistent Footer
        embed.set_footer(text=self.get_footer(ctx))
        
        await ctx.send(embed=embed)

async def setup(bot):
    bot.help_command = None
    await bot.add_cog(Help(bot))