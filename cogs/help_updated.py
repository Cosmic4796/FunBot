import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Display all available commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Bot Command Center",
            description="Here are all available commands organized by category!",
            color=0x00ff88
        )
        
        # Fun Commands (Consolidated)
        fun_commands = [
            "`/8ball <question>` - Ask the magic 8-ball",
            "`/joke` - Get jokes from JokeAPI",
            "`/roast [user]` - Get roasted (friendly)",
            "`/compliment [user]` - Receive a compliment",
            "`/dice [sides]` - Roll dice",
            "`/coinflip` - Flip a coin",
            "`/choose <options>` - Choose between options",
            "`/reverse <text>` - Reverse text",
            "`/say <message>` - Make the bot say something",
            "`/ascii <text>` - Convert to ASCII art",
            "`/mock <text>` - SpongeBob mocking text",
            "`/uwu <text>` - Convert to uwu speak",
            "`/ship <user1> [user2]` - Ship two users",
            "`/rate <thing>` - Rate something 1-10"
        ]
        
        # Games (Some consolidated, some separate)
        game_commands = [
            "`/play <game> [choice]` - Play games: rps, trivia, riddle, guess",
            "`/wouldyourather` - Would you rather questions",
            "`/truthordare <choice>` - Truth or dare",
            "`/hangman` - Play hangman",
            "`/quiz` - General knowledge quiz"
        ]
        
        # Utility Commands (Some consolidated)
        utility_commands = [
            "`/serverinfo` - Get server information",
            "`/userinfo [user]` - Get user information",
            "`/avatar [user]` - Get user's avatar",
            "`/ping` - Check bot latency",
            "`/weather <city>` - Get weather (needs API key)",
            "`/time [timezone]` - Current time in timezone",
            "`/wiki <query>` - Search Wikipedia",
            "`/calc <expression>` - Simple calculator",
            "`/password [length]` - Generate secure password"
        ]
        
        # Text Tools (Consolidated into /text)
        text_commands = [
            "`/text <action> <text>` - Text tools: upper, lower, title, count, reverse, binary, morse",
            "`/base64encode <text>` - Encode to base64",
            "`/base64decode <text>` - Decode from base64",
            "`/hash <text> [algorithm]` - Generate hash",
            "`/pig_latin <text>` - Convert to pig latin"
        ]
        
        # Images (Consolidated /animal)
        image_commands = [
            "`/animal <type>` - Random animal images (cat/dog/fox)",
            "`/meme_template` - Get meme templates",
            "`/inspire` - Inspirational quotes",
            "`/color <hex>` - Show color information",
            "`/meme` - Random meme ideas"
        ]
        
        # Information Commands (New category!)
        info_commands = [
            "`/fact` - Random facts (NumbersAPI)",
            "`/quote` - Inspirational quotes (Quotable API)", 
            "`/advice` - Random advice (Advice Slip API)",
            "`/define <word>` - Define words (Free Dictionary API)",
            "`/github <query>` - Search GitHub repos",
            "`/crypto <symbol>` - Crypto prices (placeholder)",
            "`/stock <symbol>` - Stock info (placeholder)",
            "`/news` - Latest news (placeholder)",
            "`/movie <title>` - Movie info (placeholder)",
            "`/urban <term>` - Urban dictionary (placeholder)"
        ]
        
        # Economy Commands
        economy_commands = [
            "`/profile [user]` - View economy profile",
            "`/daily` - Claim daily coins",
            "`/balance [user]` - Check coin balance",
            "`/work` - Work for coins",
            "`/rob <user>` - Rob another user (risky)",
            "`/gamble <amount>` - Gamble coins",
            "`/shop` - View the shop",
            "`/buy <item> [quantity]` - Buy from shop",
            "`/inventory [user]` - View inventory",
            "`/give <user> <amount>` - Give coins"
        ]
        
        # Social Commands
        social_commands = [
            "`/hug <user>` - Hug someone",
            "`/kiss <user>` - Kiss someone",
            "`/slap <user>` - Slap someone (playful)",
            "`/highfive <user>` - High five someone",
            "`/pat <user>` - Pat someone",
            "`/poke <user>` - Poke someone",
            "`/wave <user>` - Wave at someone",
            "`/dance` - Show dance moves",
            "`/cry` - Express sadness",
            "`/laugh` - Express laughter",
            "`/love [user]` - Spread love",
            "`/sleep` - Go to sleep",
            "`/awake` - Wake up"
        ]
        
        # Server Commands
        server_commands = [
            "`/poll <question> <options>` - Create a poll",
            "`/reminder <time> <message>` - Set reminder",
            "`/todo <action> [item]` - Manage todo list",
            "`/note <action> [content]` - Take notes",
            "`/event <name> <date>` - Create event"
        ]
        
        embed.add_field(name="🎮 Fun Commands", value="\n".join(fun_commands), inline=False)
        embed.add_field(name="🎯 Games", value="\n".join(game_commands), inline=False)
        embed.add_field(name="🔧 Utilities", value="\n".join(utility_commands), inline=False)
        embed.add_field(name="📝 Text Tools", value="\n".join(text_commands), inline=False)
        embed.add_field(name="🖼️ Images", value="\n".join(image_commands), inline=False)
        embed.add_field(name="📚 Information", value="\n".join(info_commands), inline=False)
        embed.add_field(name="💰 Economy", value="\n".join(economy_commands), inline=False)
        embed.add_field(name="❤️ Social", value="\n".join(social_commands), inline=False)
        embed.add_field(name="🏰 Server", value="\n".join(server_commands), inline=False)
        
        embed.add_field(
            name="🔑 Free APIs Used",
            value="✅ **Working APIs (No key needed):**\n• Animal images, Jokes, Facts, Quotes, Advice, Dictionary, GitHub\n\n⚠️ **Need free API keys:**\n• Weather (OpenWeatherMap)\n\n💡 **Placeholder commands:**\n• Crypto, Stock, News, Movie (links to free APIs provided)",
            inline=False
        )
        
        embed.set_footer(text="Total: 90+ Commands • Smart consolidation • Many free APIs working!")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
