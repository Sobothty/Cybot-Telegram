#!/usr/bin/env python3
"""
Telegram Broadcasting Bot MVP
A complete bot for broadcasting messages to multiple groups and channels.
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatMember,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    ChatMemberHandler,
    filters,
)
from telegram.constants import ParseMode, ChatType

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
SELECTING_ACTION, UPLOADING_IMAGE, ENTERING_TITLE, ENTERING_DESCRIPTION, ENTERING_URL, PREVIEW = range(6)

# File to store chat IDs
CHATS_FILE = 'bot_chats.json'


class ChatStorage:
    """Handles persistent storage of chat IDs."""
    
    def __init__(self, filename: str = CHATS_FILE):
        """Initialize chat storage."""
        self.filename = filename
        self.chats = self._load_chats()
    
    def _load_chats(self) -> Dict:
        """Load chats from JSON file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading chats: {e}")
        return {}
    
    def _save_chats(self) -> None:
        """Save chats to JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.chats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving chats: {e}")
    
    def add_chat(self, chat_id: int, chat_title: str, chat_type: str) -> None:
        """Add or update a chat in storage."""
        self.chats[str(chat_id)] = {
            'title': chat_title,
            'type': chat_type,
            'added_at': datetime.now().isoformat()
        }
        self._save_chats()
        logger.info(f"Added chat: {chat_title} ({chat_id})")
    
    def remove_chat(self, chat_id: int) -> None:
        """Remove a chat from storage."""
        chat_id_str = str(chat_id)
        if chat_id_str in self.chats:
            del self.chats[chat_id_str]
            self._save_chats()
            logger.info(f"Removed chat: {chat_id}")
    
    def get_all_chats(self) -> Dict:
        """Get all stored chats."""
        return self.chats
    
    def get_chat_count(self) -> int:
        """Get total number of chats."""
        return len(self.chats)


# Initialize chat storage
chat_storage = ChatStorage()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    
    welcome_message = (
        f"👋 <b>Welcome {user.first_name}!</b>\n\n"
        f"🤖 I'm your <b>Broadcasting Bot</b> - designed to help you send messages "
        f"to multiple groups and channels efficiently.\n\n"
        f"<b>📋 Available Commands:</b>\n"
        f"• /newpost - Create and broadcast a new post\n"
        f"• /listchats - View all groups/channels I'm in\n"
        f"• /help - Get detailed help information\n\n"
        f"<b>🚀 Quick Start:</b>\n"
        f"1️⃣ Add me to your groups/channels as an admin\n"
        f"2️⃣ Use /newpost to create your first broadcast\n"
        f"3️⃣ Follow the step-by-step wizard to create your message\n\n"
        f"💡 <b>Tip:</b> I automatically track all groups where I'm added as admin!\n\n"
        f"Ready to get started? Type /newpost to create your first broadcast! 🎯"
    )
    
    keyboard = [
        [InlineKeyboardButton("📝 Create New Post", callback_data='cmd_newpost')],
        [InlineKeyboardButton("📋 List Chats", callback_data='cmd_listchats')],
        [InlineKeyboardButton("❓ Help", callback_data='cmd_help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = (
        "🆘 <b>Broadcasting Bot - Help Guide</b>\n\n"
        "<b>📝 Creating a Broadcast Post:</b>\n"
        "Use /newpost to start the post creation wizard. You'll be guided through:\n"
        "• 🖼️ Image Upload (optional)\n"
        "• 📌 Title (required)\n"
        "• 📄 Description (optional)\n"
        "• 🔗 URL with button (optional)\n\n"
        "<b>💬 Managing Chats:</b>\n"
        "• Add me to groups/channels as an admin\n"
        "• I automatically track all chats\n"
        "• Use /listchats to see where I'm active\n\n"
        "<b>📡 Broadcasting:</b>\n"
        "• Posts are sent to ALL groups/channels\n"
        "• Preview before sending\n"
        "• Get detailed success/failure statistics\n"
        "• Only sends to chats where I'm admin\n\n"
        "<b>⚡ Tips:</b>\n"
        "• Use the 'Skip' button for optional fields\n"
        "• Use 'Cancel' anytime to stop\n"
        "• Preview your post before broadcasting\n"
        "• URLs are automatically validated\n\n"
        "<b>🔒 Privacy:</b>\n"
        "• I only store chat IDs and titles\n"
        "• No message content is stored\n"
        "• You have full control\n\n"
        "Need more help? Contact the bot administrator! 💬"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='cmd_start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(help_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(help_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


async def list_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /listchats command."""
    chats = chat_storage.get_all_chats()
    
    if not chats:
        message = (
            "📭 <b>No Chats Found</b>\n\n"
            "I'm not in any groups or channels yet.\n\n"
            "<b>To get started:</b>\n"
            "1️⃣ Add me to your group/channel\n"
            "2️⃣ Make me an admin\n"
            "3️⃣ I'll automatically track it!\n\n"
            "💡 After adding me, use /listchats again to see the updated list."
        )
    else:
        chat_list = []
        for chat_id, chat_info in chats.items():
            emoji = "👥" if chat_info['type'] == 'group' or chat_info['type'] == 'supergroup' else "📢"
            chat_list.append(f"{emoji} <b>{chat_info['title']}</b>\n   └ Type: {chat_info['type']}\n   └ ID: <code>{chat_id}</code>")
        
        message = (
            f"📋 <b>Active Chats ({len(chats)})</b>\n\n"
            + "\n\n".join(chat_list) +
            "\n\n✅ All these chats will receive your broadcasts!"
        )
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='cmd_start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


