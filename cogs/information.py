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

    @app_commands.command(name="crypto", description="Get cryptocurrency prices")
    async def crypto_price(self, interaction: discord.Interaction, symbol: str = "bitcoin"):
        api_key = os.getenv('COINGECKO_API_KEY')
        
        try:
            async with aiohttp.ClientSession() as session:
                if api_key:
                    # Use CoinGecko API with key for higher rate limits
                    headers = {"x-cg-demo-api-key": api_key}
                    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true"
                else:
                    # Use free tier without key
                    headers = {}
                    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true"
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if symbol in data:
                            price = data[symbol]['usd']
                            change = data[symbol].get('usd_24h_change', 0)
                            
                            color = 0x00ff00 if change >= 0 else 0xff0000
                            change_emoji = "📈" if change >= 0 else "📉"
                            
                            embed = discord.Embed(
                                title=f"💰 {symbol.title()} Price",
                                color=color
                            )
                            embed.add_field(name="💵 Price", value=f"${price:,.2f}", inline=True)
                            embed.add_field(name=f"{change_emoji} 24h Change", value=f"{change:.2f}%", inline=True)
                            embed.set_footer(text="Data from CoinGecko API")
                            
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message(f"❌ Cryptocurrency '{symbol}' not found! Try: bitcoin, ethereum, dogecoin")
                    else:
                        raise Exception(f"API returned status {response.status}")
                        
        except Exception as e:
            await interaction.response.send_message(f"❌ Error fetching crypto price: {str(e)}")

    @app_commands.command(name="news", description="Get latest news headlines")
    async def latest_news(self, interaction: discord.Interaction, category: str = "general"):
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            await interaction.response.send_message("❌ News API key not configured!")
            return
        
        valid_categories = ["general", "business", "entertainment", "health", "science", "sports", "technology"]
        if category.lower() not in valid_categories:
            await interaction.response.send_message(f"❌ Invalid category! Choose from: {', '.join(valid_categories)}")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize=5&apiKey={api_key}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data['articles']
                        
                        if articles:
                            embed = discord.Embed(
                                title=f"📰 Latest {category.title()} News",
                                color=0x4169e1
                            )
                            
                            for i, article in enumerate(articles[:3], 1):  # Show top 3
                                title = article['title'][:100] + "..." if len(article['title']) > 100 else article['title']
                                description = article['description'][:200] + "..." if article['description'] and len(article['description']) > 200 else (article['description'] or "No description")
                                
                                embed.add_field(
                                    name=f"{i}. {title}",
                                    value=f"{description}\n[Read more]({article['url']})",
                                    inline=False
                                )
                            
                            embed.set_footer(text="Powered by NewsAPI")
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message("❌ No news articles found!")
                    else:
                        raise Exception(f"API returned status {response.status}")
                        
        except Exception as e:
            await interaction.response.send_message(f"❌ Error fetching news: {str(e)}")

    @app_commands.command(name="stock", description="Get stock information")
    async def stock_info(self, interaction: discord.Interaction, symbol: str):
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            await interaction.response.send_message("❌ Alpha Vantage API key not configured!")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol.upper()}&apikey={api_key}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if "Global Quote" in data and data["Global Quote"]:
                            quote = data["Global Quote"]
                            
                            price = float(quote["05. price"])
                            change = float(quote["09. change"])
                            change_percent = quote["10. change percent"].replace("%", "")
                            
                            color = 0x00ff00 if change >= 0 else 0xff0000
                            change_emoji = "📈" if change >= 0 else "📉"
                            
                            embed = discord.Embed(
                                title=f"📈 {symbol.upper()} Stock Info",
                                color=color
                            )
                            embed.add_field(name="💵 Current Price", value=f"${price:.2f}", inline=True)
                            embed.add_field(name=f"{change_emoji} Change", value=f"${change:+.2f} ({change_percent}%)", inline=True)
                            embed.add_field(name="📊 Previous Close", value=f"${float(quote['08. previous close']):.2f}", inline=True)
                            embed.add_field(name="📈 Day High", value=f"${float(quote['03. high']):.2f}", inline=True)
                            embed.add_field(name="📉 Day Low", value=f"${float(quote['04. low']):.2f}", inline=True)
                            embed.add_field(name="📅 Last Updated", value=quote["07. latest trading day"], inline=True)
                            
                            embed.set_footer(text="Data from Alpha Vantage")
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message(f"❌ Stock symbol '{symbol.upper()}' not found!")
                    else:
                        raise Exception(f"API returned status {response.status}")
                        
        except Exception as e:
            await interaction.response.send_message(f"❌ Error fetching stock data: {str(e)}")

    @app_commands.command(name="movie", description="Get movie information")
    async def movie_info(self, interaction: discord.Interaction, title: str):
        api_key = os.getenv('OMDB_API_KEY')
        if not api_key:
            await interaction.response.send_message("❌ OMDb API key not configured!")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get("Response") == "True":
                            embed = discord.Embed(
                                title=f"🎬 {data['Title']} ({data['Year']})",
                                description=data.get('Plot', 'No plot available'),
                                color=0xff6b6b
                            )
                            
                            if data.get('Poster') != 'N/A':
                                embed.set_thumbnail(url=data['Poster'])
                            
                            embed.add_field(name="⭐ IMDb Rating", value=data.get('imdbRating', 'N/A'), inline=True)
                            embed.add_field(name="🎭 Genre", value=data.get('Genre', 'N/A'), inline=True)
                            embed.add_field(name="🎬 Director", value=data.get('Director', 'N/A'), inline=True)
                            embed.add_field(name="🎭 Actors", value=data.get('Actors', 'N/A')[:100] + "..." if len(data.get('Actors', '')) > 100 else data.get('Actors', 'N/A'), inline=False)
                            embed.add_field(name="📅 Released", value=data.get('Released', 'N/A'), inline=True)
                            embed.add_field(name="⏱️ Runtime", value=data.get('Runtime', 'N/A'), inline=True)
                            embed.add_field(name="🏆 Awards", value=data.get('Awards', 'N/A'), inline=True)
                            
                            embed.set_footer(text="Data from OMDb API")
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message(f"❌ Movie '{title}' not found!")
                    else:
                        raise Exception(f"API returned status {response.status}")
                        
        except Exception as e:
            await interaction.response.send_message(f"❌ Error fetching movie data: {str(e)}")

    @app_commands.command(name="urban", description="Urban dictionary lookup")
    async def urban_dictionary(self, interaction: discord.Interaction, term: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://api.urbandictionary.com/v0/define?term={term}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data['list']:
                            definition = data['list'][0]  # Get top definition
                            
                            # Clean up the definition (remove brackets)
                            def_text = definition['definition'].replace('[', '').replace(']', '')
                            example_text = definition.get('example', '').replace('[', '').replace(']', '')
                            
                            # Truncate if too long
                            if len(def_text) > 1000:
                                def_text = def_text[:1000] + "..."
                            if len(example_text) > 500:
                                example_text = example_text[:500] + "..."
                            
                            embed = discord.Embed(
                                title=f"📖 Urban Dictionary: {term}",
                                description=def_text,
                                color=0xff69b4
                            )
                            
                            if example_text:
                                embed.add_field(name="💡 Example", value=f"*{example_text}*", inline=False)
                            
                            embed.add_field(name="👍 Thumbs Up", value=definition['thumbs_up'], inline=True)
                            embed.add_field(name="👎 Thumbs Down", value=definition['thumbs_down'], inline=True)
                            embed.add_field(name="📅 Date", value=definition['written_on'][:10], inline=True)
                            
                            embed.set_footer(text="Urban Dictionary • Content may be inappropriate")
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message(f"❌ No definition found for '{term}'")
                    else:
                        raise Exception(f"API returned status {response.status}")
                        
        except Exception as e:
            await interaction.response.send_message(f"❌ Error looking up term: {str(e)}")

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

    @app_commands.command(name="stock", description="Get stock information")
    async def stock_info(self, interaction: discord.Interaction, symbol: str):
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            await interaction.response.send_message("❌ Alpha Vantage API key not configured!")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol.upper()}&apikey={api_key}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if "Global Quote" in data and data["Global Quote"]:
                            quote = data["Global Quote"]
                            
                            price = float(quote["05. price"])
                            change = float(quote["09. change"])
                            change_percent = quote["10. change percent"].replace("%", "")
                            
                            color = 0x00ff00 if change >= 0 else 0xff0000
                            change_emoji = "📈" if change >= 0 else "📉"
                            
                            embed = discord.Embed(
                                title=f"📈 {symbol.upper()} Stock Info",
                                color=color
                            )
                            embed.add_field(name="💵 Current Price", value=f"${price:.2f}", inline=True)
                            embed.add_field(name=f"{change_emoji} Change", value=f"${change:+.2f} ({change_percent}%)", inline=True)
                            embed.add_field(name="📊 Previous Close", value=f"${float(quote['08. previous close']):.2f}", inline=True)
                            embed.add_field(name="📈 Day High", value=f"${float(quote['03. high']):.2f}", inline=True)
                            embed.add_field(name="📉 Day Low", value=f"${float(quote['04. low']):.2f}", inline=True)
                            embed.add_field(name="📅 Last Updated", value=quote["07. latest trading day"], inline=True)
                            
                            embed.set_footer(text="Data from Alpha Vantage")
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message(f"❌ Stock symbol '{symbol.upper()}' not found!")
                    else:
                        raise Exception(f"API returned status {response.status}")
                        
        except Exception as e:
            await interaction.response.send_message(f"❌ Error fetching stock data: {str(e)}")

    @app_commands.command(name="lyrics", description="Get song lyrics using lyrics.ovh API")
    async def song_lyrics(self, interaction: discord.Interaction, artist: str, song: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        lyrics = data.get('lyrics', '')
                        
                        if lyrics:
                            # Truncate lyrics if too long for Discord
                            if len(lyrics) > 2000:
                                lyrics = lyrics[:1997] + "..."
                            
                            embed = discord.Embed(
                                title=f"🎵 {song} by {artist}",
                                description=f"```{lyrics}```",
                                color=0x9932cc
                            )
                            embed.set_footer(text="Lyrics from lyrics.ovh")
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message("❌ No lyrics found!")
                    else:
                        await interaction.response.send_message(f"❌ Lyrics not found for '{song}' by '{artist}'")
                        
        except Exception as e:
            await interaction.response.send_message(f"❌ Error fetching lyrics: {str(e)}")

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
