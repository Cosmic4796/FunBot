import discord
from discord.ext import commands
import os
import asyncio
from pathlib import Path
import json

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has landed! 🚀')
    print(f'Bot ID: {bot.user.id}')
    print('---')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

async def load_cogs():
    """Load all cog files from the cogs directory"""
    cogs_dir = Path('./cogs')
    if not cogs_dir.exists():
        print("Cogs directory not found!")
        return
    
    for filename in cogs_dir.glob('*.py'):
        if filename.name == '__init__.py':
            continue
        
        cog_name = f'cogs.{filename.stem}'
        try:
            await bot.load_extension(cog_name)
            print(f'✅ Loaded {cog_name}')
        except Exception as e:
            print(f'❌ Failed to load {cog_name}: {e}')

async def main():
    """Main function to start the bot"""
    async with bot:
        await load_cogs()
        
        # Get token from environment variable
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            print("❌ DISCORD_TOKEN environment variable not found!")
            return
        
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