async def new_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the new post creation wizard."""
    # Initialize post data
    context.user_data['post'] = {
        'image': None,
        'title': None,
        'description': None,
        'url': None,
        'button_text': None
    }
    
    message = (
        "📝 <b>Create New Broadcast Post</b>\n\n"
        "Let's create an amazing post! I'll guide you through each step.\n\n"
        "<b>Step 1/4: Image Upload</b> 🖼️\n\n"
        "Send me an image for your post, or skip this step.\n\n"
        "💡 Supported formats: JPG, PNG, GIF\n"
        "📏 Recommended size: 1200x630px for best results"
    )
    
    keyboard = [
        [InlineKeyboardButton("⏭️ Skip Image", callback_data='skip_image')],
        [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    
    return UPLOADING_IMAGE


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle image upload."""
    if update.message.photo:
        # Get the largest photo
        photo = update.message.photo[-1]
        context.user_data['post']['image'] = photo.file_id
        
        await update.message.reply_text(
            "✅ <b>Image received!</b>\n\n"
            "Moving to the next step...",
            parse_mode=ParseMode.HTML
        )
    
    return await ask_for_title(update, context)


async def skip_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skip image upload."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['post']['image'] = None
    
    return await ask_for_title(update, context)


async def ask_for_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for post title."""
    message = (
        "📝 <b>Step 2/4: Post Title</b>\n\n"
        "Enter a catchy title for your post.\n\n"
        "💡 <b>Tips:</b>\n"
        "• Keep it short and engaging (max 200 characters)\n"
        "• Use emojis to make it stand out ✨\n"
        "• Make it clear and descriptive\n\n"
        "<b>Example:</b> 🎉 New Product Launch - 50% Off!"
    )
    
    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    else:
        await update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    
    return ENTERING_TITLE


async def handle_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle title input."""
    title = update.message.text.strip()
    
    if len(title) > 200:
        await update.message.reply_text(
            "⚠️ Title is too long! Please keep it under 200 characters.\n\n"
            "Try again:",
            parse_mode=ParseMode.HTML
        )
        return ENTERING_TITLE
    
    context.user_data['post']['title'] = title
    
    await update.message.reply_text(
        "✅ <b>Title saved!</b>\n\n"
        "Moving to the next step...",
        parse_mode=ParseMode.HTML
    )
    
    return await ask_for_description(update, context)


