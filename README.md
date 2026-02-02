# VFrost Discord Bot

A feature-rich Discord bot optimized for low-memory environments, providing moderation tools, leveling system, ticketing, and fun commands.

## Features

### 🛡️ Moderation
- **Ban/Kick/Unban**: Standard moderation actions with reason logging
- **Warning System**: Issue and track warnings with persistent storage
- **Timeout/Mute**: Temporary member timeouts
- **Message Management**: Bulk delete messages, channel locking, and slowmode
- **Channel Nuke**: Quick channel recreation
- **Nickname Management**: Change member nicknames

### 📈 Leveling System
- **XP Tracking**: Automatic XP gain from user activity
- **Rank Display**: View user level and progress
- **Leaderboard**: Top 10 server members by XP

### 🎫 Ticket System
- **Ticket Setup**: Admin-configurable ticket system
- **Ticket Management**: Close tickets with proper cleanup

### 🎮 Fun Commands
- **Dice Rolling**: Roll custom dice (e.g., 2d20)
- **Coin Flip**: Heads or tails
- **Magic 8-Ball**: Get mystical answers
- **Reddit Memes**: Fetch random memes
- **Interactions**: Slap and hug other members

### 🛠️ Utility
- **Ping**: Check bot latency
- **Uptime**: View bot runtime and platform info
- **Server Info**: Detailed server statistics
- **User Info**: Member information and details
- **Avatar**: Display user profile pictures

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MocLG/VFrost.git
   cd VFrost
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   
   Create a `.env` file in the root directory:
   ```env
   TOKEN=your_discord_bot_token_here
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables
- `TOKEN`: Your Discord bot token (required)

### Bot Permissions
The bot requires the following Discord permissions:
- Manage Messages
- Manage Channels
- Manage Roles
- Ban Members
- Kick Members
- Moderate Members (for timeouts)
- Send Messages
- Embed Links
- Attach Files
- Read Message History
- Use External Emojis

### Invite Link
Generate an invite link from the Discord Developer Portal with the required permissions and Administrator scope for full functionality.

## Usage

The bot uses the command prefix `?`. Type `?help` in any channel to see the full command list.

### Example Commands
```
?help              - Display the help menu
?ban @user spam    - Ban a user for spam
?rank              - Check your level and XP
?roll 2d20         - Roll two 20-sided dice
?serverinfo        - View server information
?setup_tickets     - Set up the ticket system (Admin only)
```

## Technical Details

### Memory Optimization
VFrost is specifically optimized for environments with limited RAM (as low as 128MB):
- Member cache disabled
- Message cache limited to 50 messages
- Guild chunking disabled at startup
- Presence intents disabled

### Database
Uses SQLite (`bot.db`) for persistent storage:
- Warning system logs
- User XP and levels
- Lightweight and serverless

### Architecture
- Built with `discord.py`
- Modular cog-based structure
- Async/await for efficient I/O operations

## Project Structure

```
VFrost/
├── main.py              # Bot initialization and startup
├── requirements.txt     # Python dependencies
├── cogs/               # Command modules
│   ├── moderation.py   # Moderation commands
│   ├── levels.py       # Leveling system
│   ├── tickets.py      # Ticket system
│   ├── fun.py          # Fun commands
│   ├── utility.py      # Utility commands
│   ├── help.py         # Help command
│   └── logging.py      # Event logging
├── .env                # Environment configuration (create this)
└── bot.db              # SQLite database (auto-generated)
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available for personal and educational use.

## Credits

Developed by MocLG

## Support

For issues or questions, please open an issue on the GitHub repository.
