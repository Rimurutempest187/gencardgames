# 🎴 Quick Start Guide

## ⚡ Fast Setup (5 Minutes)

### Step 1: Get Your Bot Token
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose a name: `My Card Bot`
5. Choose a username: `my_card_collection_bot`
6. **Copy the token** (looks like: `1234567890:ABCdef...`)

### Step 2: Get Your User ID
1. Search for `@userinfobot` in Telegram
2. Send any message
3. **Copy your ID** (looks like: `123456789`)

### Step 3: Configure the Bot
1. Open `.env` file
2. Replace `your_bot_token_here` with your token
3. Replace `your_telegram_user_id_here` with your ID
4. Save the file

### Step 4: Install & Run

**On Windows:**
```bash
pip install -r requirements.txt
python bot.py
```

**On Linux/Mac:**
```bash
chmod +x install.sh start.sh
./install.sh
./start.sh
```

**Using Docker:**
```bash
docker-compose up -d
```

### Step 5: Test Your Bot
1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. You should get a welcome message! 🎉

---

## 📝 First Commands to Try

**As Owner:**
```
/help - See all commands
/upload - Add your first card
/setdrop 10 - Set drop rate (for testing)
```

**Create a Test Group:**
1. Create a new Telegram group
2. Add your bot to the group
3. Make the bot an admin
4. Send 10 messages to trigger a card drop
5. Use `/catch CardName` to collect it

---

## 🎴 Adding Your First Card

1. In private chat with bot, send: `/upload`
2. Send an image with caption:
   ```
   Naruto | Naruto Shippuden | Legendary
   ```
3. Bot will confirm the card was added
4. Now go to your test group and chat to trigger a drop!

---

## ❓ Troubleshooting

**Bot not responding?**
- Check if bot.py is running
- Verify BOT_TOKEN is correct
- Check internet connection

**Cards not dropping?**
- Use `/setdrop 5` for faster testing
- Make sure bot is admin in group
- Check if cards exist: `/stats`

**Permission denied?**
- Verify OWNER_ID matches your Telegram ID
- Restart the bot after changing .env

---

## 🎯 What's Next?

1. ✅ Add more cards with `/upload` and `/uploadvd`
2. ✅ Invite friends to your group
3. ✅ Let them collect cards
4. ✅ Try games: `/slots 100`, `/wheel 50`
5. ✅ Check leaderboard: `/top`
6. ✅ Complete missions for rewards

---

## 📚 Full Documentation

See `README.md` and `DOCUMENTATION.md` for complete details.

---

**Enjoy your card collection bot! 🎴✨**
