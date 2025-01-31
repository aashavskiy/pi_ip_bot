import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import CallbackContext, MessageHandler, filters, CommandHandler
from utils import is_user_in_vpn_whitelist

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def menu_command(update: Update, context: CallbackContext) -> None:
    logging.info("DEBUG: menu_command triggered")
    keyboard = [
        [KeyboardButton("/ip")],
        [KeyboardButton("/uptime")],
        [KeyboardButton("/vpn")],
        [KeyboardButton("/end")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("📌 **Choose an option:**", reply_markup=reply_markup, parse_mode="Markdown")

async def vpn_menu(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    logging.info(f"DEBUG: VPN menu requested by {user_id}")
    if is_user_in_vpn_whitelist(user_id):
        keyboard = [
            [KeyboardButton("📄 List My Devices")],
            [KeyboardButton("➕ Add Device")],
            [KeyboardButton("❌ Remove Device")],
            [KeyboardButton("📥 Get Config")],
            [KeyboardButton("🔙 Back to Main Menu")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text("🔐 **VPN Menu:**", reply_markup=reply_markup, parse_mode="Markdown")
    else:
        keyboard = [
            [KeyboardButton("➕ Request VPN Access")],
            [KeyboardButton("🔙 Back to Main Menu")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text("❌ You are not yet approved for VPN access.", reply_markup=reply_markup, parse_mode="Markdown")

async def start_command(update: Update, context: CallbackContext) -> None:
    logging.info("DEBUG: /start command triggered")
    await update.message.reply_text("👋 Welcome! Here is your menu:")
    await menu_command(update, context)

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()
    
    if text == "/start":
        await start_command(update, context)
    elif text == "/ip":
        from commands.ip import ip_command
        await ip_command(update, context)
    elif text == "/uptime":
        from commands.uptime import uptime_command
        await uptime_command(update, context)
    elif text == "/vpn":
        await vpn_menu(update, context)
    elif text == "/end":
        await update.message.reply_text("👋 Goodbye! Menu closed.", reply_markup=ReplyKeyboardMarkup([], resize_keyboard=True))
    elif text == "📄 List My Devices":
        from commands.vpn.devices import list_devices
        await list_devices(update, context)
    elif text == "➕ Add Device":
        from commands.vpn.devices import add_device
        await add_device(update, context)
    elif text == "❌ Remove Device":
        from commands.vpn.devices import remove_device
        await remove_device(update, context)
    elif text == "📥 Get Config":
        from commands.vpn.devices import get_config
        await get_config(update, context)
    elif text == "➕ Request VPN Access":
        from commands.vpn.request import request_vpn
        await request_vpn(update, context)
    elif text == "🔙 Back to Main Menu":
        await menu_command(update, context)
    
    await menu_command(update, context)  # Ensure menu is shown again after any action

def register_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_buttons))
