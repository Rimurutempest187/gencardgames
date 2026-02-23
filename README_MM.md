# 🎴 Card Collection Bot - မြန်မာဘာသာ လမ်းညွှန်

## 📦 Package အကြောင်း

**Card Character Collection Telegram Bot** အပြည့်အစုံ အသင့်သုံး Code ဖြစ်ပါသည်။

### ✨ Features များ

#### 🛠 Admin Commands (9 ခု)
- `/upload` - ကဒ်အသစ် (ပုံ) တင်ရန်
- `/uploadvd` - Video ကဒ်တင်ရန် (Animated)
- `/edit` - ကဒ်ပြင်ရန်
- `/delete` - ကဒ်ဖျက်ရန်
- `/setdrop` - Drop အကြိမ်ရေသတ်မှတ်ရန်
- `/stats` - Statistics ကြည့်ရန်
- `/backup` - Data backup လုပ်ရန်
- `/restore` - Data ပြန်ယူရန်
- `/allclear` - Data အားလုံးဖျက်ရန်

#### 👥 User Commands (25+ ခု)
- **Economy**: `/balance`, `/daily`, `/shop`, `/buy`, `/givecoin`
- **Games**: `/slots`, `/basket`, `/wheel`
- **Cards**: `/catch`, `/set`, `/removeset`
- **Social**: `/marry`, `/divorce`, `/trade`, `/fusion`, `/duel`
- **Rankings**: `/top`, `/titles`, `/missions`

#### 👑 Owner Commands (4 ခု)
- `/addsudo` - Admin အသစ်ခန့်ရန်
- `/sudolist` - Admin စာရင်းကြည့်ရန်
- `/broadcast` - Group အားလုံးသို့ message ပို့ရန်

### ⭐ Rarity System (9 အဆင့်)
- ⚪ Common (40%)
- 🔵 Rare (25%)
- 🟣 Epic (15%)
- 🟠 Legendary (10%)
- 🔴 Mythic (5%)
- 🟡 Divine (3%)
- 💎 Celestial (1.5%)
- 👑 Supreme (0.4%)
- ✨ Animated (0.1%) - Video ကဒ်များ

---

## 🚀 Installation အမြန်လမ်းညွှန်

