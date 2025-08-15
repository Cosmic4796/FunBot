import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime, timedelta
import asyncio

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "server_data.json"
        self.server_data = self.load_data()

    def load_data(self):
        """Load server data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_data(self):
        """Save server data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.server_data, f, indent=2)

    def get_server_data(self, guild_id: str):
        """Get server's data"""
        if guild_id not in self.server_data:
            self.server_data[guild_id] = {
                "polls": {},
                "reminders": {},
                "todos": {},
                "notes": {},
                "events": {},
                "birthdays": {}
            }
            self.save_data()
        return self.server_data[guild_id]

    @app_commands.command(name="poll", description="Create a poll with multiple options")
    async def create_poll(self, interaction: discord.Interaction, question: str, options: str):
        option_list = [opt.strip() for opt in options.split(",")]
        
        if len(option_list) < 2:
            await interaction.response.send_message("❌ You need at least 2 options separated by commas!")
            return
        
        if len(option_list) > 10:
            await interaction.response.send_message("❌ Maximum 10 options allowed!")
            return
        
        # Create poll embed
        embed = discord.Embed(
            title="📊 Poll",
            description=f"**{question}**",
            color=0x4169e1
        )
        
        # Number emojis for reactions
        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        poll_text = ""
        for i, option in enumerate(option_list):
            poll_text += f"{number_emojis[i]} {option}\n"
        
        embed.add_field(name="Options", value=poll_text, inline=False)
        embed.set_footer(text=f"Poll created by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
        
        # Add reactions
        message = await interaction.original_response()
        for i in range(len(option_list)):
            await message.add_reaction(number_emojis[i])

    @app_commands.command(name="announcement", description="Make a fancy announcement")
    async def announcement(self, interaction: discord.Interaction, title: str, message: str):
        embed = discord.Embed(
            title=f"📢 {title}",
            description=message,
            color=0xff4500,
            timestamp=datetime.now()
        )
        
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text="Official Announcement")
        
        await interaction.response.send_message("@everyone", embed=embed)

    @app_commands.command(name="reminder", description="Set a reminder (in minutes)")
    async def set_reminder(self, interaction: discord.Interaction, time_minutes: int, reminder_text: str):
        if time_minutes <= 0 or time_minutes > 1440:  # Max 24 hours
            await interaction.response.send_message("❌ Time must be between 1 and 1440 minutes (24 hours)!")
            return
        
        embed = discord.Embed(
            title="⏰ Reminder Set!",
            description=f"I'll remind you about: **{reminder_text}**\nIn {time_minutes} minute(s)",
            color=0x00ff00
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Wait and send reminder
        await asyncio.sleep(time_minutes * 60)
        
        reminder_embed = discord.Embed(
            title="🔔 Reminder!",
            description=f"{interaction.user.mention}, you asked me to remind you:\n**{reminder_text}**",
            color=0xff4500
        )
        
        await interaction.followup.send(embed=reminder_embed)

    @app_commands.command(name="todo", description="Manage your todo list")
    async def todo(self, interaction: discord.Interaction, action: str, item: str = None):
        server_data = self.get_server_data(str(interaction.guild.id))
        user_id = str(interaction.user.id)
        
        if user_id not in server_data["todos"]:
            server_data["todos"][user_id] = []
        
        if action.lower() == "add":
            if not item:
                await interaction.response.send_message("❌ Please provide an item to add!")
                return
            
            server_data["todos"][user_id].append({
                "item": item,
                "completed": False,
                "created": datetime.now().isoformat()
            })
            self.save_data()
            
            embed = discord.Embed(
                title="✅ Todo Added",
                description=f"Added: **{item}**",
                color=0x00ff00
            )
            await interaction.response.send_message(embed=embed)
            
        elif action.lower() == "list":
            todos = server_data["todos"][user_id]
            if not todos:
                await interaction.response.send_message("📝 Your todo list is empty!")
                return
            
            embed = discord.Embed(
                title=f"📝 {interaction.user.display_name}'s Todo List",
                color=0x4169e1
            )
            
            for i, todo in enumerate(todos, 1):
                status = "✅" if todo["completed"] else "❌"
                embed.add_field(
                    name=f"{i}. {status} {todo['item']}",
                    value=f"Created: {todo['created'][:10]}",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
            
        elif action.lower() == "complete":
            if not item or not item.isdigit():
                await interaction.response.send_message("❌ Please provide the todo number to complete!")
                return
            
            todo_num = int(item) - 1
            todos = server_data["todos"][user_id]
            
            if todo_num < 0 or todo_num >= len(todos):
                await interaction.response.send_message("❌ Invalid todo number!")
                return
            
            todos[todo_num]["completed"] = True
            self.save_data()
            
            embed = discord.Embed(
                title="✅ Todo Completed",
                description=f"Completed: **{todos[todo_num]['item']}**",
                color=0x00ff00
            )
            await interaction.response.send_message(embed=embed)
            
        else:
            await interaction.response.send_message("❌ Valid actions: add, list, complete")

    @app_commands.command(name="note", description="Take a note")
    async def take_note(self, interaction: discord.Interaction, title: str, content: str):
        server_data = self.get_server_data(str(interaction.guild.id))
        user_id = str(interaction.user.id)
        
        if user_id not in server_data["notes"]:
            server_data["notes"][user_id] = {}
        
        server_data["notes"][user_id][title] = {
            "content": content,
            "created": datetime.now().isoformat()
        }
        self.save_data()
        
        embed = discord.Embed(
            title="📝 Note Saved",
            description=f"**Title:** {title}\n**Content:** {content}",
            color=0x9932cc
        )
        embed.set_footer(text="Use /notes to view all your notes")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="notes", description="View your notes")
    async def view_notes(self, interaction: discord.Interaction):
        server_data = self.get_server_data(str(interaction.guild.id))
        user_id = str(interaction.user.id)
        
        if user_id not in server_data["notes"] or not server_data["notes"][user_id]:
            await interaction.response.send_message("📝 You don't have any notes!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"📝 {interaction.user.display_name}'s Notes",
            color=0x9932cc
        )
        
        for title, note_data in server_data["notes"][user_id].items():
            embed.add_field(
                name=title,
                value=f"{note_data['content']}\n*Created: {note_data['created'][:10]}*",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="timer", description="Set a timer (in minutes)")
    async def set_timer(self, interaction: discord.Interaction, minutes: int, label: str = "Timer"):
        if minutes <= 0 or minutes > 60:
            await interaction.response.send_message("❌ Timer must be between 1 and 60 minutes!")
            return
        
        embed = discord.Embed(
            title="⏲️ Timer Started",
            description=f"**{label}** set for {minutes} minute(s)",
            color=0xffd700
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Wait and notify
        await asyncio.sleep(minutes * 60)
        
        timer_embed = discord.Embed(
            title="⏰ Timer Finished!",
            description=f"{interaction.user.mention}, your **{label}** timer is done!",
            color=0xff4500
        )
        
        await interaction.followup.send(embed=timer_embed)

    @app_commands.command(name="countdown", description="Create a countdown to a future date")
    async def countdown(self, interaction: discord.Interaction, event_name: str, date: str, time: str = "00:00"):
        try:
            # Parse the date and time
            datetime_str = f"{date} {time}"
            target_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            if target_datetime <= datetime.now():
                await interaction.response.send_message("❌ Date must be in the future!")
                return
            
            time_diff = target_datetime - datetime.now()
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            embed = discord.Embed(
                title=f"⏳ Countdown: {event_name}",
                description=f"**Date:** {target_datetime.strftime('%B %d, %Y at %H:%M')}\n\n**Time remaining:**\n{days} days, {hours} hours, {minutes} minutes",
                color=0xff6b6b
            )
            
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            await interaction.response.send_message("❌ Invalid date format! Use YYYY-MM-DD and HH:MM (24-hour format)")

    @app_commands.command(name="event", description="Create an event announcement")
    async def create_event(self, interaction: discord.Interaction, title: str, date: str, time: str, description: str):
        try:
            event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            
            embed = discord.Embed(
                title=f"🎉 Event: {title}",
                description=description,
                color=0x9932cc,
                timestamp=event_datetime
            )
            
            embed.add_field(name="📅 Date", value=event_datetime.strftime("%B %d, %Y"), inline=True)
            embed.add_field(name="⏰ Time", value=event_datetime.strftime("%H:%M"), inline=True)
            embed.add_field(name="👤 Organizer", value=interaction.user.display_name, inline=True)
            
            embed.set_footer(text="React with ✅ if you're attending!")
            
            await interaction.response.send_message(embed=embed)
            
            # Add reaction for attendance
            message = await interaction.original_response()
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await message.add_reaction("❓")
            
        except ValueError:
            await interaction.response.send_message("❌ Invalid date/time format! Use YYYY-MM-DD for date and HH:MM for time")

    @app_commands.command(name="birthday", description="Add your birthday to the server list")
    async def add_birthday(self, interaction: discord.Interaction, date: str):
        try:
            # Parse birthday (MM-DD format)
            birthday = datetime.strptime(date, "%m-%d")
            
            server_data = self.get_server_data(str(interaction.guild.id))
            server_data["birthdays"][str(interaction.user.id)] = {
                "date": date,
                "name": interaction.user.display_name
            }
            self.save_data()
            
            embed = discord.Embed(
                title="🎂 Birthday Added!",
                description=f"Your birthday ({birthday.strftime('%B %d')}) has been added to the server list!",
                color=0xff69b4
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except ValueError:
            await interaction.response.send_message("❌ Invalid date format! Use MM-DD (e.g., 03-15 for March 15th)")

    @app_commands.command(name="birthdays", description="View upcoming birthdays")
    async def view_birthdays(self, interaction: discord.Interaction):
        server_data = self.get_server_data(str(interaction.guild.id))
        
        if not server_data["birthdays"]:
            await interaction.response.send_message("🎂 No birthdays registered yet!")
            return
        
        # Sort birthdays by date
        today = datetime.now()
        birthday_list = []
        
        for user_id, birthday_data in server_data["birthdays"].items():
            try:
                birthday_this_year = datetime.strptime(f"{today.year}-{birthday_data['date']}", "%Y-%m-%d")
                if birthday_this_year < today:
                    birthday_next_year = datetime.strptime(f"{today.year + 1}-{birthday_data['date']}", "%Y-%m-%d")
                    days_until = (birthday_next_year - today).days
                else:
                    days_until = (birthday_this_year - today).days
                
                birthday_list.append({
                    "name": birthday_data["name"],
                    "date": birthday_data["date"],
                    "days_until": days_until
                })
            except:
                continue
        
        birthday_list.sort(key=lambda x: x["days_until"])
        
        embed = discord.Embed(
            title="🎂 Upcoming Birthdays",
            color=0xff69b4
        )
        
        for birthday in birthday_list[:10]:  # Show first 10
            birthday_date = datetime.strptime(birthday["date"], "%m-%d")
            if birthday["days_until"] == 0:
                days_text = "🎉 TODAY!"
            elif birthday["days_until"] == 1:
                days_text = "Tomorrow!"
            else:
                days_text = f"In {birthday['days_until']} days"
            
            embed.add_field(
                name=f"{birthday['name']}",
                value=f"{birthday_date.strftime('%B %d')} - {days_text}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="View server activity leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        # This is a simple placeholder - in a real bot you'd track message counts, etc.
        embed = discord.Embed(
            title="🏆 Server Leaderboard",
            description="This feature requires message tracking implementation.\n\nTo implement:\n1. Track user messages in database\n2. Count user activity\n3. Display top users",
            color=0xffd700
        )
        embed.set_footer(text="Feature coming soon!")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Server(bot))
