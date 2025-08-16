import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import random
import os

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fact", description="Get random facts")
    async def random_fact(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://numbersapi.com/random") as response:
                    if response.status == 200:
                        fact = await response.text()
                        embed = discord.Embed(
                            title="🧠 Random Fact",
                            description=fact,
                            color=0x4169e1
                        )
                        await interaction.response.send_message(embed=embed)
                    else:
                        raise Exception("API failed")
        except:
            # Fallback facts
            facts = [
                "A group of flamingos is called a 'flamboyance'",
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible",
                "Octopuses have three hearts and blue blood",
                "Bananas are berries, but strawberries aren't",
                "A day on Venus is longer than its year"
            ]
            fact = random.choice(facts)
            embed = discord.Embed(
                title="🧠 Random Fact",
                description=fact,
                color=0x4169e1
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quote", description="Get inspirational quotes")
    async def random_quote(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.quotable.io/random") as response:
                    if response.status == 200:
                        data = await response.json()
                        embed = discord.Embed(
                            title="💭 Inspirational Quote",
                            description=f"*\"{data['content']}\"*\n\n— {data['author']}",
                            color=0x9932cc
                        )
                        await interaction.response.send_message(embed=embed)
                    else:
                        raise Exception("API failed")
        except:
            # Fallback quotes
            quotes = [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Life is what happens to you while you're busy making other plans. - John Lennon", 
                "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
                "The only impossible journey is the one you never begin. - Tony Robbins"
            ]
            quote = random.choice(quotes)
            embed = discord.Embed(
                title="💭 Inspirational Quote", 
                description=f"*{quote}*",
                color=0x9932cc
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="advice", description="Get random life advice")
    async def random_advice(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.adviceslip.com/advice") as response:
                    if response.status == 200:
                        data = await response.json()
                        embed = discord.Embed(
                            title="💡 Random Advice",
                            description=data['slip']['advice'],
                            color=0xffd700
                        )
                        await interaction.response.send_message(embed=embed)
                    else:
                        raise Exception("API failed")
        except:
            # Fallback advice
            advice_list = [
                "Always backup your code",
                "Take breaks when you're stuck on a problem",
                "Learn something new every day",
                "Be kind to others and yourself",
                "Don't be afraid to ask for help",
                "Stay curious and keep exploring",
                "Practice makes progress, not perfection"
            ]
            advice = random.choice(advice_list)
            embed = discord.Embed(
                title="💡 Random Advice",
                description=advice,
                color=0xffd700
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="crypto", description="Get cryptocurrency prices (placeholder)")
    async def crypto_price(self, interaction: discord.Interaction, symbol: str = "btc"):
        embed = discord.Embed(
            title="💰 Cryptocurrency Prices",
            description=f"To get real crypto prices, you can use:\n• **CoinGecko API** (Free): https://www.coingecko.com/en/api\n• **CoinMarketCap API** (Free tier): https://coinmarketcap.com/api/\n\nAdd the API key to your environment and update this command!",
            color=0xffd700
        )
        embed.add_field(name="Requested", value=symbol.upper(), inline=True)
        embed.set_footer(text="This is a placeholder - implement with your preferred crypto API")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="news", description="Get latest news (placeholder)")
    async def latest_news(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📰 Latest News",
            description="To get real news, you can use:\n• **NewsAPI** (Free tier): https://newsapi.org/\n• **Guardian API** (Free): https://open-platform.theguardian.com/\n\nAdd your API key and update this command!",
            color=0x4169e1
        )
        embed.set_footer(text="This is a placeholder - implement with your preferred news API")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="urban", description="Urban dictionary lookup (placeholder)")
    async def urban_dictionary(self, interaction: discord.Interaction, term: str):
        embed = discord.Embed(
            title="📖 Urban Dictionary",
            description=f"Looking up: **{term}**\n\nTo implement this, use:\n• **Urban Dictionary API**: http://api.urbandictionary.com/v0/define?term={term}\n\nNo API key needed - just implement the HTTP request!",
            color=0xff69b4
        )
        embed.set_footer(text="This is a placeholder - free API available")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="github", description="Search GitHub repositories")
    async def github_search(self, interaction: discord.Interaction, query: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=1"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['items']:
                            repo = data['items'][0]
                            embed = discord.Embed(
                                title="🐙 GitHub Repository",
                                description=repo['description'] or "No description available",
                                color=0x333333,
                                url=repo['html_url']
                            )
                            embed.add_field(name="Repository", value=repo['full_name'], inline=True)
                            embed.add_field(name="⭐ Stars", value=f"{repo['stargazers_count']:,}", inline=True)
                            embed.add_field(name="🍴 Forks", value=f"{repo['forks_count']:,}", inline=True)
                            embed.add_field(name="Language", value=repo['language'] or "Not specified", inline=True)
                            embed.add_field(name="📅 Created", value=repo['created_at'][:10], inline=True)
                            embed.add_field(name="📝 License", value=repo['license']['name'] if repo['license'] else "None", inline=True)
                            
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message(f"❌ No repositories found for '{query}'")
                    else:
                        raise Exception("GitHub API error")
        except Exception as e:
            await interaction.response.send_message(f"❌ Error searching GitHub: {str(e)}")

    @app_commands.command(name="stock", description="Stock information (placeholder)")
    async def stock_info(self, interaction: discord.Interaction, symbol: str):
        embed = discord.Embed(
            title="📈 Stock Information",
            description=f"Looking up: **{symbol.upper()}**\n\nTo get real stock data, use:\n• **Alpha Vantage** (Free): https://www.alphavantage.co/\n• **IEX Cloud** (Free tier): https://iexcloud.io/\n• **Yahoo Finance API** (Unofficial but free)\n\nAdd your API key and implement!",
            color=0x00ff00
        )
        embed.set_footer(text="This is a placeholder - multiple free APIs available")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="movie", description="Movie information (placeholder)")
    async def movie_info(self, interaction: discord.Interaction, title: str):
        embed = discord.Embed(
            title="🎬 Movie Information",
            description=f"Searching for: **{title}**\n\nTo get real movie data, use:\n• **OMDb API** (Free): http://www.omdbapi.com/\n• **The Movie DB** (Free): https://www.themoviedb.org/documentation/api\n\nBoth require free API keys!",
            color=0xff6b6b
        )
        embed.set_footer(text="This is a placeholder - free APIs available")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lyrics", description="Song lyrics (placeholder)")
    async def song_lyrics(self, interaction: discord.Interaction, artist: str, song: str):
        embed = discord.Embed(
            title="🎵 Song Lyrics",
            description=f"Searching for: **{song}** by **{artist}**\n\nTo get real lyrics, use:\n• **Lyrics.ovh API** (Free): https://lyricsovh.docs.apiary.io/\n• **Musixmatch API** (Free tier): https://developer.musixmatch.com/\n\nNo API key needed for lyrics.ovh!",
            color=0x9932cc
        )
        embed.set_footer(text="This is a placeholder - free APIs available")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="define", description="Define a word using Free Dictionary API")
    async def define_word(self, interaction: discord.Interaction, word: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        entry = data[0]
                        
                        embed = discord.Embed(
                            title=f"📖 Definition: {word.title()}",
                            color=0x4169e1
                        )
                        
                        # Get first meaning
                        meaning = entry['meanings'][0]
                        definition = meaning['definitions'][0]
                        
                        embed.add_field(name="Part of Speech", value=meaning['partOfSpeech'], inline=True)
                        embed.add_field(name="Definition", value=definition['definition'], inline=False)
                        
                        if 'example' in definition:
                            embed.add_field(name="Example", value=f"*{definition['example']}*", inline=False)
                        
                        # Add pronunciation if available
                        if 'phonetics' in entry and entry['phonetics']:
                            for phonetic in entry['phonetics']:
                                if 'text' in phonetic:
                                    embed.add_field(name="Pronunciation", value=phonetic['text'], inline=True)
                                    break
                        
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"❌ Could not find definition for '{word}'")
        except Exception as e:
            await interaction.response.send_message(f"❌ Error looking up word: {str(e)}")

async def setup(bot):
    await bot.add_cog(Information(bot))