### အဆင့် ၁ - Python Install လုပ်ပါ
**Windows:**
- https://www.python.org/downloads/ မှ download လုပ်ပါ
- Install လုပ်ရင် "Add Python to PATH" ကို ခြစ်ပါ

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# Mac
brew install python3
```

### အဆင့် ၂ - Bot Files များ ဖြည်ပါ
```bash
unzip card_collection_bot.zip
cd card_collection_bot
```

### အဆင့် ၃ - Configuration လုပ်ပါ

**၃.၁ - Bot Token ရယူပါ:**
1. Telegram တွင် `@BotFather` ကို ရှာပါ
2. `/newbot` ပို့ပါ
3. Bot name နှင့် username ထည့်ပါ
4. Token ကို copy လုပ်ပါ

**၃.၂ - User ID ရယူပါ:**
1. Telegram တွင် `@userinfobot` ကို ရှာပါ
2. Message ပို့ပါ
3. User ID ကို copy လုပ်ပါ

**၃.၃ - .env File ကို ပြင်ပါ:**
```bash
nano .env
```

ဒါမှမဟုတ် Notepad ဖြင့်ဖွင့်ပြီး:
```
BOT_TOKEN=သင့်ရဲ့_bot_token
OWNER_ID=သင့်ရဲ့_user_id
```

### အဆင့် ၄ - Dependencies Install လုပ်ပါ

**Windows:**
```cmd
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
pip3 install -r requirements.txt
```

**အလိုအလျောက်:**
```bash
chmod +x install.sh
./install.sh
```

### အဆင့် ၅ - Bot ကို Start လုပ်ပါ

**Windows:**
```cmd
python bot.py
```

**Linux/Mac:**
```bash
python3 bot.py
```

**Start Script သုံးခြင်း:**
```bash
chmod +x start.sh
./start.sh
```

**Docker သုံးခြင်း:**
```bash
docker-compose up -d
```

---

## ✅ စမ်းသပ်ခြင်း

### Bot ကို Test လုပ်ပါ:
1. Telegram ဖွင့်ပါ
2. သင့် Bot username ကို ရှာပါ
3. `/start` ပို့ပါ
4. Welcome message ပြရင် အောင်မြင်ပါပြီ! 🎉

### Group တွင် စမ်းသပ်ပါ:
1. Bot ကို Group သို့ ထည့်ပါ
2. Bot ကို Admin အဖြစ် ခန့်ပါ
3. `/setdrop 10` ပို့ပါ
4. ၁၀ ကြိမ် message ပို့ပါ
5. Card ကျလာမည်!
6. `/catch CardName` ဖြင့် ဖမ်းပါ

---

## 🎴 Card များ ထည့်ခြင်း

### ပုံကဒ် (Image Card):
1. Bot ထံ Private chat
2. `/upload` ပို့ပါ
3. ပုံတစ်ပုံပို့ပြီး Caption ထည့်ပါ:
   ```
   Naruto | Naruto Shippuden | Legendary
   ```

### Video ကဒ်:
1. Bot ထံ Private chat
2. `/uploadvd` ပို့ပါ
3. Video ပို့ပြီး Caption ထည့်ပါ:
   ```
   Sasuke | Naruto Shippuden
   ```
   (Rarity သည် Animated အဖြစ် အလိုအလျောက်သတ်မှတ်မည်)

---

## 📁 File များ

Bot Package တွင် ပါဝင်သော Files များ:

```
card_collection_bot/
├── bot.py                  # Main Bot Code (1184 lines)
├── requirements.txt        # Python Libraries
├── .env                    # Configuration File
├── .env.example           # Example Config
├── README.md              # အင်္ဂလိပ် Documentation
├── QUICKSTART.md          # ၅ မိနစ် Setup Guide
├── DOCUMENTATION.md       # Technical Details
├── FEATURES.md            # Feature List
├── INSTALL.md             # Installation Guide
├── install.sh             # Auto Installer (Linux/Mac)
├── start.sh               # Start Script
├── Dockerfile             # Docker Image
├── docker-compose.yml     # Docker Setup
├── cardbot.service        # Systemd Service
└── .gitignore            # Git Ignore File
```

**စုစုပေါင်း:**
- 🐍 Python Code: 1,184 lines
- 📚 Documentation: 1,500+ lines
- 📝 Total Files: 16 files
- 💾 Package Size: 25 KB (compressed)

---

## 🎮 အသုံးပြုနည်း

### User အဖြစ်:
1. Group တွင် chat ပြောပါ
2. Card ကျလာတိုင်း `/catch CardName` ဖြင့် ဖမ်းပါ
3. Coin များကို game ကစားရန် သုံးပါ: `/slots 100`
4. Shop မှ item ဝယ်ပါ: `/shop`, `/buy 1`
5. Daily bonus ယူပါ: `/daily`
6. Top 10 တွင် ဝင်အောင် ကြိုးစားပါ: `/top`

### Admin အဖြစ်:
1. Card များ upload လုပ်ပါ: `/upload`, `/uploadvd`
2. Drop rate သတ်မှတ်ပါ: `/setdrop 50`
3. Card များ manage လုပ်ပါ: `/edit`, `/delete`
4. Statistics ကြည့်ပါ: `/stats`
5. Backup လုပ်ပါ: `/backup`

### Owner အဖြစ်:
1. Admin များ ခန့်ပါ: Reply ပြီး `/addsudo`
2. Broadcast ပို့ပါ: `/broadcast Your message here`
3. Admin list ကြည့်ပါ: `/sudolist`

---

## 🎯 Mission System

| Mission | လိုအပ်သော Cards | Reward | Title |
|---------|------------------|--------|-------|
| Collector | 50 | 1,000 Coins | 🎴 Collector |
| Master | 100 | 2,500 Coins | 🏆 Master |
| Legend | 200 | 5,000 Coins | ⭐ Legend |
| Champion | 500 | 10,000 Coins | 👑 Champion |

---

## 🏪 Shop Items

| Item | Price | အသုံးပြုပုံ |
|------|-------|-----------|
| 🎁 Card Pack (5 Random) | 500 | ကဒ် ၅ ခု ရ |
| 💰 Coin Booster | 1,000 | Daily bonus ၂ ဆ |
| 🔮 Rarity Upgrade | 2,000 | Rarity မြှင့်ရန် |
| 🎯 Card Selector | 5,000 | ကဒ်ရွေးရန် |

---

## 🔧 ပြဿနာဖြေရှင်းခြင်း

### Bot မတုံ့ပြန်ပါက:
```bash
# Python version စစ်ပါ
python --version

# Dependencies စစ်ပါ
pip list | grep telegram

