import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import CallbackContext, MessageHandler, filters

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def menu_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton("/ip")],
        [KeyboardButton("/uptime")],
        [KeyboardButton("/vpn")],
        [KeyboardButton("/end")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("📌 **Choose an option:**", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()
    
    if text == "/ip":
        from commands.ip import ip_command
        await ip_command(update, context)
    elif text == "/uptime":
        from commands.uptime import uptime_command
        await uptime_command(update, context)
    elif text == "/vpn":
        from commands.vpn.request import request_vpn
        await request_vpn(update, context)
    elif text == "/end":
        await update.message.reply_text("👋 Goodbye! Menu closed.")