async def ask_for_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for post description."""
    message = (
        "📄 <b>Step 3/4: Description</b>\n\n"
        "Add a detailed description for your post, or skip this step.\n\n"
        "💡 <b>Tips:</b>\n"
        "• Explain your message clearly\n"
        "• Use line breaks for readability\n"
        "• Add relevant details\n"
        "• Keep it under 1000 characters\n\n"
        "<b>Example:</b>\n"
        "We're excited to announce our new product line! 🚀\n"
        "Limited time offer - Don't miss out!"
    )
    
    keyboard = [
        [InlineKeyboardButton("⏭️ Skip Description", callback_data='skip_description')],
        [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    
    return ENTERING_DESCRIPTION


async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle description input."""
    description = update.message.text.strip()
    
    if len(description) > 1000:
        await update.message.reply_text(
            "⚠️ Description is too long! Please keep it under 1000 characters.\n\n"
            "Try again:",
            parse_mode=ParseMode.HTML
        )
        return ENTERING_DESCRIPTION
    
    context.user_data['post']['description'] = description
    
    await update.message.reply_text(
        "✅ <b>Description saved!</b>\n\n"
        "Moving to the next step...",
        parse_mode=ParseMode.HTML
    )
    
    return await ask_for_url(update, context)


async def skip_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skip description."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['post']['description'] = None
    
    return await ask_for_url(update, context)


async def ask_for_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for URL and button text."""
    message = (
        "🔗 <b>Step 4/4: Call-to-Action Button</b>\n\n"
        "Add a clickable button with a URL, or skip this step.\n\n"
        "Send your URL in this format:\n"
        "<code>https://example.com | Button Text</code>\n\n"
        "💡 <b>Examples:</b>\n"
        "• <code>https://t.me/yourchannel | Join Channel</code>\n"
        "• <code>https://yoursite.com | Visit Website</code>\n"
        "• <code>https://shop.com/sale | Shop Now</code>\n\n"
        "<b>Requirements:</b>\n"
        "✓ URL must start with http:// or https://\n"
        "✓ Use | to separate URL from button text\n"
        "✓ Button text should be short and clear"
    )
    
    keyboard = [
        [InlineKeyboardButton("⏭️ Skip Button", callback_data='skip_url')],
        [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    else:
        await update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    
    return ENTERING_URL


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle URL input."""
    text = update.message.text.strip()
    
    # Parse URL and button text
    if '|' not in text:
        await update.message.reply_text(
            "⚠️ <b>Invalid format!</b>\n\n"
            "Please use this format:\n"
            "<code>URL | Button Text</code>\n\n"
            "Example:\n"
            "<code>https://example.com | Click Here</code>",
            parse_mode=ParseMode.HTML
        )
        return ENTERING_URL
    
    parts = text.split('|', 1)
    url = parts[0].strip()
    button_text = parts[1].strip() if len(parts) > 1 else "Click Here"
    
    # Validate URL
    if not (url.startswith('http://') or url.startswith('https://')):
        await update.message.reply_text(
            "⚠️ <b>Invalid URL!</b>\n\n"
            "URL must start with http:// or https://\n\n"
            "Please try again:",
            parse_mode=ParseMode.HTML
        )
        return ENTERING_URL
    
    context.user_data['post']['url'] = url
    context.user_data['post']['button_text'] = button_text
    
    await update.message.reply_text(
        "✅ <b>Button saved!</b>\n\n"
        "Generating preview...",
        parse_mode=ParseMode.HTML
    )
    
    return await show_preview(update, context)


async def skip_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skip URL."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['post']['url'] = None
    context.user_data['post']['button_text'] = None
    
    return await show_preview(update, context)


