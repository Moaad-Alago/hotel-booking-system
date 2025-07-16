from models_guests.guest import Guest
from models_guests.VIPGuest import VIPGuest
from models_guests.MemberGuest import MemberGuest

class GuestFactory:
    @staticmethod
    def create_guest(guest_type, ID, name, email="", phone_number=""):
        t = guest_type.strip().lower()
        if t == "vip":
            return VIPGuest(ID, name, email, phone_number)
        elif t == "member":
            return MemberGuest(ID, name, email, phone_number)
        else:
            return Guest(ID, name, email, phone_number, guest_type="Regular")

    @staticmethod
    def from_dict(data):
        guest = GuestFactory.create_guest(
            guest_type=data.get("guest_type", "Regular"),
            ID=data["id"],
            name=data["name"],
            email=data.get("email", ""),
            phone_number=data.get("phone_number", "")
        )

    
        guest.number = data.get("number", guest.number)
        guest.preferences = data.get("preferences", "")
        guest.notes = data.get("notes", "")
        guest.bookings = data.get("bookings", [])

        Guest.guests[guest.id] = guest
        return guest

