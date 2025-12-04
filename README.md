# 🤖 Telegram Broadcasting Bot

A powerful and user-friendly Telegram bot for broadcasting messages to multiple groups and channels simultaneously. Features a modern UI with step-by-step post creation wizard.

## ✨ Features

- 📡 **Broadcast to Multiple Chats**: Send messages to all your groups and channels at once
- 🎨 **Modern Post Templates**: Create rich posts with images, titles, descriptions, and buttons
- 🔄 **Automatic Chat Tracking**: Bot automatically tracks all groups/channels it's added to
- 📊 **Detailed Statistics**: Get success/failure reports after each broadcast
- 💬 **Interactive UI**: Step-by-step wizard with inline buttons and smart navigation
- ✅ **Admin Verification**: Only sends to chats where bot has admin rights
- 🎯 **Skip Optional Fields**: Flexible post creation - only title is required
- 🔗 **Custom Call-to-Action**: Add clickable buttons with URLs
- 📝 **Preview Before Send**: Review your post before broadcasting

## 🚀 Commands

- `/start` - Welcome message and main menu
- `/newpost` - Create and broadcast a new post
- `/listchats` - View all groups/channels the bot is in
- `/help` - Detailed help information

## 📋 Prerequisites

- Python 3.11 or higher
- A Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- pip (Python package manager)

## 🛠️ Installation

### 1. Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Send `/setjoingroups` to BotFather and enable group access
6. Send `/setprivacy` to BotFather and disable privacy mode

### 2. Clone or Download

```bash
git clone <your-repo-url>
cd Cybot-Telegram
```

Or download and extract the ZIP file.

### 3. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env file and add your bot token
# Replace 'your_bot_token_here' with your actual token
nano .env  # or use any text editor
```

Your `.env` file should look like:

```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 5. Run the Bot

```bash
python bot.py
```

You should see: `Bot started successfully!`

## 📱 Usage Guide

### Setting Up Chats

1. **Add bot to your groups/channels**

   - Open your group or channel
   - Add the bot as a member
   - Promote to admin with posting permissions

2. **Bot will automatically track the chat**
   - You'll receive a confirmation message
   - Use `/listchats` to see all tracked chats

### Creating a Broadcast

1. **Start the wizard**
   - Send `/newpost` or use the menu button
2. **Step 1: Upload Image (Optional)**
   - Send an image or skip
   - Supported: JPG, PNG, GIF
3. **Step 2: Enter Title (Required)**
   - Type your post title
   - Max 200 characters
   - Can include emojis
4. **Step 3: Add Description (Optional)**
   - Type detailed description
   - Max 1000 characters
   - Supports line breaks
5. **Step 4: Add Button (Optional)**
   - Format: `URL | Button Text`
   - Example: `https://t.me/channel | Join Now`
6. **Preview & Send**
   - Review your post
   - Click "Send Broadcast"
   - Get detailed statistics

### Tips & Best Practices

- ✅ Always preview before sending
- ✅ Use emojis to make posts engaging
- ✅ Keep titles short and catchy
- ✅ Test with a small group first
- ✅ Ensure bot has admin rights
- ✅ Use descriptive button text

## 🌐 Deployment

### Deploy to Render.com (Recommended - Free)

1. **Create Render Account**

   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**

   - Click "New +"
   - Select "Web Service"
   - Connect your repository

3. **Configure Service**

   - Name: `telegram-bot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`

4. **Add Environment Variable**

   - Go to "Environment"
   - Add: `BOT_TOKEN` = `your_token_here`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### Deploy to Railway.app

1. **Create Railway Account**

   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **New Project**

   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add Environment Variables**

   - Go to "Variables"
   - Add: `BOT_TOKEN` = `your_token_here`

4. **Deploy**
   - Railway will auto-deploy using Procfile

### Deploy to Heroku

1. **Install Heroku CLI**

   ```bash
   # Install from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**

   ```bash
   heroku login
   heroku create your-bot-name
   ```

3. **Set Environment Variables**

   ```bash
   heroku config:set BOT_TOKEN=your_token_here
   ```

4. **Deploy**
   ```bash
   git push heroku main
   heroku ps:scale worker=1
   ```

## 📁 File Structure

```
Cybot-Telegram/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create from .env.example)
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
├── Procfile           # Deployment configuration
├── render.yaml        # Render.com configuration
├── README.md          # This file
└── bot_chats.json     # Auto-generated chat storage
```

## 🔧 Configuration

### Environment Variables

- `BOT_TOKEN` (Required) - Your Telegram bot token from BotFather

### Chat Storage

- Chats are automatically stored in `bot_chats.json`
- File is created automatically on first use
- Contains chat IDs, titles, and types
- Backed up automatically

## 🐛 Troubleshooting

### Bot doesn't respond

- Check if bot is running: `python bot.py`
- Verify token is correct in `.env` file
- Check bot privacy settings with BotFather

### Can't send to groups

- Ensure bot is admin in the group
- Check bot has "Post Messages" permission
- Verify group is listed in `/listchats`

### Image upload fails

- Check file size (max 10MB for Telegram)
- Ensure format is JPG, PNG, or GIF
- Try compressing the image

### Broadcast fails

- Verify bot is admin in target chats
- Check chat IDs are valid
- Review error messages in statistics

### Common Errors

**"BOT_TOKEN environment variable not set!"**

- Create `.env` file from `.env.example`
- Add your bot token

**"Failed to send to [chat]"**

- Bot may not be admin
- Chat may have been deleted
- Bot may have been removed

**"Invalid URL format"**

- URL must start with http:// or https://
- Use format: `URL | Button Text`

## 📊 Features in Detail

### Smart Chat Tracking

- Automatically detects when added to groups
- Tracks group/channel information
- Removes chats when bot is removed
- Persistent storage across restarts

### Rich Post Creation

- **Images**: Upload photos for visual appeal
- **Titles**: Bold, attention-grabbing headlines
- **Descriptions**: Detailed information with formatting
- **Buttons**: Call-to-action with custom URLs

### Broadcast Intelligence

- Admin verification before sending
- Detailed success/failure statistics
- Error handling for each chat
- Progress indicators

### Modern UI/UX

- Inline keyboard navigation
- Step-by-step wizard
- Skip optional steps
- Cancel anytime
- Clear visual feedback

## 🔒 Security & Privacy

- Bot token stored securely in environment variables
- Only chat IDs and titles are stored
- No message content is logged
- Admin-only broadcasting
- Open source and transparent

## 📝 Development

### Project Structure

```python
bot.py
├── ChatStorage class      # Handles chat persistence
├── Command handlers       # /start, /help, /listchats
├── Conversation handlers  # Post creation wizard
├── Callback handlers      # Button interactions
└── Event handlers        # Chat tracking
```

### Adding New Features

1. Add handler function
2. Register with application
3. Update help text
4. Test thoroughly

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Handle exceptions
- Log important events

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

- Create an issue on GitHub
- Check existing issues for solutions
- Read the troubleshooting section
- Review Telegram Bot API docs

## 🎉 Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Telegram Bot API by Telegram

## 📈 Roadmap

Future enhancements:

- [ ] Scheduled broadcasts
- [ ] User targeting (specific groups)
- [ ] Analytics dashboard
- [ ] Multiple bot token support
- [ ] Web interface
- [ ] Message templates library
- [ ] Database support (PostgreSQL)

## 🔄 Updates

### Version 1.0.0 (Current)

- Initial MVP release
- Core broadcasting functionality
- Template system
- Auto chat tracking
- Modern UI

---

Made with ❤️ for the Telegram community

**Happy Broadcasting! 🚀**
