# Card Collection Bot - Documentation

## 📚 Detailed Documentation

### Bot Architecture

The bot is built using:
- **python-telegram-bot** library (version 20.7)
- **JSON-based data storage** for simplicity and portability
- **Asynchronous handlers** for better performance

### Data Structure

```json
{
  "cards": {
    "card_id": {
      "name": "Character Name",
      "movie": "Movie/Anime Name",
      "rarity": "Legendary",
      "file_id": "telegram_file_id",
      "type": "image|video",
      "created_at": "ISO timestamp"
    }
  },
  "users": {
    "user_id": {
      "username": "telegram_username",
      "cards": {"card_id": count},
      "balance": 1000,
      "last_daily": "ISO timestamp",
      "favorite_cards": ["card_id"],
      "titles": ["🎴 Collector"],
      "married_to": "user_id|null",
      "inventory": {"item_type": count},
      "completed_missions": ["mission_id"]
    }
  },
  "groups": {
    "group_id": {
      "title": "Group Name",
      "message_count": 0,
      "last_drop": "ISO timestamp"
    }
  },
  "sudo_users": [user_id],
  "drop_settings": {"group_id": message_count}
}
```

### Card Drop Mechanism

1. **Message Counting**: Every message in a group increments the counter
2. **Drop Threshold**: When counter reaches the set threshold (default: 50)
3. **Random Selection**: A random card is selected from the database
4. **Drop Announcement**: Card is posted with image/video
5. **Catch Window**: Users have 30 seconds to catch the card
6. **First Come First Served**: First correct `/catch` wins the card

### Rarity Probabilities

The rarity system uses weighted random selection:

```python
Total: 100%
Common:    40% (cumulative: 40%)
Rare:      25% (cumulative: 65%)
Epic:      15% (cumulative: 80%)
Legendary: 10% (cumulative: 90%)
Mythic:     5% (cumulative: 95%)
Divine:     3% (cumulative: 98%)
Celestial:  1.5% (cumulative: 99.5%)
Supreme:    0.4% (cumulative: 99.9%)
Animated:   0.1% (cumulative: 100%)
```

### Game Mechanics

**Slots Game:**
- 3 random symbols: 🍒 🍋 🍊 🍇 7️⃣
- Match all 3: win 3x bet (10x for triple 7️⃣)
- Otherwise: lose bet

**Basketball Game:**
- 50% chance to win
- Win: 2x bet
- Lose: lose bet

**Wheel Game:**
- Random multipliers: 0x, 0.5x, 1x, 1.5x, 2x, 3x, 5x, 10x
- Winnings = bet × multiplier
- 0x = lose entire bet

### Mission System

Missions automatically complete when requirements are met:

1. **Check on card catch**: Every time a user catches a card
2. **Count total cards**: Sum all cards in user's collection
3. **Compare requirements**: Check against mission thresholds
4. **Auto-complete**: Reward coins and titles automatically
5. **One-time only**: Each mission can only be completed once

### Trading System (Placeholder)

The trading system is designed but not fully implemented. Planned features:

- Trade cards with other users
- Accept/decline trades
- Trade history
- Fair trade validation

### Fusion System (Placeholder)

Planned features:
- Combine duplicate cards
- Upgrade rarity
- Special fusion recipes
- Rare fusion outcomes

### Marriage System

Users can marry each other:
1. User A replies to User B and uses `/marry`
2. User B receives proposal with Accept/Decline buttons
3. On acceptance, both users are marked as married
4. Benefits: shared bonuses, couple titles (future feature)
5. `/divorce` to end marriage

### Admin Workflow

**Adding Cards:**
```
1. Admin: /upload or /uploadvd
2. Bot: Prompts for image/video
3. Admin: Sends media with caption
4. Bot: Validates format and rarity
5. Bot: Creates card entry
6. Bot: Confirms with card details
```

**Managing Drops:**
```
1. Admin: /setdrop 50
2. Bot: Sets drop threshold for current group
3. Group: Messages trigger counter
4. Bot: Drops card when threshold reached
5. Bot: Resets counter
```

