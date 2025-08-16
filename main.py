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

# Data Management
DATA_FILE = "economy_data.json" # Save file location
DATA_BACKUP_MINUTES = 30       # Auto-save interval

# =============================================
#             GLOBAL VARIABLES
# =============================================
# These are initialized here and modified in functions

CURRENT_LOTTERY_PRIZE = LOTTERY_START_PRIZE
economy_data = {}
server_shops = {}
active_news = {}
lottery_winners = []

# Base shop items
BASE_SHOP_ITEMS = {
    "padlock": {
        "name": "Padlock",
        "base_price": 800,
        "description": "Protects against one robbery",
        "usable": True,
        "max_stock": 10
    },
    "fishingrod": {
        "name": "Fishing Rod",
        "base_price": 1200,
        "description": "Durability: 10 uses",
        "usable": False,
        "max_stock": 8
    },
    "luckycoin": {
        "name": "Lucky Coin",
        "base_price": 1500,
        "description": "+10% gambling win chance",
        "usable": True,
        "max_stock": 5
    },
    "workboost": {
        "name": "Work Boost",
        "base_price": 1000,
        "description": "+50% work earnings for 1 day",
        "usable": True,
        "max_stock": 7
    },
    "lotteryticket": {
        "name": "Lottery Ticket",
        "base_price": LOTTERY_TICKET_PRICE,
        "description": f"1 in {LOTTERY_WIN_CHANCE} chance to win! Current jackpot: {CURRENCY}{LOTTERY_START_PRIZE:,}",
        "usable": True,
        "max_stock": LOTTERY_MAX_STOCK
    },
    "diamondring": {
        "name": "Diamond Ring",
        "base_price": 3000,
        "description": "+20% begging success rate",
        "usable": True,
        "max_stock": 3
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

# Initialize bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

def load_data():
    global economy_data, server_shops, CURRENT_LOTTERY_PRIZE
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            economy_data = data.get("economy", {})
            server_shops = data.get("shops", {})
            CURRENT_LOTTERY_PRIZE = data.get("lottery_prize", LOTTERY_START_PRIZE)
    update_lottery_description()

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
        server_shops[guild_id_str] = {"items": {}, "last_reset": datetime.now().timestamp()}
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
            stock_change = random.randint(*STOCK_CHANGE_RANGE)
            new_stock = shop["items"][item_id]["stock"] + stock_change
            shop["items"][item_id]["stock"] = max(1, min(new_stock, item_data["max_stock"]))
            
            price_change = random.uniform(*PRICE_CHANGE_RANGE)
            shop["items"][item_id]["price"] = max(
                item_data["base_price"] * 0.5,
                min(
                    item_data["base_price"] * 1.5,
                    int(shop["items"][item_id]["price"] * (1 + price_change))
                )
            )
    
    shop["last_reset"] = datetime.now().timestamp()
    save_data()

def get_balance(user_id):
    return get_user_data(user_id)["balance"]

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
        inventory[item_name] = {"quantity": quantity, "data": data or {}}
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
    return item_name in get_user_data(user_id)["inventory"]

def check_cooldown(user_id, cooldown_type):
    last_used = get_user_data(user_id).get("cooldowns", {}).get(cooldown_type, 0)
    current_time = int(datetime.now().timestamp())
    return max(0, last_used - current_time)

def set_cooldown(user_id, cooldown_type, duration_seconds):
    user_data = get_user_data(user_id)
    if "cooldowns" not in user_data:
        user_data["cooldowns"] = {}
    user_data["cooldowns"][cooldown_type] = int(datetime.now().timestamp()) + duration_seconds
    save_data()

def adjust_lottery_prize():
    global CURRENT_LOTTERY_PRIZE
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
            f"Old prize: {CURRENCY}{old_prize:,}\n"
            f"New prize: {CURRENCY}{new_prize:,}\n"
            f"Change: {'+' if change > 0 else ''}{CURRENCY}{abs(change):,}"
        ),
        color=discord.Color.green() if change > 0 else discord.Color.red()
    )
    await channel.send(embed=embed)

