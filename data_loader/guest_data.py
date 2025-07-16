
import json, os
from models_guests.guest import Guest
from models_guests.VIPGuest import VIPGuest
from models_guests.MemberGuest import MemberGuest
from factories.guest_factory import GuestFactory 

GUEST_FILE = "data/guests.json"

def save_guests():
    data = [guest.to_dict() for guest in Guest.guests.values()]
    with open(GUEST_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_guests():
    try:
        if not os.path.exists(GUEST_FILE) or os.path.getsize(GUEST_FILE) == 0:
            print("guests.json is empty! Initializing with empty list.")
            with open(GUEST_FILE, 'w') as f:
                json.dump([], f)

        with open(GUEST_FILE, "r") as f:
            data = json.load(f)
            for guest_data in data:
                GuestFactory.from_dict(guest_data)

    except FileNotFoundError:
        pass
