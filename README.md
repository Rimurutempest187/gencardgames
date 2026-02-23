# 🎴 Card Character Collection Telegram Bot

A fully-featured Telegram bot for collecting character cards with trading, gaming, and social features.

## ✨ Features

### 🛠 Admin Commands
- `/upload` - Upload new image cards
- `/uploadvd` - Upload video cards (auto-animated rarity)
- `/edit <id> <name> <movie>` - Edit card details
- `/delete <id>` - Delete cards
- `/setdrop <number>` - Set drop frequency in groups
- `/stats` - View bot statistics
- `/backup` - Backup bot data
- `/restore` - Restore bot data
- `/allclear` - Clear all data

### 🎮 User Commands

**Economy & Shop:**
- `/balance` - Check your balance
- `/shop` - View shop items
- `/buy <number>` - Purchase items
- `/daily` - Claim daily bonus

**Games:**
- `/slots <amount>` - Slot machine game
- `/basket <amount>` - Basketball game
- `/wheel <amount>` - Wheel of fortune

**Cards:**
- `/catch <name>` - Catch dropped cards
- `/set <card_id>` - Set favorite card
- `/removeset <card_id>` - Remove favorite card

**Social & Trading:**
- `/givecoin <amount>` - Transfer coins (reply to user)
- `/trade` - Trade cards (reply to user)
- `/fusion` - Fuse cards
- `/duel` - Duel with cards (reply to user)
- `/marry` - Marry another user (reply to user)
- `/divorce` - Divorce

**Rankings:**
- `/top` - Top 10 collectors leaderboard
- `/titles` - View your titles
- `/missions` - View mission progress

### 👑 Owner Commands
- `/addsudo` - Add admin (reply to user)
- `/sudolist` - List all admins
- `/broadcast <message>` - Broadcast to all groups

## ⭐ Rarity System

- ⚪ **Common** - 40% drop chance
- 🔵 **Rare** - 25% drop chance
- 🟣 **Epic** - 15% drop chance
- 🟠 **Legendary** - 10% drop chance
- 🔴 **Mythic** - 5% drop chance
- 🟡 **Divine** - 3% drop chance
- 💎 **Celestial** - 1.5% drop chance
- 👑 **Supreme** - 0.4% drop chance
- ✨ **Animated** - 0.1% drop chance (video cards)

## 📦 Installation

### 1. Requirements
```bash
Python 3.8 or higher
pip (Python package manager)
```

### 2. Setup

**Clone or download this project:**
```bash
cd card_collection_bot
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### 3. Configuration

**Edit `.env` file:**
```env
BOT_TOKEN=your_bot_token_here
OWNER_ID=your_telegram_user_id_here
```

**How to get BOT_TOKEN:**
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token provided

**How to get OWNER_ID:**
1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
2. Send any message to the bot
3. Copy your user ID

### 4. Run the Bot

```bash
python bot.py
```

## 🎯 How to Use

### For Admins:

**1. Upload Image Card:**
```
1. Send /upload command
2. Send an image with caption: Name | Movie | Rarity
   Example: Naruto | Naruto Shippuden | Legendary
```

**2. Upload Video Card:**
```
1. Send /uploadvd command
2. Send a video with caption: Name | Movie
   (Rarity automatically set to Animated)
```

**3. Set Drop Rate:**
```
/setdrop 50
(Cards will drop every 50 messages in the group)
```

### For Users:

**1. Join a Group:**
- Add the bot to your Telegram group
- Make the bot an admin

**2. Collect Cards:**
- Chat in the group to trigger card drops
- Use `/catch <card_name>` to catch the card
- Earn coins and build your collection

**3. Play Games:**
```
/slots 100    - Bet 100 coins on slots
/basket 50    - Bet 50 coins on basketball
/wheel 200    - Bet 200 coins on wheel
```

**4. Trading:**
```
Reply to a user's message and use:
/trade - Trade cards
/givecoin 500 - Give 500 coins
```

## 🏪 Shop Items

- 🎁 **Card Pack (5 Random)** - 500 coins
- 💰 **Coin Booster (2x Daily)** - 1,000 coins
- 🔮 **Rarity Upgrade Token** - 2,000 coins
- 🎯 **Specific Card Selector** - 5,000 coins

## 🎯 Missions

| Mission | Requirement | Reward | Title |
|---------|------------|--------|-------|
| Collector | 50 cards | 1,000 coins | 🎴 Collector |
| Master | 100 cards | 2,500 coins | 🏆 Master |
| Legend | 200 cards | 5,000 coins | ⭐ Legend |
| Champion | 500 cards | 10,000 coins | 👑 Champion |

## 📁 File Structure

```
card_collection_bot/
│
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── .env               # Configuration file
├── bot_data.json      # Data storage (auto-generated)
└── README.md          # Documentation
```

## 🔧 Troubleshooting

**Bot not responding:**
- Check if BOT_TOKEN is correct
- Make sure bot is running (`python bot.py`)
- Check internet connection

**Cards not dropping:**
- Use `/setdrop` command to set drop rate
- Make sure bot is admin in the group
- Check if there are cards in the database

**Permission errors:**
- Make sure OWNER_ID is correct
- Check if user is added as sudo admin

## 🛡️ Data Backup

**Automatic Backup:**
- All data is stored in `bot_data.json`
- Use `/backup` command to download backup file
- Keep backups regularly to prevent data loss

**Restore Data:**
- Use `/restore` command
- Send the backup JSON file
- Data will be restored automatically

## ⚠️ Important Notes

1. **Keep your BOT_TOKEN secret** - Don't share it publicly
2. **Backup regularly** - Use `/backup` command weekly
3. **Test in private** - Test new features in a test group first
4. **Monitor usage** - Check `/stats` regularly
5. **Update Python** - Keep Python and dependencies updated

## 📝 License

This project is open source and free to use for personal and commercial purposes.

## 🤝 Support

For issues or questions:
1. Check this README thoroughly
2. Review the error messages
3. Make sure all dependencies are installed
4. Verify configuration in `.env` file

## 🎉 Credits

Created for Telegram Card Collection enthusiasts!

---

**Enjoy collecting cards! 🎴✨**
