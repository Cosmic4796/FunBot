import discord
from discord.ext import commands
from discord import app_commands
import random
import aiohttp

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Random facts database
        self.facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
            "A group of flamingos is called a 'flamboyance'.",
            "Bananas are berries, but strawberries aren't.",
            "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
            "Octopuses have three hearts and blue blood.",
            "The human brain contains approximately 86 billion neurons.",
            "A single cloud can weigh more than a million pounds.",
            "The Great Wall of China isn't visible from space with the naked eye.",
            "There are more possible games of chess than there are atoms in the observable universe.",
            "Wombat poop is cube-shaped.",
            "The longest English word has 189,819 letters and takes over 3 hours to pronounce.",
            "A shrimp's heart is in its head.",
            "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid of Giza.",
            "The inventor of the Pringles can is now buried in one.",
            "There are more trees on Earth than stars in the Milky Way galaxy."
        ]
        
        # Inspirational quotes
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "Do something today that your future self will thank you for. - Sean Cornwell",
            "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
            "Your limitation—it's only your imagination.",
            "Push yourself, because no one else is going to do it for you.",
            "Great things never come from comfort zones."
        ]
        
        # Random advice
        self.advice_list = [
            "Always carry a book with you. You never know when you'll have time to read.",
            "Learn to say no politely but firmly.",
            "Invest in experiences, not just things.",
            "Write down your thoughts regularly. Future you will thank you.",
            "Learn a new skill every year.",
            "Practice gratitude daily.",
            "Stay curious about the world around you.",
            "Take care of your mental health as much as your physical health.",
            "Build meaningful relationships, not just networks.",
            "Learn from your mistakes, but don't dwell on them.",
            "Be kind to yourself and others.",
            "Stay organized, but don't let perfectionism paralyze you.",
            "Save money regularly, even if it's just a small amount.",
            "Exercise regularly, even if it's just a 10-minute walk.",
            "Learn to cook a few good meals.",
            "Back up your important data.",
            "Get enough sleep. Your brain needs it to function properly.",
            "Learn to listen more than you speak.",
            "Take breaks when you're feeling overwhelmed.",
            "Celebrate small victories along the way."
        ]

    @app_commands.command(name="github", description="Search GitHub repositories (placeholder)")
    async def github_search(self, interaction: discord.Interaction, query: str):
        embed = discord.Embed(
            title="🐙 GitHub Search",
            description=f"Searching for: **{query}**\n\nThis command requires GitHub API integration.\nTo implement:\n1. Get GitHub API token\n2. Use GitHub REST API\n3. Display repository results",
            color=0x333333
        )
        embed.set_footer(text="GitHub API integration needed")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="crypto", description="Get cryptocurrency prices (placeholder)")
    async def crypto_price(self, interaction: discord.Interaction, symbol: str):
        embed = discord.Embed(
            title="₿ Cryptocurrency Prices",
            description=f"Getting price for: **{symbol.upper()}**\n\nThis command requires crypto API integration.\nPopular APIs:\n• CoinGecko API\n• CoinMarketCap API\n• Binance API",
            color=0xf7931a
        )
        embed.set_footer(text="Crypto API integration needed")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stock", description="Get stock information (placeholder)")
    async def stock_info(self, interaction: discord.Interaction, symbol: str):
        embed = discord.Embed(
            title="📈 Stock Information",
            description=f"Getting info for: **{symbol.upper()}**\n\nThis command requires stock API integration.\nPopular APIs:\n• Alpha Vantage\n• Yahoo Finance API\n• IEX Cloud",
            color=0x4caf50
        )
        embed.set_footer(text="Stock API integration needed")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="news", description="Get latest news (placeholder)")
    async def latest_news(self, interaction: discord.Interaction, topic: str = "general"):
        embed = discord.Embed(
            title="📰 Latest News",
            description=f"Topic: **{topic}**\n\nThis command requires news API integration.\nPopular APIs:\n• NewsAPI\n• Guardian API\n• Reddit API for specific subreddits",
            color=0x2196f3
        )
        embed.set_footer(text="News API integration needed")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fact", description="Get a random interesting fact")
    async def random_fact(self, interaction: discord.Interaction):
        fact = random.choice(self.facts)
        
        embed = discord.Embed(
            title="🧠 Random Fact",
            description=fact,
            color=0x9c27b0
        )
        embed.set_footer(text="Did you know? 🤓")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quote", description="Get an inspirational quote")
    async def inspirational_quote(self, interaction: discord.Interaction):
        quote = random.choice(self.quotes)
        
        embed = discord.Embed(
            title="💭 Inspirational Quote",
            description=f"*{quote}*",
            color=0xff9800
        )
        embed.set_footer(text="Stay inspired! ✨")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="advice", description="Get some random advice")
    async def random_advice(self, interaction: discord.Interaction):
        advice = random.choice(self.advice_list)
        
        embed = discord.Embed(
            title="💡 Random Advice",
            description=advice,
            color=0x00bcd4
        )
        embed.set_footer(text="Hope this helps! 🌟")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="urban", description="Urban dictionary lookup (placeholder)")
    async def urban_dictionary(self, interaction: discord.Interaction, term: str):
        embed = discord.Embed(
            title="🏙️ Urban Dictionary",
            description=f"Looking up: **{term}**\n\nThis command requires Urban Dictionary API integration.\n⚠️ **Note:** Urban Dictionary content can be inappropriate.",
            color=0x1d2951
        )
        embed.set_footer(text="Urban Dictionary API integration needed")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lyrics", description="Get song lyrics (placeholder)")
    async def song_lyrics(self, interaction: discord.Interaction, song: str, artist: str = None):
        search_term = f"{song} by {artist}" if artist else song
        
        embed = discord.Embed(
            title="🎵 Song Lyrics",
            description=f"Searching for: **{search_term}**\n\nThis command requires lyrics API integration.\nPopular APIs:\n• Genius API\n• Musixmatch API\n• Lyrics.ovh API",
            color=0xe91e63
        )
        embed.set_footer(text="Lyrics API integration needed")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="movie", description="Get movie information (placeholder)")
    async def movie_info(self, interaction: discord.Interaction, title: str):
        embed = discord.Embed(
            title="🎬 Movie Information",
            description=f"Searching for: **{title}**\n\nThis command requires movie API integration.\nPopular APIs:\n• OMDB API\n• TMDB API\n• IMDB API",
            color=0xffc107
        )
        embed.set_footer(text="Movie API integration needed")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="word_of_the_day", description="Get word of the day")
    async def word_of_the_day(self, interaction: discord.Interaction):
        # Simple word list with definitions
        words = [
            {"word": "Serendipity", "definition": "The occurrence of events by chance in a happy way", "example": "Finding this bot was pure serendipity!"},
            {"word": "Ephemeral", "definition": "Lasting for a very short time", "example": "The beauty of cherry blossoms is ephemeral."},
            {"word": "Wanderlust", "definition": "A strong desire to travel", "example": "Her wanderlust took her to 30 countries."},
            {"word": "Mellifluous", "definition": "Sweet and smooth sounding", "example": "Her mellifluous voice calmed everyone."},
            {"word": "Petrichor", "definition": "The pleasant smell of earth after rain", "example": "The petrichor filled the air after the storm."},
            {"word": "Luminous", "definition": "Giving off light; bright or shining", "example": "The luminous moon lit up the night sky."},
            {"word": "Eloquent", "definition": "Fluent and persuasive speaking or writing", "example": "His eloquent speech moved the audience."},
            {"word": "Resilience", "definition": "The ability to recover quickly from difficulties", "example": "Her resilience helped her overcome challenges."},
            {"word": "Ubiquitous", "definition": "Present everywhere at the same time", "example": "Smartphones are ubiquitous in modern society."},
            {"word": "Enigmatic", "definition": "Mysterious and difficult to understand", "example": "The Mona Lisa's smile is enigmatic."}
        ]
        
        word_data = random.choice(words)
        
        embed = discord.Embed(
            title="📚 Word of the Day",
            color=0x673ab7
        )
        embed.add_field(name="Word", value=f"**{word_data['word']}**", inline=False)
        embed.add_field(name="Definition", value=word_data['definition'], inline=False)
        embed.add_field(name="Example", value=f"*{word_data['example']}*", inline=False)
        embed.set_footer(text="Expand your vocabulary! 📖")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="riddle_fact", description="Get a riddle with its answer as a fact")
    async def riddle_fact(self, interaction: discord.Interaction):
        riddle_facts = [
            {"riddle": "What gets bigger the more you take away from it?", "answer": "A hole", "fact": "The largest hole on Earth is the Kola Superdeep Borehole in Russia, reaching 12,262 meters deep!"},
            {"riddle": "What has keys but no locks, space but no room?", "answer": "A keyboard", "fact": "The QWERTY keyboard layout was designed to prevent typewriter keys from jamming by separating commonly used letters."},
            {"riddle": "What goes up but never comes down?", "answer": "Your age", "fact": "The oldest verified human lived to 122 years and 164 days - Jeanne Louise Calment of France."},
            {"riddle": "What has one eye but cannot see?", "answer": "A needle", "fact": "The eye of a needle on modern sewing needles is punched from the inside out to create a smooth passage for thread."}
        ]
        
        riddle_data = random.choice(riddle_facts)
        
        embed = discord.Embed(
            title="🤔 Riddle + Fact",
            color=0x795548
        )
        embed.add_field(name="Riddle", value=riddle_data['riddle'], inline=False)
        embed.add_field(name="Answer", value=f"||{riddle_data['answer']}||", inline=False)
        embed.add_field(name="Fun Fact", value=riddle_data['fact'], inline=False)
        embed.set_footer(text="Click the spoiler to reveal the answer!")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="this_day", description="What happened on this day in history (placeholder)")
    async def this_day_in_history(self, interaction: discord.Interaction):
        from datetime import datetime
        today = datetime.now()
        
        embed = discord.Embed(
            title="📅 This Day in History",
            description=f"**{today.strftime('%B %d')}**\n\nThis command would show historical events that happened on this day.\n\nRequires historical events API or database integration.",
            color=0x607d8b
        )
        embed.set_footer(text="Historical events API integration needed")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="number_fact", description="Get an interesting fact about a number")
    async def number_fact(self, interaction: discord.Interaction, number: int):
        if number < 0 or number > 1000000:
            await interaction.response.send_message("❌ Please provide a number between 0 and 1,000,000!")
            return
        
        # Simple number facts
        facts = {
            0: "Zero is the only number that cannot be represented in Roman numerals!",
            1: "One is the only positive integer that is neither prime nor composite!",
            2: "Two is the only even prime number!",
            3: "Three is the first odd prime number and represents completion in many cultures!",
            7: "Seven is considered the luckiest number in many cultures!",
            13: "Thirteen is considered unlucky in Western culture but lucky in many others!",
            42: "Forty-two is the 'Answer to the Ultimate Question of Life, the Universe, and Everything' according to The Hitchhiker's Guide to the Galaxy!",
            100: "One hundred is the basis of percentages and represents completion!",
            365: "Three hundred sixty-five is the number of days in a regular year!",
            1000: "One thousand is the first four-digit number in decimal system!"
        }
        
        if number in facts:
            fact = facts[number]
        else:
            # Generate generic facts
            if number % 2 == 0:
                fact = f"{number} is an even number!"
            else:
                fact = f"{number} is an odd number!"
            
            if number > 1:
                # Simple prime check for small numbers
                is_prime = number > 1 and all(number % i != 0 for i in range(2, int(number**0.5) + 1))
                if is_prime and number < 1000:
                    fact += f" It's also a prime number!"
        
        embed = discord.Embed(
            title="🔢 Number Fact",
            description=f"**Number:** {number}\n\n{fact}",
            color=0x3f51b5
        )
        embed.set_footer(text="Numbers are fascinating! 🧮")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="color_fact", description="Get facts about colors")
    async def color_fact(self, interaction: discord.Interaction, color: str):
        color_facts = {
            "red": {
                "fact": "Red is the first color that babies can see clearly after black and white!",
                "psychology": "Red increases heart rate and creates urgency.",
                "culture": "Red symbolizes good luck and prosperity in Chinese culture.",
                "hex": "#FF0000"
            },
            "blue": {
                "fact": "Blue is the rarest color in nature - very few animals and plants are naturally blue!",
                "psychology": "Blue has a calming effect and can lower blood pressure.",
                "culture": "Blue represents trust and reliability in Western cultures.",
                "hex": "#0000FF"
            },
            "green": {
                "fact": "The human eye can distinguish more shades of green than any other color!",
                "psychology": "Green reduces eye strain and promotes relaxation.",
                "culture": "Green symbolizes nature, growth, and renewal.",
                "hex": "#00FF00"
            },
            "yellow": {
                "fact": "Yellow is the most visible color from a distance, which is why it's used for warning signs!",
                "psychology": "Yellow stimulates mental activity and generates muscle energy.",
                "culture": "Yellow represents happiness and optimism in many cultures.",
                "hex": "#FFFF00"
            },
            "purple": {
                "fact": "Purple was historically the most expensive dye, making it a symbol of royalty!",
                "psychology": "Purple is associated with creativity and imagination.",
                "culture": "Purple represents luxury and nobility.",
                "hex": "#800080"
            },
            "orange": {
                "fact": "Orange is named after the fruit, not the other way around!",
                "psychology": "Orange increases enthusiasm and encourages socialization.",
                "culture": "Orange represents energy and warmth.",
                "hex": "#FFA500"
            },
            "black": {
                "fact": "Black absorbs all visible light wavelengths and reflects none!",
                "psychology": "Black conveys sophistication and elegance.",
                "culture": "Black has different meanings across cultures - from mourning to formality.",
                "hex": "#000000"
            },
            "white": {
                "fact": "White reflects all visible light wavelengths equally!",
                "psychology": "White represents cleanliness and simplicity.",
                "culture": "White symbolizes purity and peace in many cultures.",
                "hex": "#FFFFFF"
            }
        }
        
        color_lower = color.lower()
        if color_lower not in color_facts:
            available_colors = ", ".join(color_facts.keys())
            await interaction.response.send_message(f"❌ Color not found! Available colors: {available_colors}")
            return
        
        color_data = color_facts[color_lower]
        
        embed = discord.Embed(
            title=f"🎨 {color.title()} Facts",
            color=int(color_data['hex'].replace('#', '0x'), 16)
        )
        embed.add_field(name="🧬 Scientific Fact", value=color_data['fact'], inline=False)
        embed.add_field(name="🧠 Psychology", value=color_data['psychology'], inline=False)
        embed.add_field(name="🌍 Culture", value=color_data['culture'], inline=False)
        embed.add_field(name="🎯 Hex Code", value=color_data['hex'], inline=True)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="tech_fact", description="Get interesting technology facts")
    async def tech_fact(self, interaction: discord.Interaction):
        tech_facts = [
            "The first computer bug was an actual bug - a moth stuck in a relay of the Harvard Mark II computer in 1947!",
            "The term 'robot' comes from the Czech word 'robota', meaning 'forced labor'.",
            "The first computer virus was called 'Creeper' and was created in 1971.",
            "Email was invented before the World Wide Web!",
            "The first domain name ever registered was Symbolics.com on March 15, 1985.",
            "The '@' symbol was used in email addresses because it was the only preposition available on the keyboard.",
            "The first iPhone was released in 2007, but the first smartphone was IBM's Simon in 1992.",
            "Google processes over 8.5 billion searches per day!",
            "The Internet weighs about 50 grams - roughly the same as a strawberry!",
            "More people have mobile phones than have access to clean water.",
            "The first webcam was created to monitor a coffee pot at Cambridge University!",
            "YouTube was originally designed as a video dating site.",
            "The first banner ad appeared in 1994 and had a click-through rate of 44%!",
            "The term 'Wi-Fi' doesn't actually stand for anything - it's just a catchy name!"
        ]
        
        fact = random.choice(tech_facts)
        
        embed = discord.Embed(
            title="💻 Tech Fact",
            description=fact,
            color=0x00bcd4
        )
        embed.set_footer(text="Technology is amazing! 🚀")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Information(bot))
