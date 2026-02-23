# 📥 Installation Instructions

## 🎯 Choose Your Installation Method

### Method 1: Windows (Recommended for Beginners)

**Step 1: Install Python**
1. Download Python from https://www.python.org/downloads/
2. Run installer and **CHECK** "Add Python to PATH"
3. Click "Install Now"

**Step 2: Extract Bot Files**
1. Extract `card_collection_bot.zip`
2. Open folder in File Explorer

**Step 3: Configure Bot**
1. Open `.env` file with Notepad
2. Replace `your_bot_token_here` with your actual bot token
3. Replace `your_telegram_user_id_here` with your Telegram user ID
4. Save and close

**Step 4: Install Dependencies**
1. Open Command Prompt in bot folder (Shift + Right Click → "Open PowerShell window here")
2. Run: `pip install -r requirements.txt`

**Step 5: Start Bot**
```cmd
python bot.py
```

✅ Bot should start! Keep window open while bot runs.

---

### Method 2: Linux/Mac (Terminal)

**Step 1: Extract and Navigate**
```bash
unzip card_collection_bot.zip
cd card_collection_bot
```

**Step 2: Make Scripts Executable**
```bash
chmod +x install.sh start.sh
```

**Step 3: Configure**
```bash
nano .env
# Edit BOT_TOKEN and OWNER_ID
# Press Ctrl+X, then Y, then Enter to save
```

**Step 4: Install**
```bash
./install.sh
```

**Step 5: Start**
```bash
./start.sh
```

---

### Method 3: Docker (For Advanced Users)

**Step 1: Install Docker**
- Windows/Mac: Docker Desktop
- Linux: `sudo apt install docker.io docker-compose`

**Step 2: Configure**
```bash
nano .env
# Edit BOT_TOKEN and OWNER_ID
```

**Step 3: Run**
```bash
docker-compose up -d
```

**To View Logs:**
```bash
docker-compose logs -f
```

**To Stop:**
```bash
docker-compose down
```

---

### Method 4: Linux Server with Systemd

**Step 1: Setup**
```bash
# Create user
sudo useradd -m -s /bin/bash cardbot

# Copy files
sudo mkdir /opt/card_collection_bot
sudo cp -r * /opt/card_collection_bot/
sudo chown -R cardbot:cardbot /opt/card_collection_bot

# Configure
sudo nano /opt/card_collection_bot/.env
```

**Step 2: Install Dependencies**
```bash
sudo su - cardbot
cd /opt/card_collection_bot
pip3 install -r requirements.txt
exit
```

**Step 3: Setup Service**
```bash
# Copy service file
sudo cp cardbot.service /etc/systemd/system/

# Edit if needed
sudo nano /etc/systemd/system/cardbot.service

# Start service
sudo systemctl daemon-reload
sudo systemctl enable cardbot
sudo systemctl start cardbot
```

**Step 4: Manage Service**
```bash
# Check status
sudo systemctl status cardbot

# View logs
sudo journalctl -u cardbot -f

# Restart
sudo systemctl restart cardbot

# Stop
sudo systemctl stop cardbot
```

---

## 🔑 Getting Your Bot Credentials

### Get Bot Token (From @BotFather)

1. Open Telegram
2. Search for **@BotFather**
3. Send: `/newbot`
4. Enter bot name: `My Card Collection Bot`
5. Enter username: `my_card_bot` (must end with 'bot')
6. Copy the token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Get Your User ID (From @userinfobot)

1. Open Telegram
2. Search for **@userinfobot**
3. Send: `/start` or any message
4. Copy your ID number (looks like: `123456789`)

---

## ✅ Verification

After starting the bot:

1. **Open Telegram**
2. **Search** for your bot username
3. **Send**: `/start`
4. **Expected**: Welcome message with commands

If you see the welcome message, **congratulations! Your bot is working! 🎉**

---

## 🔧 Troubleshooting

### Bot Not Responding

**Check 1: Is bot running?**
- Windows: Command Prompt window should be open
- Linux: Check `ps aux | grep bot.py`
- Docker: `docker-compose ps`