async def announce_lottery_winner(winner: discord.User, amount):
    embed = discord.Embed(
        title="🎉 LOTTERY WINNER!",
        description=f"**{winner.display_name}** won {CURRENCY}{amount:,}!",
        color=discord.Color.gold()
    )
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
                try:
                    await channel.send(embed=embed)
                    break
                except:
                    continue

async def send_breaking_news(channel, item_id, price_change_percent, duration_minutes):
    item_data = BASE_SHOP_ITEMS[item_id]
    duration = min(duration_minutes * 60, 300)
    new_price = max(
        item_data["base_price"] * 0.5,
        int(item_data["base_price"] * (1 + price_change_percent / 100))
    )
    
    for guild_id_str in server_shops:
        if item_id in server_shops[guild_id_str]["items"]:
            server_shops[guild_id_str]["items"][item_id]["price"] = new_price
    
    embed = discord.Embed(
        title="📰 BREAKING NEWS",
        description=(
            f"**{item_data['name']} prices {'increased' if price_change_percent > 0 else 'dropped'} "
            f"by {abs(price_change_percent)}%!**\n"
            f"New price: {CURRENCY}{new_price:,} (for {duration_minutes} minutes)"
        ),
        color=discord.Color.red() if price_change_percent > 0 else discord.Color.green()
    )
    await channel.send(embed=embed)
    
    active_news[item_id] = {
        "end_time": datetime.now() + timedelta(seconds=duration),
        "original_prices": {
            guild_id: server_shops[guild_id]["items"][item_id]["price"]
            for guild_id in server_shops if item_id in server_shops[guild_id]["items"]
        }
    }
    
    await asyncio.sleep(duration)
    if item_id in active_news:
        for guild_id_str in server_shops:
            if item_id in server_shops[guild_id_str]["items"]:
                original_price = active_news[item_id]["original_prices"].get(guild_id_str)
                if original_price is not None:
                    server_shops[guild_id_str]["items"][item_id]["price"] = original_price
        del active_news[item_id]

@tasks.loop(minutes=SHOP_RESET_MINUTES)
async def shop_reset_task():
    for guild_id_str in server_shops:
        update_server_shop(int(guild_id_str))
    
    if random.random() < NEWS_CHANCE:
        item_id = random.choice(list(BASE_SHOP_ITEMS.keys()))
        price_change = random.choice([-30, -20, -15, 10, 15, 20])
        duration = random.randint(1, 5)
        
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
                    await send_breaking_news(channel, item_id, price_change, duration)
                    return

@tasks.loop(minutes=1)
async def check_news_expiry():
    current_time = datetime.now()
    for item_id, news_data in list(active_news.items()):
        if current_time >= news_data["end_time"]:
            for guild_id_str in server_shops:
                if item_id in server_shops[guild_id_str]["items"]:
                    original_price = news_data["original_prices"].get(guild_id_str)
                    if original_price is not None:
                        server_shops[guild_id_str]["items"][item_id]["price"] = original_price
            del active_news[item_id]

@tasks.loop(minutes=DATA_BACKUP_MINUTES)
async def data_backup_task():
    save_data()

@bot.event
async def on_ready():
    print(f'{BOT_NAME} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    
    shop_reset_task.start()
    check_news_expiry.start()
    data_backup_task.start()

# =============================================
#             COMMAND IMPLEMENTATIONS
# =============================================

@bot.tree.command(name="balance", description="Check your balance")
async def balance(interaction: discord.Interaction, user: discord.User = None):
    target = user or interaction.user
    bal = get_balance(target.id)
    await interaction.response.send_message(f"{target.display_name} has {CURRENCY}{bal:,}")

@bot.tree.command(name="beg", description="Beg for money")
async def beg(interaction: discord.Interaction):
    user_id = interaction.user.id
    if random.random() < BEG_CHANCE:
        amount = random.randint(BEG_MIN, BEG_MAX)
        new_balance = update_balance(user_id, amount)
        responses = [
            f"A kind stranger gave you {CURRENCY}{amount:,}!",
            f"You found {CURRENCY}{amount:,} on the ground!",
            f"Someone took pity on you and gave you {CURRENCY}{amount:,}."
        ]
        await interaction.response.send_message(random.choice(responses))
    else:
        responses = [
            "No one gave you anything. Try again later.",
            "You were ignored by everyone.",
            "People walked past you without noticing."
        ]
        await interaction.response.send_message(random.choice(responses))

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
            f"You're too tired to work right now. Try again in {cooldown_left//60}m {cooldown_left%60}s."
        )
        return
    
    # User can work
    base_amount = random.randint(WORK_MIN_EARNINGS, WORK_MAX_EARNINGS)
    amount = int(base_amount * work_multiplier)
    new_balance = update_balance(user_id, amount)
    
    # Update stats and cooldown
    user_data["stats"]["times_worked"] += 1
    set_cooldown(user_id, "work", WORK_COOLDOWN)
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
        f"{random.choice(jobs)}{boost_msg} {CURRENCY}{amount:,}! Your new balance is {CURRENCY}{new_balance:,}"
    )

