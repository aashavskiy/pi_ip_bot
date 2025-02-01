from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils import is_user_in_vpn_whitelist
from commands.vpn.devices import add_device, list_devices, get_config, remove_device
from commands.ip import ip_command
from commands.uptime import uptime_command

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("IP", callback_data='ip')],
        [InlineKeyboardButton("Uptime", callback_data='uptime')],
        [InlineKeyboardButton("VPN", callback_data='vpn')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_vpn_menu():
    keyboard = [
        [InlineKeyboardButton("Add Device", callback_data='add_device')],
        [InlineKeyboardButton("List Devices", callback_data='list_devices')],
        [InlineKeyboardButton("Get Config", callback_data='get_config')],
        [InlineKeyboardButton("Remove Device", callback_data='remove_device')],
        [InlineKeyboardButton("Back to Menu", callback_data='menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

async def menu_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu())

async def vpn_menu(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)
    if is_user_in_vpn_whitelist(user_id):
        await update.message.reply_text("🔐 VPN Menu:", reply_markup=get_vpn_menu())
    else:
        await update.message.reply_text("❌ You are not authorized for VPN access.")

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'ip':
        await ip_command(update, context)
    elif data == 'uptime':
        await uptime_command(update, context)
    elif data == 'vpn':
        await vpn_menu(update, context)
    elif data == 'add_device':
        await add_device(update, context)
    elif data == 'list_devices':
        await list_devices(update, context)
    elif data == 'get_config':
        await get_config(update, context)
    elif data == 'remove_device':
        await remove_device(update, context)
    elif data == 'menu':
        await menu_command(update, context)
    else:
        await query.edit_message_text("❌ Unknown command. Please use the menu or type /help for available commands.")