import os
from telegram import Update

WHITELIST_FILE = "whitelist.txt"
ADMIN_ID = os.getenv("ADMIN_ID")

# Function to load whitelisted user IDs
def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return set()
    with open(WHITELIST_FILE, "r") as f:
        return {line.split("#")[0].strip() for line in f if line.strip() and not line.startswith("#")}

WHITELIST = load_whitelist()

# Function to add a new user to whitelist with a comment (username)
def add_to_whitelist(user_id, username="Unknown"):
    WHITELIST.add(str(user_id))
    with open(WHITELIST_FILE, "a") as f:
        f.write(f"{user_id}  # {username}\n")