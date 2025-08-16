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

    @app_commands.command(name="meme_template", description="Get popular meme templates")
    async def meme_template(self, interaction: discord.Interaction):
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
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inspire", description="Get an inspirational quote with image")
    async def inspirational_quote(self, interaction: discord.Interaction):
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "Do something today that your future self will thank you for. - Sean Cornwell"
        ]
        
        quote = random.choice(quotes)
        
        embed = discord.Embed(
            title="✨ Daily Inspiration",
            description=f"*{quote}*",
            color=0x9932cc
        )
        embed.set_footer(text="Stay motivated! 💪")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="color", description="Show color information")
    async def color_info(self, interaction: discord.Interaction, hex_code: str):
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
        
        # Convert to HSL (simplified)
        r_norm, g_norm, b_norm = r/255, g/255, b/255
        max_val = max(r_norm, g_norm, b_norm)
        min_val = min(r_norm, g_norm, b_norm)
        
        # Lightness
        l = (max_val + min_val) / 2
        
        embed = discord.Embed(
            title="🎨 Color Information",
            color=int(hex_code, 16)
        )
        
        embed.add_field(name="Hex", value=f"#{hex_code.upper()}", inline=True)
        embed.add_field(name="RGB", value=f"{r}, {g}, {b}", inline=True)
        embed.add_field(name="Lightness", value=f"{int(l*100)}%", inline=True)
        
        # Add a color preview (using the embed color)
        embed.set_footer(text="Color preview shown in embed color")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="blur", description="Blur effect (placeholder - requires image processing)")
    async def blur_image(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌫️ Image Blur",
            description="Image blurring requires image processing libraries like Pillow.\nTo implement this:\n1. Install Pillow: `pip install Pillow`\n2. Accept image attachments\n3. Apply blur filter\n4. Return processed image",
            color=0x87ceeb
        )
        embed.set_footer(text="This is a placeholder command")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="grayscale", description="Convert image to grayscale (placeholder)")
    async def grayscale_image(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="⬜ Grayscale Converter",
            description="Grayscale conversion requires image processing.\nTo implement this:\n1. Install Pillow: `pip install Pillow`\n2. Accept image attachments\n3. Convert to grayscale\n4. Return processed image",
            color=0x808080
        )
        embed.set_footer(text="This is a placeholder command")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="meme", description="Random meme (placeholder)")
    async def random_meme(self, interaction: discord.Interaction):
        meme_ideas = [
            "When you finally understand a coding concept",
            "Me explaining why my code doesn't work",
            "When the bug fixes itself",
            "Trying to center a div in CSS",
            "When someone asks me to fix their computer",
            "Me after staying up all night coding",
            "When your code works on the first try",
            "Debugging at 3 AM be like"
        ]
        
        meme_idea = random.choice(meme_ideas)
        
        embed = discord.Embed(
            title="😂 Random Meme Idea",
            description=f"**Meme concept:** {meme_idea}",
            color=0xffff00
        )
        embed.add_field(
            name="How to create:",
            value="1. Use imgflip.com or similar\n2. Choose a template\n3. Add your text\n4. Share with friends!",
            inline=False
        )
        embed.set_footer(text="Meme generation requires API integration")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Images(bot))
