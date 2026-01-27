import discord
import os
import aiosqlite
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# --- MEMORY OPTIMIZATION FOR 128MB RAM ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = False


bot = commands.Bot(
    command_prefix="?",
    intents=intents,
    max_messages=50, 
    chunk_guilds_at_startup=False,
    help_command=None
)

# Database Setup
async def init_db():
    async with aiosqlite.connect("bot.db") as db:
        # Warnings Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER,
                guild_id INTEGER,
                reason TEXT,
                moderator_id INTEGER,
                timestamp TEXT
            )
        """)
        # Levels Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS levels (
                user_id INTEGER,
                guild_id INTEGER,
                xp INTEGER,
                level INTEGER,
                PRIMARY KEY (user_id, guild_id)
            )
        """)
        await db.commit()

@bot.event
async def on_ready():
    await init_db()
    print(f"Logged in as {bot.user} on {len(bot.guilds)} servers.")
    print("Memory Optimization: Active (Member Cache Disabled)")
    
    # Load Cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    try:
        bot.run(os.getenv("TOKEN"))
    except Exception as e:
        print(f"Error: {e}")