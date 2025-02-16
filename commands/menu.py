# /Users/alexanderashavskiy/projects/pi_ip_bot/menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher

# Get the current dispatcher instance
dp = Dispatcher.get_current()

# Define main menu buttons
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="IP")],
        [KeyboardButton(text="UPTIME")],
        [KeyboardButton(text="VPN")]
    ],
    resize_keyboard=True
)

# Function to return the main menu markup
def get_main_menu():
    return main_menu

# Command handler for opening the menu
@dp.message_handler(Command("menu"))
async def menu_command(message: Message):
    await message.reply("Main menu:", reply_markup=get_main_menu())

# Placeholder for conversation handler (if needed)
def get_conversation_handler():
    pass  # Implement if needed