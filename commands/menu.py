# /Users/alexanderashavskiy/projects/pi_ip_bot/menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define main menu buttons
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="IP", callback_data="get_ip")],
    [InlineKeyboardButton(text="UPTIME", callback_data="get_uptime")],
    [InlineKeyboardButton(text="VPN", callback_data="get_vpn")]
])

# Function to return the main menu markup
def get_main_menu():
    return main_menu