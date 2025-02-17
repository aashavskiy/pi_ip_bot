# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_utils.py

import os

WHITELIST_FILE = "router_whitelist.txt"

def is_router_admin(user_id: str) -> bool:
    """Check if the user is in the router whitelist."""
    if not os.path.exists(WHITELIST_FILE):
        print(f"🚫 Whitelist file not found: {WHITELIST_FILE}")
        return False  # File does not exist, deny access

    with open(WHITELIST_FILE, "r") as file:
        allowed_users = {line.strip() for line in file.readlines()}

    print(f"🔍 Checking user {user_id} in whitelist: {allowed_users}")

    return user_id in allowed_users