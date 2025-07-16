import json,os
from models_rooms.room import Room

ROOMS_FILE = "data/rooms.json"



def save_rooms():
    data = [r.to_dict() for r in Room.rooms.values()]
    with open(ROOMS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_rooms():
    try:
        if not os.path.exists(ROOMS_FILE) or os.path.getsize(ROOMS_FILE) == 0:
            print("rooms.json is empty! Initializing with empty list.")
            with open(ROOMS_FILE, 'w') as f:
                json.dump([], f)

        with open(ROOMS_FILE, "r") as f:
            data = json.load(f)
            for r in data:
                Room.from_dict(r)
    except FileNotFoundError:
        pass
