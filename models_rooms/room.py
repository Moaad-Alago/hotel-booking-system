class Room:
    rooms = {}
    room_types = {"single", "double", "suite"}
    availability = {"available": True, "taken": False, "maintenance": False}

    def __init__(self, number, room_type, price, available=True, features=None):
        self.number = number
        self.room_type = room_type
        self.price = price
        self.available = available
        self.features = features or []  # List of strings like ["Balcony", "Jacuzzi"]
        Room.rooms[self.number] = self

    def update_room(self, number=None, room_type=None, price=None, available=None, features=None):
        if number is not None:
            self.number = number
        if room_type is not None:
            self.room_type = room_type
        if price is not None:
            self.price = price
        if available is not None:
            self.available = available
        if features is not None:
            self.features = features

    @staticmethod
    def delete_room(room_number):
        if room_number in Room.rooms:
            del Room.rooms[room_number]
            return True
        return False

    @staticmethod
    def list_rooms():
        return list(Room.rooms.values())

    def to_dict(self):
        return {
            "number": self.number,
            "room_type": self.room_type,
            "price": self.price,
            "available": self.available,
            "features": self.features
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            number=data["number"],
            room_type=data["room_type"],
            price=data["price"],
            available=data.get("available", True),
            features=data.get("features", [])
        )

    def __repr__(self):
        availability_str = "Available" if self.available else "Unavailable"
        features_str = ", ".join(self.features) if self.features else "None"
        return (
            f"ROOM {self.number}\n"
            f"Type: {self.room_type}, Price: ${self.price}, "
            f"Available: {availability_str}, Features: {features_str}\n"
        )
