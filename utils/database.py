import json
import os

DATA_FILE = "data.json"

def save_message_mapping(user_id, user_message_id, group_message_id):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    else:
        data = {}

    data[str(user_id)] = {
        "user_message_id": user_message_id,
        "group_message_id": group_message_id
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def load_message_mappings():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}