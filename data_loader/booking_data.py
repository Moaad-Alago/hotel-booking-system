import json,os
from models_bookings.booking import Booking

BOOKING_FILE = "data/bookings.json"



def save_bookings():
    data = [booking.to_dict() for booking in Booking.bookings.values()]
    with open(BOOKING_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_bookings():
    try:

        if not os.path.exists(BOOKING_FILE) or os.path.getsize(BOOKING_FILE) == 0:
            print("bookings.json is empty! Initializing with empty list.")
            with open(BOOKING_FILE, 'w') as f:
                json.dump([], f)

        with open(BOOKING_FILE, "r") as f:
            data = json.load(f)
            for booking_data in data:
                Booking.from_dict(booking_data)
    except FileNotFoundError:
        pass
