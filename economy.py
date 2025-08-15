import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os
from datetime import datetime, timedelta

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "economy_data.json"
        self.economy_data = self.load_data()
        
        # Shop items
        self.shop_items = {
            "coffee": {"price": 50, "description": "☕ A nice cup of coffee", "emoji": "☕"},
            "cookie": {"price": 25, "description": "🍪 A delicious cookie", "emoji": "🍪"},
            "pizza": {"price": 100, "description": "🍕 A tasty pizza slice", "emoji": "🍕"},
            "trophy": {"price": 500, "description": "🏆 A shiny trophy", "emoji": "🏆"},
            "gem": {"price": 1000, "description": "💎 A precious gem", "emoji": "💎"},
            "car": {"price": 5000, "description": "🚗 A nice car", "emoji": "🚗"},
            "house": {"price": 25000, "description": "🏠 A beautiful house", "emoji": "🏠"},
            "rocket": {"price": 100000, "description": "🚀 A space rocket", "emoji": "🚀"}
        }
        
        # Work jobs
        self.jobs = [
            {"name": "Programmer", "min_pay": 100, "max_pay": 500, "emoji": "💻"},
            {"name": "Teacher", "min_pay": 80, "max_pay": 300, "emoji": "📚"},
            {"name": "Chef", "min_pay": 60, "max_pay": 250, "emoji": "👨‍🍳"},
            {"name": "Doctor", "min_pay": 200, "max_pay": 800, "emoji": "👨‍⚕️"},
            {"name": "Artist", "min_pay": 50, "max_pay": 400, "emoji": "🎨"},
            {"name": "Musician", "min_pay": 70, "max_pay": 350, "emoji": "🎵"},
            {"name": "Writer", "min_pay": 40, "max_pay": 200, "emoji": "✍️"},
            {"name": "Delivery Driver", "min_pay": 30, "max_pay": 150, "emoji": "🚚"}
        ]

    def load_data(self):
        """Load economy data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_data(self):
        """Save economy data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.economy_data, f, indent=2)

    def get_user_data(self, user_id: str):
        """Get user's economy data"""
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {
                "balance": 1000,  # Starting balance
                "inventory": {},
                "last_daily": None,
                "last_work": None
            }
            self.save_data()
        return self.economy_data[user_id]

    def can_use_command(self, user_data: dict, command: str, cooldown_hours: int):
        """Check if user can use a command (cooldown check)"""
        last_used = user_data.get(f"last_{command}")
        if not last_used:
            return True
        
        last_time = datetime.fromisoformat(last_used)
        now = datetime.now()
        return now - last_time >= timedelta(hours=cooldown_hours)

    @app_commands.command(name="profile", description="View your economy profile")
    async def profile(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        user_data = self.get_user_data(str(target.id))
        
        # Calculate net worth (balance + inventory value)
        inventory_value = 0
        for item, count in user_data["inventory"].items():
            if item in self.shop_items:
                inventory_value += self.shop_items[item]["price"] * count
        
        net_worth = user_data["balance"] + inventory_value
        
        embed = discord.Embed(
            title=f"💰 {target.display_name}'s Profile",
            color=0xffd700
        )
        
        embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)
        
        embed.add_field(name="💵 Balance", value=f"{user_data['balance']:,} coins", inline=True)
        embed.add_field(name="📦 Items", value=f"{len(user_data['inventory'])} types", inline=True)
        embed.add_field(name="💎 Net Worth", value=f"{net_worth:,} coins", inline=True)
        
        # Show top 3 items in inventory
        if user_data["inventory"]:
            top_items = sorted(user_data["inventory"].items(), key=lambda x: x[1], reverse=True)[:3]
            items_text = "\n".join([f"{self.shop_items.get(item, {}).get('emoji', '📦')} {item.title()}: {count}" 
                                  for item, count in top_items])
            embed.add_field(name="🎒 Top Items", value=items_text, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="Claim your daily coins")
    async def daily_reward(self, interaction: discord.Interaction):
        user_data = self.get_user_data(str(interaction.user.id))
        
        if not self.can_use_command(user_data, "daily", 24):
            last_daily = datetime.fromisoformat(user_data["last_daily"])
            next_daily = last_daily + timedelta(hours=24)
            time_left = next_daily - datetime.now()
            
            hours, remainder = divmod(int(time_left.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            
            embed = discord.Embed(
                title="⏰ Daily Cooldown",
                description=f"You've already claimed your daily reward!\nCome back in {hours}h {minutes}m",
                color=0xff4500
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Give daily reward
        daily_amount = random.randint(100, 500)
        user_data["balance"] += daily_amount
        user_data["last_daily"] = datetime.now().isoformat()
        self.save_data()
        
        embed = discord.Embed(
            title="🎁 Daily Reward",
            description=f"You received {daily_amount} coins!\nCome back tomorrow for more!",
            color=0x00ff00
        )
        embed.add_field(name="💰 New Balance", value=f"{user_data['balance']:,} coins", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="balance", description="Check your coin balance")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        user_data = self.get_user_data(str(target.id))
        
        embed = discord.Embed(
            title=f"💰 {target.display_name}'s Balance",
            description=f"**{user_data['balance']:,}** coins",
            color=0xffd700
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="work", description="Work to earn coins")
    async def work(self, interaction: discord.Interaction):
        user_data = self.get_user_data(str(interaction.user.id))
        
        if not self.can_use_command(user_data, "work", 1):  # 1 hour cooldown
            last_work = datetime.fromisoformat(user_data["last_work"])
            next_work = last_work + timedelta(hours=1)
            time_left = next_work - datetime.now()
            
            minutes, _ = divmod(int(time_left.total_seconds()), 60)
            
            embed = discord.Embed(
                title="😴 Work Cooldown",
                description=f"You're too tired to work!\nRest for {minutes} more minutes",
                color=0xff4500
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Choose random job
        job = random.choice(self.jobs)
        earnings = random.randint(job["min_pay"], job["max_pay"])
        
        user_data["balance"] += earnings
        user_data["last_work"] = datetime.now().isoformat()
        self.save_data()
        
        embed = discord.Embed(
            title="💼 Work Complete!",
            description=f"You worked as a {job['emoji']} **{job['name']}** and earned **{earnings}** coins!",
            color=0x00ff00
        )
        embed.add_field(name="💰 New Balance", value=f"{user_data['balance']:,} coins", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rob", description="Try to rob another user (risky!)")
    async def rob(self, interaction: discord.Interaction, target: discord.Member):
        if target.id == interaction.user.id:
            await interaction.response.send_message("❌ You can't rob yourself!")
            return
        
        if target.bot:
            await interaction.response.send_message("❌ You can't rob bots!")
            return
        
        robber_data = self.get_user_data(str(interaction.user.id))
        target_data = self.get_user_data(str(target.id))
        
        # Check if robber has enough money to attempt
        if robber_data["balance"] < 100:
            await interaction.response.send_message("❌ You need at least 100 coins to attempt a robbery!")
            return
        
        # Check if target has money to rob
        if target_data["balance"] < 50:
            await interaction.response.send_message(f"❌ {target.display_name} doesn't have enough coins to rob!")
            return
        
        # 60% chance of success
        if random.randint(1, 100) <= 60:
            # Successful robbery
            stolen_amount = random.randint(50, min(target_data["balance"] // 2, 1000))
            
            target_data["balance"] -= stolen_amount
            robber_data["balance"] += stolen_amount
            self.save_data()
            
            embed = discord.Embed(
                title="🕵️ Robbery Successful!",
                description=f"You successfully robbed **{stolen_amount}** coins from {target.display_name}!",
                color=0x00ff00
            )
            embed.add_field(name="💰 Your Balance", value=f"{robber_data['balance']:,} coins", inline=False)
        else:
            # Failed robbery - lose money
            penalty = random.randint(100, min(robber_data["balance"] // 4, 500))
            robber_data["balance"] -= penalty
            self.save_data()
            
            embed = discord.Embed(
                title="🚨 Robbery Failed!",
                description=f"You got caught! You lost **{penalty}** coins as a fine!",
                color=0xff0000
            )
            embed.add_field(name="💰 Your Balance", value=f"{robber_data['balance']:,} coins", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gamble", description="Gamble your coins (double or nothing)")
    async def gamble(self, interaction: discord.Interaction, amount: int):
        user_data = self.get_user_data(str(interaction.user.id))
        
        if amount <= 0:
            await interaction.response.send_message("❌ You must bet a positive amount!")
            return
        
        if amount > user_data["balance"]:
            await interaction.response.send_message("❌ You don't have enough coins!")
            return
        
        # 45% chance to win (house edge)
        if random.randint(1, 100) <= 45:
            # Win
            user_data["balance"] += amount
            self.save_data()
            
            embed = discord.Embed(
                title="🎰 You Won!",
                description=f"Congratulations! You won **{amount}** coins!",
                color=0x00ff00
            )
            embed.add_field(name="💰 New Balance", value=f"{user_data['balance']:,} coins", inline=False)
        else:
            # Lose
            user_data["balance"] -= amount
            self.save_data()
            
            embed = discord.Embed(
                title="🎰 You Lost!",
                description=f"Better luck next time! You lost **{amount}** coins!",
                color=0xff0000
            )
            embed.add_field(name="💰 New Balance", value=f"{user_data['balance']:,} coins", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shop", description="View the shop")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛒 Shop",
            description="Welcome to the shop! Use `/buy <item>` to purchase items.",
            color=0x4169e1
        )
        
        for item_name, item_data in self.shop_items.items():
            embed.add_field(
                name=f"{item_data['emoji']} {item_name.title()}",
                value=f"{item_data['description']}\n**Price:** {item_data['price']:,} coins",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Buy an item from the shop")
    async def buy_item(self, interaction: discord.Interaction, item: str, quantity: int = 1):
        user_data = self.get_user_data(str(interaction.user.id))
        item = item.lower()
        
        if item not in self.shop_items:
            available_items = ", ".join(self.shop_items.keys())
            await interaction.response.send_message(f"❌ Item not found! Available items: {available_items}")
            return
        
        if quantity <= 0:
            await interaction.response.send_message("❌ Quantity must be positive!")
            return
        
        total_cost = self.shop_items[item]["price"] * quantity
        
        if user_data["balance"] < total_cost:
            await interaction.response.send_message(f"❌ You need {total_cost:,} coins but only have {user_data['balance']:,} coins!")
            return
        
        # Make purchase
        user_data["balance"] -= total_cost
        if item in user_data["inventory"]:
            user_data["inventory"][item] += quantity
        else:
            user_data["inventory"][item] = quantity
        
        self.save_data()
        
        embed = discord.Embed(
            title="✅ Purchase Successful!",
            description=f"You bought {quantity}x {self.shop_items[item]['emoji']} **{item.title()}** for {total_cost:,} coins!",
            color=0x00ff00
        )
        embed.add_field(name="💰 New Balance", value=f"{user_data['balance']:,} coins", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory", description="View your inventory")
    async def inventory(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        user_data = self.get_user_data(str(target.id))
        
        if not user_data["inventory"]:
            embed = discord.Embed(
                title=f"🎒 {target.display_name}'s Inventory",
                description="Inventory is empty! Visit the shop to buy items.",
                color=0xff4500
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"🎒 {target.display_name}'s Inventory",
            color=0x9932cc
        )
        
        total_value = 0
        for item, quantity in user_data["inventory"].items():
            if item in self.shop_items:
                item_data = self.shop_items[item]
                value = item_data["price"] * quantity
                total_value += value
                
                embed.add_field(
                    name=f"{item_data['emoji']} {item.title()}",
                    value=f"Quantity: {quantity}\nValue: {value:,} coins",
                    inline=True
                )
        
        embed.add_field(name="💎 Total Value", value=f"{total_value:,} coins", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="give", description="Give coins to another user")
    async def give_coins(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if user.id == interaction.user.id:
            await interaction.response.send_message("❌ You can't give coins to yourself!")
            return
        
        if user.bot:
            await interaction.response.send_message("❌ You can't give coins to bots!")
            return
        
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive!")
            return
        
        giver_data = self.get_user_data(str(interaction.user.id))
        receiver_data = self.get_user_data(str(user.id))
        
        if giver_data["balance"] < amount:
            await interaction.response.send_message(f"❌ You only have {giver_data['balance']:,} coins!")
            return
        
        # Transfer coins
        giver_data["balance"] -= amount
        receiver_data["balance"] += amount
        self.save_data()
        
        embed = discord.Embed(
            title="💝 Coins Transferred!",
            description=f"{interaction.user.display_name} gave {amount:,} coins to {user.display_name}!",
            color=0x00ff00
        )
        embed.add_field(name="💰 Your Balance", value=f"{giver_data['balance']:,} coins", inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
