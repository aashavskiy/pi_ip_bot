import os

# Function to load a whitelist from file
def load_whitelist(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r") as f:
        return {line.split("#")[0].strip() for line in f.read().splitlines()}  # ✅ Store only user IDs

# Function to add a user to a whitelist
def add_to_whitelist(user_id, username, filename):
    whitelist = load_whitelist(filename)  # Load existing users

    # ✅ Check if user is already in the whitelist to prevent duplicates
    if user_id in whitelist:
        return

    with open(filename, "a") as f:
        f.write(f"{user_id}#{username}\n")  # ✅ Append user to the file