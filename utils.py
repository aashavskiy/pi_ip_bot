import os

WHITELIST_FILE = "whitelist.txt"
VPN_WHITELIST_FILE = "vpn_whitelist.txt"

def load_whitelist(filename=WHITELIST_FILE):
    """ Load the whitelist from a file. """
    if not os.path.exists(filename):
        return set()
    
    with open(filename, "r") as file:
        return set(line.strip().split()[0] for line in file if line.strip())

def add_to_whitelist(user_id, username, filename=WHITELIST_FILE):
    """ Add a user to the whitelist. """
    if not os.path.exists(filename):
        open(filename, "w").close()  # Create file if missing
    
    with open(filename, "a") as file:
        file.write(f"{user_id} # {username}\n")

def check_whitelist(user_id):
    """ Check if a user is in the whitelist. """
    whitelist = load_whitelist()
    return str(user_id) in whitelist