import os
import asyncio
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ChatType
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))

# Data storage
DATA_FILE = 'bot_data.json'
BACKUP_FILE = 'bot_backup.json'

# Rarity system
RARITIES = {
    'Common': {'emoji': '⚪', 'value': 10, 'drop_chance': 40},
    'Rare': {'emoji': '🔵', 'value': 25, 'drop_chance': 25},
    'Epic': {'emoji': '🟣', 'value': 50, 'drop_chance': 15},
    'Legendary': {'emoji': '🟠', 'value': 100, 'drop_chance': 10},
    'Mythic': {'emoji': '🔴', 'value': 200, 'drop_chance': 5},
    'Divine': {'emoji': '🟡', 'value': 400, 'drop_chance': 3},
    'Celestial': {'emoji': '💎', 'value': 800, 'drop_chance': 1.5},
    'Supreme': {'emoji': '👑', 'value': 1600, 'drop_chance': 0.4},
    'Animated': {'emoji': '✨', 'value': 3200, 'drop_chance': 0.1}
}

# Global data structure
bot_data = {
    'cards': {},
    'users': {},
    'groups': {},
    'sudo_users': [],
    'drop_settings': {},
    'pending_uploads': {},
    'pending_trades': {},
    'pending_duels': {},
    'pending_fusions': {}
}

# Shop items
SHOP_ITEMS = {
    '🎁 Card Pack (5 Random)': {'price': 500, 'type': 'pack'},
    '💰 Coin Booster (2x Daily)': {'price': 1000, 'type': 'booster'},
    '🔮 Rarity Upgrade Token': {'price': 2000, 'type': 'upgrade'},
    '🎯 Specific Card Selector': {'price': 5000, 'type': 'selector'}
}

# Missions
MISSIONS = {
    'collector': {'name': 'Collector', 'requirement': 50, 'reward': 1000, 'title': '🎴 Collector'},
    'master': {'name': 'Master', 'requirement': 100, 'reward': 2500, 'title': '🏆 Master'},
    'legend': {'name': 'Legend', 'requirement': 200, 'reward': 5000, 'title': '⭐ Legend'},
    'champion': {'name': 'Champion', 'requirement': 500, 'reward': 10000, 'title': '👑 Champion'}
}

# Load data
def load_data():
    global bot_data
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                bot_data = json.load(f)
            logger.info("Data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading data: {e}")

