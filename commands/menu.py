from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils import is_user_in_vpn_whitelist
from commands.vpn.devices import add_device, list_devices, get_config, remove_device
from commands.ip import ip_command
from commands.uptime import uptime_command

def get_main_menu():
    return ReplyKeyboardMarkup([
        ["📡 IP Address", "🕒 Uptime"],
        ["🔐 VPN"]
    ], resize_keyboard=True)

def get_vpn_menu():
    return ReplyKeyboardMarkup([
        ["➕ Add Device", "📄 List My Devices"],
        ["📥 Get Config", "❌ Remove Device"],
        ["🔙 Back"]
    ], resize_keyboard=True)

async def menu_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu())

async def vpn_menu(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if is_user_in_vpn_whitelist(user_id):
        await update.message.reply_text("🔐 VPN Menu:", reply_markup=get_vpn_menu())
    else:
        await update.message.reply_text("❌ You are not authorized for VPN access.")

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "📡 IP Address":
        await ip_command(update, context)
    elif text == "🕒 Uptime":
        await uptime_command(update, context)
    elif text == "🔐 VPN":
        await vpn_menu(update, context)
    elif text == "➕ Add Device":
        await add_device(update, context)
    elif text == "📄 List My Devices":
        await list_devices(update, context)
    elif text == "📥 Get Config":
        await get_config(update, context)
    elif text == "❌ Remove Device":
        await remove_device(update, context)
    elif text == "🔙 Back":
        await menu_command(update, context)
    else:
        await update.message.reply_text("❌ Unknown command.")