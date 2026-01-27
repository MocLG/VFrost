import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def footer_text(self, ctx):
        return f"?{ctx.command} ▪ Executed by {ctx.author}"

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
            "* `?setup_tickets`: Embed with a ticket button (Admin only).\n"
            "* `?close`: Closes the current ticket channel."
        )
        embed.add_field(name="🎫 Tickets", value=ticket_commands, inline=False)

        # 🎮 Fun Section
        fun_commands = (
            "* `?roll [XdX]`: Rolls dice (e.g., 2d20). Default 1d6.\n"
            "* `?coinflip`: Flips a coin (Heads/Tails).\n"
            "* `?8ball <question>`: Magic 8-ball response.\n"
            "* `?meme`: Random meme from Reddit.\n"
            "* `?slap <member>`: Sends a fun slap interaction.\n"
            "* `?hug <member>`: Sends a fun hug interaction."
        )
        embed.add_field(name="🎮 Fun", value=fun_commands, inline=False)

        # 🛠️ Utility Section
        util_commands = (
            "* `?ping`: Shows the bot's current latency.\n"
            "* `?uptime`: Displays how long the bot has been live.\n"
            "* `?serverinfo`: Detailed server information.\n"
            "* `?userinfo [member]`: Detailed user information.\n"
            "* `?avatar [member]`: Shows user's profile picture."
        )
        embed.add_field(name="🛠️ Utility", value=util_commands, inline=False)

        # ❓ General Section
        general_commands = "* `?help`: Displays this menu."
        embed.add_field(name="❓ General", value=general_commands, inline=False)

        execution_line = f"\n{self.footer_text(ctx)}"
        
        await ctx.send(content=execution_line, embed=embed)

async def setup(bot):
    bot.help_command = None
    await bot.add_cog(Help(bot))