import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import json
import os
from datetime import datetime, timedelta
import asyncio

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Bot configuration
BOT_NAME = "Fun.Bot"
OWNER_ID = 928108286916583474  # Your user ID
STARTING_BALANCE = 1000
CURRENCY = "$"
DATA_FILE = "economy_data.json"

# Lottery configuration
CURRENT_LOTTERY_PRIZE = 50000  # Starting prize
LOTTERY_WIN_CHANCE = 650  # 1 in 650 chance
LOTTERY_MIN_PRIZE = 10000
LOTTERY_MAX_PRIZE = 100000

# Base shop items with initial prices
BASE_SHOP_ITEMS = {
    "padlock": {
        "name": "Padlock",
        "base_price": 800,
        "description": "Protects your wallet from one robbery attempt",
        "usable": True,
        "max_stock": 10
    },
    "fishingrod": {
        "name": "Fishing Rod",
        "base_price": 1200,
        "description": "Required for fishing (durability: 10 uses)",
        "usable": False,
        "max_stock": 8
    },
    "luckycoin": {
        "name": "Lucky Coin",
        "base_price": 1500,
        "description": "Increases gambling win chance by 10%",
        "usable": True,
        "max_stock": 5
    },
    "workboost": {
        "name": "Work Boost",
        "base_price": 1000,
        "description": "Increases work earnings by 50% for 1 day",
        "usable": True,
        "max_stock": 7
    },
    "lotteryticket": {
        "name": "Lottery Ticket",
        "base_price": 500,
        "description": f"1 in {LOTTERY_WIN_CHANCE} chance to win! Current jackpot: {CURRENCY}{CURRENT_LOTTERY_PRIZE:,}",
        "usable": True,
        "max_stock": 15
    },
    "diamondring": {
        "name": "Diamond Ring",
        "base_price": 3000,
        "description": "Increases begging success rate by 20%",
        "usable": True,
        "max_stock": 3
    }
}

# Initialize bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Economy data storage
economy_data = {}
server_shops = {}  # Stores shop data per server
active_news = {}   # Stores active news events
lottery_winners = []  # Stores recent lottery winners

def load_data():
    global economy_data, server_shops, CURRENT_LOTTERY_PRIZE
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            economy_data = data.get("economy", {})
            server_shops = data.get("shops", {})
            CURRENT_LOTTERY_PRIZE = data.get("lottery_prize", 50000)
    else:
        economy_data = {}
        server_shops = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "economy": economy_data,
            "shops": server_shops,
            "lottery_prize": CURRENT_LOTTERY_PRIZE
        }, f)

def update_lottery_description():
    BASE_SHOP_ITEMS["lotteryticket"]["description"] = (
        f"1 in {LOTTERY_WIN_CHANCE} chance to win! Current jackpot: {CURRENCY}{CURRENT_LOTTERY_PRIZE:,}"
    )

def get_user_data(user_id):
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
                "lottery_wins": 0
            },
            "cooldowns": {}
        }
    return economy_data[user_id_str]

