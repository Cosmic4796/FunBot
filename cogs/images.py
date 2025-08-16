import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import random

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_animal_image(self, animal_type: str):
        """Get animal images from free APIs"""
        try:
            async with aiohttp.ClientSession() as session:
                if animal_type == "cat":
                    async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return data[0]['url']
                elif animal_type == "dog":
                    async with session.get("https://api.thedogapi.com/v1/images/search") as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return data[0]['url']
                elif animal_type == "fox":
                    async with session.get("https://randomfox.ca/floof/") as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return data['image']
                return None
        except Exception:
            return None

    @app_commands.command(name="animal", description="Get random animal images: cat, dog, fox")
    async def animal_image(self, interaction: discord.Interaction, animal: str):
        animal = animal.lower()
        valid_animals = ["cat", "dog", "fox"]
        
        if animal not in valid_animals:
            embed = discord.Embed(
                title="🐾 Available Animals",
                description=f"Choose from: {', '.join(valid_animals)}",
                color=0xff69b4
            )
            await interaction.response.send_message(embed=embed)
            return
        
        image_url = await self.get_animal_image(animal)
        
        emojis = {"cat": "🐱", "dog": "🐶", "fox": "🦊"}
        colors = {"cat": 0xff69b4, "dog": 0x8b4513, "fox": 0xff4500}
        
        if image_url:
            embed = discord.Embed(
                title=f"{emojis[animal]} Random {animal.title()}",
                color=colors[animal]
            )
            embed.set_image(url=image_url)
        else:
            embed = discord.Embed(
                title=f"{emojis[animal]} {animal.title()} Image",
                description=f"Here's a cute {animal} for you! 🐾",
                color=colors[animal]
            )
            embed.set_footer(text="API temporarily unavailable")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cat", description="Get a random cat image")
    async def cat_image(self, interaction: discord.Interaction):
        image_url = await self.get_animal_image("cat")
        
        if image_url:
            embed = discord.Embed(
                title="🐱 Random Cat",
                color=0xff69b4
            )
            embed.set_image(url=image_url)
        else:
            embed = discord.Embed(
                title="🐱 Cat Image",
                description="Here's a cute cat for you! 🐾",
                color=0xff69b4
            )
            embed.set_footer(text="API unavailable - showing placeholder")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dog", description="Get a random dog image")
    async def dog_image(self, interaction: discord.Interaction):
        image_url = await self.get_animal_image("dog")
        
        if image_url:
            embed = discord.Embed(
                title="🐶 Random Dog",
                color=0x8b4513
            )
            embed.set_image(url=image_url)
        else:
            embed = discord.Embed(
                title="🐶 Dog Image",
                description="Here's a good boy/girl for you! 🦴",
                color=0x8b4513
            )
            embed.set_footer(text="API unavailable - showing placeholder")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fox", description="Get a random fox image")
    async def fox_image(self, interaction: discord.Interaction):
        image_url = await self.get_animal_image("fox")
        
        if image_url:
            embed = discord.Embed(
                title="🦊 Random Fox",
                color=0xff4500
            )
            embed.set_image(url=image_url)
        else:
            embed = discord.Embed(
                title="🦊 Fox Image",
                description="What does the fox say? 🦊",
                color=0xff4500
            )
            embed.set_footer(text="API unavailable - showing placeholder")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bird", description="Get a random bird image")
    async def bird_image(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🐦 Random Bird",
            description="Tweet tweet! Here's a beautiful bird! 🪶",
            color=0x87ceeb
        )
        embed.set_footer(text="Bird API integration needed")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="panda", description="Get a random panda image")
    async def panda_image(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🐼 Random Panda",
            description="Bamboo lover spotted! 🎋",
            color=0x000000
        )
        embed.set_footer(text="Panda API integration needed")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="content", description="Get content: meme templates, inspirational quotes, color info")
    async def get_content(self, interaction: discord.Interaction, type: str, hex_code: str = None):
        type = type.lower()
        
        if type == "meme" or type == "template":
            templates = [
                {"name": "Drake Pointing", "description": "Drake disapproving/approving meme"},
                {"name": "Distracted Boyfriend", "description": "Guy looking at another girl"},
                {"name": "Woman Yelling at Cat", "description": "Angry woman pointing at confused cat"},
                {"name": "This is Fine", "description": "Dog in burning house"},
                {"name": "Expanding Brain", "description": "Brain getting bigger with ideas"},
                {"name": "Two Buttons", "description": "Superhero choosing between two buttons"},
                {"name": "Change My Mind", "description": "Guy sitting at table with sign"},
                {"name": "Pikachu Surprised Face", "description": "Shocked Pikachu expression"}
            ]
            
            template = random.choice(templates)
            
            embed = discord.Embed(
                title="😂 Meme Template",
                description=f"**{template['name']}**\n{template['description']}",
                color=0xffff00
            )
            embed.set_footer(text="Use meme generators like imgflip.com to create memes!")
            
        elif type == "inspire" or type == "quote":
            quotes = [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Life is what happens to you while you're busy making other plans. - John Lennon",
                "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                "It is during our darkest moments that we must focus to see the light. - Aristotle",
                "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
                "The only impossible journey is the one you never begin. - Tony Robbins",
                "In the middle of difficulty lies opportunity. - Albert Einstein",
                "Believe you can and you're halfway there. - Theodore Roosevelt"
            ]
            
            quote = random.choice(quotes)
            
            embed = discord.Embed(
                title="✨ Daily Inspiration",
                description=f"*{quote}*",
                color=0x9932cc
            )
            embed.set_footer(text="Stay motivated! 💪")
            
        elif type == "color" and hex_code:
            # Remove # if present
            hex_code = hex_code.replace("#", "")
            
            # Validate hex code
            if len(hex_code) != 6 or not all(c in '0123456789abcdefABCDEF' for c in hex_code):
                await interaction.response.send_message("❌ Invalid hex color! Please use format: #RRGGBB or RRGGBB")
                return
            
            # Convert to RGB
            try:
                r = int(hex_code[0:2], 16)
                g = int(hex_code[2:4], 16)
                b = int(hex_code[4:6], 16)
            except ValueError:
                await interaction.response.send_message("❌ Invalid hex color!")
                return
            
            embed = discord.Embed(
                title="🎨 Color Information",
                color=int(hex_code, 16)
            )
            
            embed.add_field(name="Hex", value=f"#{hex_code.upper()}", inline=True)
            embed.add_field(name="RGB", value=f"{r}, {g}, {b}", inline=True)
            embed.add_field(name="Preview", value="See embed color", inline=True)
            
        else:
            embed = discord.Embed(
                title="❌ Invalid Type",
                description="Available types: **meme**, **inspire**, **color** (requires hex_code)",
                color=0xff4500
            )
            embed.add_field(name="Usage Examples:", value="`/content meme`\n`/content inspire`\n`/content color ff0000`", inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Images(bot))
