import os

DEVICE_LIST_DIR = "device_lists"

def get_device_list_file(username):
    return os.path.join(DEVICE_LIST_DIR, f"devices.{username}.txt")

def save_device_list(filename, username, device_name, remove=False):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if remove:
        with open(filename, "r") as file:
            lines = file.readlines()
        with open(filename, "w") as file:
            for line in lines:
                if line.strip() != f"{username}_{device_name}":
                    file.write(line)
    else:
        with open(filename, "a") as file:
            file.write(f"{username}_{device_name}\n")
