# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_utils.py

import os

WHITELIST_FILE = "router_whitelist.txt"

def is_router_admin(user_id: str) -> bool:
    """Check if the user is in the router whitelist."""
    if not os.path.exists(WHITELIST_FILE):
        return False  # If the file doesn't exist, deny access

    with open(WHITELIST_FILE, "r") as file:
        allowed_users = {line.strip() for line in file.readlines()}

    return user_id in allowed_users