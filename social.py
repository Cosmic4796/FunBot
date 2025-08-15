import discord
from discord.ext import commands
from discord import app_commands
import random

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # GIF URLs for different actions (you'd replace these with actual GIF URLs from tenor/giphy APIs)
        self.action_gifs = {
            "hug": [
                "https://media.tenor.com/example-hug-1.gif",
                "https://media.tenor.com/example-hug-2.gif",
                "https://media.tenor.com/example-hug-3.gif"
            ],
            "kiss": [
                "https://media.tenor.com/example-kiss-1.gif",
                "https://media.tenor.com/example-kiss-2.gif"
            ],
            "slap": [
                "https://media.tenor.com/example-slap-1.gif",
                "https://media.tenor.com/example-slap-2.gif"
            ],
            "pat": [
                "https://media.tenor.com/example-pat-1.gif",
                "https://media.tenor.com/example-pat-2.gif"
            ]
        }

    async def create_action_embed(self, interaction, target, action, color, emoji):
        """Create an embed for social actions"""
        if target.id == interaction.user.id:
            # Self action
            descriptions = {
                "hug": f"{interaction.user.mention} hugs themselves! 🤗",
                "kiss": f"{interaction.user.mention} kisses themselves in the mirror! 😘",
                "slap": f"{interaction.user.mention} slaps themselves... why though? 🤔",
                "pat": f"{interaction.user.mention} pats themselves on the back! 👏",
                "poke": f"{interaction.user.mention} pokes themselves... weird but ok! 👆",
                "highfive": f"{interaction.user.mention} high-fives the air! ✋",
                "wave": f"{interaction.user.mention} waves at everyone! 👋"
            }
        else:
            # Action towards another user
            descriptions = {
                "hug": f"{interaction.user.mention} gives {target.mention} a warm hug! 🤗",
                "kiss": f"{interaction.user.mention} kisses {target.mention}! 😘",
                "slap": f"{interaction.user.mention} slaps {target.mention}! (playfully!) 🖐️",
                "pat": f"{interaction.user.mention} pats {target.mention} on the head! 👋",
                "poke": f"{interaction.user.mention} pokes {target.mention}! 👆",
                "highfive": f"{interaction.user.mention} high-fives {target.mention}! ✋",
                "wave": f"{interaction.user.mention} waves at {target.mention}! 👋"
            }
        
        embed = discord.Embed(
            title=f"{emoji} {action.title()}",
            description=descriptions.get(action, f"{interaction.user.mention} {action}s {target.mention}!"),
            color=color
        )
        
        # In a real implementation, you'd use the GIF URLs
        # embed.set_image(url=random.choice(self.action_gifs.get(action, [])))
        embed.set_footer(text="Social interactions make the server fun! ❤️")
        
        return embed

    @app_commands.command(name="hug", description="Give someone a warm hug")
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        embed = await self.create_action_embed(interaction, user, "hug", 0xff69b4, "🤗")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kiss", description="Give someone a kiss")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member):
        embed = await self.create_action_embed(interaction, user, "kiss", 0xff1493, "😘")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="slap", description="Playfully slap someone")
    async def slap(self, interaction: discord.Interaction, user: discord.Member):
        embed = await self.create_action_embed(interaction, user, "slap", 0xff4500, "🖐️")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="highfive", description="Give someone a high five")
    async def highfive(self, interaction: discord.Interaction, user: discord.Member):
        embed = await self.create_action_embed(interaction, user, "highfive", 0x00ff00, "✋")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pat", description="Pat someone on the head")
    async def pat(self, interaction: discord.Interaction, user: discord.Member):
        embed = await self.create_action_embed(interaction, user, "pat", 0x87ceeb, "👋")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="poke", description="Poke someone to get their attention")
    async def poke(self, interaction: discord.Interaction, user: discord.Member):
        embed = await self.create_action_embed(interaction, user, "poke", 0xffd700, "👆")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="wave", description="Wave at someone")
    async def wave(self, interaction: discord.Interaction, user: discord.Member):
        embed = await self.create_action_embed(interaction, user, "wave", 0x4169e1, "👋")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dance", description="Show off your dance moves")
    async def dance(self, interaction: discord.Interaction):
        dance_moves = [
            "does the robot! 🤖",
            "breaks it down! 💃",
            "does the moonwalk! 🕺",
            "shows off some sick moves! 🕺💃",
            "dances like nobody's watching! 💃",
            "busts a move! 🕺",
            "does the floss! 🦷",
            "dances to the beat! 🎵"
        ]
        
        move = random.choice(dance_moves)
        
        embed = discord.Embed(
            title="💃 Dance Time!",
            description=f"{interaction.user.mention} {move}",
            color=0x9932cc
        )
        embed.set_footer(text="Dance like nobody's watching! 🎵")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cry", description="Express your sadness")
    async def cry(self, interaction: discord.Interaction):
        crying_messages = [
            "😭 *sobs quietly*",
            "😢 *tears up*",
            "😭 *cries dramatically*",
            "😢 *wipes away tears*",
            "😭 *needs comfort*",
            "😢 *feeling emotional*"
        ]
        
        message = random.choice(crying_messages)
        
        embed = discord.Embed(
            title="😭 Emotional Moment",
            description=f"{interaction.user.mention} {message}",
            color=0x4169e1
        )
        embed.set_footer(text="There, there... everything will be okay ❤️")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="laugh", description="Express your joy with laughter")
    async def laugh(self, interaction: discord.Interaction):
        laugh_types = [
            "😂 *bursts out laughing*",
            "🤣 *can't stop giggling*",
            "😂 *laughs hysterically*",
            "🤣 *rolls on the floor laughing*",
            "😂 *chuckles softly*",
            "🤣 *laughs until they cry*",
            "😂 *has a good belly laugh*",
            "🤣 *snorts while laughing*"
        ]
        
        laugh = random.choice(laugh_types)
        
        embed = discord.Embed(
            title="😂 Laughter is the Best Medicine",
            description=f"{interaction.user.mention} {laugh}",
            color=0xffff00
        )
        embed.set_footer(text="Laughter is contagious! 😄")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="angry", description="Express your anger")
    async def angry(self, interaction: discord.Interaction):
        angry_expressions = [
            "😠 *grumbles angrily*",
            "😡 *is fuming mad*",
            "🤬 *is absolutely furious*",
            "😤 *huffs and puffs*",
            "😠 *crosses arms angrily*",
            "😡 *sees red*",
            "🤬 *steam comes out of ears*"
        ]
        
        expression = random.choice(angry_expressions)
        
        embed = discord.Embed(
            title="😡 Anger Management",
            description=f"{interaction.user.mention} {expression}",
            color=0xff0000
        )
        embed.set_footer(text="Take a deep breath and count to 10 🧘‍♀️")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="confused", description="Express your confusion")
    async def confused(self, interaction: discord.Interaction):
        confused_expressions = [
            "🤔 *scratches head in confusion*",
            "😕 *looks puzzled*",
            "🤷‍♀️ *shrugs in bewilderment*",
            "😵‍💫 *is completely lost*",
            "🤔 *tilts head confused*",
            "😕 *doesn't understand*",
            "🤷‍♂️ *has no idea what's going on*"
        ]
        
        expression = random.choice(confused_expressions)
        
        embed = discord.Embed(
            title="🤔 Confusion Station",
            description=f"{interaction.user.mention} {expression}",
            color=0x9932cc
        )
        embed.set_footer(text="It's okay to not understand everything! 💭")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="love", description="Spread some love")
    async def love(self, interaction: discord.Interaction, user: discord.Member = None):
        if user:
            if user.id == interaction.user.id:
                description = f"{interaction.user.mention} loves themselves! Self-love is important! 💕"
            else:
                description = f"{interaction.user.mention} sends love to {user.mention}! 💖"
        else:
            description = f"{interaction.user.mention} spreads love to everyone in the chat! 💕✨"
        
        embed = discord.Embed(
            title="💖 Love is in the Air",
            description=description,
            color=0xff69b4
        )
        embed.set_footer(text="Love makes the world go round! ❤️")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sleep", description="Go to sleep")
    async def sleep(self, interaction: discord.Interaction):
        sleep_messages = [
            "😴 *falls asleep peacefully*",
            "💤 *starts snoring softly*",
            "😴 *curls up for a nap*",
            "💤 *dreams of electric sheep*",
            "😴 *counts sheep*",
            "💤 *enters dreamland*",
            "😴 *sleeps like a baby*"
        ]
        
        message = random.choice(sleep_messages)
        
        embed = discord.Embed(
            title="😴 Sweet Dreams",
            description=f"{interaction.user.mention} {message}",
            color=0x191970
        )
        embed.set_footer(text="Good night! Don't let the bed bugs bite! 🌙")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="awake", description="Wake up and greet everyone")
    async def awake(self, interaction: discord.Interaction):
        wake_messages = [
            "☀️ *yawns and stretches*",
            "🌅 *rubs eyes sleepily*",
            "☀️ *springs out of bed*",
            "🌅 *slowly opens eyes*",
            "☀️ *greets the morning*",
            "🌅 *rises and shines*",
            "☀️ *is ready for a new day*"
        ]
        
        message = random.choice(wake_messages)
        
        embed = discord.Embed(
            title="🌅 Rise and Shine!",
            description=f"{interaction.user.mention} {message}",
            color=0xffd700
        )
        embed.set_footer(text="Good morning! Have a wonderful day! ☀️")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Social(bot))
