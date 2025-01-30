import os
from telegram import Update

WHITELIST_FILE = "whitelist.txt"
ADMIN_ID = os.getenv("ADMIN_ID")

# Function to load whitelisted user IDs
def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return set()
    with open(WHITELIST_FILE, "r") as f:
        return {line.strip() for line in f}

WHITELIST = load_whitelist()

# Function to add a new user to whitelist
def add_to_whitelist(user_id):
    WHITELIST.add(str(user_id))
    with open(WHITELIST_FILE, "a") as f:
        f.write(f"{user_id}\n")

# Function to check if a user is allowed
def is_user_allowed(update: Update):
    user_id = update.message.from_user.id
    return str(user_id) in WHITELIST