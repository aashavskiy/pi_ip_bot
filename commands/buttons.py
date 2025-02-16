# File: commands/buttons.py

from telegram import Update
from telegram.ext import CallbackContext
from commands.vpn.menu import vpn_menu
from commands.ip import ip_command
from commands.uptime import uptime_command
from commands.menu import menu_command

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    """
    Handles button presses in the main menu.
    """
    text = update.message.text

    if text in ["🔐 VPN", "VPN"]:
        await vpn_menu(update, context)
    elif text in ["🌐 IP", "IP"]:
        await ip_command(update, context)
    elif text in ["⏳ Uptime", "Uptime"]:
        await uptime_command(update, context)
    elif text in ["🔙 Main Menu", "Main Menu"]:
        await menu_command(update, context)
    else:
        await update.message.reply_text("Unknown command, please use the menu.")