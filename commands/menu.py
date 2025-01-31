import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Message
from telegram.ext import CallbackContext, CallbackQueryHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def menu_command(update: Update, context: CallbackContext) -> None:
    """Display the inline menu with buttons."""
    keyboard = [
        [InlineKeyboardButton("📡 IP Address", callback_data="menu_ip")],
        [InlineKeyboardButton("📊 Uptime", callback_data="menu_uptime")],
        [InlineKeyboardButton("🔐 VPN Access", callback_data="menu_vpn")],
        [InlineKeyboardButton("👋 End", callback_data="menu_end")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📌 **Choose an option:**", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    """Handle button clicks from the inline menu."""
    query = update.callback_query
    await query.answer()

    command_map = {
        "menu_ip": "/ip",
        "menu_uptime": "/uptime",
        "menu_vpn": "/vpn",
        "menu_end": "/end"
    }

    command = command_map.get(query.data)
    if command:
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"⌛ Executing {command}...")
        fake_update = Update(
            update.update_id,
            message=Message(
                message_id=query.message.message_id,
                date=query.message.date,
                chat=query.message.chat,
                from_user=query.from_user,
                text=command,
                bot=context.bot  # Attach the bot instance
            )
        )
        fake_update._bot = context.bot  # Manually associate bot instance

        if command == "/ip":
            from commands.ip import ip_command
            await ip_command(fake_update, context)
        elif command == "/uptime":
            from commands.uptime import uptime_command
            await uptime_command(fake_update, context)
        elif command == "/vpn":
            from commands.vpn.request import request_vpn
            await request_vpn(fake_update, context)
        elif command == "/end":
            await query.message.reply_text("👋 Goodbye! Closing the menu.")
