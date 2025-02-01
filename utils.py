import os
from telegram import Bot

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
    authorized_users = load_whitelist("whitelist.txt")
    return user_id in authorized_users

def request_approval(user_id, username):
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    message = f"🚨 Approval request:\nUser ID: {user_id}\nUsername: @{username}"
    bot.send_message(chat_id=ADMIN_ID, text=message)
