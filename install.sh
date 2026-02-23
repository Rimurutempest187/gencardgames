#!/bin/bash

echo "🎴 Card Collection Bot Installer"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Check .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Please create .env file with:"
    echo "BOT_TOKEN=your_bot_token"
    echo "OWNER_ID=your_user_id"
    exit 1
fi

echo "✅ Configuration file found"
echo ""

# Check if BOT_TOKEN is set
source .env
if [ -z "$BOT_TOKEN" ] || [ "$BOT_TOKEN" = "your_bot_token_here" ]; then
    echo "❌ BOT_TOKEN is not configured!"
    echo "Please edit .env file and add your bot token"
    exit 1
fi

if [ -z "$OWNER_ID" ] || [ "$OWNER_ID" = "your_telegram_user_id_here" ]; then
    echo "❌ OWNER_ID is not configured!"
    echo "Please edit .env file and add your Telegram user ID"
    exit 1
fi

echo "✅ Bot configuration is complete"
echo ""
echo "🚀 Installation complete!"
echo ""
echo "To start the bot, run:"
echo "  python3 bot.py"
echo ""
echo "Or use the start script:"
echo "  ./start.sh"
