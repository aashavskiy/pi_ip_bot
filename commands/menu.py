from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils import is_user_in_vpn_whitelist

# Main menu function
def menu_command(update: Update, context: CallbackContext) -> None:
    keyboard = [["📡 IP Address", "🕒 Uptime"],
                ["🔐 VPN"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("🔽 Main Menu:", reply_markup=reply_markup)

# VPN menu function
def vpn_menu(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if not is_user_in_vpn_whitelist(user_id):
        update.message.reply_text("🔐 You need approval to access VPN services.")
        return
    
    keyboard = [["📄 List My Devices", "➕ Add Device"],
                ["📥 Get Config", "❌ Remove Device"],
                ["⬅ Back"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("🔽 VPN Menu:", reply_markup=reply_markup)

# Handle button clicks
def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    
    if text == "🔐 VPN":
        vpn_menu(update, context)
    elif text == "⬅ Back":
        menu_command(update, context)