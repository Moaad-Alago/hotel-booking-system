class Guest:

    guests = {}
    guest_number = 1

    def __init__(self, ID, name, email, phone_number,guest_type="regular"):
        self.id = ID
        self.number = Guest.guest_number
        Guest.guest_number += 1
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.bookings = []
        self.preferences = "" 
        self.notes = ""
        self.guest_type = guest_type
        Guest.guests[self.id] = self

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "bookings": [b if isinstance(b, str) else b.id for b in self.bookings],
            "guest_type": self.get_guest_type(),
            "preferences": self.preferences,    
            "notes": self.notes      
        }



    @classmethod
    def from_dict(cls, data):
        guest_type = data.get("guest_type", "regular")
        from factories.guest_factory import GuestFactory
        guest = GuestFactory.create_guest(
            guest_type=guest_type,
            ID=data["id"],
            name=data["name"],
            email=data.get("email", ""),
            phone_number=data.get("phone_number", "")
        )

        guest.guest_type = guest_type.title()

        guest.number = data.get("number", guest.number)
        guest.preferences = data.get("preferences", "")
        guest.notes = data.get("notes", "")
        guest.bookings = data.get("bookings", [])
        cls.guests[guest.id] = guest

        return guest

        
    def change(self, ID=None, name=None, phone_number=None,guest_type=None,email=None):
        if ID is not None:
            self.id = ID
        if name is not None:
            self.name = name
        if phone_number is not None:
            self.phone_number = phone_number
        if guest_type is not None:
            self.guest_type = guest_type
        if email is not None:
            self.email = email


    @staticmethod
    def update(guest_id, name=None, phone_number=None,guest_type=None,email=None):
        guest = Guest.guests.get(guest_id)
        if guest:
            guest.change(name=name, phone_number=phone_number,guest_type=guest_type,email=email)
            return True
        return False

    def guest_info(self):
        return f"*Guest ID: {self.id} | Guest NAME: {self.name} | Guest PHONE: {self.phone_number} Guest Type: {self.get_guest_type()}\nEmail: {self.email} \n| Preferences: {self.preferences} \n| Notes: {self.notes}"

    @staticmethod
    def get_guest_info(guest_id):
        guest = Guest.guests.get(guest_id)
        if guest:
            return guest.guest_info()
        return None

    @staticmethod
    def delete_guest(guest_id):
        if guest_id in Guest.guests:
            del Guest.guests[guest_id]
            return True
        return False

    def calculate_discount(self):
        return 0  

    def get_guest_type(self):
        return self.guest_type


    def update_preferences(self, preferences):
        self.preferences = preferences

    def update_notes(self, notes):
        self.notes = notes

    def __str__(self):
        return f"{self.get_guest_type()} Guest: {self.name} ({self.email})"
