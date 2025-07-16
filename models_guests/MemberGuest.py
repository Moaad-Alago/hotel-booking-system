from .guest import Guest

class MemberGuest(Guest):
    def calculate_discount(self):
        return 0.1  

    def get_guest_type(self):
        return "member"
