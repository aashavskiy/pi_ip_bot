import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import CallbackContext

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def menu_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton("📡 IP Address")],
        [KeyboardButton("📊 Uptime")],
        [KeyboardButton("🔐 VPN Access")],
        [KeyboardButton("👋 End")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("📌 **Choose an option:**", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()

    command_map = {
        "📡 IP Address": "/ip",
        "📊 Uptime": "/uptime",
        "🔐 VPN Access": "/vpn",
        "👋 End": "/end"
    }

    command = command_map.get(text)
    if command:
        if command == "/ip":
            from commands.ip import ip_command
            await ip_command(update, context)
        elif command == "/uptime":
            from commands.uptime import uptime_command
            await uptime_command(update, context)
        elif command == "/vpn":
            from commands.vpn.request import request_vpn
            await request_vpn(update, context)
        elif command == "/end":
            await update.message.reply_text("👋 Goodbye! Menu closed.")
