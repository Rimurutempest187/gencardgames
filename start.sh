#!/bin/bash

echo "🎴 Starting Card Collection Bot..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please run install.sh first"
    exit 1
fi

# Check if dependencies are installed
python3 -c "import telegram" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Dependencies not installed!"
    echo "Please run: pip3 install -r requirements.txt"
    exit 1
fi

# Start the bot
echo "✅ Starting bot..."
echo ""
python3 bot.py
