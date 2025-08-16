import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.trivia_questions = [
            {"question": "What is the capital of France?", "answer": "paris", "options": ["London", "Berlin", "Paris", "Madrid"]},
            {"question": "Which planet is known as the Red Planet?", "answer": "mars", "options": ["Venus", "Mars", "Jupiter", "Saturn"]},
            {"question": "What is 2 + 2?", "answer": "4", "options": ["3", "4", "5", "6"]},
            {"question": "Who painted the Mona Lisa?", "answer": "leonardo da vinci", "options": ["Picasso", "Leonardo da Vinci", "Van Gogh", "Michelangelo"]},
            {"question": "What is the largest ocean on Earth?", "answer": "pacific", "options": ["Atlantic", "Indian", "Pacific", "Arctic"]},
            {"question": "How many continents are there?", "answer": "7", "options": ["5", "6", "7", "8"]},
            {"question": "What is the chemical symbol for gold?", "answer": "au", "options": ["Go", "Gd", "Au", "Ag"]},
            {"question": "Which year did World War II end?", "answer": "1945", "options": ["1944", "1945", "1946", "1947"]},
            {"question": "What is the smallest country in the world?", "answer": "vatican city", "options": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"]},
            {"question": "Who wrote Romeo and Juliet?", "answer": "shakespeare", "options": ["Shakespeare", "Dickens", "Austen", "Twain"]}
        ]
        
        self.riddles = [
            {"question": "I have keys but no locks. I have space but no room. You can enter, but you can't go outside. What am I?", "answer": "keyboard"},
            {"question": "What has hands but cannot clap?", "answer": "clock"},
            {"question": "I'm tall when I'm young, and short when I'm old. What am I?", "answer": "candle"},
            {"question": "What goes up but never comes down?", "answer": "age"},
            {"question": "What has one eye but cannot see?", "answer": "needle"},
            {"question": "What gets wetter the more it dries?", "answer": "towel"},
            {"question": "What runs around the whole yard without moving?", "answer": "fence"},
            {"question": "What can you break, even if you never pick it up or touch it?", "answer": "promise"},
            {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
            {"question": "I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?", "answer": "fire"}
        ]
        
        self.would_you_rather = [
            "Would you rather have the ability to fly or be invisible?",
            "Would you rather never have to sleep or never have to eat?",
            "Would you rather be able to read minds or predict the future?",
            "Would you rather live underwater or in space?",
            "Would you rather have super strength or super speed?",
            "Would you rather be famous or be the smartest person alive?",
            "Would you rather travel back in time or travel to the future?",
            "Would you rather never use the internet again or never watch TV again?",
            "Would you rather have unlimited money or unlimited time?",
            "Would you rather be able to speak all languages or talk to animals?"
        ]
        
        self.truth_questions = [
            "What's your biggest fear?",
            "What's the most embarrassing thing that's happened to you?",
            "Who was your first crush?",
            "What's a secret you've never told anyone?",
            "What's your biggest regret?",
            "What's the weirdest dream you've ever had?",
            "What's your most unpopular opinion?",
            "What's something you're glad your parents don't know about?",
            "What's the most trouble you've ever been in?",
            "What's your worst habit?"
        ]
        
        self.dare_challenges = [
            "Do 20 push-ups",
            "Sing your favorite song",
            "Dance for 30 seconds",
            "Do your best impression of a celebrity",
            "Speak in an accent for the next 3 messages",
            "Tell a joke",
            "Do your best animal impression",
            "Compliment everyone in the chat",
            "Share a funny story",
            "Do the chicken dance"
        ]

    @app_commands.command(name="play", description="Play various games: rps, trivia, riddle, hangman, guess, quiz")
    async def play_game(self, interaction: discord.Interaction, game: str, choice: str = None):
    @app_commands.command(name="play", description="Play various games: rps, trivia, riddle, hangman, guess, quiz")
    async def play_game(self, interaction: discord.Interaction, game: str, choice: str = None):
        game = game.lower()
        
        if game == "rps" and choice:
            # Rock Paper Scissors
            choices = ["rock", "paper", "scissors"]
            if choice.lower() not in choices:
                await interaction.response.send_message("Please choose rock, paper, or scissors!")
                return
            
            bot_choice = random.choice(choices)
            user_choice = choice.lower()
            
            emojis = {"rock": "🗿", "paper": "📄", "scissors": "✂️"}
            
            if user_choice == bot_choice:
                result = "It's a tie!"
                color = 0xffff00
            elif (user_choice == "rock" and bot_choice == "scissors") or \
                 (user_choice == "paper" and bot_choice == "rock") or \
                 (user_choice == "scissors" and bot_choice == "paper"):
                result = "You win!"
                color = 0x00ff00
            else:
                result = "I win!"
                color = 0xff0000
            
            embed = discord.Embed(title="🎮 Rock Paper Scissors", color=color)
            embed.add_field(name="You chose", value=f"{emojis[user_choice]} {user_choice.title()}", inline=True)
            embed.add_field(name="I chose", value=f"{emojis[bot_choice]} {bot_choice.title()}", inline=True)
            embed.add_field(name="Result", value=result, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        elif game == "trivia":
            # Trivia game
            question_data = random.choice(self.trivia_questions)
            
            embed = discord.Embed(
                title="🧠 Trivia Time!",
                description=question_data["question"],
                color=0x4169e1
            )
            
            options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(question_data["options"])])
            embed.add_field(name="Options", value=options_text, inline=False)
            embed.set_footer(text="You have 30 seconds to answer! Type the number of your choice.")
            
            await interaction.response.send_message(embed=embed)
            
            def check(message):
                return (message.author == interaction.user and 
                       message.channel == interaction.channel and
                       message.content.isdigit() and
                       1 <= int(message.content) <= 4)
            
            try:
                response = await self.bot.wait_for('message', timeout=30.0, check=check)
                user_answer = question_data["options"][int(response.content) - 1]
                
                if user_answer.lower() == question_data["answer"] or question_data["answer"] in user_answer.lower():
                    result_embed = discord.Embed(
                        title="✅ Correct!",
                        description=f"Great job! The answer was **{user_answer}**",
                        color=0x00ff00
                    )
                else:
                    correct_option = next(opt for opt in question_data["options"] if question_data["answer"] in opt.lower())
                    result_embed = discord.Embed(
                        title="❌ Incorrect!",
                        description=f"The correct answer was **{correct_option}**",
                        color=0xff0000
                    )
                
                await response.reply(embed=result_embed)
                
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="⏰ Time's up!",
                    description="You took too long to answer!",
                    color=0xff4500
                )
                await interaction.followup.send(embed=timeout_embed)
                
        elif game == "riddle":
            # Riddle game
            riddle_data = random.choice(self.riddles)
            
            embed = discord.Embed(
                title="🤔 Riddle Me This!",
                description=riddle_data["question"],
                color=0x9932cc
            )
            embed.set_footer(text="You have 60 seconds to answer!")
            
            await interaction.response.send_message(embed=embed)
            
            def check(message):
                return (message.author == interaction.user and 
                       message.channel == interaction.channel)
            
            try:
                response = await self.bot.wait_for('message', timeout=60.0, check=check)
                
                if riddle_data["answer"].lower() in response.content.lower():
                    result_embed = discord.Embed(
                        title="🎉 Correct!",
                        description=f"Excellent! The answer was **{riddle_data['answer']}**",
                        color=0x00ff00
                    )
                else:
                    result_embed = discord.Embed(
                        title="❌ Not quite!",
                        description=f"The answer was **{riddle_data['answer']}**\nBetter luck next time!",
                        color=0xff0000
                    )
                
                await response.reply(embed=result_embed)
                
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="⏰ Time's up!",
                    description=f"The answer was **{riddle_data['answer']}**",
                    color=0xff4500
                )
                await interaction.followup.send(embed=timeout_embed)
                
        elif game == "guess":
            # Number guessing game
            number = random.randint(1, 100)
            attempts = 0
            max_attempts = 7
            
            embed = discord.Embed(
                title="🎲 Number Guessing Game",
                description="I'm thinking of a number between 1 and 100!\nYou have 7 attempts to guess it.",
                color=0x4169e1
            )
            embed.set_footer(text="Type your guess!")
            
            await interaction.response.send_message(embed=embed)
            
            while attempts < max_attempts:
                def check(message):
                    return (message.author == interaction.user and 
                           message.channel == interaction.channel and
                           message.content.isdigit())
                
                try:
                    response = await self.bot.wait_for('message', timeout=60.0, check=check)
                    guess = int(response.content)
                    attempts += 1
                    
                    if guess < 1 or guess > 100:
                        await response.reply("Please guess a number between 1 and 100!")
                        attempts -= 1
                        continue
                    
                    if guess == number:
                        win_embed = discord.Embed(
                            title="🎉 Congratulations!",
                            description=f"You guessed it! The number was **{number}**\nIt took you {attempts} attempt(s)!",
                            color=0x00ff00
                        )
                        await response.reply(embed=win_embed)
                        break
                    elif guess < number:
                        hint_embed = discord.Embed(
                            title="📈 Too Low!",
                            description=f"Your guess ({guess}) is too low!\nAttempts remaining: {max_attempts - attempts}",
                            color=0xff4500
                        )
                        await response.reply(embed=hint_embed)
                    else:
                        hint_embed = discord.Embed(
                            title="📉 Too High!",
                            description=f"Your guess ({guess}) is too high!\nAttempts remaining: {max_attempts - attempts}",
                            color=0xff4500
                        )
                        await response.reply(embed=hint_embed)
                    
                    if attempts >= max_attempts:
                        lose_embed = discord.Embed(
                            title="😔 Game Over!",
                            description=f"You ran out of attempts! The number was **{number}**",
                            color=0xff0000
                        )
                        await response.reply(embed=lose_embed)
                        break
                        
                except asyncio.TimeoutError:
                    timeout_embed = discord.Embed(
                        title="⏰ Game timed out!",
                        description=f"You took too long! The number was **{number}**",
                        color=0xff4500
                    )
                    await interaction.followup.send(embed=timeout_embed)
                    break
                    
        else:
            embed = discord.Embed(
                title="🎮 Available Games",
                description="Choose from: **rps** (rock paper scissors), **trivia**, **riddle**, **guess** (number guessing)",
                color=0x4169e1
            )
            embed.add_field(name="Usage", value="`/play rps rock` or `/play trivia`", inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="trivia", description="Answer a random trivia question")
    async def trivia(self, interaction: discord.Interaction):
        question_data = random.choice(self.trivia_questions)
        
        embed = discord.Embed(
            title="🧠 Trivia Time!",
            description=question_data["question"],
            color=0x4169e1
        )
        
        options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(question_data["options"])])
        embed.add_field(name="Options", value=options_text, inline=False)
        embed.set_footer(text="You have 30 seconds to answer! Type the number of your choice.")
        
        await interaction.response.send_message(embed=embed)
        
        def check(message):
            return (message.author == interaction.user and 
                   message.channel == interaction.channel and
                   message.content.isdigit() and
                   1 <= int(message.content) <= 4)
        
        try:
            response = await self.bot.wait_for('message', timeout=30.0, check=check)
            user_answer = question_data["options"][int(response.content) - 1]
            
            if user_answer.lower() == question_data["answer"] or question_data["answer"] in user_answer.lower():
                result_embed = discord.Embed(
                    title="✅ Correct!",
                    description=f"Great job! The answer was **{user_answer}**",
                    color=0x00ff00
                )
            else:
                correct_option = next(opt for opt in question_data["options"] if question_data["answer"] in opt.lower())
                result_embed = discord.Embed(
                    title="❌ Incorrect!",
                    description=f"The correct answer was **{correct_option}**",
                    color=0xff0000
                )
            
            await response.reply(embed=result_embed)
            
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="⏰ Time's up!",
                description="You took too long to answer!",
                color=0xff4500
            )
            await interaction.followup.send(embed=timeout_embed)

    @app_commands.command(name="riddle", description="Solve a random riddle")
    async def riddle(self, interaction: discord.Interaction):
        riddle_data = random.choice(self.riddles)
        
        embed = discord.Embed(
            title="🤔 Riddle Me This!",
            description=riddle_data["question"],
            color=0x9932cc
        )
        embed.set_footer(text="You have 60 seconds to answer!")
        
        await interaction.response.send_message(embed=embed)
        
        def check(message):
            return (message.author == interaction.user and 
                   message.channel == interaction.channel)
        
        try:
            response = await self.bot.wait_for('message', timeout=60.0, check=check)
            
            if riddle_data["answer"].lower() in response.content.lower():
                result_embed = discord.Embed(
                    title="🎉 Correct!",
                    description=f"Excellent! The answer was **{riddle_data['answer']}**",
                    color=0x00ff00
                )
            else:
                result_embed = discord.Embed(
                    title="❌ Not quite!",
                    description=f"The answer was **{riddle_data['answer']}**\nBetter luck next time!",
                    color=0xff0000
                )
            
            await response.reply(embed=result_embed)
            
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="⏰ Time's up!",
                description=f"The answer was **{riddle_data['answer']}**",
                color=0xff4500
            )
            await interaction.followup.send(embed=timeout_embed)

    @app_commands.command(name="wouldyourather", description="Get a Would You Rather question")
    async def would_you_rather(self, interaction: discord.Interaction):
        question = random.choice(self.would_you_rather)
        
        embed = discord.Embed(
            title="🤷 Would You Rather?",
            description=question,
            color=0xff6b6b
        )
        embed.set_footer(text="Think about it and share your choice!")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="truthordare", description="Get a truth question or dare challenge")
    async def truth_or_dare(self, interaction: discord.Interaction, choice: str):
        if choice.lower() not in ["truth", "dare"]:
            await interaction.response.send_message("Please choose either 'truth' or 'dare'!")
            return
        
        if choice.lower() == "truth":
            question = random.choice(self.truth_questions)
            embed = discord.Embed(
                title="🤐 Truth",
                description=question,
                color=0x4169e1
            )
        else:
            dare = random.choice(self.dare_challenges)
            embed = discord.Embed(
                title="😈 Dare",
                description=dare,
                color=0xff4500
            )
        
        embed.set_footer(text="Have fun and be safe!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hangman", description="Play a game of hangman")
    async def hangman(self, interaction: discord.Interaction):
        words = [
            "python", "discord", "computer", "keyboard", "monitor", "internet",
            "gaming", "coding", "programming", "artificial", "intelligence",
            "machine", "learning", "algorithm", "database", "network"
        ]
        
        word = random.choice(words).upper()
        guessed_letters = set()
        incorrect_guesses = 0
        max_incorrect = 6
        
        def get_display_word():
            return " ".join([letter if letter in guessed_letters else "_" for letter in word])
        
        def get_hangman_art():
            stages = [
                "```\n  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========\n```",
                "```\n  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========\n```",
                "```\n  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========\n```",
                "```\n  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========\n```",
                "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========\n```",
                "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========\n```",
                "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========\n```"
            ]
            return stages[incorrect_guesses]
        
        embed = discord.Embed(
            title="🎯 Hangman",
            description=f"Guess the word!\n\n**Word:** {get_display_word()}\n\n{get_hangman_art()}",
            color=0x00ff00
        )
        embed.add_field(name="Instructions", value="Type a single letter to guess!", inline=False)
        embed.set_footer(text=f"Incorrect guesses: {incorrect_guesses}/{max_incorrect}")
        
        await interaction.response.send_message(embed=embed)
        
        while incorrect_guesses < max_incorrect and "_" in get_display_word():
            def check(message):
                return (message.author == interaction.user and 
                       message.channel == interaction.channel and
                       len(message.content) == 1 and
                       message.content.isalpha())
            
            try:
                response = await self.bot.wait_for('message', timeout=60.0, check=check)
                letter = response.content.upper()
                
                if letter in guessed_letters:
                    await response.reply("You already guessed that letter!")
                    continue
                
                guessed_letters.add(letter)
                
                if letter in word:
                    if "_" not in get_display_word():
                        win_embed = discord.Embed(
                            title="🎉 You Won!",
                            description=f"Congratulations! The word was **{word}**",
                            color=0x00ff00
                        )
                        await response.reply(embed=win_embed)
                        break
                    else:
                        continue_embed = discord.Embed(
                            title="✅ Good guess!",
                            description=f"**Word:** {get_display_word()}\n\n{get_hangman_art()}",
                            color=0x00ff00
                        )
                        continue_embed.set_footer(text=f"Incorrect guesses: {incorrect_guesses}/{max_incorrect}")
                        await response.reply(embed=continue_embed)
                else:
                    incorrect_guesses += 1
                    if incorrect_guesses >= max_incorrect:
                        lose_embed = discord.Embed(
                            title="💀 Game Over!",
                            description=f"You lost! The word was **{word}**\n\n{get_hangman_art()}",
                            color=0xff0000
                        )
                        await response.reply(embed=lose_embed)
                        break
                    else:
                        continue_embed = discord.Embed(
                            title="❌ Wrong letter!",
                            description=f"**Word:** {get_display_word()}\n\n{get_hangman_art()}",
                            color=0xff4500
                        )
                        continue_embed.set_footer(text=f"Incorrect guesses: {incorrect_guesses}/{max_incorrect}")
                        await response.reply(embed=continue_embed)
                        
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="⏰ Game timed out!",
                    description=f"You took too long! The word was **{word}**",
                    color=0xff4500
                )
                await interaction.followup.send(embed=timeout_embed)
                break

    @app_commands.command(name="guess", description="Number guessing game (1-100)")
    async def guess_number(self, interaction: discord.Interaction):
        number = random.randint(1, 100)
        attempts = 0
        max_attempts = 7
        
        embed = discord.Embed(
            title="🎲 Number Guessing Game",
            description="I'm thinking of a number between 1 and 100!\nYou have 7 attempts to guess it.",
            color=0x4169e1
        )
        embed.set_footer(text="Type your guess!")
        
        await interaction.response.send_message(embed=embed)
        
        while attempts < max_attempts:
            def check(message):
                return (message.author == interaction.user and 
                       message.channel == interaction.channel and
                       message.content.isdigit())
            
            try:
                response = await self.bot.wait_for('message', timeout=60.0, check=check)
                guess = int(response.content)
                attempts += 1
                
                if guess < 1 or guess > 100:
                    await response.reply("Please guess a number between 1 and 100!")
                    attempts -= 1
                    continue
                
                if guess == number:
                    win_embed = discord.Embed(
                        title="🎉 Congratulations!",
                        description=f"You guessed it! The number was **{number}**\nIt took you {attempts} attempt(s)!",
                        color=0x00ff00
                    )
                    await response.reply(embed=win_embed)
                    break
                elif guess < number:
                    hint_embed = discord.Embed(
                        title="📈 Too Low!",
                        description=f"Your guess ({guess}) is too low!\nAttempts remaining: {max_attempts - attempts}",
                        color=0xff4500
                    )
                    await response.reply(embed=hint_embed)
                else:
                    hint_embed = discord.Embed(
                        title="📉 Too High!",
                        description=f"Your guess ({guess}) is too high!\nAttempts remaining: {max_attempts - attempts}",
                        color=0xff4500
                    )
                    await response.reply(embed=hint_embed)
                
                if attempts >= max_attempts:
                    lose_embed = discord.Embed(
                        title="😔 Game Over!",
                        description=f"You ran out of attempts! The number was **{number}**",
                        color=0xff0000
                    )
                    await response.reply(embed=lose_embed)
                    break
                    
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="⏰ Game timed out!",
                    description=f"You took too long! The number was **{number}**",
                    color=0xff4500
                )
                await interaction.followup.send(embed=timeout_embed)
                break

    @app_commands.command(name="quiz", description="Take a quick general knowledge quiz")
    async def quiz(self, interaction: discord.Interaction):
        quiz_questions = random.sample(self.trivia_questions, 5)  # 5 random questions
        score = 0
        
        embed = discord.Embed(
            title="📚 Quick Quiz",
            description="Answer 5 questions to test your knowledge!\nType the number of your choice for each question.",
            color=0x9932cc
        )
        await interaction.response.send_message(embed=embed)
        
        for i, question_data in enumerate(quiz_questions, 1):
            question_embed = discord.Embed(
                title=f"Question {i}/5",
                description=question_data["question"],
                color=0x4169e1
            )
            
            options_text = "\n".join([f"{j+1}. {option}" for j, option in enumerate(question_data["options"])])
            question_embed.add_field(name="Options", value=options_text, inline=False)
            question_embed.set_footer(text="You have 20 seconds to answer!")
            
            await interaction.followup.send(embed=question_embed)
            
            def check(message):
                return (message.author == interaction.user and 
                       message.channel == interaction.channel and
                       message.content.isdigit() and
                       1 <= int(message.content) <= 4)
            
            try:
                response = await self.bot.wait_for('message', timeout=20.0, check=check)
                user_answer = question_data["options"][int(response.content) - 1]
                
                if user_answer.lower() == question_data["answer"] or question_data["answer"] in user_answer.lower():
                    score += 1
                    await response.add_reaction("✅")
                else:
                    await response.add_reaction("❌")
                    
            except asyncio.TimeoutError:
                timeout_msg = await interaction.followup.send("⏰ Time's up for this question!")
                await asyncio.sleep(2)
        
        # Final results
        percentage = (score / 5) * 100
        
        if percentage >= 80:
            grade = "🏆 Excellent!"
            color = 0x00ff00
        elif percentage >= 60:
            grade = "👍 Good job!"
            color = 0x4169e1
        elif percentage >= 40:
            grade = "📚 Not bad!"
            color = 0xffff00
        else:
            grade = "📖 Keep studying!"
            color = 0xff4500
        
        results_embed = discord.Embed(
            title="🎓 Quiz Results",
            description=f"**Score:** {score}/5 ({percentage}%)\n**Grade:** {grade}",
            color=color
        )
        
        await interaction.followup.send(embed=results_embed)

async def setup(bot):
    await bot.add_cog(Games(bot))
