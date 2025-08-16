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
        
        # Games (Consolidated into /play)
        game_commands = [
            "`/play rps <choice>` - Rock Paper Scissors",
            "`/play trivia` - Random trivia question",
            "`/play riddle` - Get a random riddle",
            "`/play guess` - Number guessing game",
            "`/wouldyourather` - Would you rather questions",
            "`/truthordare <choice>` - Truth or dare",
            "`/hangman` - Play hangman (separate command)"
        ]
        
        # Utility Commands (Consolidated)
        utility_commands = [
            "`/serverinfo` - Get server information",
            "`/userinfo [user]` - Get user information",
            "`/avatar [user]` - Get user's avatar",
            "`/ping` - Check bot latency",
            "`/weather <city>` - Get weather (needs API key)",
            "`/time [timezone]` - Current time in timezone",
            "`/facts [type]` - Get facts/quotes/advice",
            "`/wiki <query>` - Search Wikipedia",
            "`/calc <expression>` - Simple calculator",
            "`/password [length]` - Generate secure password"
        ]
        
        # Text Tools (Consolidated)
        text_commands = [
            "`/upper <text>` - Convert to uppercase",
            "`/lower <text>` - Convert to lowercase", 
            "`/title <text>` - Convert to title case",
            "`/count <text>` - Count characters/words",
            "`/base64encode <text>` - Encode to base64",
            "`/base64decode <text>` - Decode from base64",
            "`/hash <text> [algorithm]` - Generate hash",
            "`/binary <text>` - Convert to binary",
            "`/morse <text>` - Convert to morse code",
            "`/pig_latin <text>` - Convert to pig latin"
        ]
        
        # Images (Consolidated)
        image_commands = [
            "`/animal <type>` - Random animal images (cat/dog/fox)",
            "`/meme_template` - Get meme templates",
            "`/inspire` - Inspirational quotes",
            "`/color <hex>` - Show color information",
            "`/meme` - Random meme ideas"
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
        embed.add_field(name="💰 Economy", value="\n".join(economy_commands), inline=False)
        embed.add_field(name="❤️ Social", value="\n".join(social_commands), inline=False)
        embed.add_field(name="🏰 Server", value="\n".join(server_commands), inline=False)
        
        embed.add_field(
            name="🔑 API Setup Required",
            value="Some commands need free API keys:\n• Weather: OpenWeatherMap\n• All other APIs are free and work automatically!",
            inline=False
        )
        
        embed.set_footer(text="Total: 80+ Commands (Optimized) • Many commands consolidated for efficiency")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
