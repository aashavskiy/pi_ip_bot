import os
from datetime import datetime
from bot_utils import load_whitelist

BOT_WHITELIST_FILE = "bot_whitelist.txt"

# Log user requests
async def log_request(user_id, username, command):  # ✅ Ensure it expects three arguments
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {username} ({user_id}) used: {command}\n"

    with open("bot_requests.log", "a") as log_file:
        log_file.write(log_entry)

    # Check if the user is in the whitelist
    bot_whitelist = load_whitelist(BOT_WHITELIST_FILE)
    if str(user_id) not in bot_whitelist:
        print(f"🚨 Unauthorized access attempt: {username} ({user_id}) tried {command}")