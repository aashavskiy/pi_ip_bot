from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils import load_whitelist

VPN_WHITELIST_FILE = "vpn_whitelist.txt"

async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)

    # Basic buttons for all users
    buttons = [["/ip", "/uptime"], ["/vpn"]]

    # Show additional VPN commands only to whitelisted users
    if user_id in vpn_whitelist:
        buttons.append(["/adddevice", "/listdevices", "/removedevice"])

    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("📍 Choose a command:", reply_markup=keyboard)