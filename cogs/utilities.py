import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import base64
import hashlib
import random
import string
import asyncio
from datetime import datetime
import pytz

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Get information about this server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"🏰 {guild.name}",
            color=0x7289da
        )
        
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        embed.add_field(name="👑 Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="🆔 ID", value=guild.id, inline=True)
        
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(name="📝 Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)
        
        embed.add_field(name="🔒 Verification Level", value=str(guild.verification_level).title(), inline=True)
        embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="🚀 Boost Level", value=guild.premium_tier, inline=True)
        
        if guild.description:
            embed.add_field(name="📄 Description", value=guild.description, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Get information about a user")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user
        
        embed = discord.Embed(
            title=f"👤 {user.display_name}",
            color=user.color if user.color != discord.Color.default() else 0x7289da
        )
        
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        
        embed.add_field(name="🏷️ Username", value=f"{user.name}#{user.discriminator}", inline=True)
        embed.add_field(name="🆔 ID", value=user.id, inline=True)
        embed.add_field(name="🤖 Bot", value="Yes" if user.bot else "No", inline=True)
        
        embed.add_field(name="📅 Account Created", value=user.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="📥 Joined Server", value=user.joined_at.strftime("%B %d, %Y") if user.joined_at else "Unknown", inline=True)
        
        if user.premium_since:
            embed.add_field(name="💎 Nitro Since", value=user.premium_since.strftime("%B %d, %Y"), inline=True)
        
        roles = [role.mention for role in user.roles[1:]]  # Exclude @everyone
        if roles:
            embed.add_field(name=f"🎭 Roles ({len(roles)})", value=" ".join(roles) if len(" ".join(roles)) < 1024 else f"{len(roles)} roles", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Get a user's avatar")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user
        
        embed = discord.Embed(
            title=f"🖼️ {user.display_name}'s Avatar",
            color=0x7289da
        )
        
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        embed.set_image(url=avatar_url)
        embed.add_field(name="🔗 Download", value=f"[Click here]({avatar_url})", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        
        if latency < 100:
            color = 0x00ff00
            status = "Excellent"
        elif latency < 200:
            color = 0xffff00
            status = "Good"
        elif latency < 300:
            color = 0xff4500
            status = "Fair"
        else:
            color = 0xff0000
            status = "Poor"
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**Latency:** {latency}ms\n**Status:** {status}",
            color=color
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="weather", description="Get weather information for a city")
    async def weather(self, interaction: discord.Interaction, city: str):
        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            await interaction.response.send_message("❌ Weather API key not configured!")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        temp = data['main']['temp']
                        feels_like = data['main']['feels_like']
                        humidity = data['main']['humidity']
                        description = data['weather'][0]['description'].title()
                        
                        embed = discord.Embed(
                            title=f"🌤️ Weather in {city}",
                            description=f"**{description}**",
                            color=0x87ceeb
                        )
                        embed.add_field(name="🌡️ Temperature", value=f"{temp}°C", inline=True)
                        embed.add_field(name="🤔 Feels Like", value=f"{feels_like}°C", inline=True)
                        embed.add_field(name="💧 Humidity", value=f"{humidity}%", inline=True)
                        
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"❌ City '{city}' not found!")
        except Exception as e:
            await interaction.response.send_message(f"❌ Error fetching weather: {str(e)}")

    @app_commands.command(name="facts", description="Get random facts, quotes, or advice")
    async def get_facts(self, interaction: discord.Interaction, type: str = "fact"):
        type = type.lower()
        
        try:
            async with aiohttp.ClientSession() as session:
                if type == "fact":
                    url = "http://numbersapi.com/random"
                    async with session.get(url) as response:
                        if response.status == 200:
                            fact = await response.text()
                            embed = discord.Embed(
                                title="🧠 Random Fact",
                                description=fact,
                                color=0x4169e1
                            )
                elif type == "quote":
                    url = "https://api.quotable.io/random"
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            embed = discord.Embed(
                                title="💭 Random Quote",
                                description=f"*\"{data['content']}\"*\n\n— {data['author']}",
                                color=0x9932cc
                            )
                elif type == "advice":
                    url = "https://api.adviceslip.com/advice"
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            embed = discord.Embed(
                                title="💡 Random Advice",
                                description=data['slip']['advice'],
                                color=0xffd700
                            )
                else:
                    embed = discord.Embed(
                        title="❌ Invalid Type",
                        description="Choose from: **fact**, **quote**, **advice**",
                        color=0xff4500
                    )
                
                await interaction.response.send_message(embed=embed)
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Error fetching {type}: {str(e)}")

    @app_commands.command(name="time", description="Get current time in a timezone")
    async def current_time(self, interaction: discord.Interaction, timezone: str = "UTC"):
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            
            embed = discord.Embed(
                title="🕐 Current Time",
                description=f"**Timezone:** {timezone}\n**Time:** {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}",
                color=0x4169e1
            )
            
            await interaction.response.send_message(embed=embed)
            
        except pytz.exceptions.UnknownTimeZoneError:
            await interaction.response.send_message(f"❌ Unknown timezone: {timezone}\nTry common ones like: UTC, US/Eastern, Europe/London, Asia/Tokyo")

    @app_commands.command(name="translate", description="Translate text (Note: Requires API)")
    async def translate(self, interaction: discord.Interaction, text: str, target_language: str = "en"):
        await interaction.response.send_message("⚠️ Translation requires Google Translate API or similar service. This is a placeholder - you'd need to implement with your preferred translation service.")

    @app_commands.command(name="define", description="Get the definition of a word")
    async def define(self, interaction: discord.Interaction, word: str):
        await interaction.response.send_message("⚠️ Dictionary lookup requires an API key from Dictionary API. This is a placeholder command.")

    @app_commands.command(name="wiki", description="Search Wikipedia for a topic")
    async def wikipedia_search(self, interaction: discord.Interaction, query: str):
        try:
            import wikipedia
            
            # Search for the topic
            summary = wikipedia.summary(query, sentences=3)
            page = wikipedia.page(query)
            
            embed = discord.Embed(
                title=f"📖 Wikipedia: {page.title}",
                description=summary,
                color=0x000000,
                url=page.url
            )
            
            if page.images:
                embed.set_thumbnail(url=page.images[0])
            
            await interaction.response.send_message(embed=embed)
            
        except wikipedia.exceptions.DisambiguationError as e:
            suggestions = e.options[:5]  # First 5 suggestions
            embed = discord.Embed(
                title="🤔 Multiple results found",
                description=f"Did you mean one of these?\n" + "\n".join([f"• {option}" for option in suggestions]),
                color=0xff4500
            )
            await interaction.response.send_message(embed=embed)
            
        except wikipedia.exceptions.PageError:
            await interaction.response.send_message(f"❌ No Wikipedia page found for '{query}'")
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error searching Wikipedia: {str(e)}")

    @app_commands.command(name="calc", description="Simple calculator")
    async def calculator(self, interaction: discord.Interaction, expression: str):
        try:
            # Security: Only allow basic math operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                await interaction.response.send_message("❌ Invalid characters! Only numbers and basic operators (+, -, *, /, parentheses) are allowed.")
                return
            
            # Evaluate the expression
            result = eval(expression)
            
            embed = discord.Embed(
                title="🧮 Calculator",
                color=0x4169e1
            )
            embed.add_field(name="Expression", value=f"`{expression}`", inline=False)
            embed.add_field(name="Result", value=f"`{result}`", inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except ZeroDivisionError:
            await interaction.response.send_message("❌ Cannot divide by zero!")
        except Exception:
            await interaction.response.send_message("❌ Invalid expression! Please check your math.")

    @app_commands.command(name="base64encode", description="Encode text to base64")
    async def base64_encode(self, interaction: discord.Interaction, text: str):
        try:
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            
            embed = discord.Embed(
                title="🔐 Base64 Encoder",
                color=0x00ff88
            )
            embed.add_field(name="Original", value=f"```{text}```", inline=False)
            embed.add_field(name="Encoded", value=f"```{encoded}```", inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error encoding: {str(e)}")

    @app_commands.command(name="base64decode", description="Decode base64 text")
    async def base64_decode(self, interaction: discord.Interaction, encoded_text: str):
        try:
            decoded = base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
            
            embed = discord.Embed(
                title="🔓 Base64 Decoder",
                color=0x00ff88
            )
            embed.add_field(name="Encoded", value=f"```{encoded_text}```", inline=False)
            embed.add_field(name="Decoded", value=f"```{decoded}```", inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error decoding: Invalid base64 string")

    @app_commands.command(name="qr", description="Generate QR code (Note: Requires API)")
    async def qr_code(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message("⚠️ QR Code generation requires a QR API service. This is a placeholder command.")

    @app_commands.command(name="shorten", description="Shorten URL (Note: Requires API)")
    async def shorten_url(self, interaction: discord.Interaction, url: str):
        await interaction.response.send_message("⚠️ URL shortening requires an API key from a service like bit.ly or tinyurl. This is a placeholder command.")

    @app_commands.command(name="password", description="Generate a secure password")
    async def generate_password(self, interaction: discord.Interaction, length: int = 12):
        if length < 4 or length > 50:
            await interaction.response.send_message("❌ Password length must be between 4 and 50 characters!")
            return
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*"
        
        # Ensure at least one character from each set
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(symbols)
        ]
        
        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + symbols
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
        
        # Shuffle the password
        random.shuffle(password)
        final_password = ''.join(password)
        
        embed = discord.Embed(
            title="🔐 Password Generated",
            description=f"Here's your secure password:",
            color=0x00ff00
        )
        embed.add_field(name="Password", value=f"||`{final_password}`||", inline=False)
        embed.add_field(name="Length", value=f"{length} characters", inline=True)
        embed.add_field(name="Security", value="Contains uppercase, lowercase, numbers, and symbols", inline=False)
        embed.set_footer(text="Click the spoiler to reveal • Keep this password safe!")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="text", description="Text manipulation: upper, lower, title, count, reverse, binary, morse")
    async def text_tools(self, interaction: discord.Interaction, action: str, text: str):
        action = action.lower()
        
        if action == "upper":
            result = text.upper()
            title = "🔤 Uppercase"
        elif action == "lower":
            result = text.lower()
            title = "🔤 Lowercase"
        elif action == "title":
            result = text.title()
            title = "🔤 Title Case"
        elif action == "reverse":
            result = text[::-1]
            title = "🔄 Reversed"
        elif action == "count":
            char_count = len(text)
            word_count = len(text.split())
            embed = discord.Embed(
                title="📊 Text Statistics",
                color=0x9932cc
            )
            embed.add_field(name="Characters", value=char_count, inline=True)
            embed.add_field(name="Words", value=word_count, inline=True)
            embed.add_field(name="Chars (no spaces)", value=len(text.replace(' ', '')), inline=True)
            await interaction.response.send_message(embed=embed)
            return
        elif action == "binary":
            if len(text) > 50:
                await interaction.response.send_message("❌ Text too long! Please keep it under 50 characters.")
                return
            result = ' '.join(format(ord(char), '08b') for char in text)
            title = "🤖 Binary"
        elif action == "morse":
            morse_dict = {
                'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
                'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
                'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
                'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
                '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
                '9': '----.', '0': '-----', ' ': '/'
            }
            result = ' '.join(morse_dict.get(char.upper(), char) for char in text)
            title = "📡 Morse Code"
        else:
            embed = discord.Embed(
                title="❌ Invalid Action",
                description="Available actions: **upper**, **lower**, **title**, **count**, **reverse**, **binary**, **morse**",
                color=0xff4500
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(title=title, color=0x4169e1)
        embed.add_field(name="Original", value=f"```{text}```", inline=False)
        embed.add_field(name="Result", value=f"```{result}```", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lower", description="Convert text to lowercase")
    async def to_lowercase(self, interaction: discord.Interaction, text: str):
        embed = discord.Embed(
            title="🔤 Text Converter",
            color=0x4169e1
        )
        embed.add_field(name="Original", value=text, inline=False)
        embed.add_field(name="Lowercase", value=text.lower(), inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="title", description="Convert text to title case")
    async def to_titlecase(self, interaction: discord.Interaction, text: str):
        embed = discord.Embed(
            title="🔤 Text Converter",
            color=0x4169e1
        )
        embed.add_field(name="Original", value=text, inline=False)
        embed.add_field(name="Title Case", value=text.title(), inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="count", description="Count characters and words in text")
    async def count_text(self, interaction: discord.Interaction, text: str):
        char_count = len(text)
        word_count = len(text.split())
        char_no_spaces = len(text.replace(' ', ''))
        
        embed = discord.Embed(
            title="📊 Text Statistics",
            color=0x9932cc
        )
        embed.add_field(name="Characters", value=char_count, inline=True)
        embed.add_field(name="Words", value=word_count, inline=True)
        embed.add_field(name="Chars (no spaces)", value=char_no_spaces, inline=True)
        embed.add_field(name="Text", value=f"```{text[:500]}{'...' if len(text) > 500 else ''}```", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hash", description="Generate hash of text")
    async def hash_text(self, interaction: discord.Interaction, text: str, algorithm: str = "md5"):
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }
        
        if algorithm.lower() not in algorithms:
            await interaction.response.send_message(f"❌ Unsupported algorithm! Available: {', '.join(algorithms.keys())}")
            return
        
        hash_func = algorithms[algorithm.lower()]
        hash_result = hash_func(text.encode('utf-8')).hexdigest()
        
        embed = discord.Embed(
            title="🔒 Text Hash",
            color=0xff6b6b
        )
        embed.add_field(name="Algorithm", value=algorithm.upper(), inline=True)
        embed.add_field(name="Original Text", value=f"```{text[:100]}{'...' if len(text) > 100 else ''}```", inline=False)
        embed.add_field(name="Hash", value=f"```{hash_result}```", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="binary", description="Convert text to binary")
    async def text_to_binary(self, interaction: discord.Interaction, text: str):
        if len(text) > 50:
            await interaction.response.send_message("❌ Text too long! Please keep it under 50 characters.")
            return
        
        binary = ' '.join(format(ord(char), '08b') for char in text)
        
        embed = discord.Embed(
            title="🤖 Binary Converter",
            color=0x00ff00
        )
        embed.add_field(name="Text", value=f"```{text}```", inline=False)
        embed.add_field(name="Binary", value=f"```{binary}```", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="morse", description="Convert text to morse code")
    async def text_to_morse(self, interaction: discord.Interaction, text: str):
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
            '9': '----.', '0': '-----', ' ': '/'
        }
        
        morse = ' '.join(morse_dict.get(char.upper(), char) for char in text)
        
        embed = discord.Embed(
            title="📡 Morse Code Converter",
            color=0xffd700
        )
        embed.add_field(name="Text", value=f"```{text}```", inline=False)
        embed.add_field(name="Morse Code", value=f"```{morse}```", inline=False)
        embed.set_footer(text="• = dot (short) | - = dash (long) | / = space")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pig_latin", description="Convert text to pig latin")
    async def pig_latin(self, interaction: discord.Interaction, text: str):
        def convert_word(word):
            if not word.isalpha():
                return word
            
            vowels = 'aeiouAEIOU'
            if word[0] in vowels:
                return word + 'way'
            else:
                # Find first vowel
                for i, char in enumerate(word):
                    if char in vowels:
                        return word[i:] + word[:i] + 'ay'
                # No vowels found
                return word + 'ay'
        
        words = text.split()
        pig_latin_words = [convert_word(word) for word in words]
        result = ' '.join(pig_latin_words)
        
        embed = discord.Embed(
            title="🐷 Pig Latin Converter",
            color=0xffc0cb
        )
        embed.add_field(name="English", value=f"```{text}```", inline=False)
        embed.add_field(name="Pig Latin", value=f"```{result}```", inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))
