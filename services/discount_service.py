class DiscountService:
    @staticmethod
    def apply_discount(booking):
        guest = booking.guest
        room = booking.room
        nights = (booking.check_out_date - booking.check_in_date).days
        base_price = room.price * nights

        discount_rate = guest.calculate_discount()
        discount_amount = base_price * discount_rate
        total_price = base_price - discount_amount

        return {
            "base_price": base_price,
            "discount_rate": discount_rate,
            "discount_amount": discount_amount,
            "total_price": total_price
        }