# Save data
def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(bot_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving data: {e}")

# Initialize user
def init_user(user_id: int, username: str = None):
    user_id = str(user_id)
    if user_id not in bot_data['users']:
        bot_data['users'][user_id] = {
            'username': username,
            'cards': {},
            'balance': 1000,
            'last_daily': None,
            'favorite_cards': [],
            'titles': [],
            'married_to': None,
            'inventory': {},
            'completed_missions': []
        }
        save_data()

# Initialize group
def init_group(chat_id: int, chat_title: str):
    chat_id = str(chat_id)
    if chat_id not in bot_data['groups']:
        bot_data['groups'][chat_id] = {
            'title': chat_title,
            'message_count': 0,
            'last_drop': None
        }
        save_data()

# Get rarity by chance
def get_random_rarity():
    rand = random.uniform(0, 100)
    cumulative = 0
    for rarity, data in RARITIES.items():
        cumulative += data['drop_chance']
        if rand <= cumulative:
            return rarity
    return 'Common'

# Check if user is sudo
def is_sudo(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in bot_data['sudo_users']

# Admin Commands
async def upload_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    await update.message.reply_text(
        "📤 ကဒ်အသစ်တင်ရန်:\n"
        "1️⃣ ဓာတ်ပုံပို့ပါ\n"
        "2️⃣ Caption တွင်: name | movie | rarity ထည့်ပါ\n\n"
        "ဥပမာ: Naruto | Naruto Shippuden | Legendary"
    )
    bot_data['pending_uploads'][str(update.effective_user.id)] = 'waiting'
    save_data()

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if user_id in bot_data['pending_uploads']:
        if not update.message.caption:
            await update.message.reply_text("❌ Caption ထည့်ပါ: name | movie | rarity")
            return
        
        try:
            parts = update.message.caption.split('|')
            if len(parts) != 3:
                await update.message.reply_text("❌ Format မှား: name | movie | rarity")
                return
            
            name, movie, rarity = [p.strip() for p in parts]
            
            if rarity not in RARITIES:
                await update.message.reply_text(f"❌ Rarity မှား: {', '.join(RARITIES.keys())}")
                return
            
            # Get photo file
            photo = update.message.photo[-1]
            file_id = photo.file_id
            
            # Create card
            card_id = str(len(bot_data['cards']) + 1)
            bot_data['cards'][card_id] = {
                'name': name,
                'movie': movie,
                'rarity': rarity,
                'file_id': file_id,
                'type': 'image',
                'created_at': datetime.now().isoformat()
            }
            
            del bot_data['pending_uploads'][user_id]
            save_data()
            
            emoji = RARITIES[rarity]['emoji']
            await update.message.reply_text(
                f"✅ ကဒ်အသစ်ထည့်ပြီး!\n\n"
                f"🆔 ID: {card_id}\n"
                f"👤 Name: {name}\n"
                f"🎬 Movie: {movie}\n"
                f"{emoji} Rarity: {rarity}"
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

async def upload_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    await update.message.reply_text(
        "📤 Video ကဒ်တင်ရန်:\n"
        "1️⃣ Video ပို့ပါ\n"
        "2️⃣ Caption တွင်: name | movie ထည့်ပါ\n\n"
        "(Rarity သည် Animated အဖြစ် အလိုအလျောက်သတ်မှတ်ပါမည်)"
    )
    bot_data['pending_uploads'][str(update.effective_user.id)] = 'video'
    save_data()

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if user_id in bot_data['pending_uploads'] and bot_data['pending_uploads'][user_id] == 'video':
        if not update.message.caption:
            await update.message.reply_text("❌ Caption ထည့်ပါ: name | movie")
            return
        
        try:
            parts = update.message.caption.split('|')
            if len(parts) != 2:
                await update.message.reply_text("❌ Format မှား: name | movie")
                return
            
            name, movie = [p.strip() for p in parts]
            
            # Get video file
            video = update.message.video
            file_id = video.file_id
            
            # Create card with Animated rarity
            card_id = str(len(bot_data['cards']) + 1)
            bot_data['cards'][card_id] = {
                'name': name,
                'movie': movie,
                'rarity': 'Animated',
                'file_id': file_id,
                'type': 'video',
                'created_at': datetime.now().isoformat()
            }
            
            del bot_data['pending_uploads'][user_id]
            save_data()
            
            await update.message.reply_text(
                f"✅ Video ကဒ်ထည့်ပြီး!\n\n"
                f"🆔 ID: {card_id}\n"
                f"👤 Name: {name}\n"
                f"🎬 Movie: {movie}\n"
                f"✨ Rarity: Animated"
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

async def edit_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    if len(context.args) < 3:
        await update.message.reply_text("❌ Format: /edit <id> <name> <movie>")
        return
    
    card_id = context.args[0]
    name = context.args[1]
    movie = ' '.join(context.args[2:])
    
    if card_id not in bot_data['cards']:
        await update.message.reply_text("❌ ကဒ် ID မတွေ့ပါ")
        return
    
    bot_data['cards'][card_id]['name'] = name
    bot_data['cards'][card_id]['movie'] = movie
    save_data()
    
    await update.message.reply_text(f"✅ ကဒ် {card_id} ကို ပြင်ဆင်ပြီး!")

async def delete_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /delete <id>")
        return
    
    card_id = context.args[0]
    
    if card_id not in bot_data['cards']:
        await update.message.reply_text("❌ ကဒ် ID မတွေ့ပါ")
        return
    
    del bot_data['cards'][card_id]
    save_data()
    
    await update.message.reply_text(f"✅ ကဒ် {card_id} ကို ဖျက်ပြီး!")

async def set_drop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /setdrop <number>")
        return
    
    try:
        drop_count = int(context.args[0])
        chat_id = str(update.effective_chat.id)
        bot_data['drop_settings'][chat_id] = drop_count
        save_data()
        
        await update.message.reply_text(f"✅ Drop time ကို {drop_count} messages အဖြစ်သတ်မှတ်ပြီး!")
    except ValueError:
        await update.message.reply_text("❌ ကိန်းဂဏန်းထည့်ပါ")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    total_users = len(bot_data['users'])
    total_groups = len(bot_data['groups'])
    total_cards = len(bot_data['cards'])
    
    stats_text = (
        f"📊 Bot Statistics\n\n"
        f"👥 Total Users: {total_users}\n"
        f"💬 Total Groups: {total_groups}\n"
        f"🎴 Total Cards: {total_cards}\n\n"
        f"🔝 Top 5 Groups:\n"
    )
    
    sorted_groups = sorted(
        bot_data['groups'].items(),
        key=lambda x: x[1].get('message_count', 0),
        reverse=True
    )[:5]
    
    for i, (gid, gdata) in enumerate(sorted_groups, 1):
        stats_text += f"{i}. {gdata.get('title', 'Unknown')} - {gdata.get('message_count', 0)} msgs\n"
    
    await update.message.reply_text(stats_text)

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    try:
        with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(bot_data, f, ensure_ascii=False, indent=2)
        
        await update.message.reply_document(
            document=open(BACKUP_FILE, 'rb'),
            filename=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            caption="✅ Backup အောင်မြင်ပါသည်!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Backup Error: {str(e)}")

async def restore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    await update.message.reply_text("📥 Backup file ပို့ပါ")
    bot_data['pending_uploads'][str(update.effective_user.id)] = 'restore'
    save_data()

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if user_id in bot_data['pending_uploads'] and bot_data['pending_uploads'][user_id] == 'restore':
        try:
            file = await context.bot.get_file(update.message.document.file_id)
            await file.download_to_drive('temp_restore.json')
            
            with open('temp_restore.json', 'r', encoding='utf-8') as f:
                global bot_data
                bot_data = json.load(f)
            
            save_data()
            os.remove('temp_restore.json')
            
            del bot_data['pending_uploads'][user_id]
            save_data()
            
            await update.message.reply_text("✅ Data ပြန်ယူပြီး!")
        except Exception as e:
            await update.message.reply_text(f"❌ Restore Error: {str(e)}")

async def allclear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, Clear All", callback_data="clear_confirm"),
            InlineKeyboardButton("❌ Cancel", callback_data="clear_cancel")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚠️ သတိပေးချက်!\n\n"
        "Data အားလုံးဖျက်မှာသေချာပါသလား?\n"
        "ဒီလုပ်ဆောင်ချက်ကို နောက်ပြန်ပြင်၍မရပါ!",
        reply_markup=reply_markup
    )

# Owner Commands
async def add_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ User ကို Reply လုပ်ပါ")
        return
    
    new_sudo = update.message.reply_to_message.from_user.id
    
    if new_sudo not in bot_data['sudo_users']:
        bot_data['sudo_users'].append(new_sudo)
        save_data()
        await update.message.reply_text(f"✅ {update.message.reply_to_message.from_user.first_name} ကို Admin ခန့်ပြီး!")
    else:
        await update.message.reply_text("❌ ဤ user သည် Admin ဖြစ်နေပြီးဖြစ်သည်")

async def sudo_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    if not bot_data['sudo_users']:
        await update.message.reply_text("📋 Admin များမရှိသေးပါ")
        return
    
    sudo_text = "👥 Admin List:\n\n"
    for i, sudo_id in enumerate(bot_data['sudo_users'], 1):
        try:
            user = await context.bot.get_chat(sudo_id)
            sudo_text += f"{i}. {user.first_name} (ID: {sudo_id})\n"
        except:
            sudo_text += f"{i}. User ID: {sudo_id}\n"
    
    await update.message.reply_text(sudo_text)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    if len(context.args) == 0:
        await update.message.reply_text("❌ Format: /broadcast <message>")
        return
    
    message = ' '.join(context.args)
    success = 0
    failed = 0
    
    status_msg = await update.message.reply_text("📢 Broadcasting...")
    
    for group_id in bot_data['groups'].keys():
        try:
            await context.bot.send_message(chat_id=int(group_id), text=message)
            success += 1
        except:
            failed += 1
        await asyncio.sleep(0.05)  # Avoid flood limits
    
    await status_msg.edit_text(
        f"📢 Broadcast ပြီးပါပြီ!\n\n"
        f"✅ အောင်မြင်: {success}\n"
        f"❌ မအောင်မြင်: {failed}"
    )

# User Commands
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    user_balance = bot_data['users'][user_id]['balance']
    card_count = len(bot_data['users'][user_id]['cards'])
    
    await update.message.reply_text(
        f"💰 {update.effective_user.first_name} ၏ Account\n\n"
        f"💵 Balance: {user_balance:,} Coins\n"
        f"🎴 Cards: {card_count}"
    )

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    last_daily = bot_data['users'][user_id].get('last_daily')
    
    if last_daily:
        last_time = datetime.fromisoformat(last_daily)
        if datetime.now() - last_time < timedelta(hours=24):
            remaining = timedelta(hours=24) - (datetime.now() - last_time)
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            await update.message.reply_text(f"⏰ {hours}h {minutes}m ပြန်လာပါ!")
            return
    
    reward = random.randint(500, 1000)
    bot_data['users'][user_id]['balance'] += reward
    bot_data['users'][user_id]['last_daily'] = datetime.now().isoformat()
    save_data()
    
    await update.message.reply_text(f"🎁 Daily Bonus: +{reward:,} Coins!")

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    shop_text = "🏪 Shop\n\n"
    
    for i, (item_name, item_data) in enumerate(SHOP_ITEMS.items(), 1):
        shop_text += f"{i}. {item_name}\n   💰 {item_data['price']:,} Coins\n\n"
    
    shop_text += "📝 /buy <item_number> ဖြင့် ဝယ်ပါ"
    
    await update.message.reply_text(shop_text)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /buy <item_number>")
        return
    
    try:
        item_num = int(context.args[0]) - 1
        items_list = list(SHOP_ITEMS.items())
        
        if item_num < 0 or item_num >= len(items_list):
            await update.message.reply_text("❌ ပစ္စည်း နံပါတ် မှားနေပါသည်")
            return
        
        item_name, item_data = items_list[item_num]
        
        if bot_data['users'][user_id]['balance'] < item_data['price']:
            await update.message.reply_text("❌ Coins မလုံလောက်ပါ")
            return
        
        bot_data['users'][user_id]['balance'] -= item_data['price']
        
        if item_data['type'] == 'pack':
            cards_won = []
            for _ in range(5):
                if bot_data['cards']:
                    card_id = random.choice(list(bot_data['cards'].keys()))
                    card = bot_data['cards'][card_id]
                    
                    if card_id not in bot_data['users'][user_id]['cards']:
                        bot_data['users'][user_id]['cards'][card_id] = 0
                    bot_data['users'][user_id]['cards'][card_id] += 1
                    
                    cards_won.append(f"{RARITIES[card['rarity']]['emoji']} {card['name']}")
            
            save_data()
            await update.message.reply_text(
                f"🎁 Pack ဖွင့်ပြီး!\n\n" + "\n".join(cards_won)
            )
        else:
            if item_data['type'] not in bot_data['users'][user_id]['inventory']:
                bot_data['users'][user_id]['inventory'][item_data['type']] = 0
            bot_data['users'][user_id]['inventory'][item_data['type']] += 1
            save_data()
            
            await update.message.reply_text(f"✅ {item_name} ဝယ်ပြီး!")
            
    except ValueError:
        await update.message.reply_text("❌ နံပါတ် ထည့်ပါ")

# Games
async def slots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /slots <amount>")
        return
    
    try:
        bet = int(context.args[0])
        if bet <= 0:
            await update.message.reply_text("❌ ပမာဏ မှားနေပါသည်")
            return
        
        if bot_data['users'][user_id]['balance'] < bet:
            await update.message.reply_text("❌ Coins မလုံလောက်ပါ")
            return
        
        symbols = ['🍒', '🍋', '🍊', '🍇', '7️⃣']
        result = [random.choice(symbols) for _ in range(3)]
        
        if result[0] == result[1] == result[2]:
            if result[0] == '7️⃣':
                win = bet * 10
            else:
                win = bet * 3
            bot_data['users'][user_id]['balance'] += win
            save_data()
            await update.message.reply_text(
                f"🎰 {' '.join(result)}\n\n"
                f"🎉 သင်နိုင်ပြီ! +{win:,} Coins!"
            )
        else:
            bot_data['users'][user_id]['balance'] -= bet
            save_data()
            await update.message.reply_text(
                f"🎰 {' '.join(result)}\n\n"
                f"😢 ရှုံးပါသည်! -{bet:,} Coins"
            )
    except ValueError:
        await update.message.reply_text("❌ ကိန်းဂဏန်းထည့်ပါ")

async def basket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /basket <amount>")
        return
    
    try:
        bet = int(context.args[0])
        if bet <= 0 or bot_data['users'][user_id]['balance'] < bet:
            await update.message.reply_text("❌ ပမာဏ/Coins မှားနေပါသည်")
            return
        
        success = random.randint(0, 100) < 50
        
        if success:
            win = bet * 2
            bot_data['users'][user_id]['balance'] += win
            save_data()
            await update.message.reply_text(f"🏀 သွင်းပြီး! +{win:,} Coins!")
        else:
            bot_data['users'][user_id]['balance'] -= bet
            save_data()
            await update.message.reply_text(f"🏀 လွဲသွားပြီ! -{bet:,} Coins")
    except ValueError:
        await update.message.reply_text("❌ ကိန်းဂဏန်းထည့်ပါ")

async def wheel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /wheel <amount>")
        return
    
    try:
        bet = int(context.args[0])
        if bet <= 0 or bot_data['users'][user_id]['balance'] < bet:
            await update.message.reply_text("❌ ပမာဏ/Coins မှားနေပါသည်")
            return
        
        multipliers = [0, 0.5, 1, 1.5, 2, 3, 5, 10]
        multiplier = random.choice(multipliers)
        
        if multiplier == 0:
            bot_data['users'][user_id]['balance'] -= bet
            result_text = f"🎡 Wheel: 0x\n😢 ရှုံးပါသည်! -{bet:,} Coins"
        else:
            win = int(bet * multiplier)
            bot_data['users'][user_id]['balance'] += win - bet
            result_text = f"🎡 Wheel: {multiplier}x\n🎉 +{win:,} Coins!"
        
        save_data()
        await update.message.reply_text(result_text)
    except ValueError:
        await update.message.reply_text("❌ ကိန်းဂဏန်းထည့်ပါ")

# Card Drop System
async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        chat_id = str(update.effective_chat.id)
        init_group(update.effective_chat.id, update.effective_chat.title)
        
        bot_data['groups'][chat_id]['message_count'] += 1
        
        drop_threshold = bot_data['drop_settings'].get(chat_id, 50)
        
        if bot_data['groups'][chat_id]['message_count'] >= drop_threshold:
            bot_data['groups'][chat_id]['message_count'] = 0
            bot_data['groups'][chat_id]['last_drop'] = datetime.now().isoformat()
            save_data()
            
            if bot_data['cards']:
                # Random card drop
                card_id = random.choice(list(bot_data['cards'].keys()))
                card = bot_data['cards'][card_id]
                rarity_emoji = RARITIES[card['rarity']]['emoji']
                
                drop_text = (
                    f"🎴 ကဒ်ကျလာပြီ!\n\n"
                    f"{rarity_emoji} {card['name']}\n"
                    f"🎬 {card['movie']}\n\n"
                    f"📝 /catch {card['name']} ဖြင့် ဖမ်းပါ!"
                )
                
                if card['type'] == 'video':
                    await context.bot.send_video(
                        chat_id=update.effective_chat.id,
                        video=card['file_id'],
                        caption=drop_text
                    )
                else:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=card['file_id'],
                        caption=drop_text
                    )
                
                # Store last drop for catching
                context.chat_data['last_drop'] = {
                    'card_id': card_id,
                    'card_name': card['name'].lower(),
                    'time': datetime.now()
                }

async def catch_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    if 'last_drop' not in context.chat_data:
        await update.message.reply_text("❌ ဖမ်းရန် ကဒ်မရှိပါ")
        return
    
    if len(context.args) == 0:
        await update.message.reply_text("❌ Format: /catch <card_name>")
        return
    
    guess = ' '.join(context.args).lower()
    last_drop = context.chat_data['last_drop']
    
    # Check if drop expired (30 seconds)
    if datetime.now() - last_drop['time'] > timedelta(seconds=30):
        del context.chat_data['last_drop']
        await update.message.reply_text("⏰ Time Out!")
        return
    
    if guess == last_drop['card_name']:
        card_id = last_drop['card_id']
        card = bot_data['cards'][card_id]
        
        if card_id not in bot_data['users'][user_id]['cards']:
            bot_data['users'][user_id]['cards'][card_id] = 0
        bot_data['users'][user_id]['cards'][card_id] += 1
        
        # Bonus coins
        coin_bonus = RARITIES[card['rarity']]['value']
        bot_data['users'][user_id]['balance'] += coin_bonus
        
        # Check missions
        total_cards = sum(bot_data['users'][user_id]['cards'].values())
        for mission_id, mission in MISSIONS.items():
            if mission_id not in bot_data['users'][user_id]['completed_missions']:
                if total_cards >= mission['requirement']:
                    bot_data['users'][user_id]['completed_missions'].append(mission_id)
                    bot_data['users'][user_id]['balance'] += mission['reward']
                    bot_data['users'][user_id]['titles'].append(mission['title'])
                    await update.message.reply_text(
                        f"🏆 Mission Complete!\n\n"
                        f"{mission['title']} ရရှိပြီး!\n"
                        f"💰 Reward: {mission['reward']:,} Coins"
                    )
        
        save_data()
        del context.chat_data['last_drop']
        
        rarity_emoji = RARITIES[card['rarity']]['emoji']
        await update.message.reply_text(
            f"✅ {update.effective_user.first_name} ဖမ်းရပြီ!\n\n"
            f"{rarity_emoji} {card['name']}\n"
            f"💰 +{coin_bonus} Coins"
        )
    else:
        await update.message.reply_text("❌ နာမည် မှားနေပါသည်")

# Trading
async def give_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ User ကို Reply လုပ်ပါ")
        return
    
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /givecoin <amount>")
        return
    
    sender_id = str(update.effective_user.id)
    receiver_id = str(update.message.reply_to_message.from_user.id)
    
    init_user(update.effective_user.id, update.effective_user.username)
    init_user(update.message.reply_to_message.from_user.id, 
              update.message.reply_to_message.from_user.username)
    
    try:
        amount = int(context.args[0])
        
        if amount <= 0:
            await update.message.reply_text("❌ ပမာဏ မှားနေပါသည်")
            return
        
        if bot_data['users'][sender_id]['balance'] < amount:
            await update.message.reply_text("❌ Coins မလုံလောက်ပါ")
            return
        
        bot_data['users'][sender_id]['balance'] -= amount
        bot_data['users'][receiver_id]['balance'] += amount
        save_data()
        
        await update.message.reply_text(
            f"✅ {update.message.reply_to_message.from_user.first_name} သို့ "
            f"{amount:,} Coins လွှဲပြီး!"
        )
    except ValueError:
        await update.message.reply_text("❌ ကိန်းဂဏန်းထည့်ပါ")

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ User ကို Reply လုပ်ပါ")
        return
    
    await update.message.reply_text("🔄 Trade system ကို မကြာမီ ထည့်သွင်းပါမည်")

async def fusion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚗️ Fusion system ကို မကြာမီ ထည့်သွင်းပါမည်")

async def duel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚔️ Duel system ကို မကြာမီ ထည့်သွင်းပါမည်")

# Social
async def marry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ User ကို Reply လုပ်ပါ")
        return
    
    user_id = str(update.effective_user.id)
    partner_id = str(update.message.reply_to_message.from_user.id)
    
    init_user(update.effective_user.id, update.effective_user.username)
    init_user(update.message.reply_to_message.from_user.id,
              update.message.reply_to_message.from_user.username)
    
    if bot_data['users'][user_id]['married_to']:
        await update.message.reply_text("❌ သင်လက်ထပ်ပြီးသားဖြစ်သည်")
        return
    
    if bot_data['users'][partner_id]['married_to']:
        await update.message.reply_text("❌ ဤ user လက်ထပ်ပြီးသားဖြစ်သည်")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("💍 Accept", callback_data=f"marry_accept_{user_id}"),
            InlineKeyboardButton("❌ Decline", callback_data="marry_decline")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"💝 {update.effective_user.first_name} က "
        f"{update.message.reply_to_message.from_user.first_name} ကို "
        f"လက်ထပ်ချင်နေပါသည်!",
        reply_markup=reply_markup
    )

async def divorce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    if not bot_data['users'][user_id]['married_to']:
        await update.message.reply_text("❌ သင်လက်ထပ်ထားခြင်းမရှိပါ")
        return
    
    partner_id = bot_data['users'][user_id]['married_to']
    bot_data['users'][user_id]['married_to'] = None
    bot_data['users'][partner_id]['married_to'] = None
    save_data()
    
    await update.message.reply_text("💔 ကွာရှင်းပြီးပါပြီ")

# Rankings
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_users = sorted(
        bot_data['users'].items(),
        key=lambda x: sum(x[1].get('cards', {}).values()),
        reverse=True
    )[:10]
    
    top_text = "🏆 Top 10 Collectors\n\n"
    
    for i, (uid, udata) in enumerate(sorted_users, 1):
        card_count = sum(udata.get('cards', {}).values())
        username = udata.get('username', 'Unknown')
        titles = ' '.join(udata.get('titles', []))
        top_text += f"{i}. {username} {titles}\n   🎴 {card_count} cards\n\n"
    
    await update.message.reply_text(top_text)

async def titles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    user_titles = bot_data['users'][user_id].get('titles', [])
    
    if not user_titles:
        await update.message.reply_text("❌ ဘွဲ့များမရှိသေးပါ")
        return
    
    titles_text = f"👑 {update.effective_user.first_name} ၏ ဘွဲ့များ\n\n"
    titles_text += '\n'.join(user_titles)
    
    await update.message.reply_text(titles_text)

async def missions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    total_cards = sum(bot_data['users'][user_id].get('cards', {}).values())
    completed = bot_data['users'][user_id].get('completed_missions', [])
    
    missions_text = "🎯 Missions\n\n"
    
    for mission_id, mission in MISSIONS.items():
        status = "✅" if mission_id in completed else "⏳"
        progress = min(total_cards, mission['requirement'])
        missions_text += (
            f"{status} {mission['name']}\n"
            f"   📊 {progress}/{mission['requirement']} cards\n"
            f"   🎁 {mission['reward']:,} Coins + {mission['title']}\n\n"
        )
    
    await update.message.reply_text(missions_text)

async def set_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /set <card_id>")
        return
    
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    card_id = context.args[0]
    
    if card_id not in bot_data['users'][user_id].get('cards', {}):
        await update.message.reply_text("❌ သင့်တွင် ဤကဒ်မရှိပါ")
        return
    
    if len(bot_data['users'][user_id]['favorite_cards']) >= 5:
        await update.message.reply_text("❌ Favorite ကဒ် 5 ခုအပြည့်ရှိနေပြီ")
        return
    
    if card_id not in bot_data['users'][user_id]['favorite_cards']:
        bot_data['users'][user_id]['favorite_cards'].append(card_id)
        save_data()
        await update.message.reply_text("✅ Favorite ကဒ်အဖြစ်သတ်မှတ်ပြီး!")
    else:
        await update.message.reply_text("❌ ဤကဒ်သည် Favorite တွင်ရှိပြီးသား")

async def remove_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /removeset <card_id>")
        return
    
    user_id = str(update.effective_user.id)
    init_user(update.effective_user.id, update.effective_user.username)
    
    card_id = context.args[0]
    
    if card_id in bot_data['users'][user_id]['favorite_cards']:
        bot_data['users'][user_id]['favorite_cards'].remove(card_id)
        save_data()
        await update.message.reply_text("✅ Favorite မှ ဖယ်ရှားပြီး!")
    else:
        await update.message.reply_text("❌ ဤကဒ်သည် Favorite တွင်မရှိပါ")

# Callback handlers
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "clear_confirm":
        global bot_data
        bot_data = {
            'cards': {},
            'users': {},
            'groups': {},
            'sudo_users': [],
            'drop_settings': {},
            'pending_uploads': {},
            'pending_trades': {},
            'pending_duels': {},
            'pending_fusions': {}
        }
        save_data()
        await query.edit_message_text("✅ Data အားလုံးဖျက်ပြီးပါပြီ!")
    
    elif data == "clear_cancel":
        await query.edit_message_text("❌ ဖျက်ခြင်းကို ပယ်ဖျက်ပြီးပါပြီ")
    
    elif data.startswith("marry_accept_"):
        sender_id = data.split("_")[2]
        receiver_id = str(query.from_user.id)
        
        bot_data['users'][sender_id]['married_to'] = receiver_id
        bot_data['users'][receiver_id]['married_to'] = sender_id
        save_data()
        
        await query.edit_message_text("💍 လက်ထပ်ပြီးပါပြီ! ဂုဏ်ယူပါတယ်!")
    
    elif data == "marry_decline":
        await query.edit_message_text("💔 လက်မထပ်ပါ")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_user(user_id, update.effective_user.username)
    
    welcome_text = (
        f"👋 မင်္ဂလာပါ {update.effective_user.first_name}!\n\n"
        f"🎴 Card Collection Bot မှ ကြိုဆိုပါသည်\n\n"
        f"📝 /help - Command များကြည့်ရန်\n"
        f"💰 /balance - လက်ကျန်ငွေ\n"
        f"🎁 /daily - နေ့စဉ် Bonus\n"
        f"🏪 /shop - ဆိုင်ကြည့်ရန်"
    )
    
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🎴 Card Collection Bot Commands

👤 User Commands:
💰 /balance - လက်ကျန်ငွေစစ်ရန်
🎁 /daily - နေ့စဉ် Bonus
🏪 /shop - ဆိုင်ဖွင့်ရန်
🛒 /buy <number> - ပစ္စည်းဝယ်ရန်

🎮 Games:
🎰 /slots <amount> - Slot ကစားရန်
🏀 /basket <amount> - Basketball
🎡 /wheel <amount> - Wheel ကစားရန်

🎴 Cards:
📥 /catch <name> - ကဒ်ဖမ်းရန်
⭐ /set <id> - Favorite သတ်မှတ်ရန်
❌ /removeset <id> - Favorite ဖယ်ရန်

👥 Social:
💵 /givecoin <amount> - Coin လွှဲရန်
💍 /marry - လက်ထပ်ရန် (Reply)
💔 /divorce - ကွာရှင်းရန်

📊 Rankings:
🏆 /top - Top 10 ကြည့်ရန်
👑 /titles - ဘွဲ့များ
🎯 /missions - Mission များ
"""
    
    if is_sudo(update.effective_user.id):
        help_text += """
🛠 Admin Commands:
📤 /upload - ကဒ်တင်ရန်
📹 /uploadvd - Video ကဒ်
✏️ /edit <id> <name> <movie>
🗑 /delete <id>
⚙️ /setdrop <number>
📊 /stats
💾 /backup
📥 /restore
"""
    
    if update.effective_user.id == OWNER_ID:
        help_text += """
👑 Owner Commands:
👤 /addsudo (Reply)
📋 /sudolist
📢 /broadcast <message>
🗑 /allclear
"""
    
    await update.message.reply_text(help_text)

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception: {context.error}")

# Main function
def main():
    # Load data on startup
    load_data()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Admin commands
    application.add_handler(CommandHandler("upload", upload_card))
    application.add_handler(CommandHandler("uploadvd", upload_video))
    application.add_handler(CommandHandler("edit", edit_card))
    application.add_handler(CommandHandler("delete", delete_card))
    application.add_handler(CommandHandler("setdrop", set_drop))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("backup", backup))
    application.add_handler(CommandHandler("restore", restore))
    application.add_handler(CommandHandler("allclear", allclear))
    
    # Owner commands
    application.add_handler(CommandHandler("addsudo", add_sudo))
    application.add_handler(CommandHandler("sudolist", sudo_list))
    application.add_handler(CommandHandler("broadcast", broadcast))
    
    # User commands
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CommandHandler("buy", buy))
    
    # Games
    application.add_handler(CommandHandler("slots", slots))
    application.add_handler(CommandHandler("basket", basket))
    application.add_handler(CommandHandler("wheel", wheel))
    
    # Cards
    application.add_handler(CommandHandler("catch", catch_card))
    application.add_handler(CommandHandler("set", set_favorite))
    application.add_handler(CommandHandler("removeset", remove_favorite))
    
    # Social
    application.add_handler(CommandHandler("givecoin", give_coin))
    application.add_handler(CommandHandler("trade", trade))
    application.add_handler(CommandHandler("fusion", fusion))
    application.add_handler(CommandHandler("duel", duel))
    application.add_handler(CommandHandler("marry", marry))
    application.add_handler(CommandHandler("divorce", divorce))
    
    # Rankings
    application.add_handler(CommandHandler("top", top))
    application.add_handler(CommandHandler("titles", titles))
    application.add_handler(CommandHandler("missions", missions))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP),
        handle_group_message
    ))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
