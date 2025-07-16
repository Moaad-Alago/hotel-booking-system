from .guest import Guest

class VIPGuest(Guest):
    def calculate_discount(self):
        return 0.2 

    def get_guest_type(self):
        return "vip"