**Backup/Restore:**
```
Backup:
1. Admin: /backup
2. Bot: Creates JSON backup
3. Bot: Sends file with timestamp

Restore:
1. Admin: /restore
2. Bot: Prompts for file
3. Admin: Sends backup JSON
4. Bot: Validates and loads data
5. Bot: Confirms restoration
```

### Security Features

1. **Owner-only commands**: Only OWNER_ID can use critical commands
2. **Sudo system**: Owner can add trusted admins
3. **Confirmation dialogs**: Critical operations require confirmation
4. **Data validation**: All inputs are validated
5. **Error handling**: Graceful error recovery

### Performance Optimization

1. **Asynchronous operations**: Non-blocking I/O
2. **Lazy loading**: Data loaded only when needed
3. **Efficient data structures**: JSON for fast read/write
4. **Message throttling**: Broadcast with delays to avoid flood limits
5. **Memory management**: Periodic cleanup of old data

### Error Handling

The bot includes comprehensive error handling:

- **Connection errors**: Automatic retry
- **Invalid commands**: User-friendly error messages
- **Missing data**: Graceful degradation
- **File errors**: Backup preservation
- **API limits**: Rate limiting and queuing

### Scalability Considerations

For large-scale deployment:

1. **Database**: Migrate to PostgreSQL or MongoDB
2. **Caching**: Implement Redis for session data
3. **Queue system**: Use Celery for background tasks
4. **Load balancing**: Multiple bot instances
5. **CDN**: Store media files in cloud storage

### Customization

**Adding new rarities:**
```python
RARITIES = {
    'YourRarity': {
        'emoji': '🌟',
        'value': 5000,
        'drop_chance': 0.05
    }
}
```

**Adding shop items:**
```python
SHOP_ITEMS = {
    '🎁 Item Name': {
        'price': 1000,
        'type': 'item_type'
    }
}
```

**Adding missions:**
```python
MISSIONS = {
    'mission_id': {
        'name': 'Mission Name',
        'requirement': 1000,
        'reward': 50000,
        'title': '🌟 Title'
    }
}
```

### Deployment

**Local Deployment:**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env
nano .env

# Run bot
python bot.py
```

**Server Deployment (Linux):**
```bash
# Install Python 3
sudo apt update
sudo apt install python3 python3-pip

# Clone/upload files
cd /opt
mkdir card_bot
cd card_bot

# Install dependencies
pip3 install -r requirements.txt

# Configure
nano .env

# Run with nohup
nohup python3 bot.py &

# Or use systemd service
sudo nano /etc/systemd/system/cardbot.service
```

**Systemd Service Example:**
```ini
[Unit]
Description=Card Collection Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/opt/card_bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Docker Deployment:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

### Monitoring

**Logs:**
- Bot uses Python logging module
- Check console output for errors
- Redirect to file: `python bot.py > bot.log 2>&1`

**Statistics:**
- Use `/stats` command for overview
- Monitor user growth
- Track card collection rates
- Analyze game usage

### Maintenance

**Regular tasks:**
1. **Daily**: Check logs for errors
2. **Weekly**: Create backups with `/backup`
3. **Monthly**: Review and clean old data
4. **Quarterly**: Update dependencies

**Troubleshooting:**
1. Check bot token validity
2. Verify network connectivity
3. Review recent code changes
4. Check Telegram API status
5. Review error logs

### Future Enhancements

Planned features:
- [ ] Complete trading system
- [ ] Fusion mechanics
- [ ] Duel battles with cards
- [ ] Leaderboard rankings
- [ ] Seasonal events
- [ ] Card abilities and stats
- [ ] Guild/team system
- [ ] Achievement system
- [ ] Premium features
- [ ] Multi-language support

### Contributing

To contribute:
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

### Support

For help:
- Check README.md first
- Review this documentation
- Check error messages
- Test in isolation
- Ask community

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Author**: Card Collection Bot Team