**Check 2: Correct token?**
```bash
# Verify .env file
cat .env
# Should show your actual token, not placeholder
```

**Check 3: Dependencies installed?**
```bash
pip list | grep telegram
# Should show: python-telegram-bot
```

**Check 4: Internet connection?**
```bash
ping telegram.org
```

### Permission Errors (Linux)

```bash
# Fix file permissions
chmod +x *.sh
chmod 644 bot.py

# Fix ownership
sudo chown -R $USER:$USER .
```

### Port Already in Use

Bot doesn't use ports, but if you get conflicts:
```bash
# Find process
ps aux | grep bot.py

# Kill old process
kill <process_id>

# Or
pkill -f bot.py
```

### Module Not Found Error

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or with pip3
pip3 install -r requirements.txt --force-reinstall
```

### Bot Token Error

```bash
# Error: "Token is invalid"
# Solution: Get new token from @BotFather
# 1. Send /token to @BotFather
# 2. Select your bot
# 3. Copy new token
# 4. Update .env file
```

---

## 📱 Adding Bot to Groups

**Step 1: Add Bot**
1. Open your group in Telegram
2. Click group name → Add Members
3. Search for your bot username
4. Add bot to group

**Step 2: Make Admin**
1. Click group name → Administrators
2. Add your bot
3. Enable "Delete Messages" permission (recommended)

**Step 3: Configure Drop Rate**
```
/setdrop 50
```
(Cards will drop every 50 messages)

**Step 4: Test**
- Send 50 messages in group
- Bot should drop a card
- Use `/catch CardName` to collect

---

## 🎴 Adding Your First Cards

**Method 1: Image Card**
```
1. Private chat with bot
2. Send: /upload
3. Send image with caption:
   Naruto | Naruto Shippuden | Legendary
```

**Method 2: Video Card**
```
1. Private chat with bot
2. Send: /uploadvd
3. Send video with caption:
   Sasuke | Naruto Shippuden
   (Rarity automatically set to Animated)
```

---

## 🎯 Testing Your Bot

**Test Commands:**
```
/start          - Check if bot responds
/help           - View all commands
/balance        - Check your balance (should be 1000)
/daily          - Get daily bonus
/upload         - Try uploading a card (admin)
/stats          - View bot statistics (admin)
```

**Test in Group:**
```
1. Add bot to test group
2. Make bot admin
3. /setdrop 5 (for quick testing)
4. Send 5 messages
5. Card should drop!
6. /catch CardName to collect
```

---

## 📊 Monitoring

**Check Logs:**
```bash
# Linux/Mac
tail -f bot_data.json

# Docker
docker-compose logs -f

# Systemd
journalctl -u cardbot -f
```

**Bot Status:**
```
Private chat with bot:
/stats - See users, groups, cards count
```

---

## 🆘 Need Help?

**Common Issues:**
1. ❌ **Bot not responding** → Check if process is running
2. ❌ **Cards not dropping** → Use `/setdrop` command
3. ❌ **Permission denied** → Verify OWNER_ID is correct
4. ❌ **Import errors** → Reinstall dependencies
5. ❌ **Invalid token** → Get new token from @BotFather

**Still stuck?**
- Check README.md for detailed info
- Review DOCUMENTATION.md for technical details
- Verify all steps were followed
- Check error messages in console

---

## 🎉 Success Checklist

- ✅ Python 3.8+ installed
- ✅ Bot files extracted
- ✅ .env configured with real credentials
- ✅ Dependencies installed (requirements.txt)
- ✅ Bot running (console shows "Bot started!")
- ✅ Bot responds to /start in Telegram
- ✅ Bot added to group as admin
- ✅ Drop rate configured with /setdrop
- ✅ Cards added with /upload or /uploadvd
- ✅ First card dropped and caught successfully

**If all checked, you're ready to go! 🚀**

---

**Version**: 1.0.0  
**Support**: See README.md and DOCUMENTATION.md  
**License**: Open Source - Free to use and modify

**Happy collecting! 🎴✨**
