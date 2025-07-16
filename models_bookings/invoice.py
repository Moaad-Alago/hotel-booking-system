from models_rooms.room import Room

class Invoice:

    def __init__(self, booking):
        self.booking = booking

    def generate_invoice_text(self):
        guest = self.booking.guest
        room = Room.rooms.get(self.booking.room_number)

        if not room:
            return f"Error: Room {self.booking.room_number} not found."

        nights = (self.booking.check_out_date - self.booking.check_in_date).days
        base_price = room.price * nights

        discount_rate = guest.calculate_discount()
        discount_amount = base_price * discount_rate
        total_price = base_price - discount_amount

        invoice_lines = [
            "===== Hotel Booking Invoice =====",
            f"Guest Name: {guest.name}",
            f"Guest Type: {guest.get_guest_type()}",
            f"Room Type: {room.room_type}",
            f"Check-in Date: {self.booking.check_in_date.date()}",
            f"Check-out Date: {self.booking.check_out_date.date()}",
            f"Number of Nights: {nights}",
            f"Price per Night: ${room.price:.2f}",
            f"Base Price: ${base_price:.2f}",
            f"Discount Applied: {discount_rate * 100:.0f}%",
            f"Discount Amount: -${discount_amount:.2f}",
            f"Total Cost: ${total_price:.2f}",
            f"Payment Status: {'Paid' if self.booking.paid else 'Unpaid'}",
            "=================================="
        ]

        return "\n".join(invoice_lines)

    def print_invoice(self):
        print(self.generate_invoice_text())
