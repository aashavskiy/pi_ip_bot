# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/vpn/vpn.py

from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

# Create a router instance
router = Router()

# Handler for the VPN command
@router.message(Command("VPN"))
async def vpn_button_handler(message: Message):
    await message.reply("VPN command executed successfully.")