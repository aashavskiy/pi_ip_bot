from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from utils import is_user_in_vpn_whitelist, is_user_authorized, request_approval
from commands.vpn.devices import add_device, list_devices, get_config, remove_device
from commands.ip import ip_command
from commands.uptime import uptime_command

def get_main_menu():
    return ReplyKeyboardMarkup([
        ["/ip", "/uptime"],
        ["/vpn"]
    ], resize_keyboard=True, one_time_keyboard=True)

def get_vpn_menu():
    return ReplyKeyboardMarkup([
        ["/add_device", "/list_devices"],
        ["/get_config", "/remove_device"],
        ["/menu"]
    ], resize_keyboard=True, one_time_keyboard=True)

async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username)
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=ReplyKeyboardRemove()
    )
    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu()
    )

async def vpn_menu(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if is_user_in_vpn_whitelist(user_id):
        await update.message.reply_text("🔐 VPN Menu:", reply_markup=get_vpn_menu())
    else:
        await update.message.reply_text("❌ You are not authorized for VPN access.")

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    if update.message:
        text = update.message.text.strip()
    elif update.callback_query:
        text = update.callback_query.data
    else:
        return

    if text == "/start":
        await menu_command(update, context)
    elif text == "/ip":
        await ip_command(update, context)
    elif text == "/uptime":
        await uptime_command(update, context)
    elif text == "/vpn":
        await vpn_menu(update, context)
    elif text == "/add_device":
        await add_device(update, context)
    elif text == "/list_devices":
        await list_devices(update, context)
    elif text == "/get_config":
        await get_config(update, context)
    elif text == "/remove_device":
        await remove_device(update, context)
    elif text == "/menu":
        await menu_command(update, context)
    else:
        await update.message.reply_text("❌ Unknown command. Please use the menu or type /help for available commands.")