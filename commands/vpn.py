# File: commands/vpn.py

from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from commands.vpn.menu import vpn_menu

async def vpn_button_handler(update: Update, context: CallbackContext) -> None:
    """
    Handles the VPN button press
    """
    await vpn_menu(update, context)

# Register handler
vpn_handler = MessageHandler(filters.Regex("^🔐 VPN$"), vpn_button_handler)