# Process running ဟုတ်မဟုတ်စစ်ပါ
ps aux | grep bot.py
```

### Cards မကျပါက:
```
1. /setdrop 10 သုံးပြီး စမ်းကြည့်ပါ
2. Bot က Group အတွင်း Admin ဖြစ်ရမည်
3. /stats ဖြင့် cards ရှိမရှိ စစ်ပါ
```

### Permission Error:
```
1. .env ထဲက OWNER_ID မှန်မမှန်စစ်ပါ
2. Bot ကို restart လုပ်ပါ
```

---

## 💡 အကြံပြုချက်များ

### လုံခြုံရေး:
- ✅ BOT_TOKEN ကို လုံခြုံစွာ သိမ်းဆည်းပါ
- ✅ အပတ်စဉ် `/backup` လုပ်ပါ
- ✅ OWNER_ID ကို မျှဝေခြင်းမပြုပါနှင့်
- ✅ .env file ကို public မဖြစ်အောင်ထားပါ

### Performance:
- ✅ Drop rate ကို အသင့်လျော်သတ်မှတ်ပါ (50-100)
- ✅ အသုံးပြုသူများလာတိုင်း Coin inflation ကို ထိန်းပါ
- ✅ Card များကို အဆင့်ဆင့်ထည့်ပါ
- ✅ Data ကို ပုံမှန် backup လုပ်ပါ

### Community:
- ✅ Rules သတ်မှတ်ပါ
- ✅ Fair play ကို အားပေးပါ
- ✅ Events များ လုပ်ပါ
- ✅ Leaderboard ကို အားပေးပါ

---

## 📊 အချက်အလက်များ

### စွမ်းဆောင်ရည်:
- ⚡ **Commands**: 40+ commands
- 🎴 **Cards**: Unlimited
- 👥 **Users**: Unlimited
- 💬 **Groups**: Unlimited (recommended < 100 for JSON storage)
- 🎮 **Games**: 3 types
- 🏆 **Missions**: 4 levels
- 💎 **Rarities**: 9 levels
- 🏪 **Shop Items**: 4 items

### နည်းပညာ:
- 🐍 Python 3.8+
- 📦 python-telegram-bot 20.7
- 💾 JSON-based storage
- ⚡ Async handlers
- 🔒 Security features
- 📝 Comprehensive logging
- 🐳 Docker support
- 🔄 Backup/Restore system

---

## 🎉 အောင်မြင်မှု Checklist

Installation မှန်ကန်မှုစစ်ဆေးခြင်း:

- ✅ Python 3.8+ install ပြီး
- ✅ Bot files များ extract ပြီး
- ✅ .env file တွင် credentials ထည့်ပြီး
- ✅ Dependencies install ပြီး (`pip install -r requirements.txt`)
- ✅ Bot running ဖြစ်နေပြီ (console shows "Bot started!")
- ✅ Telegram တွင် `/start` တုံ့ပြန်ပြီး
- ✅ Group သို့ bot ထည့်ပြီး admin ခန့်ပြီး
- ✅ Drop rate သတ်မှတ်ပြီး (`/setdrop 50`)
- ✅ Card များ upload လုပ်ပြီး
- ✅ ပထမဆုံး card drop နှင့် catch အောင်မြင်ပြီး

**အားလုံးပြည့်မီပါက အသင့်အသုံးပြုနိုင်ပါပြီ! 🚀**

---

## 📞 အကူအညီလိုပါက

### Documentation များ ဖတ်ပါ:
1. **QUICKSTART.md** - အမြန်စတင်ရန်
2. **INSTALL.md** - Installation အသေးစိတ်
3. **README.md** - Feature အပြည့်အစုံ
4. **DOCUMENTATION.md** - Technical details
5. **FEATURES.md** - Feature စာရင်းအပြည့်

### အဆင့်ဆင့်စစ်ဆေးပါ:
1. Bot token မှန်ကန်ရမည်
2. Python version 3.8+ ဖြစ်ရမည်
3. Dependencies install လုပ်ရမည်
4. Internet connection ရှိရမည်
5. Bot process running ဖြစ်ရမည်

---

## 🌟 အထူးမှတ်ချက်များ

### ဘာကြောင့် ကောင်းသလဲ:
1. ✅ **အပြည့်အစုံ** - 40+ commands နှင့် အသင့်သုံး
2. ✅ **လွယ်ကူ** - Setup 5 မိနစ်အတွင်း
3. ✅ **Documentation** - မြန်မာ + အင်္ဂလိပ် လမ်းညွှန်များ
4. ✅ **Security** - Admin level controls
5. ✅ **Backup** - Data loss prevention
6. ✅ **Scalable** - Unlimited cards and users
7. ✅ **Games** - Engaging mini-games
8. ✅ **Social** - Trading, marriage features
9. ✅ **Free** - Open source, no cost
10. ✅ **Support** - Complete documentation

---

## 📌 Version Info

- **Version**: 1.0.0
- **Status**: Production Ready ✅
- **Code**: 1,184 lines Python
- **Docs**: 1,500+ lines
- **License**: Open Source
- **Language**: English + Myanmar
- **Support**: Full documentation

---

## 🎊 အဆုံး

Bot package တွင် လိုအပ်သမျှ အားလုံးပါဝင်ပါသည်:
- ✅ Working bot code
- ✅ Installation scripts
- ✅ Documentation (English + Myanmar)
- ✅ Docker support
- ✅ Systemd service
- ✅ Example configurations

**အသုံးပြုပြီး ပျော်ရွှင်ပါစေ! 🎴✨**

---

**Created with ❤️ for Telegram Bot enthusiasts**  
**Package Date**: 2024  
**Download**: card_collection_bot.zip (25 KB)