@bot.tree.command(name="daily", description="Claim your daily reward")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_data = get_user_data(user_id)
    
    # Check cooldown
    cooldown_left = check_cooldown(user_id, "daily")
    if cooldown_left > 0:
        await interaction.response.send_message(
            f"You've already claimed your daily today! Come back in {cooldown_left//3600}h {(cooldown_left%3600)//60}m."
        )
        return
    
    # Calculate daily amount (base + bonus for streak)
    streak = user_data.get("daily_streak", 0) + 1
    bonus_amount = min(500, streak * 50)  # Max 500 bonus
    total_amount = DAILY_REWARD + bonus_amount
    
    # Update balance and cooldown
    new_balance = update_balance(user_id, total_amount)
    set_cooldown(user_id, "daily", 86400)  # 24 hours
    user_data["daily_streak"] = streak
    save_data()
    
    await interaction.response.send_message(
        f"🎉 You claimed your daily reward of {CURRENCY}{total_amount:,} "
        f"(streak: {streak} days)! Your new balance is {CURRENCY}{new_balance:,}"
    )

@bot.tree.command(name="gamble", description="Gamble some money")
async def gamble(interaction: discord.Interaction, amount: int):
    user_id = interaction.user.id
    current_balance = get_balance(user_id)
    
    if amount <= 0:
        await interaction.response.send_message("Amount must be positive!")
        return
    
    if amount > current_balance:
        await interaction.response.send_message("You don't have enough money!")
        return
    
    # Check for lucky coin
    win_chance = 0.45  # 45% base
    if has_item(user_id, "luckycoin"):
        win_chance = 0.55  # 55% with lucky coin
    
    # Update stats
    get_user_data(user_id)["stats"]["times_gambled"] += 1
    save_data()
    
    if random.random() < win_chance:
        win_amount = amount * 2
        new_balance = update_balance(user_id, win_amount)
        await interaction.response.send_message(
            f"🎉 You won {CURRENCY}{win_amount:,}! New balance: {CURRENCY}{new_balance:,}"
        )
    else:
        new_balance = update_balance(user_id, -amount)
        await interaction.response.send_message(
            f"😢 You lost {CURRENCY}{amount:,}. New balance: {CURRENCY}{new_balance:,}"
        )

@bot.tree.command(name="slots", description="Play the slot machine")
async def slots(interaction: discord.Interaction, bet: int):
    user_id = interaction.user.id
    current_balance = get_balance(user_id)
    
    if bet <= 0:
        await interaction.response.send_message("Bet must be positive!")
        return
    
    if bet > current_balance:
        await interaction.response.send_message("You don't have enough money!")
        return
    
    # Slot machine logic
    emojis = ["🍒", "🍋", "🍊", "🍇", "🍉", "7️⃣"]
    slots = [random.choice(emojis) for _ in range(3)]
    result = " ".join(slots)
    
    # Check for wins
    if slots[0] == slots[1] == slots[2]:
        if slots[0] == "7️⃣":
            win_amount = bet * 10
            outcome = "JACKPOT! 🎰"
        else:
            win_amount = bet * 5
            outcome = "Big win!"
    elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
        win_amount = bet * 2
        outcome = "Small win!"
    else:
        win_amount = -bet
        outcome = "You lost!"
    
    new_balance = update_balance(user_id, win_amount)
    
    if win_amount > 0:
        message = f"{result}\n{outcome} You won {CURRENCY}{win_amount:,}! New balance: {CURRENCY}{new_balance:,}"
    else:
        message = f"{result}\n{outcome} {CURRENCY}{bet:,}. New balance: {CURRENCY}{new_balance:,}"
    
    await interaction.response.send_message(message)