async def show_preview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show preview of the post."""
    post = context.user_data['post']
    
    # Build preview message
    preview_text = "👁️ <b>POST PREVIEW</b>\n\n"
    preview_text += "─" * 30 + "\n\n"
    
    if post['title']:
        preview_text += f"<b>{post['title']}</b>\n\n"
    
    if post['description']:
        preview_text += f"{post['description']}\n\n"
    
    preview_text += "─" * 30 + "\n\n"
    preview_text += f"📊 <b>Broadcast Info:</b>\n"
    preview_text += f"• Will be sent to <b>{chat_storage.get_chat_count()}</b> chats\n"
    preview_text += f"• Image: {'✅ Yes' if post['image'] else '❌ No'}\n"
    preview_text += f"• Button: {'✅ Yes' if post['url'] else '❌ No'}\n\n"
    preview_text += "Ready to broadcast? 🚀"
    
    # Build keyboard
    keyboard = [
        [InlineKeyboardButton("✅ Send Broadcast", callback_data='confirm_send')],
        [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
    ]
    
    # Add button to preview if URL exists
    if post['url']:
        keyboard.insert(0, [InlineKeyboardButton(post['button_text'], url=post['url'])])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send preview
    if post['image']:
        if update.callback_query:
            await update.callback_query.message.reply_photo(
                photo=post['image'],
                caption=preview_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_photo(
                photo=post['image'],
                caption=preview_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    else:
        if update.callback_query:
            await update.callback_query.message.edit_text(
                preview_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                preview_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    return PREVIEW


async def confirm_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Confirm and send broadcast."""
    query = update.callback_query
    await query.answer()
    
    post = context.user_data['post']
    chats = chat_storage.get_all_chats()
    
    if not chats:
        await query.message.reply_text(
            "❌ <b>No Chats Available</b>\n\n"
            "Please add me to some groups/channels first!",
            parse_mode=ParseMode.HTML
        )
        return ConversationHandler.END
    
    # Send "sending" message
    status_message = await query.message.reply_text(
        "📡 <b>Broadcasting...</b>\n\n"
        f"Sending to {len(chats)} chats...",
        parse_mode=ParseMode.HTML
    )
    
    # Broadcast to all chats
    success_count = 0
    failed_count = 0
    failed_chats = []
    
    for chat_id, chat_info in chats.items():
        try:
            # Check if bot is admin
            chat_member = await context.bot.get_chat_member(int(chat_id), context.bot.id)
            if chat_member.status not in ['administrator', 'creator']:
                failed_count += 1
                failed_chats.append(f"{chat_info['title']} (not admin)")
                continue
            
            # Build message
            message_text = ""
            if post['title']:
                message_text += f"<b>{post['title']}</b>\n\n"
            if post['description']:
                message_text += f"{post['description']}"
            
            # Build keyboard
            reply_markup = None
            if post['url']:
                keyboard = [[InlineKeyboardButton(post['button_text'], url=post['url'])]]
                reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send message
            if post['image']:
                await context.bot.send_photo(
                    chat_id=int(chat_id),
                    photo=post['image'],
                    caption=message_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
            else:
                await context.bot.send_message(
                    chat_id=int(chat_id),
                    text=message_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
            
            success_count += 1
            
        except Exception as e:
            failed_count += 1
            failed_chats.append(f"{chat_info['title']} ({str(e)[:30]})")
            logger.error(f"Failed to send to {chat_id}: {e}")
    
    # Send results
    result_message = "📊 <b>Broadcast Complete!</b>\n\n"
    result_message += f"✅ <b>Successful:</b> {success_count}/{len(chats)}\n"
    result_message += f"❌ <b>Failed:</b> {failed_count}/{len(chats)}\n\n"
    
    if failed_chats:
        result_message += "<b>Failed Chats:</b>\n"
        for failed in failed_chats[:5]:  # Show first 5
            result_message += f"• {failed}\n"
        if len(failed_chats) > 5:
            result_message += f"• ... and {len(failed_chats) - 5} more\n"
    
    result_message += "\n🎉 Your message has been delivered!"
    
    await status_message.edit_text(result_message, parse_mode=ParseMode.HTML)
    
    # Clear user data
    context.user_data.clear()
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    query = update.callback_query
    
    if query:
        await query.answer()
        await query.message.edit_text(
            "❌ <b>Operation Cancelled</b>\n\n"
            "Your post was not sent.\n"
            "Use /newpost to start over anytime!",
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            "❌ <b>Operation Cancelled</b>\n\n"
            "Your post was not sent.\n"
            "Use /newpost to start over anytime!",
            parse_mode=ParseMode.HTML
        )
    
    context.user_data.clear()
    return ConversationHandler.END


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'cmd_newpost':
        await new_post(update, context)
    elif query.data == 'cmd_listchats':
        await list_chats(update, context)
    elif query.data == 'cmd_help':
        await help_command(update, context)
    elif query.data == 'cmd_start':
        # Recreate start message
        user = update.effective_user
        welcome_message = (
            f"👋 <b>Welcome back {user.first_name}!</b>\n\n"
            f"What would you like to do?"
        )
        keyboard = [
            [InlineKeyboardButton("📝 Create New Post", callback_data='cmd_newpost')],
            [InlineKeyboardButton("📋 List Chats", callback_data='cmd_listchats')],
            [InlineKeyboardButton("❓ Help", callback_data='cmd_help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(welcome_message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


async def track_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Automatically track when bot is added to a chat."""
    chat = update.effective_chat
    
    # Only track groups and channels
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
        chat_storage.add_chat(chat.id, chat.title, chat.type)
        
        # Try to send a welcome message
        try:
            welcome = (
                "👋 <b>Hello!</b>\n\n"
                "Thanks for adding me to this chat!\n\n"
                "I'm now ready to broadcast messages here. "
                "Make sure I have admin rights to post messages.\n\n"
                "The bot owner can now include this chat in broadcasts! 📡"
            )
            await update.message.reply_text(welcome, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Could not send welcome message: {e}")


async def track_chat_removal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Track when bot is removed from a chat."""
    chat = update.effective_chat
    my_chat_member = update.my_chat_member
    
    # Check if bot was removed
    if my_chat_member.new_chat_member.status in ['left', 'kicked']:
        chat_storage.remove_chat(chat.id)
        logger.info(f"Bot removed from chat: {chat.title} ({chat.id})")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """Start the bot."""
    # Get token from environment variable
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        logger.error("BOT_TOKEN environment variable not set!")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add conversation handler for new post
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('newpost', new_post),
            CallbackQueryHandler(new_post, pattern='^cmd_newpost$')
        ],
        states={
            UPLOADING_IMAGE: [
                MessageHandler(filters.PHOTO, handle_image),
                CallbackQueryHandler(skip_image, pattern='^skip_image$'),
                CallbackQueryHandler(cancel, pattern='^cancel$')
            ],
            ENTERING_TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_title),
                CallbackQueryHandler(cancel, pattern='^cancel$')
            ],
            ENTERING_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description),
                CallbackQueryHandler(skip_description, pattern='^skip_description$'),
                CallbackQueryHandler(cancel, pattern='^cancel$')
            ],
            ENTERING_URL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url),
                CallbackQueryHandler(skip_url, pattern='^skip_url$'),
                CallbackQueryHandler(cancel, pattern='^cancel$')
            ],
            PREVIEW: [
                CallbackQueryHandler(confirm_send, pattern='^confirm_send$'),
                CallbackQueryHandler(cancel, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CallbackQueryHandler(cancel, pattern='^cancel$')
        ]
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("listchats", list_chats))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_chat))
    application.add_handler(ChatMemberHandler(track_chat_removal, ChatMemberHandler.MY_CHAT_MEMBER))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    logger.info("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
