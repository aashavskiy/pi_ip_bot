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

async def vpn_menu(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("VPN Menu:", reply_markup=get_vpn_menu())

async def add_device_command(update: Update, context: CallbackContext) -> None:
    await add_device(update, context)

async def list_devices_command(update: Update, context: CallbackContext) -> None:
    await list_devices(update, context)

async def get_config_command(update: Update, context: CallbackContext) -> None:
    await get_config(update, context)

async def remove_device_command(update: Update, context: CallbackContext) -> None:
    await remove_device(update, context)

menu_handler = CommandHandler("menu", menu_command)
vpn_menu_handler = MessageHandler(filters.Regex("^🔐 VPN$"), vpn_menu)
add_device_handler = MessageHandler(filters.Regex("^➕ Add Device$"), add_device_command)
list_devices_handler = MessageHandler(filters.Regex("^📋 List Devices$"), list_devices_command)
get_config_handler = MessageHandler(filters.Regex("^🔑 Get Config$"), get_config_command)
remove_device_handler = MessageHandler(filters.Regex("^❌ Remove Device$"), remove_device_command)
