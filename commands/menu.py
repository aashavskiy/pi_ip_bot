from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
from bot_utils import is_user_in_vpn_whitelist, is_user_authorized, request_approval
from commands.vpn.devices import add_device, list_devices, get_config, remove_device
from commands.ip import ip_command
from commands.uptime import uptime_command
import logging

# Define states for the conversation
DEVICE_NAME, REMOVE_DEVICE_NAME = range(2)

def get_main_menu():
    return ReplyKeyboardMarkup([
        ["🌐 IP", "⏳ Uptime"],
        ["🔐 VPN"]
    ], resize_keyboard=True, one_time_keyboard=True)

def get_vpn_menu():
    return ReplyKeyboardMarkup([
        ["➕ Add Device", "📋 List Devices"],
        ["🔑 Get Config", "❌ Remove Device"],
        ["🔙 Main Menu"]
    ], resize_keyboard=True, one_time_keyboard=True)

async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        return

    await update.message.reply_text("Main Menu:", reply_markup=get_main_menu())

async def uptime_button_handler(update: Update, context: CallbackContext) -> None:
    """Handles the Uptime button press"""
    await uptime_command(update, context)

async def vpn_button_handler(update: Update, context: CallbackContext) -> None:
    """Handles the VPN button press"""
    await vpn_menu(update, context)

async def add_device_button_handler(update: Update, context: CallbackContext) -> None:
    """Handles the Add Device button press"""
    await add_device(update, context)

async def list_devices_button_handler(update: Update, context: CallbackContext) -> None:
    """Handles the List Devices button press"""
    await list_devices(update, context)

async def get_config_button_handler(update: Update, context: CallbackContext) -> None:
    """Handles the Get Config button press"""
    await get_config(update, context)

async def remove_device_button_handler(update: Update, context: CallbackContext) -> None:
    """Handles the Remove Device button press"""
    await remove_device(update, context)

async def main_menu_button_handler(update: Update, context: CallbackContext) -> None:
    """Handles the Main Menu button press"""
    await menu_command(update, context)

# Register handlers
menu_handler = CommandHandler("menu", menu_command)
ip_button_handler = MessageHandler(filters.Regex("^🌐 IP$"), ip_command)
uptime_button_handler = MessageHandler(filters.Regex("^⏳ Uptime$"), uptime_button_handler)
vpn_button_handler = MessageHandler(filters.Regex("^🔐 VPN$"), vpn_button_handler)
add_device_button_handler = MessageHandler(filters.Regex("^➕ Add Device$"), add_device_button_handler)
list_devices_button_handler = MessageHandler(filters.Regex("^📋 List Devices$"), list_devices_button_handler)
get_config_button_handler = MessageHandler(filters.Regex("^🔑 Get Config$"), get_config_button_handler)
remove_device_button_handler = MessageHandler(filters.Regex("^❌ Remove Device$"), remove_device_button_handler)
main_menu_button_handler = MessageHandler(filters.Regex("^🔙 Main Menu$"), main_menu_button_handler)