@bot.tree.command(name="rob", description="Attempt to rob another user")
async def rob(interaction: discord.Interaction, user: discord.User):
    robber_id = interaction.user.id
    victim_id = user.id
    
    if robber_id == victim_id:
        await interaction.response.send_message("You can't rob yourself!")
        return
    
    robber_balance = get_balance(robber_id)
    victim_balance = get_balance(victim_id)
    victim_data = get_user_data(victim_id)
    
    # Check if victim has padlock protection
    if has_item(victim_id, "padlock"):
        remove_item_from_inventory(victim_id, "padlock")
        await interaction.response.send_message(
            f"{user.display_name}'s wallet is protected by a padlock! Your robbery attempt failed, but the padlock broke."
        )
        return
    
    if victim_balance < 100:
        await interaction.response.send_message(f"{user.display_name} doesn't have enough money to rob!")
        return
    
    # Robbery attempt
    if random.random() < ROB_CHANCE:
        amount = random.randint(1, min(500, victim_balance))
        update_balance(victim_id, -amount)
        new_balance = update_balance(robber_id, amount)
        
        responses = [
            f"You successfully robbed {user.display_name} and got away with {CURRENCY}{amount:,}!",
            f"You mugged {user.display_name} and stole {CURRENCY}{amount:,}!",
            f"After a daring heist, you stole {CURRENCY}{amount:,} from {user.display_name}!"
        ]
        await interaction.response.send_message(random.choice(responses))
    else:
        # Failed robbery - lose money
        fine = random.randint(ROB_MIN_FINE, ROB_MAX_FINE)
        new_balance = update_balance(robber_id, -fine)
        
        responses = [
            f"You got caught trying to rob {user.display_name} and had to pay a fine of {CURRENCY}{fine:,}!",
            f"Your robbery attempt failed and you were fined {CURRENCY}{fine:,}!",
            f"{user.display_name} fought back and you had to pay {CURRENCY}{fine:,} in damages!"
        ]
        await interaction.response.send_message(random.choice(responses))

@bot.tree.command(name="pay", description="Pay another user")
async def pay(interaction: discord.Interaction, user: discord.User, amount: int):
    sender_id = interaction.user.id
    receiver_id = user.id
    
    if sender_id == receiver_id:
        await interaction.response.send_message("You can't pay yourself!")
        return
    
    if amount <= 0:
        await interaction.response.send_message("Amount must be positive!")
        return
    
    sender_balance = get_balance(sender_id)
    if amount > sender_balance:
        await interaction.response.send_message("You don't have enough money!")
        return
    
    # Process payment
    update_balance(sender_id, -amount)
    update_balance(receiver_id, amount)
    
    await interaction.response.send_message(
        f"You paid {user.display_name} {CURRENCY}{amount:,}!"
    )

@bot.tree.command(name="shop", description="View the shop")
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
                name=f"{item_data['name']} - {CURRENCY}{shop_item['price']:,} (Stock: {shop_item['stock']})",
                value=item_data["description"],
                inline=False
            )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="buy", description="Buy an item")
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
        # Check for win
        if random.randint(1, LOTTERY_WIN_CHANCE) == 1:
            win_amount = CURRENT_LOTTERY_PRIZE
            new_balance = update_balance(user_id, win_amount)
            
            # Update stats
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
            CURRENT_LOTTERY_PRIZE = LOTTERY_MIN_PRIZE
            update_lottery_description()
            save_data()
            
            await interaction.response.send_message(
                f"🎉 YOU WON THE LOTTERY! {CURRENCY}{win_amount:,} has been added to your account! "
                f"Your new balance is {CURRENCY}{new_balance:,}"
            )
            return
    
    # For all other items
    add_item_to_inventory(user_id, item)
    
    # Update stock and balance
    shop_item["stock"] -= 1
    update_balance(user_id, -price)
    save_data()
    
    await interaction.response.send_message(
        f"You bought {item_data['name']} for {CURRENCY}{price:,}! Use `/inventory` to see your items."
    )

