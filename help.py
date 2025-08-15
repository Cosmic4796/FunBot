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
            description="Here are all the available commands organized by category!",
            color=0x00ff88
        )
        
        # Fun Commands
        fun_commands = [
            "`/8ball` - Ask the magic 8-ball a question",
            "`/joke` - Get a random joke",
            "`/meme` - Generate a random meme",
            "`/roast` - Get roasted (friendly)",
            "`/compliment` - Receive a compliment",
            "`/dice` - Roll dice (1-6)",
            "`/coinflip` - Flip a coin",
            "`/choose` - Choose between options",
            "`/reverse` - Reverse text",
            "`/say` - Make the bot say something",
            "`/ascii` - Convert text to ASCII art",
            "`/mock` - Mock text (sPoNgEbOb style)",
            "`/uwu` - Convert text to uwu speak",
            "`/ship` - Ship two users",
            "`/rate` - Rate something 1-10"
        ]
        
        # Games
        game_commands = [
            "`/rps` - Rock Paper Scissors",
            "`/trivia` - Random trivia question",
            "`/riddle` - Get a random riddle",
            "`/wouldyourather` - Would you rather game",
            "`/truthordare` - Truth or dare",
            "`/hangman` - Play hangman",
            "`/tictactoe` - Play tic-tac-toe",
            "`/guess` - Number guessing game",
            "`/akinator` - 20 questions style game",
            "`/quiz` - General knowledge quiz"
        ]
        
        # Utility Commands
        utility_commands = [
            "`/serverinfo` - Get server information",
            "`/userinfo` - Get user information",
            "`/avatar` - Get user's avatar",
            "`/ping` - Check bot latency",
            "`/weather` - Get weather info (city required)",
            "`/time` - Get current time in timezone",
            "`/translate` - Translate text",
            "`/define` - Define a word",
            "`/wiki` - Search Wikipedia",
            "`/calc` - Simple calculator",
            "`/base64encode` - Encode to base64",
            "`/base64decode` - Decode from base64",
            "`/qr` - Generate QR code",
            "`/shorten` - Shorten URL",
            "`/password` - Generate secure password"
        ]
        
        # Image Commands
        image_commands = [
            "`/cat` - Random cat image",
            "`/dog` - Random dog image",
            "`/fox` - Random fox image",
            "`/bird` - Random bird image",
            "`/panda` - Random panda image",
            "`/meme_template` - Get meme templates",
            "`/inspire` - Inspirational quote image",
            "`/color` - Show color information",
            "`/blur` - Blur an image",
            "`/grayscale` - Convert image to grayscale"
        ]
        
        # Text Manipulation
        text_commands = [
            "`/upper` - Convert to uppercase",
            "`/lower` - Convert to lowercase",
            "`/title` - Convert to title case",
            "`/count` - Count characters/words",
            "`/encode` - Encode text",
            "`/decode` - Decode text",
            "`/hash` - Generate text hash",
            "`/binary` - Convert to binary",
            "`/morse` - Convert to morse code",
            "`/pig_latin` - Convert to pig latin"
        ]
        
        # Economy/RPG (Simple)
        rpg_commands = [
            "`/profile` - View your profile",
            "`/daily` - Claim daily coins",
            "`/balance` - Check your balance",
            "`/work` - Work for coins",
            "`/rob` - Rob another user",
            "`/gamble` - Gamble your coins",
            "`/shop` - View the shop",
            "`/buy` - Buy items from shop",
            "`/inventory` - View your inventory",
            "`/give` - Give coins to someone"
        ]
        
        # Information Commands
        info_commands = [
            "`/github` - Search GitHub repositories",
            "`/crypto` - Get cryptocurrency prices",
            "`/stock` - Get stock information",
            "`/news` - Get latest news",
            "`/fact` - Random fact",
            "`/quote` - Random quote",
            "`/advice` - Get random advice",
            "`/urban` - Urban dictionary lookup",
            "`/lyrics` - Get song lyrics",
            "`/movie` - Movie information"
        ]
        
        # Social Commands
        social_commands = [
            "`/hug` - Hug someone",
            "`/kiss` - Kiss someone",
            "`/slap` - Slap someone (playfully)",
            "`/highfive` - High five someone",
            "`/pat` - Pat someone",
            "`/poke` - Poke someone",
            "`/wave` - Wave at someone",
            "`/dance` - Dance",
            "`/cry` - Cry",
            "`/laugh` - Laugh"
        ]
        
        # Server Fun
        server_commands = [
            "`/poll` - Create a poll",
            "`/announcement` - Make an announcement",
            "`/reminder` - Set a reminder",
            "`/todo` - Manage your todo list",
            "`/note` - Take notes",
            "`/timer` - Set a timer",
            "`/countdown` - Create a countdown",
            "`/event` - Create an event",
            "`/birthday` - Manage birthdays",
            "`/leaderboard` - View server leaderboard"
        ]
        
        embed.add_field(name="🎮 Fun Commands", value="\n".join(fun_commands[:10]), inline=False)
        embed.add_field(name="🎯 Games", value="\n".join(game_commands), inline=False)
        embed.add_field(name="🔧 Utilities", value="\n".join(utility_commands), inline=False)
        embed.add_field(name="🖼️ Images", value="\n".join(image_commands), inline=False)
        embed.add_field(name="📝 Text Tools", value="\n".join(text_commands), inline=False)
        embed.add_field(name="💰 Economy", value="\n".join(rpg_commands), inline=False)
        embed.add_field(name="📚 Information", value="\n".join(info_commands), inline=False)
        embed.add_field(name="❤️ Social", value="\n".join(social_commands), inline=False)
        embed.add_field(name="🏰 Server", value="\n".join(server_commands), inline=False)
        
        embed.set_footer(text="Use /help to see this menu again • Total: 100+ Commands")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
