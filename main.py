# =============================================
#             CONFIGURATION SECTION
# =============================================
# All customizable settings are in this section

# Bot Identity
BOT_NAME = "Fun.Bot"
OWNER_ID = 928108286916583474  # Your Discord user ID
COMMAND_PREFIX = "/"           # Not used for slash commands
CURRENCY = "$"                 # Currency symbol

# Economy Settings
STARTING_BALANCE = 1000        # New users start with this
WORK_MIN_EARNINGS = 50         # Minimum from /work
WORK_MAX_EARNINGS = 150        # Maximum from /work
WORK_COOLDOWN = 3600           # 1 hour cooldown (seconds)
DAILY_REWARD = 500             # Base daily amount
BEG_MIN = 1                    # Minimum from /beg
BEG_MAX = 100                  # Maximum from /beg
BEG_CHANCE = 0.7               # 70% success chance
ROB_MIN_FINE = 50              # Minimum robbery fine
ROB_MAX_FINE = 200             # Maximum robbery fine
ROB_CHANCE = 0.3               # 30% robbery success chance

# Lottery Settings
LOTTERY_WIN_CHANCE = 650       # 1 in 650 chance
LOTTERY_MIN_PRIZE = 10000      # Minimum jackpot
LOTTERY_MAX_PRIZE = 100000     # Maximum jackpot
LOTTERY_START_PRIZE = 50000    # Starting jackpot
LOTTERY_TICKET_PRICE = 500     # Price per ticket
LOTTERY_MAX_STOCK = 15         # Max tickets per server

# Shop Settings
SHOP_RESET_MINUTES = 10        # How often shop restocks
NEWS_CHANCE = 0.2              # 20% chance for news
PRICE_CHANGE_RANGE = (-0.3, 0.2)  # Min/max price changes
STOCK_CHANGE_RANGE = (-2, 3)   # Stock fluctuation range

# Fishing Settings
FISH_COOLDOWN = 900            # 15 minutes
FISHING_ROD_USES = 10          # Uses before breaking

# Data Management
DATA_FILE = "economy_data.json" # Save file location
DATA_BACKUP_MINUTES = 30       # Auto-save interval

# =============================================
#             GLOBAL VARIABLES
# =============================================

CURRENT_LOTTERY_PRIZE = LOTTERY_START_PRIZE
economy_data = {}
server_shops = {}
active_news = {}
lottery_winners = []

# Base shop items with enhanced descriptions
BASE_SHOP_ITEMS = {
    "padlock": {
        "name": "🔒 Padlock",
        "base_price": 800,
        "description": "Protects against one robbery attempt",
        "emoji": "🔒",
        "usable": True,
        "max_stock": 10
    },
    "fishingrod": {
        "name": "🎣 Fishing Rod",
        "base_price": 1200,
        "description": f"Catch fish for money! ({FISHING_ROD_USES} uses)",
        "emoji": "🎣",
        "usable": False,
        "max_stock": 8
    },
    "luckycoin": {
        "name": "🍀 Lucky Coin",
        "base_price": 1500,
        "description": "+10% gambling win chance (permanent)",
        "emoji": "🍀",
        "usable": True,
        "max_stock": 5
    },
    "workboost": {
        "name": "⚡ Work Boost",
        "base_price": 1000,
        "description": "+50% work earnings for 24 hours",
        "emoji": "⚡",
        "usable": True,
        "max_stock": 7
    },
    "lotteryticket": {
        "name": "🎫 Lottery Ticket",
        "base_price": LOTTERY_TICKET_PRICE,
        "description": f"Scratch to win! Current jackpot: {CURRENCY}{LOTTERY_START_PRIZE:,}",
        "emoji": "🎫",
        "usable": True,
        "max_stock": LOTTERY_MAX_STOCK
    },
    "diamondring": {
        "name": "💎 Diamond Ring",
        "base_price": 3000,
        "description": "+20% begging success rate (permanent)",
        "emoji": "💎",
        "usable": True,
        "max_stock": 3
    },
    "energydrink": {
        "name": "⚡ Energy Drink",
        "base_price": 250,
        "description": "Reduces all cooldowns by 30 minutes",
        "emoji": "⚡",
        "usable": True,
        "max_stock": 12
    },
    "multiplier": {
        "name": "✨ 2x Multiplier",
        "base_price": 2500,
        "description": "Double all earnings for 1 hour",
        "emoji": "✨",
        "usable": True,
        "max_stock": 4
    }
}

# Fish types for fishing system
FISH_TYPES = {
    "common": {
        "fish": ["🐟 Sardine", "🐠 Goldfish", "🦐 Shrimp"],
        "value_range": (20, 80),
        "chance": 0.6
    },
    "rare": {
        "fish": ["🐡 Pufferfish", "🦞 Lobster", "🐙 Octopus"],
        "value_range": (100, 300),
        "chance": 0.25
    },
    "legendary": {
        "fish": ["🦈 Shark", "🐳 Whale", "🐉 Sea Dragon"],
        "value_range": (500, 1500),
        "chance": 0.1
    },
    "mythic": {
        "fish": ["👑 Golden Fish", "💎 Diamond Fish", "🌟 Cosmic Fish"],
        "value_range": (2000, 5000),
        "chance": 0.05
    }
}

# =============================================
#             BOT IMPLEMENTATION
# =============================================

import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import json
import os
from datetime import datetime, timedelta
import asyncio
from typing import Optional

# Initialize bot with enhanced intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# =============================================
#             UTILITY FUNCTIONS
# =============================================

def load_data():
    """Load all bot data from JSON file"""
    global economy_data, server_shops, CURRENT_LOTTERY_PRIZE
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                economy_data = data.get("economy", {})
                server_shops = data.get("shops", {})
                CURRENT_LOTTERY_PRIZE = data.get("lottery_prize", LOTTERY_START_PRIZE)
        except Exception as e:
            print(f"Error loading data: {e}")
    update_lottery_description()

