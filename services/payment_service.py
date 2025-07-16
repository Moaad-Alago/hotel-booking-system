class PaymentService:
    @staticmethod
    def mark_as_paid(booking):
        if booking.paid:
            print("Booking is already marked as paid.")
        else:
            booking.mark_as_paid()
            print("Payment completed successfully.")