# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/menu_utils.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from commands.router_utils import is_router_admin

# Function to generate the main menu
def get_main_menu(user_id: str):
    keyboard = [
        [InlineKeyboardButton("🌐 IP", callback_data="ip")],
        [InlineKeyboardButton("⏳ Uptime", callback_data="uptime")]
    ]

    # Add Router Control Menu button **only for whitelisted users**
    if is_router_admin(user_id):
        keyboard.append([InlineKeyboardButton("⚙ Router Control", callback_data="router_menu")])

    return InlineKeyboardMarkup(keyboard)