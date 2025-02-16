# /Users/alexanderashavskiy/projects/pi_ip_bot/menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Define main menu buttons
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="IP")],
        [KeyboardButton(text="UPTIME")],
        [KeyboardButton(text="VPN")]
    ],
    resize_keyboard=True
)