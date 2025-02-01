import os
import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

ADMIN_ID = os.getenv("ADMIN_ID")

def load_whitelist(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r") as f:
        return set(line.strip().split()[0] for line in f if line.strip())

def add_to_whitelist(filename, user_id, username=None):
    with open(filename, "a") as f:
        if username:
            f.write(f"{user_id}  # {username}\n")
        else:
            f.write(f"{user_id}\n")

def is_user_in_whitelist(filename, user_id):
    whitelist = load_whitelist(filename)
    return str(user_id) in whitelist

def check_whitelist(user_id):
    return is_user_in_whitelist(BOT_WHITELIST_FILE, user_id)

BOT_WHITELIST_FILE = "bot_whitelist.txt"
VPN_WHITELIST_FILE = "vpn_whitelist.txt"

VPN_WHITELIST = load_whitelist(VPN_WHITELIST_FILE)

def is_user_in_bot_whitelist(user_id):
    return is_user_in_whitelist(BOT_WHITELIST_FILE, user_id)

def is_user_in_vpn_whitelist(user_id):
    return is_user_in_whitelist(VPN_WHITELIST_FILE, user_id)

def add_user_to_bot_whitelist(user_id, username=None):
    add_to_whitelist(BOT_WHITELIST_FILE, user_id, username)

def add_to_vpn_whitelist(user_id, username=None):
    add_to_whitelist(VPN_WHITELIST_FILE, user_id, username)

def is_user_authorized(user_id):
    authorized_users = load_whitelist(BOT_WHITELIST_FILE)
    logging.info(f"Authorized users: {authorized_users}")
    return user_id in authorized_users

async def request_approval(user_id, username, approval_type):
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    admin_id = os.getenv("ADMIN_ID")
    if not admin_id:
        raise ValueError("ADMIN_ID is not set in the environment variables.")
    message = f"🚨 Approval request for {approval_type} access:\nUser ID: {user_id}\nUsername: @{username}"
    keyboard = [
        [
            InlineKeyboardButton("Approve", callback_data=f"approve:{user_id}:{username}:{approval_type}"),
            InlineKeyboardButton("Deny", callback_data=f"deny:{user_id}:{username}:{approval_type}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(chat_id=admin_id, text=message, reply_markup=reply_markup)