@bot.tree.command(name="inventory", description="View your inventory")
async def inventory(interaction: discord.Interaction, user: discord.User = None):
    target = user or interaction.user
    user_id = target.id
    user_data = get_user_data(user_id)
    inventory = user_data.get("inventory", {})
    
    if not inventory:
        await interaction.response.send_message(f"{target.display_name}'s inventory is empty!")
        return
    
    embed = discord.Embed(
        title=f"🎒 {target.display_name}'s Inventory",
        color=discord.Color.blue()
    )
    
    for item_name, item_data in inventory.items():
        shop_item = BASE_SHOP_ITEMS.get(item_name, {})
        display_name = shop_item.get("name", item_name.title())
        
        if "durability" in item_data.get("data", {}):
            value = f"Quantity: {item_data['quantity']}\nDurability: {item_data['data']['durability']}"
        else:
            value = f"Quantity: {item_data['quantity']}"
        
        embed.add_field(
            name=display_name,
            value=value,
            inline=True
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="use", description="Use an item")
async def use(interaction: discord.Interaction, item: str):
    user_id = interaction.user.id
    
    if not has_item(user_id, item):
        await interaction.response.send_message(f"You don't have any {item} in your inventory!")
        return
    
    if item not in BASE_SHOP_ITEMS or not BASE_SHOP_ITEMS[item].get("usable", False):
        await interaction.response.send_message("You can't use that item!")
        return
    
    # Handle specific items
    if item == "workboost":
        set_cooldown(user_id, "workboost", 86400)  # 1 day
        remove_item_from_inventory(user_id, item)
        await interaction.response.send_message(
            "You activated a work boost! Your next work earnings will be increased by 50% for 24 hours."
        )
    elif item == "luckycoin":
        await interaction.response.send_message(
            "The lucky coin is automatically applied to your gambling attempts!"
        )
    elif item == "padlock":
        await interaction.response.send_message(
            "The padlock is automatically applied to protect against robberies!"
        )
    else:
        await interaction.response.send_message("You used the item!")

@bot.tree.command(name="lottery", description="Check lottery status")
async def lottery(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Lottery Information",
        description=(
            f"Buy lottery tickets from the shop for a chance to win big!\n"
            f"Each ticket has a 1 in {LOTTERY_WIN_CHANCE} chance to win!\n"
            f"Current jackpot: {CURRENCY}{CURRENT_LOTTERY_PRIZE:,}\n\n"
            f"Recent winners:"
        ),
        color=discord.Color.gold()
    )
    
    # Add recent winners (up to 5)
    if lottery_winners:
        for winner in lottery_winners[-5:]:
            time_ago = datetime.now() - winner["time"]
            hours = time_ago.seconds // 3600
            minutes = (time_ago.seconds % 3600) // 60
            embed.add_field(
                name=f"{winner['user'].display_name}",
                value=f"Won {CURRENCY}{winner['amount']:,} {hours}h {minutes}m ago",
                inline=False
            )
    else:
        embed.add_field(
            name="No recent winners",
            value="Could you be the first?",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="baltop", description="Show richest users")
async def baltop(interaction: discord.Interaction):
    users = []
    for user_id_str, data in economy_data.items():
        try:
            user_id = int(user_id_str)
            user = await bot.fetch_user(user_id)
            users.append((user.display_name, data["balance"]))
        except:
            continue
    
    # Sort by balance (descending)
    users.sort(key=lambda x: x[1], reverse=True)
    
    embed = discord.Embed(
        title="🏆 Richest Users",
        color=discord.Color.gold()
    )
    
    # Add top 10 users
    for i, (name, balance) in enumerate(users[:10], 1):
        embed.add_field(
            name=f"{i}. {name}",
            value=f"{CURRENCY}{balance:,}",
            inline=False
        )
    
    # Add current user's position if not in top 10
    current_user_id = interaction.user.id
    current_balance = get_balance(current_user_id)
    current_position = next((i+1 for i, (_, bal) in enumerate(users) if bal <= current_balance), len(users)+1)
    
    embed.set_footer(text=f"Your position: #{current_position} with {CURRENCY}{current_balance:,}")
    
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
        await interaction.response.send_message("Amount must be positive!")
        return
    
    new_balance = update_balance(user.id, amount)
    await interaction.response.send_message(
        f"Gave {user.display_name} {CURRENCY}{amount:,}. New balance: {CURRENCY}{new_balance:,}"
    )

