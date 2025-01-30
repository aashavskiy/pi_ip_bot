import os
from datetime import datetime
from utils import load_whitelist

BOT_WHITELIST_FILE = "bot_whitelist.txt"

# Log user requests
def log_request(user_id, username, command):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {username} ({user_id}) used: {command}\n"

    with open("bot_requests.log", "a") as log_file:
        log_file.write(log_entry)

    # Check if the user is in the whitelist
    bot_whitelist = load_whitelist(BOT_WHITELIST_FILE)
    if user_id not in bot_whitelist:
        print(f"🚨 Unauthorized access attempt: {username} ({user_id}) tried {command}")