# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/menu_utils.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Function to generate the inline keyboard menu
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🌐 IP", callback_data="ip")],
        [InlineKeyboardButton("⏳ Uptime", callback_data="uptime")]
    ]
    return InlineKeyboardMarkup(keyboard)