@bot.tree.command(name="take", description="[Owner] Take money from a user")
@is_owner()
async def take(interaction: discord.Interaction, user: discord.User, amount: int):
    current_balance = get_balance(user.id)
    if amount <= 0:
        await interaction.response.send_message("Amount must be positive!")
        return
    
    if amount > current_balance:
        amount = current_balance
    
    new_balance = update_balance(user.id, -amount)
    await interaction.response.send_message(
        f"Took {CURRENCY}{amount:,} from {user.display_name}. New balance: {CURRENCY}{new_balance:,}"
    )

@bot.tree.command(name="give_all", description="[Owner] Give money to everyone")
@is_owner()
async def give_all(interaction: discord.Interaction, amount: int):
    if amount <= 0:
        await interaction.response.send_message("Amount must be positive!")
        return
    
    members = interaction.guild.members
    count = 0
    
    for member in members:
        if not member.bot:
            update_balance(member.id, amount)
            count += 1
    
    await interaction.response.send_message(
        f"Gave {CURRENCY}{amount:,} to {count} members!"
    )

@bot.tree.command(name="global_announcement", description="[Owner] Announce to all servers")
@is_owner()
async def global_announcement(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Sending announcement to all servers...")
    
    total = 0
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
                try:
                    embed = discord.Embed(
                        title="📢 Global Announcement",
                        description=message,
                        color=discord.Color.gold()
                    )
                    embed.set_footer(text=f"Announcement from {interaction.user.display_name}")
                    await channel.send(embed=embed)
                    total += 1
                    break
                except:
                    continue
    
    await interaction.followup.send(f"Announcement sent to {total} servers!")

@bot.tree.command(name="reset_economy", description="[Owner] Reset all economy data")
@is_owner()
async def reset_economy(interaction: discord.Interaction):
    global economy_data, server_shops, CURRENT_LOTTERY_PRIZE
    economy_data = {}
    server_shops = {}
    CURRENT_LOTTERY_PRIZE = LOTTERY_START_PRIZE
    save_data()
    await interaction.response.send_message("Economy data has been reset!")

@bot.tree.command(name="help", description="Show all commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"{BOT_NAME} Commands",
        description="Here are all available commands:",
        color=discord.Color.blue()
    )
    
    # Economy commands
    embed.add_field(
        name="💰 Economy Commands",
        value=(
            "`/balance` - Check your balance\n"
            "`/beg` - Beg for money\n"
            "`/work` - Work to earn money\n"
            "`/daily` - Claim daily reward\n"
            "`/gamble` - Gamble money\n"
            "`/slots` - Play slot machine\n"
            "`/rob` - Attempt robbery\n"
            "`/pay` - Pay another user\n"
            "`/fish` - Go fishing\n"
            "`/baltop` - Richest users"
        ),
        inline=False
    )
    
    # Shop commands
    embed.add_field(
        name="🛒 Shop Commands",
        value=(
            "`/shop` - View shop\n"
            "`/buy` - Buy items\n"
            "`/inventory` - View inventory\n"
            "`/use` - Use items\n"
            "`/lottery` - Lottery info"
        ),
        inline=False
    )
    
    # Owner commands (only shown to owner)
    if interaction.user.id == OWNER_ID:
        embed.add_field(
            name="👑 Owner Commands",
            value=(
                "`/give` - Give money\n"
                "`/take` - Take money\n"
                "`/give_all` - Give to everyone\n"
                "`/global_announcement` - Announce to all servers\n"
                "`/reset_economy` - Reset all data"
            ),
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

# =============================================
#             BOT STARTUP
# =============================================

if __name__ == "__main__":
    load_data()
    bot_token = os.getenv("DISCORD_TOKEN")
    if not bot_token:
        raise ValueError("No DISCORD_TOKEN environment variable found!")
    bot.run(bot_token)
