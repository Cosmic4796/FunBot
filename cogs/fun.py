import discord
from discord.ext import commands
from discord import app_commands
import random
import aiohttp
import json

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.eight_ball_responses = [
            "It is certain", "Without a doubt", "Yes definitely", "You may rely on it",
            "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes",
            "Reply hazy, try again", "Ask again later", "Better not tell you now",
            "Cannot predict now", "Concentrate and ask again", "Don't count on it",
            "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"
        ]
        
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the coffee file a police report? It got mugged!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a sleeping bull? A bulldozer!"
        ]
        
        self.roasts = [
            "You're like a software update - whenever I see you, I think 'not now'",
            "I'd explain it to you but I don't have any crayons with me",
            "You're proof that even God makes mistakes sometimes",
            "If I wanted to kill myself I'd climb your ego and jump to your IQ",
            "You're like Monday mornings - nobody likes you",
            "I'm not saying you're stupid, but you have bad luck thinking",
            "You're the reason the gene pool needs a lifeguard",
            "If laughter is the best medicine, your face must be curing the world",
            "You're like a cloud - when you disappear, it's a beautiful day",
            "I'd agree with you but then we'd both be wrong"
        ]
        
        self.compliments = [
            "You're absolutely amazing!",
            "You light up any room you enter!",
            "You have the best laugh!",
            "You're incredibly talented!",
            "You make everyone around you feel special!",
            "You have such a positive energy!",
            "You're one of a kind!",
            "You inspire me to be better!",
            "You have great taste!",
            "You're absolutely wonderful!"
        ]

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        response = random.choice(self.eight_ball_responses)
        embed = discord.Embed(title="🎱 Magic 8-Ball", color=0x000000)
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=response, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="joke", description="Get random jokes from JokeAPI")
    async def joke(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                # Using JokeAPI - completely free
                url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        joke_text = data.get('joke', random.choice(self.jokes))
                    else:
                        joke_text = random.choice(self.jokes)
            
            embed = discord.Embed(title="😂 Random Joke", description=joke_text, color=0xffff00)
            await interaction.response.send_message(embed=embed)
            
        except Exception:
            # Fallback to local jokes
            joke_text = random.choice(self.jokes)
            embed = discord.Embed(title="😂 Random Joke", description=joke_text, color=0xffff00)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roast", description="Get roasted (friendly)")
    async def roast(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        roast = random.choice(self.roasts)
        embed = discord.Embed(
            title="🔥 Roast Time!",
            description=f"{target.mention}, {roast}",
            color=0xff4500
        )
        embed.set_footer(text="This is all in good fun! ❤️")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="compliment", description="Receive a nice compliment")
    async def compliment(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        compliment = random.choice(self.compliments)
        embed = discord.Embed(
            title="💖 Compliment",
            description=f"{target.mention}, {compliment}",
            color=0xff69b4
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dice", description="Roll a dice")
    async def dice(self, interaction: discord.Interaction, sides: int = 6):
        if sides < 2 or sides > 100:
            await interaction.response.send_message("Please choose between 2 and 100 sides!")
            return
        
        result = random.randint(1, sides)
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"You rolled a **{result}** on a {sides}-sided dice!",
            color=0x00ff00
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        emoji = "🗣️" if result == "Heads" else "🏛️"
        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"{emoji} **{result}**!",
            color=0xffd700
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="choose", description="Choose between options (separate with commas)")
    async def choose(self, interaction: discord.Interaction, options: str):
        choices = [choice.strip() for choice in options.split(",")]
        if len(choices) < 2:
            await interaction.response.send_message("Please provide at least 2 options separated by commas!")
            return
        
        choice = random.choice(choices)
        embed = discord.Embed(
            title="🤔 Choice Made!",
            description=f"I choose: **{choice}**",
            color=0x9932cc
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reverse", description="Reverse any text")
    async def reverse(self, interaction: discord.Interaction, text: str):
        reversed_text = text[::-1]
        embed = discord.Embed(
            title="🔄 Text Reversed",
            description=f"**Original:** {text}\n**Reversed:** {reversed_text}",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="say", description="Make the bot say something")
    async def say(self, interaction: discord.Interaction, message: str):
        if len(message) > 2000:
            await interaction.response.send_message("Message too long! Please keep it under 2000 characters.")
            return
        
        embed = discord.Embed(description=message, color=0x7289da)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ascii", description="Convert text to ASCII art")
    async def ascii(self, interaction: discord.Interaction, text: str):
        if len(text) > 10:
            await interaction.response.send_message("Text too long! Please keep it under 10 characters.")
            return
        
        # Simple ASCII art conversion
        ascii_chars = {
            'a': ['  █  ', ' █ █ ', '█████', '█   █', '█   █'],
            'b': ['████ ', '█   █', '████ ', '█   █', '████ '],
            'c': [' ████', '█    ', '█    ', '█    ', ' ████'],
            'd': ['████ ', '█   █', '█   █', '█   █', '████ '],
            'e': ['█████', '█    ', '████ ', '█    ', '█████'],
            'f': ['█████', '█    ', '████ ', '█    ', '█    '],
            'g': [' ████', '█    ', '█ ███', '█   █', ' ████'],
            'h': ['█   █', '█   █', '█████', '█   █', '█   █'],
            'i': ['█████', '  █  ', '  █  ', '  █  ', '█████'],
            'j': ['█████', '    █', '    █', '█   █', ' ████'],
            'k': ['█   █', '█  █ ', '███  ', '█  █ ', '█   █'],
            'l': ['█    ', '█    ', '█    ', '█    ', '█████'],
            'm': ['█   █', '██ ██', '█ █ █', '█   █', '█   █'],
            'n': ['█   █', '██  █', '█ █ █', '█  ██', '█   █'],
            'o': [' ███ ', '█   █', '█   █', '█   █', ' ███ '],
            'p': ['████ ', '█   █', '████ ', '█    ', '█    '],
            'q': [' ███ ', '█   █', '█ █ █', '█  █ ', ' ██ █'],
            'r': ['████ ', '█   █', '████ ', '█  █ ', '█   █'],
            's': [' ████', '█    ', ' ███ ', '    █', '████ '],
            't': ['█████', '  █  ', '  █  ', '  █  ', '  █  '],
            'u': ['█   █', '█   █', '█   █', '█   █', ' ███ '],
            'v': ['█   █', '█   █', '█   █', ' █ █ ', '  █  '],
            'w': ['█   █', '█   █', '█ █ █', '██ ██', '█   █'],
            'x': ['█   █', ' █ █ ', '  █  ', ' █ █ ', '█   █'],
            'y': ['█   █', ' █ █ ', '  █  ', '  █  ', '  █  '],
            'z': ['█████', '   █ ', '  █  ', ' █   ', '█████'],
            ' ': ['     ', '     ', '     ', '     ', '     ']
        }
        
        result = []
        for i in range(5):
            line = ''
            for char in text.lower():
                if char in ascii_chars:
                    line += ascii_chars[char][i] + ' '
                else:
                    line += '     '
            result.append(line)
        
        ascii_art = '\n'.join(result)
        embed = discord.Embed(
            title="🎨 ASCII Art",
            description=f"```\n{ascii_art}\n```",
            color=0xff6b6b
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mock", description="Convert text to mocking SpongeBob case")
    async def mock(self, interaction: discord.Interaction, text: str):
        mocked = ''.join(char.upper() if i % 2 == 0 else char.lower() 
                       for i, char in enumerate(text) if char.isalpha())
        
        original_case = list(text)
        char_index = 0
        for i, char in enumerate(original_case):
            if char.isalpha():
                original_case[i] = mocked[char_index]
                char_index += 1
        
        result = ''.join(original_case)
        
        embed = discord.Embed(
            title="🧽 Mocking SpongeBob",
            description=f"**Original:** {text}\n**Mocked:** {result}",
            color=0xffff00
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="uwu", description="Convert text to uwu speak")
    async def uwu(self, interaction: discord.Interaction, text: str):
        uwu_text = text.lower()
        uwu_text = uwu_text.replace('r', 'w').replace('l', 'w')
        uwu_text = uwu_text.replace('na', 'nya').replace('ne', 'nye')
        uwu_text = uwu_text.replace('ni', 'nyi').replace('no', 'nyo')
        uwu_text = uwu_text.replace('nu', 'nyu')
        
        uwu_text += random.choice([' uwu', ' owo', ' >w<', ' :3', ' ^w^'])
        
        embed = discord.Embed(
            title="💖 UwU Translator",
            description=f"**Original:** {text}\n**UwU:** {uwu_text}",
            color=0xff69b4
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ship", description="Ship two users together")
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member = None):
        if user2 is None:
            user2 = interaction.user
        
        if user1 == user2:
            await interaction.response.send_message("You can't ship someone with themselves!")
            return
        
        compatibility = random.randint(0, 100)
        
        if compatibility < 30:
            rating = "💔 Not compatible"
            color = 0xff0000
        elif compatibility < 60:
            rating = "💛 Could work"
            color = 0xffff00
        elif compatibility < 80:
            rating = "💚 Great match!"
            color = 0x00ff00
        else:
            rating = "💖 Perfect match!"
            color = 0xff69b4
        
        ship_name = user1.display_name[:len(user1.display_name)//2] + user2.display_name[len(user2.display_name)//2:]
        
        embed = discord.Embed(
            title="💕 Ship Generator",
            description=f"**{user1.display_name}** × **{user2.display_name}**",
            color=color
        )
        embed.add_field(name="Ship Name", value=ship_name, inline=True)
        embed.add_field(name="Compatibility", value=f"{compatibility}%", inline=True)
        embed.add_field(name="Rating", value=rating, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rate", description="Rate something out of 10")
    async def rate(self, interaction: discord.Interaction, thing: str):
        rating = random.randint(1, 10)
        
        if rating <= 3:
            emoji = "💔"
            comment = "Oof, that's rough"
        elif rating <= 5:
            emoji = "😐"
            comment = "It's alright I guess"
        elif rating <= 7:
            emoji = "👍"
            comment = "Pretty good!"
        elif rating <= 9:
            emoji = "⭐"
            comment = "Amazing!"
        else:
            emoji = "🔥"
            comment = "ABSOLUTELY PERFECT!"
        
        embed = discord.Embed(
            title="📊 Rating System",
            description=f"I rate **{thing}** a **{rating}/10** {emoji}",
            color=0x4169e1
        )
        embed.add_field(name="My thoughts", value=comment, inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
