# 🤖 Multi-Purpose Discord Bot

A feature-rich Discord bot with 100+ commands covering fun, games, utilities, economy, social interactions, and more!

## ✨ Features

- **🎮 Fun Commands** - Jokes, 8ball, memes, text manipulation
- **🎯 Games** - Rock Paper Scissors, trivia, hangman, number guessing
- **🔧 Utilities** - Server info, calculations, text tools, time zones  
- **🖼️ Images** - Random animal pictures, color tools
- **💰 Economy System** - Coins, shop, work, gambling, inventory
- **❤️ Social Commands** - Hugs, kisses, dance, reactions
- **🏰 Server Tools** - Polls, reminders, todos, events, birthdays
- **📚 Information** - Facts, quotes, advice, word of the day

## 🚀 Quick Deploy to Railway

1. **Fork this repository** to your GitHub account

2. **Create a Discord Application:**
   - Go to https://discord.com/developers/applications
   - Click "New Application" and give it a name
   - Go to the "Bot" tab and create a bot
   - Copy the bot token (keep it secret!)
   - Under "Privileged Gateway Intents", enable:
     - Message Content Intent
     - Server Members Intent

3. **Deploy to Railway:**
   - Go to https://railway.app
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository
   - Add environment variable: `DISCORD_TOKEN` with your bot token
   - Deploy!

4. **Invite Bot to Server:**
   - In Discord Developer Portal, go to "OAuth2" → "URL Generator"
   - Select scopes: `bot` and `applications.commands`
   - Select permissions: `Send Messages`, `Use Slash Commands`, `Add Reactions`, `Embed Links`
   - Copy the generated URL and open it to invite the bot

## 🛠️ Local Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment Setup:**
```bash
cp .env.example .env
# Edit .env and add your Discord bot token
```

4. **Run the bot:**
```bash
python main.py
```

## 📋 Command Categories

### 🎮 Fun Commands (15)
- `/8ball` - Ask the magic 8-ball
- `/joke` - Random jokes
- `/roast` - Playful roasts
- `/compliment` - Nice compliments
- `/dice` - Roll dice
- `/coinflip` - Flip a coin
- `/choose` - Choose between options
- `/reverse` - Reverse text
- `/say` - Make the bot speak
- `/ascii` - ASCII art text
- `/mock` - SpongeBob mocking text
- `/uwu` - UwU text converter
- `/ship` - Ship users together
- `/rate` - Rate anything 1-10
- `/meme` - Random memes

### 🎯 Games (10)
- `/rps` - Rock Paper Scissors
- `/trivia` - Trivia questions
- `/riddle` - Brain teasers
- `/wouldyourather` - Would you rather
- `/truthordare` - Truth or dare
- `/hangman` - Classic word game
- `/tictactoe` - Tic-tac-toe
- `/guess` - Number guessing
- `/akinator` - 20 questions style
- `/quiz` - Knowledge quiz

### 🔧 Utilities (15)
- `/serverinfo` - Server information
- `/userinfo` - User profiles
- `/avatar` - User avatars
- `/ping` - Bot latency
- `/weather` - Weather info*
- `/time` - World time zones
- `/translate` - Text translation*
- `/wiki` - Wikipedia search
- `/calc` - Calculator
- `/base64encode` - Base64 encoding
- `/base64decode` - Base64 decoding
- `/password` - Password generator
- `/upper/lower/title` - Text case conversion
- `/count` - Character/word counter
- `/hash` - Text hashing

### 🖼️ Images (10)
- `/cat` - Random cats
- `/dog` - Random dogs  
- `/fox` - Random foxes
- `/bird` - Random birds
- `/panda` - Random pandas
- `/meme_template` - Meme templates
- `/inspire` - Inspirational images
- `/color` - Color information
- `/blur/grayscale` - Image effects*

### 💰 Economy (10)
- `/profile` - Economy profile
- `/daily` - Daily coin reward
- `/balance` - Check balance
- `/work` - Work for coins
- `/rob` - Rob other users
- `/gamble` - Coin gambling
- `/shop` - Item shop
- `/buy` - Purchase items
- `/inventory` - View items
- `/give` - Transfer coins

### ❤️ Social (15)
- `/hug` - Hug someone
- `/kiss` - Kiss someone
- `/slap` - Playful slaps
- `/highfive` - High fives
- `/pat` - Pat heads
- `/poke` - Poke users
- `/wave` - Wave hello
- `/dance` - Dance moves
- `/cry` - Express sadness
- `/laugh` - Show joy
- `/angry` - Express anger
- `/confused` - Show confusion
- `/love` - Spread love
- `/sleep` - Go to sleep
- `/awake` - Wake up

### 🏰 Server (10)
- `/poll` - Create polls
- `/announcement` - Announcements
- `/reminder` - Set reminders
- `/todo` - Todo lists
- `/note` - Take notes
- `/timer` - Set timers
- `/countdown` - Event countdowns
- `/event` - Create events
- `/birthday` - Birthday tracking
- `/leaderboard` - Activity rankings

### 📚 Information (15)
- `/fact` - Random facts
- `/quote` - Inspirational quotes
- `/advice` - Life advice
- `/word_of_the_day` - Vocabulary
- `/number_fact` - Number trivia
- `/color_fact` - Color facts
- `/tech_fact` - Technology facts
- `/riddle_fact` - Riddles with facts
- `/github` - GitHub search*
- `/crypto` - Crypto prices*
- `/stock` - Stock info*
- `/news` - Latest news*
- `/urban` - Urban dictionary*
- `/lyrics` - Song lyrics*
- `/movie` - Movie info*

*\*Requires API integration*

## 🔧 API Integration

Some commands require external APIs for full functionality:

- **Weather**: OpenWeatherMap API
- **Translation**: Google Translate API
- **News**: NewsAPI
- **Crypto**: CoinGecko API
- **Stocks**: Alpha Vantage API
- **GIFs**: Tenor/Giphy API

Add the API keys to your environment variables to enable these features.

## 📁 Project Structure

```
discord-bot/
├── main.py              # Main bot file
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── README.md           # This file
├── cogs/               # Command modules
│   ├── __init__.py
│   ├── help.py         # Help command
│   ├── fun.py          # Fun commands
│   ├── games.py        # Game commands
│   ├── utilities.py    # Utility commands
│   ├── images.py       # Image commands
│   ├── economy.py      # Economy system
│   ├── social.py       # Social commands
│   ├── server.py       # Server management
│   └── information.py  # Info commands
├── economy_data.json   # Economy data (auto-generated)
└── server_data.json    # Server data (auto-generated)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you need help:
1. Check this README
2. Look at the code comments
3. Create an issue on GitHub
4. Join our support server: [Discord Link]

## 🎯 Roadmap

- [ ] Web dashboard
- [ ] Music commands
- [ ] Advanced moderation
- [ ] Custom command builder
- [ ] Database integration
- [ ] Multi-language support

---

**Made with ❤️ for the Discord community!**
