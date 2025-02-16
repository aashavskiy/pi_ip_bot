# /Users/alexanderashavskiy/projects/pi_ip_bot/menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

# Create a router instance
router = Router()

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
@router.message(Command("menu"))
async def menu_command(message: Message):
    await message.reply("Main menu:", reply_markup=get_main_menu())

# Placeholder for conversation handler (if needed)
def get_conversation_handler():
    pass  # Implement if needed