def save_data():
    """Save all bot data to JSON file"""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump({
                "economy": economy_data,
                "shops": server_shops,
                "lottery_prize": CURRENT_LOTTERY_PRIZE
            }, f, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")

def update_lottery_description():
    """Update lottery ticket description with current jackpot"""
    BASE_SHOP_ITEMS["lotteryticket"]["description"] = (
        f"Scratch to win! Current jackpot: {CURRENCY}{CURRENT_LOTTERY_PRIZE:,}"
    )

def get_user_data(user_id: int) -> dict:
    """Get or create user data"""
    user_id_str = str(user_id)
    if user_id_str not in economy_data:
        economy_data[user_id_str] = {
            "balance": STARTING_BALANCE,
            "inventory": {},
            "stats": {
                "times_worked": 0,
                "times_gambled": 0,
                "times_fished": 0,
                "total_earned": 0,
                "total_spent": 0,
                "lottery_wins": 0,
                "fish_caught": 0
            },
            "cooldowns": {},
            "multipliers": {},
            "daily_streak": 0
        }
    return economy_data[user_id_str]

def get_server_shop(guild_id: int) -> dict:
    """Get or create server shop data"""
    guild_id_str = str(guild_id)
    if guild_id_str not in server_shops:
        server_shops[guild_id_str] = {
            "items": {},
            "last_reset": datetime.now().timestamp()
        }
        # Initialize shop items
        for item_id, item_data in BASE_SHOP_ITEMS.items():
            server_shops[guild_id_str]["items"][item_id] = {
                "price": item_data["base_price"],
                "stock": random.randint(1, item_data["max_stock"] // 2)
            }
    return server_shops[guild_id_str]

def update_server_shop(guild_id: int):
    """Update server shop prices and stock"""
    shop = get_server_shop(guild_id)
    
    for item_id, item_data in BASE_SHOP_ITEMS.items():
        if item_id not in shop["items"]:
            shop["items"][item_id] = {
                "price": item_data["base_price"],
                "stock": random.randint(1, item_data["max_stock"] // 2)
            }
        else:
            # Update stock
            stock_change = random.randint(*STOCK_CHANGE_RANGE)
            new_stock = shop["items"][item_id]["stock"] + stock_change
            shop["items"][item_id]["stock"] = max(1, min(new_stock, item_data["max_stock"]))
            
            # Update price
            price_change = random.uniform(*PRICE_CHANGE_RANGE)
            new_price = int(shop["items"][item_id]["price"] * (1 + price_change))
            shop["items"][item_id]["price"] = max(
                item_data["base_price"] // 2,
                min(item_data["base_price"] * 2, new_price)
            )
    
    shop["last_reset"] = datetime.now().timestamp()
    save_data()

def get_balance(user_id: int) -> int:
    """Get user's current balance"""
    return get_user_data(user_id)["balance"]

def update_balance(user_id: int, amount: int, apply_multiplier: bool = True) -> int:
    """Update user balance and apply multipliers if applicable"""
    user_data = get_user_data(user_id)
    
    # Apply 2x multiplier if active and earning money
    if apply_multiplier and amount > 0 and is_multiplier_active(user_id):
        amount *= 2
    
    user_data["balance"] += amount
    
    # Update stats
    if amount > 0:
        user_data["stats"]["total_earned"] += amount
    else:
        user_data["stats"]["total_spent"] += abs(amount)
    
    save_data()
    return user_data["balance"]

def add_item_to_inventory(user_id: int, item_name: str, quantity: int = 1, data: dict = None):
    """Add item to user inventory"""
    user_data = get_user_data(user_id)
    inventory = user_data["inventory"]
    
    if item_name in inventory:
        inventory[item_name]["quantity"] += quantity
        if data and "durability" in data:
            inventory[item_name]["data"] = data
    else:
        inventory[item_name] = {
            "quantity": quantity,
            "data": data or {}
        }
    save_data()

def remove_item_from_inventory(user_id: int, item_name: str, quantity: int = 1) -> bool:
    """Remove item from user inventory"""
    user_data = get_user_data(user_id)
    inventory = user_data["inventory"]
    
    if item_name in inventory and inventory[item_name]["quantity"] >= quantity:
        if inventory[item_name]["quantity"] <= quantity:
            del inventory[item_name]
        else:
            inventory[item_name]["quantity"] -= quantity
        save_data()
        return True
    return False

def has_item(user_id: int, item_name: str) -> bool:
    """Check if user has item"""
    inventory = get_user_data(user_id).get("inventory", {})
    return item_name in inventory and inventory[item_name]["quantity"] > 0

def check_cooldown(user_id: int, cooldown_type: str) -> int:
    """Check remaining cooldown time"""
    last_used = get_user_data(user_id).get("cooldowns", {}).get(cooldown_type, 0)
    current_time = int(datetime.now().timestamp())
    return max(0, last_used - current_time)

def set_cooldown(user_id: int, cooldown_type: str, duration_seconds: int):
    """Set cooldown for user"""
    user_data = get_user_data(user_id)
    if "cooldowns" not in user_data:
        user_data["cooldowns"] = {}
    user_data["cooldowns"][cooldown_type] = int(datetime.now().timestamp()) + duration_seconds
    save_data()

def reduce_cooldowns(user_id: int, reduction_seconds: int):
    """Reduce all cooldowns by specified amount"""
    user_data = get_user_data(user_id)
    cooldowns = user_data.get("cooldowns", {})
    current_time = int(datetime.now().timestamp())
    
    for cooldown_type in cooldowns:
        if cooldowns[cooldown_type] > current_time:
            cooldowns[cooldown_type] = max(current_time, cooldowns[cooldown_type] - reduction_seconds)
    
    save_data()

def is_multiplier_active(user_id: int) -> bool:
    """Check if 2x multiplier is active"""
    user_data = get_user_data(user_id)
    multiplier_end = user_data.get("multipliers", {}).get("2x_end", 0)
    return multiplier_end > datetime.now().timestamp()

def format_time(seconds: int) -> str:
    """Format seconds into readable time"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def create_embed(title: str, description: str = "", color = discord.Color.blue()) -> discord.Embed:
    """Create a standardized embed"""
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=f"{BOT_NAME} • Economy Bot")
    embed.timestamp = datetime.now()
    return embed

# =============================================
#             BACKGROUND TASKS
# =============================================

@tasks.loop(minutes=SHOP_RESET_MINUTES)
async def shop_reset_task():
    """Reset shop prices and stock periodically"""
    for guild_id_str in server_shops:
        update_server_shop(int(guild_id_str))
    
    # Random news events
    if random.random() < NEWS_CHANCE:
        await trigger_news_event()

@tasks.loop(minutes=DATA_BACKUP_MINUTES)
async def data_backup_task():
    """Auto-save data periodically"""
    save_data()

async def trigger_news_event():
    """Trigger a random news event affecting prices"""
    item_id = random.choice(list(BASE_SHOP_ITEMS.keys()))
    price_change = random.choice([-30, -20, -15, 10, 15, 20])
    duration = random.randint(2, 8)  # 2-8 minutes
    
    # Apply to all servers
    for guild_id_str in server_shops:
        if item_id in server_shops[guild_id_str]["items"]:
            current_price = server_shops[guild_id_str]["items"][item_id]["price"]
            new_price = max(
                BASE_SHOP_ITEMS[item_id]["base_price"] // 2,
                int(current_price * (1 + price_change / 100))
            )
            server_shops[guild_id_str]["items"][item_id]["price"] = new_price
    
    # Announce to all servers
    item_data = BASE_SHOP_ITEMS[item_id]
    embed = create_embed(
        "📰 BREAKING NEWS",
        f"**{item_data['name']} prices {'surged' if price_change > 0 else 'crashed'} by {abs(price_change)}%!**\n"
        f"This effect will last for {duration} minutes.",
        discord.Color.red() if price_change > 0 else discord.Color.green()
    )
    
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    await channel.send(embed=embed)
                    break
                except:
                    continue
    
    # Reset after duration
    await asyncio.sleep(duration * 60)
    for guild_id_str in server_shops:
        update_server_shop(int(guild_id_str))

# =============================================
#             BOT EVENTS
# =============================================

@bot.event
async def on_ready():
    """Bot startup event"""
    print(f'🚀 {BOT_NAME} has connected to Discord!')
    print(f'📊 Loaded {len(economy_data)} users and {len(server_shops)} server shops')
    
    try:
        synced = await bot.tree.sync()
        print(f"⚡ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")
    
    # Start background tasks
    if not shop_reset_task.is_running():
        shop_reset_task.start()
    if not data_backup_task.is_running():
        data_backup_task.start()
    
    print("✅ Bot is ready!")

# =============================================
#             ECONOMY COMMANDS
# =============================================

@bot.tree.command(name="balance", description="💰 Check your or someone else's balance")
async def balance(interaction: discord.Interaction, user: Optional[discord.User] = None):
    target = user or interaction.user
    bal = get_balance(target.id)
    user_data = get_user_data(target.id)
    
    embed = create_embed(f"💰 {target.display_name}'s Balance", color=discord.Color.gold())
    embed.add_field(name="Balance", value=f"{CURRENCY}{bal:,}", inline=True)
    
    # Show multiplier status
    if is_multiplier_active(target.id):
        multiplier_end = user_data.get("multipliers", {}).get("2x_end", 0)
        time_left = int(multiplier_end - datetime.now().timestamp())
        embed.add_field(name="✨ Active Multiplier", value=f"2x for {format_time(time_left)}", inline=True)
    
    embed.set_thumbnail(url=target.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="work", description="⚡ Work to earn money")
async def work(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_data = get_user_data(user_id)
    
    # Check cooldown
    cooldown_left = check_cooldown(user_id, "work")
    if cooldown_left > 0:
        embed = create_embed(
            "😴 Too Tired to Work",
            f"You need to rest! Try again in **{format_time(cooldown_left)}**",
            discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    # Calculate earnings with boosts
    base_amount = random.randint(WORK_MIN_EARNINGS, WORK_MAX_EARNINGS)
    multiplier = 1.0
    boost_msg = ""
    
    # Work boost check
    if has_item(user_id, "workboost"):
        boost_end = user_data.get("cooldowns", {}).get("workboost", 0)
        if boost_end > datetime.now().timestamp():
            multiplier *= 1.5
            boost_msg += " (Work Boost Active!)"
    
    amount = int(base_amount * multiplier)
    new_balance = update_balance(user_id, amount)
    
    # Update stats and cooldown
    user_data["stats"]["times_worked"] += 1
    set_cooldown(user_id, "work", WORK_COOLDOWN)
    
    jobs = [
        ("💻 Programming", "You coded a web application"),
        ("🚚 Delivery", "You delivered packages across town"),
        ("☕ Barista", "You served coffee and pastries"),
        ("🔨 Construction", "You helped build a house"),
        ("📝 Freelancing", "You completed a writing project"),
        ("🎨 Graphic Design", "You created stunning visuals"),
        ("🏪 Retail", "You helped customers at the store"),
        ("🚗 Rideshare", "You drove passengers around the city")
    ]
    
    job_emoji, job_desc = random.choice(jobs)
    
    embed = create_embed(f"{job_emoji} Work Complete!", color=discord.Color.green())
    embed.add_field(name="Job", value=job_desc, inline=False)
    embed.add_field(name="Earnings", value=f"{CURRENCY}{amount:,}{boost_msg}", inline=True)
    embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily", description="🎁 Claim your daily reward")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_data = get_user_data(user_id)
    
    # Check cooldown
    cooldown_left = check_cooldown(user_id, "daily")
    if cooldown_left > 0:
        embed = create_embed(
            "⏰ Daily Already Claimed",
            f"Come back in **{format_time(cooldown_left)}** for your next daily!",
            discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    # Calculate daily amount with streak bonus
    streak = user_data.get("daily_streak", 0) + 1
    bonus_amount = min(1000, streak * 25)  # Max 1000 bonus
    total_amount = DAILY_REWARD + bonus_amount
    
    # Update balance and streak
    new_balance = update_balance(user_id, total_amount)
    set_cooldown(user_id, "daily", 86400)  # 24 hours
    user_data["daily_streak"] = streak
    save_data()
    
    embed = create_embed("🎁 Daily Reward Claimed!", color=discord.Color.gold())
    embed.add_field(name="Base Reward", value=f"{CURRENCY}{DAILY_REWARD:,}", inline=True)
    embed.add_field(name="Streak Bonus", value=f"{CURRENCY}{bonus_amount:,}", inline=True)
    embed.add_field(name="Total Earned", value=f"{CURRENCY}{total_amount:,}", inline=True)
    embed.add_field(name="Current Streak", value=f"{streak} days", inline=True)
    embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="beg", description="🤲 Beg for money from strangers")
async def beg(interaction: discord.Interaction):
    user_id = interaction.user.id
    
    # Check for diamond ring boost
    success_chance = BEG_CHANCE
    if has_item(user_id, "diamondring"):
        success_chance += 0.2  # +20% success rate
    
    if random.random() < success_chance:
        amount = random.randint(BEG_MIN, BEG_MAX)
        new_balance = update_balance(user_id, amount)
        
        success_messages = [
            ("💝", "A kind stranger took pity on you"),
            ("💰", "You found money someone dropped"),
            ("🎩", "A generous person gave you a tip"),
            ("✨", "Lady luck smiled upon you"),
            ("💎", "Someone appreciated your honesty")
        ]
        
        emoji, message = random.choice(success_messages)
        embed = create_embed(f"{emoji} Begging Success!", color=discord.Color.green())
        embed.add_field(name="Result", value=f"{message} and gave you {CURRENCY}{amount:,}!", inline=False)
        embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    else:
        failure_messages = [
            ("😔", "Everyone ignored you completely"),
            ("🚶", "People walked past without noticing"),
            ("😤", "Someone told you to get a job"),
            ("🙄", "You were shooed away by security"),
            ("😕", "Not a single person stopped to help")
        ]
        
        emoji, message = random.choice(failure_messages)
        embed = create_embed(f"{emoji} No Luck Today", color=discord.Color.red())
        embed.add_field(name="Result", value=message, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="fish", description="🎣 Go fishing to catch valuable fish")
async def fish(interaction: discord.Interaction):
    user_id = interaction.user.id
    
    # Check for fishing rod
    if not has_item(user_id, "fishingrod"):
        embed = create_embed(
            "🎣 No Fishing Rod",
            "You need a fishing rod to go fishing! Buy one from the shop.",
            discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    # Check cooldown
    cooldown_left = check_cooldown(user_id, "fish")
    if cooldown_left > 0:
        embed = create_embed(
            "🐟 Fishing Cooldown",
            f"The fish need time to return! Try again in **{format_time(cooldown_left)}**",
            discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    # Determine fish rarity
    rand = random.random()
    if rand < FISH_TYPES["common"]["chance"]:
        rarity = "common"
        color = discord.Color.green()
    elif rand < FISH_TYPES["common"]["chance"] + FISH_TYPES["rare"]["chance"]:
        rarity = "rare"
        color = discord.Color.blue()
    elif rand < (FISH_TYPES["common"]["chance"] + FISH_TYPES["rare"]["chance"] + 
                FISH_TYPES["legendary"]["chance"]):
        rarity = "legendary"
        color = discord.Color.purple()
    else:
        rarity = "mythic"
        color = discord.Color.gold()
    
    # Get random fish and value
    fish_data = FISH_TYPES[rarity]
    fish_name = random.choice(fish_data["fish"])
    fish_value = random.randint(*fish_data["value_range"])
    
    # Update balance and stats
    new_balance = update_balance(user_id, fish_value)
    user_data = get_user_data(user_id)
    user_data["stats"]["times_fished"] += 1
    user_data["stats"]["fish_caught"] += 1
    
    # Use fishing rod durability
    inventory = user_data["inventory"]["fishingrod"]
    if "durability" not in inventory["data"]:
        inventory["data"]["durability"] = FISHING_ROD_USES
    
    inventory["data"]["durability"] -= 1
    durability_msg = ""
    
    if inventory["data"]["durability"] <= 0:
        remove_item_from_inventory(user_id, "fishingrod")
        durability_msg = "\n🔥 Your fishing rod broke!"
    
    # Set cooldown
    set_cooldown(user_id, "fish", FISH_COOLDOWN)
    save_data()
    
    embed = create_embed(f"🎣 Fishing Success!", color=color)
    embed.add_field(name="Catch", value=f"{fish_name} ({rarity.title()})", inline=True)
    embed.add_field(name="Value", value=f"{CURRENCY}{fish_value:,}", inline=True)
    embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    
    if durability_msg:
        embed.add_field(name="⚠️ Notice", value=durability_msg, inline=False)
    
    await interaction.response.send_message(embed=embed)

# =============================================
#             GAMBLING COMMANDS
# =============================================

@bot.tree.command(name="gamble", description="🎰 Gamble your money for a chance to double it")
async def gamble(interaction: discord.Interaction, amount: int):
    user_id = interaction.user.id
    current_balance = get_balance(user_id)
    
    if amount <= 0:
        embed = create_embed("❌ Invalid Amount", "Amount must be positive!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    if amount > current_balance:
        embed = create_embed("💸 Insufficient Funds", "You don't have enough money!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    # Calculate win chance
    win_chance = 0.45  # 45% base
    if has_item(user_id, "luckycoin"):
        win_chance = 0.55  # 55% with lucky coin
    
    # Update stats
    get_user_data(user_id)["stats"]["times_gambled"] += 1
    save_data()
    
    if random.random() < win_chance:
        win_amount = amount * 2
        new_balance = update_balance(user_id, win_amount)
        
        embed = create_embed("🎉 Gambling Win!", color=discord.Color.green())
        embed.add_field(name="Bet", value=f"{CURRENCY}{amount:,}", inline=True)
        embed.add_field(name="Won", value=f"{CURRENCY}{win_amount:,}", inline=True)
        embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    else:
        new_balance = update_balance(user_id, -amount)
        
        embed = create_embed("😢 Gambling Loss", color=discord.Color.red())
        embed.add_field(name="Lost", value=f"{CURRENCY}{amount:,}", inline=True)
        embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="slots", description="🎰 Play the slot machine")
async def slots(interaction: discord.Interaction, bet: int):
    user_id = interaction.user.id
    current_balance = get_balance(user_id)
    
    if bet <= 0:
        embed = create_embed("❌ Invalid Bet", "Bet must be positive!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    if bet > current_balance:
        embed = create_embed("💸 Insufficient Funds", "You don't have enough money!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    # Slot machine logic
    emojis = ["🍒", "🍋", "🍊", "🍇", "🍉", "7️⃣", "💎"]
    slots = [random.choice(emojis) for _ in range(3)]
    result = " | ".join(slots)
    
    # Check for wins
    win_amount = 0
    outcome = ""
    
    if slots[0] == slots[1] == slots[2]:
        if slots[0] == "7️⃣":
            win_amount = bet * 15
            outcome = "🎰 MEGA JACKPOT!"
        elif slots[0] == "💎":
            win_amount = bet * 12
            outcome = "💎 DIAMOND JACKPOT!"
        else:
            win_amount = bet * 6
            outcome = "🎉 TRIPLE MATCH!"
    elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
        win_amount = bet * 2
        outcome = "✨ PAIR MATCH!"
    else:
        win_amount = -bet
        outcome = "😔 No Match"
    
    new_balance = update_balance(user_id, win_amount)
    color = discord.Color.gold() if win_amount > bet * 5 else (discord.Color.green() if win_amount > 0 else discord.Color.red())
    
    embed = create_embed("🎰 Slot Machine", color=color)
    embed.add_field(name="Result", value=f"```{result}```", inline=False)
    embed.add_field(name="Outcome", value=outcome, inline=True)
    
    if win_amount > 0:
        embed.add_field(name="Won", value=f"{CURRENCY}{win_amount:,}", inline=True)
    else:
        embed.add_field(name="Lost", value=f"{CURRENCY}{bet:,}", inline=True)
    
    embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="scratch", description="🎫 Scratch your lottery tickets")
async def scratch(interaction: discord.Interaction):
    global CURRENT_LOTTERY_PRIZE  # Moved to the top of the function
    
    user_id = interaction.user.id
    
    if not has_item(user_id, "lotteryticket"):
        embed = create_embed(
            "🎫 No Lottery Tickets",
            "You don't have any lottery tickets! Buy some from the shop.",
            discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    # Use one ticket
    remove_item_from_inventory(user_id, "lotteryticket", 1)
    
    # Create scratch animation
    embed = create_embed("🎫 Scratching Lottery Ticket...", "✨ Scratching... ✨", discord.Color.yellow())
    await interaction.response.send_message(embed=embed)
    
    await asyncio.sleep(2)  # Build suspense
    
    # Check for win
    if random.randint(1, LOTTERY_WIN_CHANCE) == 1:
        # WINNER!
        win_amount = CURRENT_LOTTERY_PRIZE
        new_balance = update_balance(user_id, win_amount, apply_multiplier=False)  # Lottery wins don't get multiplied
        
        # Update stats
        user_data = get_user_data(user_id)
        user_data["stats"]["lottery_wins"] += 1
        save_data()
        
        # Add to winners list
        lottery_winners.append({
            "user": interaction.user,
            "amount": win_amount,
            "time": datetime.now()
        })
        
        # Create winner embed
        embed = create_embed("🎉 LOTTERY WINNER! 🎉", color=discord.Color.gold())
        embed.add_field(name="🏆 JACKPOT WINNER!", value=f"**{interaction.user.display_name}**", inline=False)
        embed.add_field(name="💰 Prize Won", value=f"{CURRENCY}{win_amount:,}", inline=True)
        embed.add_field(name="💳 New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        # Reset lottery prize
        CURRENT_LOTTERY_PRIZE = random.randint(LOTTERY_MIN_PRIZE, LOTTERY_START_PRIZE)
        update_lottery_description()
        save_data()
        
        # Announce globally
        await interaction.edit_original_response(embed=embed)
        
        # Send announcement to all servers
        announcement_embed = create_embed(
            "🎉 LOTTERY WINNER ANNOUNCEMENT! 🎉",
            f"**{interaction.user.display_name}** just won {CURRENCY}{win_amount:,} from a lottery ticket!",
            discord.Color.gold()
        )
        
        for guild in bot.guilds:
            if guild.id != interaction.guild_id:  # Don't spam the same server
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        try:
                            await channel.send(embed=announcement_embed)
                            break
                        except:
                            continue
    else:
        # No win
        losing_messages = [
            ("🍀", "Better luck next time!"),
            ("🎲", "The odds weren't in your favor today."),
            ("⭐", "Keep trying - someone has to win!"),
            ("🎯", "So close! Try another ticket."),
            ("🔮", "Fortune favors the persistent!")
        ]
        
        emoji, message = random.choice(losing_messages)
        embed = create_embed(f"{emoji} No Win This Time", color=discord.Color.orange())
        embed.add_field(name="Result", value=message, inline=False)
        embed.add_field(name="Current Jackpot", value=f"{CURRENCY}{CURRENT_LOTTERY_PRIZE:,}", inline=True)
        
        remaining_tickets = get_user_data(user_id)["inventory"].get("lotteryticket", {}).get("quantity", 0)
        if remaining_tickets > 0:
            embed.add_field(name="Remaining Tickets", value=str(remaining_tickets), inline=True)
        
        await interaction.edit_original_response(embed=embed)

# =============================================
#             SOCIAL COMMANDS
# =============================================

@bot.tree.command(name="rob", description="🦹 Attempt to rob another user")
async def rob(interaction: discord.Interaction, user: discord.User):
    robber_id = interaction.user.id
    victim_id = user.id
    
    if robber_id == victim_id:
        embed = create_embed("🤷 Can't Rob Yourself", "Nice try, but you can't rob yourself!", discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        return
    
    if user.bot:
        embed = create_embed("🤖 Can't Rob Bots", "Bots don't carry money!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    robber_balance = get_balance(robber_id)
    victim_balance = get_balance(victim_id)
    victim_data = get_user_data(victim_id)
    
    # Check if victim has padlock protection
    if has_item(victim_id, "padlock"):
        remove_item_from_inventory(victim_id, "padlock")
        embed = create_embed("🔒 Robbery Blocked!", color=discord.Color.blue())
        embed.add_field(name="Protected", value=f"{user.display_name}'s wallet was protected by a padlock!", inline=False)
        embed.add_field(name="Result", value="The padlock broke, but they're safe!", inline=False)
        await interaction.response.send_message(embed=embed)
        return
    
    if victim_balance < 100:
        embed = create_embed("💸 Target Too Poor", f"{user.display_name} doesn't have enough money to rob!", discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        return
    
    # Robbery attempt
    if random.random() < ROB_CHANCE:
        # Success
        max_steal = min(1000, victim_balance // 2)  # Can steal up to half, max 1000
        amount = random.randint(100, max_steal)
        
        update_balance(victim_id, -amount, apply_multiplier=False)
        new_balance = update_balance(robber_id, amount)
        
        success_scenarios = [
            ("🥷", "You successfully mugged", "and escaped into the shadows!"),
            ("🎭", "You disguised yourself and robbed", "without being recognized!"),
            ("⚡", "You performed a lightning-fast heist on", "and got away clean!"),
            ("🔓", "You picked the pocket of", "like a master thief!"),
        ]
        
        emoji, action1, action2 = random.choice(success_scenarios)
        
        embed = create_embed(f"{emoji} Robbery Success!", color=discord.Color.green())
        embed.add_field(name="Heist Complete", value=f"{action1} {user.display_name} {action2}", inline=False)
        embed.add_field(name="Stolen", value=f"{CURRENCY}{amount:,}", inline=True)
        embed.add_field(name="Your Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
        
    else:
        # Failed robbery
        fine = random.randint(ROB_MIN_FINE, min(ROB_MAX_FINE, robber_balance))
        new_balance = update_balance(robber_id, -fine, apply_multiplier=False)
        
        failure_scenarios = [
            ("🚨", "You got caught red-handed", "and had to pay a fine!"),
            ("👮", "The police caught you", "and fined you for attempted theft!"),
            ("🥊", "Your target fought back", "and you had to pay for damages!"),
            ("📸", "Security cameras caught you", "and you were fined!"),
        ]
        
        emoji, failure1, failure2 = random.choice(failure_scenarios)
        
        embed = create_embed(f"{emoji} Robbery Failed!", color=discord.Color.red())
        embed.add_field(name="Caught!", value=f"{failure1} trying to rob {user.display_name} {failure2}", inline=False)
        embed.add_field(name="Fine Paid", value=f"{CURRENCY}{fine:,}", inline=True)
        embed.add_field(name="Your Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="pay", description="💸 Pay money to another user")
async def pay(interaction: discord.Interaction, user: discord.User, amount: int):
    sender_id = interaction.user.id
    receiver_id = user.id
    
    if sender_id == receiver_id:
        embed = create_embed("🤷 Can't Pay Yourself", "You can't pay money to yourself!", discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        return
    
    if user.bot:
        embed = create_embed("🤖 Can't Pay Bots", "Bots don't need money!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    if amount <= 0:
        embed = create_embed("❌ Invalid Amount", "Amount must be positive!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    sender_balance = get_balance(sender_id)
    if amount > sender_balance:
        embed = create_embed("💸 Insufficient Funds", "You don't have enough money!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    # Process payment
    update_balance(sender_id, -amount, apply_multiplier=False)
    update_balance(receiver_id, amount, apply_multiplier=False)
    
    embed = create_embed("💸 Payment Sent!", color=discord.Color.green())
    embed.add_field(name="From", value=interaction.user.display_name, inline=True)
    embed.add_field(name="To", value=user.display_name, inline=True)
    embed.add_field(name="Amount", value=f"{CURRENCY}{amount:,}", inline=True)
    embed.set_thumbnail(url=user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

# =============================================
#             SHOP COMMANDS
# =============================================

@bot.tree.command(name="shop", description="🛒 Browse the shop and buy items")
async def shop(interaction: discord.Interaction):
    shop_data = get_server_shop(interaction.guild.id)
    
    embed = create_embed("🛒 Fun.Bot Shop", "Buy items to enhance your experience!", discord.Color.blue())
    
    for item_id, item_data in BASE_SHOP_ITEMS.items():
        if item_id in shop_data["items"]:
            shop_item = shop_data["items"][item_id]
            stock_indicator = "🔴 Out of Stock" if shop_item['stock'] <= 0 else f"📦 Stock: {shop_item['stock']}"
            
            # Price change indicator
            base_price = item_data["base_price"]
            current_price = shop_item["price"]
            if current_price > base_price:
                price_indicator = f"📈 {CURRENCY}{current_price:,} (↑{((current_price/base_price-1)*100):.0f}%)"
            elif current_price < base_price:
                price_indicator = f"📉 {CURRENCY}{current_price:,} (↓{((1-current_price/base_price)*100):.0f}%)"
            else:
                price_indicator = f"{CURRENCY}{current_price:,}"
            
            embed.add_field(
                name=f"{item_data['name']} - {price_indicator}",
                value=f"{item_data['description']}\n{stock_indicator}",
                inline=False
            )
    
    embed.set_footer(text="Use /buy to purchase items • Prices and stock update every 10 minutes")
    await interaction.response.send_message(embed=embed)

class ShopSelect(discord.ui.Select):
    def __init__(self, shop_data, guild_id):
        self.shop_data = shop_data
        self.guild_id = guild_id
        
        options = []
        for item_id, item_data in BASE_SHOP_ITEMS.items():
            if item_id in shop_data["items"]:
                shop_item = shop_data["items"][item_id]
                if shop_item['stock'] > 0:  # Only show in-stock items
                    options.append(discord.SelectOption(
                        label=item_data['name'],
                        description=f"{CURRENCY}{shop_item['price']:,} - {item_data['description'][:50]}...",
                        emoji=item_data.get('emoji', '🛍️'),
                        value=item_id
                    ))
        
        super().__init__(placeholder="Choose an item to buy...", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction):
        item_id = self.values[0]
        user_id = interaction.user.id
        current_balance = get_balance(user_id)
        
        item_data = BASE_SHOP_ITEMS[item_id]
        shop_item = self.shop_data["items"][item_id]
        price = shop_item["price"]
        
        if shop_item["stock"] <= 0:
            embed = create_embed("❌ Out of Stock", f"{item_data['name']} is currently out of stock!", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if current_balance < price:
            embed = create_embed("💸 Insufficient Funds", f"You need {CURRENCY}{price-current_balance:,} more to buy {item_data['name']}!", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Handle lottery tickets specially (they get scratched immediately)
        if item_id == "lotteryticket":
            # Deduct money first
            update_balance(user_id, -price, apply_multiplier=False)
            shop_item["stock"] -= 1
            save_data()
            
            # Auto-scratch the ticket
            embed = create_embed("🎫 Scratching Your Lottery Ticket...", "✨ Scratching... ✨", discord.Color.yellow())
            await interaction.response.send_message(embed=embed)
            
            await asyncio.sleep(2)
            
            # Check for win
            if random.randint(1, LOTTERY_WIN_CHANCE) == 1:
                # WINNER!
                win_amount = CURRENT_LOTTERY_PRIZE
                new_balance = update_balance(user_id, win_amount, apply_multiplier=False)
                
                user_data = get_user_data(user_id)
                user_data["stats"]["lottery_wins"] += 1
                save_data()
                
                lottery_winners.append({
                    "user": interaction.user,
                    "amount": win_amount,
                    "time": datetime.now()
                })
                
                embed = create_embed("🎉 INSTANT LOTTERY WINNER! 🎉", color=discord.Color.gold())
                embed.add_field(name="🏆 JACKPOT!", value=f"You won {CURRENCY}{win_amount:,}!", inline=False)
                embed.add_field(name="💳 New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
                
                global CURRENT_LOTTERY_PRIZE
                CURRENT_LOTTERY_PRIZE = random.randint(LOTTERY_MIN_PRIZE, LOTTERY_START_PRIZE)
                update_lottery_description()
                save_data()
                
            else:
                losing_messages = [
                    "🍀 Better luck next time!",
                    "🎯 So close! Try again.",
                    "⭐ Keep playing - someone has to win!"
                ]
                
                embed = create_embed("🎫 No Win This Time", random.choice(losing_messages), discord.Color.orange())
                embed.add_field(name="Current Jackpot", value=f"{CURRENCY}{CURRENT_LOTTERY_PRIZE:,}", inline=True)
            
            await interaction.edit_original_response(embed=embed)
            return
        
        # For fishing rods, add durability data
        item_data_to_add = {}
        if item_id == "fishingrod":
            item_data_to_add = {"durability": FISHING_ROD_USES}
        
        # Process purchase
        add_item_to_inventory(user_id, item_id, 1, item_data_to_add)
        shop_item["stock"] -= 1
        new_balance = update_balance(user_id, -price, apply_multiplier=False)
        save_data()
        
        embed = create_embed("✅ Purchase Successful!", color=discord.Color.green())
        embed.add_field(name="Item", value=item_data['name'], inline=True)
        embed.add_field(name="Price", value=f"{CURRENCY}{price:,}", inline=True)
        embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class ShopView(discord.ui.View):
    def __init__(self, shop_data, guild_id):
        super().__init__(timeout=300)
        self.add_item(ShopSelect(shop_data, guild_id))

@bot.tree.command(name="buy", description="🛍️ Buy items from the shop")
async def buy(interaction: discord.Interaction):
    shop_data = get_server_shop(interaction.guild.id)
    
    # Check if any items are in stock
    in_stock_items = [item_id for item_id, shop_item in shop_data["items"].items() if shop_item["stock"] > 0]
    
    if not in_stock_items:
        embed = create_embed("🚫 Shop Empty", "All items are currently out of stock! Check back later.", discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        return
    
    embed = create_embed("🛍️ Purchase Menu", "Select an item from the dropdown menu below to buy it!", discord.Color.blue())
    view = ShopView(shop_data, interaction.guild.id)
    
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="inventory", description="🎒 View your or someone else's inventory")
async def inventory(interaction: discord.Interaction, user: Optional[discord.User] = None):
    target = user or interaction.user
    user_data = get_user_data(target.id)
    inventory = user_data.get("inventory", {})
    
    if not inventory:
        embed = create_embed(f"🎒 {target.display_name}'s Inventory", "This inventory is empty!", discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        return
    
    embed = create_embed(f"🎒 {target.display_name}'s Inventory", color=discord.Color.blue())
    embed.set_thumbnail(url=target.display_avatar.url)
    
    for item_name, item_info in inventory.items():
        shop_item = BASE_SHOP_ITEMS.get(item_name, {})
        display_name = shop_item.get("name", item_name.title())
        
        value_parts = [f"Quantity: {item_info['quantity']}"]
        
        if "durability" in item_info.get("data", {}):
            value_parts.append(f"Durability: {item_info['data']['durability']}")
        
        embed.add_field(
            name=display_name,
            value="\n".join(value_parts),
            inline=True
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="use", description="🔧 Use an item from your inventory")
async def use(interaction: discord.Interaction, item: str):
    user_id = interaction.user.id
    
    # Find item in inventory (case insensitive)
    user_data = get_user_data(user_id)
    inventory = user_data.get("inventory", {})
    
    item_key = None
    for key in inventory.keys():
        if key.lower() == item.lower():
            item_key = key
            break
    
    if not item_key:
        embed = create_embed("❌ Item Not Found", f"You don't have '{item}' in your inventory!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    if item_key not in BASE_SHOP_ITEMS:
        embed = create_embed("❌ Invalid Item", "This item cannot be used!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    if not BASE_SHOP_ITEMS[item_key].get("usable", False):
        embed = create_embed("❌ Not Usable", "This item cannot be used directly!", discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    # Handle specific item usage
    if item_key == "workboost":
        set_cooldown(user_id, "workboost", 86400)  # 1 day
        remove_item_from_inventory(user_id, item_key)
        
        embed = create_embed("⚡ Work Boost Activated!", color=discord.Color.yellow())
        embed.add_field(name="Effect", value="Your work earnings are increased by 50% for the next 24 hours!", inline=False)
        
    elif item_key == "energydrink":
        reduce_cooldowns(user_id, 1800)  # Reduce by 30 minutes
        remove_item_from_inventory(user_id, item_key)
        
        embed = create_embed("⚡ Energy Drink Consumed!", color=discord.Color.green())
        embed.add_field(name="Effect", value="All your cooldowns have been reduced by 30 minutes!", inline=False)
        
    elif item_key == "multiplier":
        # Activate 2x multiplier for 1 hour
        user_data["multipliers"]["2x_end"] = datetime.now().timestamp() + 3600
        remove_item_from_inventory(user_id, item_key)
        save_data()
        
        embed = create_embed("✨ 2x Multiplier Activated!", color=discord.Color.purple())
        embed.add_field(name="Effect", value="All your earnings are doubled for the next hour!", inline=False)
        
    elif item_key in ["luckycoin", "diamondring", "padlock"]:
        embed = create_embed("ℹ️ Passive Item", color=discord.Color.blue())
        embed.add_field(
            name="Auto-Active",
            value=f"This item is automatically applied when relevant! You have {inventory[item_key]['quantity']} in your inventory.",
            inline=False
        )
        
    else:
        embed = create_embed("❌ Unknown Item", "I don't know how to use this item!", discord.Color.red())
    
    await interaction.response.send_message(embed=embed)

# =============================================
#             INFORMATION COMMANDS
# =============================================

@bot.tree.command(name="lottery", description="🎫 Check current lottery information")
async def lottery(interaction: discord.Interaction):
    embed = create_embed("🎫 Lottery Information", color=discord.Color.gold())
    
    embed.add_field(
        name="💰 Current Jackpot",
        value=f"{CURRENCY}{CURRENT_LOTTERY_PRIZE:,}",
        inline=True
    )
    
    embed.add_field(
        name="🎯 Win Chance",
        value=f"1 in {LOTTERY_WIN_CHANCE}",
        inline=True
    )
    
    embed.add_field(
        name="🎫 Ticket Price",
        value=f"{CURRENCY}{LOTTERY_TICKET_PRICE:,}",
        inline=True
    )
    
    # Show recent winners
    if lottery_winners:
        recent_winners = lottery_winners[-5:]  # Last 5 winners
        winner_text = []
        
        for winner_data in recent_winners:
            time_ago = datetime.now() - winner_data["time"]
            if time_ago.days > 0:
                time_str = f"{time_ago.days}d ago"
            elif time_ago.seconds > 3600:
                time_str = f"{time_ago.seconds//3600}h ago"
            else:
                time_str = f"{time_ago.seconds//60}m ago"
            
            winner_text.append(f"**{winner_data['user'].display_name}** - {CURRENCY}{winner_data['amount']:,} ({time_str})")
        
        embed.add_field(
            name="🏆 Recent Winners",
            value="\n".join(winner_text) if winner_text else "No recent winners",
            inline=False
        )
    else:
        embed.add_field(
            name="🏆 Recent Winners",
            value="No winners yet - could you be the first?",
            inline=False
        )
    
    embed.add_field(
        name="ℹ️ How to Play",
        value="Buy lottery tickets from the shop, then use `/scratch` to see if you won!",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="baltop", description="🏆 View the richest users")
async def baltop(interaction: discord.Interaction):
    users = []
    
    for user_id_str, data in economy_data.items():
        try:
            user_id = int(user_id_str)
            user = await bot.fetch_user(user_id)
            if not user.bot:  # Exclude bots
                users.append((user.display_name, data["balance"], user))
        except:
            continue
    
    # Sort by balance (descending)
    users.sort(key=lambda x: x[1], reverse=True)
    
    embed = create_embed("🏆 Richest Users Leaderboard", color=discord.Color.gold())
    
    # Add top 10 users with medals
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    
    for i, (name, balance, user_obj) in enumerate(users[:10], 1):
        medal = medals[i-1] if i <= 10 else "🔸"
        embed.add_field(
            name=f"{medal} #{i} {name}",
            value=f"{CURRENCY}{balance:,}",
            inline=False
        )
    
    # Add current user's position if not in top 10
    current_user_id = interaction.user.id
    current_balance = get_balance(current_user_id)
    current_position = next((i+1 for i, (_, bal, _) in enumerate(users) if bal <= current_balance), len(users)+1)
    
    if current_position > 10:
        embed.add_field(
            name="📊 Your Position",
            value=f"#{current_position} with {CURRENCY}{current_balance:,}",
            inline=False
        )
    
    embed.set_footer(text=f"Total users tracked: {len(users)}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="stats", description="📊 View your or someone else's statistics")
async def stats(interaction: discord.Interaction, user: Optional[discord.User] = None):
    target = user or interaction.user
    user_data = get_user_data(target.id)
    stats = user_data.get("stats", {})
    
    embed = create_embed(f"📊 {target.display_name}'s Statistics", color=discord.Color.purple())
    embed.set_thumbnail(url=target.display_avatar.url)
    
    # Economy stats
    embed.add_field(name="💼 Times Worked", value=f"{stats.get('times_worked', 0):,}", inline=True)
    embed.add_field(name="🎰 Times Gambled", value=f"{stats.get('times_gambled', 0):,}", inline=True)
    embed.add_field(name="🎣 Times Fished", value=f"{stats.get('times_fished', 0):,}", inline=True)
    
    # Money stats
    embed.add_field(name="💰 Total Earned", value=f"{CURRENCY}{stats.get('total_earned', 0):,}", inline=True)
    embed.add_field(name="💸 Total Spent", value=f"{CURRENCY}{stats.get('total_spent', 0):,}", inline=True)
    embed.add_field(name="🏆 Lottery Wins", value=f"{stats.get('lottery_wins', 0):,}", inline=True)
    
    # Additional stats
    embed.add_field(name="🐟 Fish Caught", value=f"{stats.get('fish_caught', 0):,}", inline=True)
    embed.add_field(name="🔥 Daily Streak", value=f"{user_data.get('daily_streak', 0)} days", inline=True)
    embed.add_field(name="💳 Current Balance", value=f"{CURRENCY}{user_data.get('balance', 0):,}", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="cooldowns", description="⏰ Check your current cooldowns")
async def cooldowns(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_data = get_user_data(user_id)
    
    cooldown_types = {
        "work": "💼 Work",
        "daily": "🎁 Daily Reward",
        "fish": "🎣 Fishing"
    }
    
    embed = create_embed("⏰ Your Cooldowns", color=discord.Color.blue())
    
    has_cooldowns = False
    for cooldown_type, display_name in cooldown_types.items():
        remaining = check_cooldown(user_id, cooldown_type)
        if remaining > 0:
            embed.add_field(
                name=display_name,
                value=f"Ready in {format_time(remaining)}",
                inline=True
            )
            has_cooldowns = True
        else:
            embed.add_field(
                name=display_name,
                value="✅ Ready!",
                inline=True
            )
    
    # Check multipliers
    if is_multiplier_active(user_id):
        multiplier_end = user_data.get("multipliers", {}).get("2x_end", 0)
        time_left = int(multiplier_end - datetime.now().timestamp())
        embed.add_field(
            name="✨ 2x Multiplier",
            value=f"Active for {format_time(time_left)}",
            inline=True
        )
    
    # Check work boost
    workboost_end = user_data.get("cooldowns", {}).get("workboost", 0)
    if workboost_end > datetime.now().timestamp():
        time_left = int(workboost_end - datetime.now().timestamp())
        embed.add_field(
            name="⚡ Work Boost",
            value=f"Active for {format_time(time_left)}",
            inline=True
        )
    
    if not has_cooldowns and not is_multiplier_active(user_id) and workboost_end <= datetime.now().timestamp():
        embed.add_field(
            name="🎉 All Clear!",
            value="No active cooldowns or effects!",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="leaderboard", description="🏅 View various leaderboards")
@app_commands.describe(category="Choose which leaderboard to view")
@app_commands.choices(category=[
    app_commands.Choice(name="💰 Richest Users", value="balance"),
    app_commands.Choice(name="💼 Most Work Done", value="work"),
    app_commands.Choice(name="🎰 Biggest Gamblers", value="gambling"),
    app_commands.Choice(name="🎣 Best Fishers", value="fishing"),
    app_commands.Choice(name="🏆 Lottery Winners", value="lottery")
])
async def leaderboard(interaction: discord.Interaction, category: str):
    users_data = []
    
    for user_id_str, data in economy_data.items():
        try:
            user_id = int(user_id_str)
            user = await bot.fetch_user(user_id)
            if not user.bot:
                users_data.append((user.display_name, data, user))
        except:
            continue
    
    if category == "balance":
        users_data.sort(key=lambda x: x[1]["balance"], reverse=True)
        title = "🏆 Richest Users"
        value_func = lambda data: f"{CURRENCY}{data['balance']:,}"
        
    elif category == "work":
        users_data.sort(key=lambda x: x[1]["stats"].get("times_worked", 0), reverse=True)
        title = "💼 Hardest Workers"
        value_func = lambda data: f"{data['stats'].get('times_worked', 0):,} times"
        
    elif category == "gambling":
        users_data.sort(key=lambda x: x[1]["stats"].get("times_gambled", 0), reverse=True)
        title = "🎰 Biggest Gamblers"
        value_func = lambda data: f"{data['stats'].get('times_gambled', 0):,} times"
        
    elif category == "fishing":
        users_data.sort(key=lambda x: x[1]["stats"].get("fish_caught", 0), reverse=True)
        title = "🎣 Master Fishers"
        value_func = lambda data: f"{data['stats'].get('fish_caught', 0):,} fish"
        
    elif category == "lottery":
        users_data.sort(key=lambda x: x[1]["stats"].get("lottery_wins", 0), reverse=True)
        title = "🏆 Lucky Lottery Winners"
        value_func = lambda data: f"{data['stats'].get('lottery_wins', 0):,} wins"
    
    embed = create_embed(title, color=discord.Color.gold())
    
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    
    for i, (name, data, user_obj) in enumerate(users_data[:10], 1):
        medal = medals[i-1] if i <= 10 else "🔸"
        embed.add_field(
            name=f"{medal} #{i} {name}",
            value=value_func(data),
            inline=False
        )
    
    if not users_data:
        embed.add_field(name="No Data", value="No users found for this category!", inline=False)
    
    await interaction.response.send_message(embed=embed)

# =============================================
#             OWNER COMMANDS
# =============================================

def is_owner():
    def predicate(interaction: discord.Interaction):
        return interaction.user.id == OWNER_ID
    return app_commands.check(predicate)

@bot.tree.command(name="give", description="[Owner] Give money to a user")
@is_owner()
async def give(interaction: discord.Interaction, user: discord.User, amount: int):
    if amount <= 0:
        embed = create_embed("❌ Invalid Amount", "Amount must be positive!", discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    new_balance = update_balance(user.id, amount, apply_multiplier=False)
    
    embed = create_embed("💰 Money Given", color=discord.Color.green())
    embed.add_field(name="Recipient", value=user.display_name, inline=True)
    embed.add_field(name="Amount", value=f"{CURRENCY}{amount:,}", inline=True)
    embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="take", description="[Owner] Take money from a user")
@is_owner()
async def take(interaction: discord.Interaction, user: discord.User, amount: int):
    current_balance = get_balance(user.id)
    
    if amount <= 0:
        embed = create_embed("❌ Invalid Amount", "Amount must be positive!", discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if amount > current_balance:
        amount = current_balance
    
    new_balance = update_balance(user.id, -amount, apply_multiplier=False)
    
    embed = create_embed("💸 Money Taken", color=discord.Color.orange())
    embed.add_field(name="Target", value=user.display_name, inline=True)
    embed.add_field(name="Amount Taken", value=f"{CURRENCY}{amount:,}", inline=True)
    embed.add_field(name="New Balance", value=f"{CURRENCY}{new_balance:,}", inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="give_all", description="[Owner] Give money to everyone in this server")
@is_owner()
async def give_all(interaction: discord.Interaction, amount: int):
    if amount <= 0:
        embed = create_embed("❌ Invalid Amount", "Amount must be positive!", discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    members = interaction.guild.members
    count = 0
    
    for member in members:
        if not member.bot:
            update_balance(member.id, amount, apply_multiplier=False)
            count += 1
    
    embed = create_embed("🎉 Money Distributed", color=discord.Color.green())
    embed.add_field(name="Amount Per User", value=f"{CURRENCY}{amount:,}", inline=True)
    embed.add_field(name="Recipients", value=f"{count} members", inline=True)
    embed.add_field(name="Total Given", value=f"{CURRENCY}{amount * count:,}", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="set_lottery", description="[Owner] Set the lottery jackpot")
@is_owner()
async def set_lottery(interaction: discord.Interaction, amount: int):
    global CURRENT_LOTTERY_PRIZE  # Added global declaration
    
    if amount < LOTTERY_MIN_PRIZE:
        embed = create_embed("❌ Too Low", f"Minimum lottery prize is {CURRENCY}{LOTTERY_MIN_PRIZE:,}!", discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    old_prize = CURRENT_LOTTERY_PRIZE
    CURRENT_LOTTERY_PRIZE = amount
    update_lottery_description()
    save_data()
    
    embed = create_embed("🎫 Lottery Prize Updated", color=discord.Color.gold())
    embed.add_field(name="Old Prize", value=f"{CURRENCY}{old_prize:,}", inline=True)
    embed.add_field(name="New Prize", value=f"{CURRENCY}{amount:,}", inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="reset_economy", description="[Owner] Reset all economy data")
@is_owner()
async def reset_economy(interaction: discord.Interaction):
    # Create confirmation view
    class ConfirmReset(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
        
        @discord.ui.button(label="Confirm Reset", style=discord.ButtonStyle.danger)
        async def confirm(self, button_interaction: discord.Interaction, button: discord.ui.Button):
            global economy_data, server_shops, CURRENT_LOTTERY_PRIZE
            economy_data = {}
            server_shops = {}
            CURRENT_LOTTERY_PRIZE = LOTTERY_START_PRIZE
            update_lottery_description()
            save_data()
            
            embed = create_embed("✅ Economy Reset Complete", "All economy data has been wiped clean!", discord.Color.green())
            await button_interaction.response.edit_message(embed=embed, view=None)
        
        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
        async def cancel(self, button_interaction: discord.Interaction, button: discord.ui.Button):
            embed = create_embed("❌ Reset Cancelled", "Economy data is safe!", discord.Color.blue())
            await button_interaction.response.edit_message(embed=embed, view=None)
    
    embed = create_embed(
        "⚠️ Economy Reset Confirmation",
        "This will permanently delete ALL economy data including:\n"
        "• All user balances and inventories\n"
        "• All shop data\n"
        "• All statistics\n"
        "• Lottery winners history\n\n"
        "**This action cannot be undone!**",
        discord.Color.red()
    )
    
    await interaction.response.send_message(embed=embed, view=ConfirmReset(), ephemeral=True)

@bot.tree.command(name="global_announcement", description="[Owner] Send announcement to all servers")
@is_owner()
async def global_announcement(interaction: discord.Interaction, message: str):
    await interaction.response.defer(ephemeral=True)
    
    total_sent = 0
    failed = 0
    
    for guild in bot.guilds:
        sent_to_guild = False
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    embed = create_embed(
                        "📢 Global Announcement",
                        message,
                        discord.Color.gold()
                    )
                    embed.set_footer(text=f"Announcement from {interaction.user.display_name}")
                    await channel.send(embed=embed)
                    total_sent += 1
                    sent_to_guild = True
                    break
                except:
                    continue
        
        if not sent_to_guild:
            failed += 1
    
    embed = create_embed("📢 Announcement Sent", color=discord.Color.green())
    embed.add_field(name="Servers Reached", value=str(total_sent), inline=True)
    embed.add_field(name="Failed", value=str(failed), inline=True)
    embed.add_field(name="Total Servers", value=str(len(bot.guilds)), inline=True)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="bot_stats", description="[Owner] View bot statistics")
@is_owner()
async def bot_stats(interaction: discord.Interaction):
    total_users = len(economy_data)
    total_servers = len(bot.guilds)
    total_balance = sum(data["balance"] for data in economy_data.values())
    total_lottery_wins = len(lottery_winners)
    
    embed = create_embed("🤖 Bot Statistics", color=discord.Color.blue())
    embed.add_field(name="👥 Total Users", value=f"{total_users:,}", inline=True)
    embed.add_field(name="🏠 Total Servers", value=f"{total_servers:,}", inline=True)
    embed.add_field(name="💰 Total Economy", value=f"{CURRENCY}{total_balance:,}", inline=True)
    embed.add_field(name="🎫 Lottery Winners", value=f"{total_lottery_wins:,}", inline=True)
    embed.add_field(name="🏆 Current Jackpot", value=f"{CURRENCY}{CURRENT_LOTTERY_PRIZE:,}", inline=True)
    embed.add_field(name="📊 Active Shops", value=f"{len(server_shops):,}", inline=True)
    
    # Memory usage and uptime could be added here
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# =============================================
#             HELP COMMAND
# =============================================

@bot.tree.command(name="help", description="📋 Show all available commands")
async def help_command(interaction: discord.Interaction):
    embed = create_embed(f"{BOT_NAME} Command Guide", "Here are all the available commands organized by category!", discord.Color.blue())
    
    # Economy commands
    embed.add_field(
        name="💰 Economy Commands",
        value=(
            "`/balance` - Check balance\n"
            "`/work` - Work for money\n"
            "`/daily` - Daily reward\n"
            "`/beg` - Beg for money\n"
            "`/fish` - Go fishing\n"
            "`/pay` - Pay another user"
        ),
        inline=True
    )
    
    # Gambling commands
    embed.add_field(
        name="🎰 Gambling Commands",
        value=(
            "`/gamble` - Gamble money\n"
            "`/slots` - Slot machine\n"
            "`/scratch` - Scratch lottery tickets\n"
            "`/lottery` - Lottery info"
        ),
        inline=True
    )
    
    # Shop commands
    embed.add_field(
        name="🛒 Shop Commands",
        value=(
            "`/shop` - View shop\n"
            "`/buy` - Buy items\n"
            "`/inventory` - View inventory\n"
            "`/use` - Use items"
        ),
        inline=True
    )
    
    # Social commands
    embed.add_field(
        name="👥 Social Commands",
        value=(
            "`/rob` - Rob another user\n"
            "`/baltop` - Richest users\n"
            "`/stats` - View statistics\n"
            "`/leaderboard` - Various leaderboards"
        ),
        inline=True
    )
    
    # Utility commands
    embed.add_field(
        name="🔧 Utility Commands",
        value=(
            "`/cooldowns` - Check cooldowns\n"
            "`/help` - Show this help"
        ),
        inline=True
    )
    
    # Owner commands (only show to owner)
    if interaction.user.id == OWNER_ID:
        embed.add_field(
            name="👑 Owner Commands",
            value=(
                "`/give` - Give money\n"
                "`/take` - Take money\n"
                "`/give_all` - Give to everyone\n"
                "`/set_lottery` - Set lottery prize\n"
                "`/global_announcement` - Global announce\n"
                "`/bot_stats` - Bot statistics\n"
                "`/reset_economy` - Reset all data"
            ),
            inline=True
        )
    
    embed.add_field(
        name="💡 Pro Tips",
        value=(
            "• Buy items from the shop to boost your earnings\n"
            "• Prices fluctuate - buy low, sell high!\n"
            "• Keep your daily streak for bigger rewards\n"
            "• Use `/cooldowns` to track when you can earn again"
        ),
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

# =============================================
#             BOT STARTUP
# =============================================

if __name__ == "__main__":
    print("🔄 Loading Fun.Bot...")
    load_data()
    
    bot_token = os.getenv("DISCORD_TOKEN")
    if not bot_token:
        print("❌ No DISCORD_TOKEN environment variable found!")
        print("Please set your bot token in the environment variables.")
        exit(1)
    
    print("🚀 Starting Fun.Bot...")
    try:
        bot.run(bot_token)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        exit(1)