def get_server_shop(guild_id):
    guild_id_str = str(guild_id)
    if guild_id_str not in server_shops:
        # Initialize shop with random stock
        server_shops[guild_id_str] = {
            "items": {},
            "last_reset": datetime.now().timestamp()
        }
        for item_id, item_data in BASE_SHOP_ITEMS.items():
            server_shops[guild_id_str]["items"][item_id] = {
                "price": item_data["base_price"],
                "stock": random.randint(1, item_data["max_stock"] // 2)
            }
    return server_shops[guild_id_str]

def update_server_shop(guild_id):
    shop = get_server_shop(guild_id)
    for item_id, item_data in BASE_SHOP_ITEMS.items():
        if item_id not in shop["items"]:
            shop["items"][item_id] = {
                "price": item_data["base_price"],
                "stock": random.randint(1, item_data["max_stock"] // 2)
            }
        else:
            # Randomly adjust stock (but never exceed max_stock)
            stock_change = random.randint(-2, 3)
            new_stock = shop["items"][item_id]["stock"] + stock_change
            shop["items"][item_id]["stock"] = max(1, min(new_stock, item_data["max_stock"]))
            
            # Small random price fluctuation (5% up or down)
            price_change = random.uniform(-0.05, 0.05)
            shop["items"][item_id]["price"] = max(
                item_data["base_price"] * 0.5,  # Never less than 50% of base
                min(
                    item_data["base_price"] * 1.5,  # Never more than 150% of base
                    int(shop["items"][item_id]["price"] * (1 + price_change))
                )
            )
    
    shop["last_reset"] = datetime.now().timestamp()
    save_data()

def get_balance(user_id):
    return get_user_data(user_id)["balance"]

def set_balance(user_id, amount):
    get_user_data(user_id)["balance"] = amount
    save_data()

def update_balance(user_id, amount):
    user_data = get_user_data(user_id)
    user_data["balance"] += amount
    if amount > 0:
        user_data["stats"]["total_earned"] += amount
    else:
        user_data["stats"]["total_spent"] += abs(amount)
    save_data()
    return user_data["balance"]

def add_item_to_inventory(user_id, item_name, quantity=1, data=None):
    user_data = get_user_data(user_id)
    inventory = user_data["inventory"]
    
    if item_name in inventory:
        inventory[item_name]["quantity"] += quantity
    else:
        inventory[item_name] = {
            "quantity": quantity,
            "data": data or {}
        }
    save_data()

def remove_item_from_inventory(user_id, item_name, quantity=1):
    user_data = get_user_data(user_id)
    inventory = user_data["inventory"]
    
    if item_name in inventory:
        if inventory[item_name]["quantity"] <= quantity:
            del inventory[item_name]
        else:
            inventory[item_name]["quantity"] -= quantity
        save_data()
        return True
    return False

def has_item(user_id, item_name):
    user_data = get_user_data(user_id)
    return item_name in user_data["inventory"]

def get_cooldown(user_id, cooldown_type):
    user_data = get_user_data(user_id)
    cooldowns = user_data.get("cooldowns", {})
    last_used = cooldowns.get(cooldown_type, 0)
    return last_used

def set_cooldown(user_id, cooldown_type, duration_seconds):
    user_data = get_user_data(user_id)
    if "cooldowns" not in user_data:
        user_data["cooldowns"] = {}
    user_data["cooldowns"][cooldown_type] = int(datetime.now().timestamp()) + duration_seconds
    save_data()

def check_cooldown(user_id, cooldown_type):
    last_used = get_cooldown(user_id, cooldown_type)
    current_time = int(datetime.now().timestamp())
    return max(0, last_used - current_time) if last_used > current_time else 0

def adjust_lottery_prize():
    global CURRENT_LOTTERY_PRIZE
    # Randomly adjust prize (between -20% to +20% but within min/max bounds)
    change_percent = random.uniform(-0.2, 0.2)
    new_prize = int(CURRENT_LOTTERY_PRIZE * (1 + change_percent))
    CURRENT_LOTTERY_PRIZE = max(LOTTERY_MIN_PRIZE, min(LOTTERY_MAX_PRIZE, new_prize))
    update_lottery_description()
    save_data()
    return CURRENT_LOTTERY_PRIZE

async def announce_lottery_prize_change(channel, old_prize, new_prize):
    change = new_prize - old_prize
    embed = discord.Embed(
        title="📰 LOTTERY UPDATE",
        description=(
            f"**The lottery jackpot has {'increased' if change > 0 else 'decreased'}!**\n"
            f"Old prize: {format_money(old_prize)}\n"
            f"New prize: {format_money(new_prize)}\n"
            f"Change: {'+' if change > 0 else ''}{format_money(change)}"
        ),
        color=discord.Color.green() if change > 0 else discord.Color.red()
    )
    await channel.send(embed=embed)

async def announce_lottery_winner(winner: discord.User, amount):
    embed = discord.Embed(
        title="🎉 LOTTERY WINNER!",
        description=f"**{winner.display_name}** has won the lottery and received {format_money(amount)}!",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Congratulations! A new lottery has started.")
    
    # Send to all servers
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
                try:
                    await channel.send(embed=embed)
                    break  # Only send to one channel per server
                except:
                    continue

# Helper functions
def format_money(amount):
    return f"{CURRENCY}{amount:,}"

def format_time(seconds):
    if seconds >= 3600:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m"
    elif seconds >= 60:
        return f"{seconds // 60}m {seconds % 60}s"
    return f"{seconds}s"

async def send_breaking_news(channel, item_id, price_change_percent, duration_minutes):
    item_data = BASE_SHOP_ITEMS[item_id]
    duration = min(duration_minutes * 60, 300)  # Never more than 5 minutes
    
    # Calculate new price
    new_price = max(
        item_data["base_price"] * 0.5,  # Never less than 50% of base
        int(item_data["base_price"] * (1 + price_change_percent / 100))
    )
    
    # Apply to all servers
    for guild_id_str in server_shops:
        if item_id in server_shops[guild_id_str]["items"]:
            server_shops[guild_id_str]["items"][item_id]["price"] = new_price
    
    # Create news embed
    embed = discord.Embed(
        title="📰 BREAKING NEWS",
        description=(
            f"**{item_data['name']} prices {'increased' if price_change_percent > 0 else 'dropped'} "
            f"by {abs(price_change_percent)}%!**\n"
            f"New price: {format_money(new_price)} (for {duration_minutes} minutes)"
        ),
        color=discord.Color.red() if price_change_percent > 0 else discord.Color.green()
    )
    
    await channel.send(embed=embed)
    
    # Store active news
    active_news[item_id] = {
        "end_time": datetime.now() + timedelta(seconds=duration),
        "original_prices": {
            guild_id: server_shops[guild_id]["items"][item_id]["price"]
            for guild_id in server_shops if item_id in server_shops[guild_id]["items"]
        }
    }
    
    # Schedule price reset
    await asyncio.sleep(duration)
    if item_id in active_news:
        reset_item_price(item_id)
        del active_news[item_id]

def reset_item_price(item_id):
    if item_id in active_news:
        for guild_id_str in server_shops:
            if item_id in server_shops[guild_id_str]["items"]:
                original_price = active_news[item_id]["original_prices"].get(guild_id_str)
                if original_price is not None:
                    server_shops[guild_id_str]["items"][item_id]["price"] = original_price
        save_data()

# Background tasks
@tasks.loop(minutes=10)
async def shop_reset_task():
    for guild_id_str in server_shops:
        update_server_shop(int(guild_id_str))
    
    # Occasionally adjust lottery prize (30% chance)
    if random.random() < 0.3:
        old_prize = CURRENT_LOTTERY_PRIZE
        new_prize = adjust_lottery_prize()
        
        # Find a random channel to announce the change
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
                    await announce_lottery_prize_change(channel, old_prize, new_prize)
                    break
    
    # Send news occasionally (20% chance every 10 minutes)
    if random.random() < 0.2:
        item_id = random.choice(list(BASE_SHOP_ITEMS.keys()))
        price_change = random.choice([-30, -20, -15, 10, 15, 20])  # More likely to decrease prices
        duration = random.randint(1, 5)  # 1-5 minutes
        
        # Find a random channel to send news to
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
                    await send_breaking_news(channel, item_id, price_change, duration)
                    return

@tasks.loop(minutes=1)
async def check_news_expiry():
    current_time = datetime.now()
    expired_news = []
    
    for item_id, news_data in active_news.items():
        if current_time >= news_data["end_time"]:
            reset_item_price(item_id)
            expired_news.append(item_id)
    
    for item_id in expired_news:
        del active_news[item_id]

# Bot events
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    
    # Start background tasks
    shop_reset_task.start()
    check_news_expiry.start()
    update_lottery_description()

# Economy Commands (same as before but with adjusted money amounts)
@bot.tree.command(name="work", description="Work to earn money")
async def work(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_data = get_user_data(user_id)
    
    # Check work boost
    work_multiplier = 1.0
    if has_item(user_id, "workboost") and get_cooldown(user_id, "workboost") > datetime.now().timestamp():
        work_multiplier = 1.5
    
    # Check cooldown
    cooldown_left = check_cooldown(user_id, "work")
    if cooldown_left > 0:
        await interaction.response.send_message(
            f"You're too tired to work right now. Try again in {format_time(cooldown_left)}."
        )
        return
    
    # User can work
    base_amount = random.randint(50, 150)  # Reduced from original
    amount = int(base_amount * work_multiplier)
    new_balance = update_balance(user_id, amount)
    
    # Update stats and cooldown
    user_data["stats"]["times_worked"] += 1
    set_cooldown(user_id, "work", 3600)  # 1 hour cooldown
    save_data()
    
    jobs = [
        "You worked as a programmer and earned",
        "You delivered food and earned",
        "You worked at a cafe and earned",
        "You did some freelancing and earned",
        "You worked construction and earned"
    ]
    
    boost_msg = " (work boost active!)" if work_multiplier > 1 else ""
    await interaction.response.send_message(
        f"{random.choice(jobs)}{boost_msg} {format_money(amount)}! Your new balance is {format_money(new_balance)}"
    )

# Shop Commands
@bot.tree.command(name="shop", description="View items available for purchase")
async def shop(interaction: discord.Interaction):
    shop_data = get_server_shop(interaction.guild.id)
    
    embed = discord.Embed(
        title="🛒 Fun.Bot Shop",
        description="Buy items to enhance your experience!",
        color=discord.Color.green()
    )
    
    for item_id, item_data in BASE_SHOP_ITEMS.items():
        if item_id in shop_data["items"]:
            shop_item = shop_data["items"][item_id]
            embed.add_field(
                name=f"{item_data['name']} - {format_money(shop_item['price'])} (Stock: {shop_item['stock']})",
                value=item_data["description"],
                inline=False
            )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="buy", description="Purchase an item from the shop")
async def buy(interaction: discord.Interaction, item: str):
    user_id = interaction.user.id
    current_balance = get_balance(user_id)
    shop_data = get_server_shop(interaction.guild.id)
    
    if item not in BASE_SHOP_ITEMS or item not in shop_data["items"]:
        await interaction.response.send_message("That item doesn't exist in the shop!")
        return
    
    item_data = BASE_SHOP_ITEMS[item]
    shop_item = shop_data["items"][item]
    price = shop_item["price"]
    stock = shop_item["stock"]
    
    if stock <= 0:
        await interaction.response.send_message(f"Sorry, {item_data['name']} is out of stock!")
        return
    
    if current_balance < price:
        await interaction.response.send_message(f"You don't have enough money to buy {item_data['name']}!")
        return
    
    # Handle lottery tickets specially
    if item == "lotteryticket":
        add_item_to_inventory(user_id, item)
        # 1 in 650 chance to win
        if random.randint(1, LOTTERY_WIN_CHANCE) == 1:
            win_amount = CURRENT_LOTTERY_PRIZE
            new_balance = update_balance(user_id, win_amount)
            
            # Update user stats
            user_data = get_user_data(user_id)
            user_data["stats"]["lottery_wins"] += 1
            save_data()
            
            # Record winner
            lottery_winners.append({
                "user": interaction.user,
                "amount": win_amount,
                "time": datetime.now()
            })
            
            # Announce winner globally
            await announce_lottery_winner(interaction.user, win_amount)
            
            # Reset lottery prize
            global CURRENT_LOTTERY_PRIZE
            CURRENT_LOTTERY_PRIZE = LOTTERY_MIN_PRIZE
            update_lottery_description()
            save_data()
            
            await interaction.response.send_message(
                f"🎉 YOU WON THE LOTTERY! {format_money(win_amount)} has been added to your account! "
                f"Your new balance is {format_money(new_balance)}"
            )
            return
    
    # For all other items
    add_item_to_inventory(user_id, item)
    
    # Update stock and balance
    shop_item["stock"] -= 1
    update_balance(user_id, -price)
    save_data()
    
    await interaction.response.send_message(
        f"You bought {item_data['name']} for {format_money(price)}! Use `/inventory` to see your items."
    )

# Lottery Command
@bot.tree.command(name="lottery", description="Check current lottery status")
async def lottery(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Lottery Information",
        description=(
            f"Buy lottery tickets from the shop for a chance to win big!\n"
            f"Each ticket has a 1 in {LOTTERY_WIN_CHANCE} chance to win!\n"
            f"Current jackpot: {format_money(CURRENT_LOTTERY_PRIZE)}\n\n"
            f"Recent winners:"
        ),
        color=discord.Color.gold()
    )
    
    # Add recent winners (up to 5)
    if lottery_winners:
        for winner in lottery_winners[-5:]:  # Show last 5 winners
            time_ago = datetime.now() - winner["time"]
            hours = time_ago.seconds // 3600
            minutes = (time_ago.seconds % 3600) // 60
            embed.add_field(
                name=f"{winner['user'].display_name}",
                value=f"Won {format_money(winner['amount'])} {hours}h {minutes}m ago",
                inline=False
            )
    else:
        embed.add_field(
            name="No recent winners",
            value="Could you be the first?",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == "__main__":
    load_data()
    bot_token = os.getenv("DISCORD_TOKEN")
    if not bot_token:
        raise ValueError("No DISCORD_TOKEN environment variable found!")
    bot.run(bot_token)
