import unittest
from datetime import datetime
from models_guests.guest import Guest
from models_rooms.room import Room
from models_bookings.booking import Booking, BookingStatus

class TestBooking(unittest.TestCase):

    def setUp(self):
        Guest.guests = {}
        Room.rooms = {}
        Booking.bookings = {}

        self.guest = Guest("G1", "Ali", "ali@example.com", "0599999999")
        self.room = Room(101, "Single", 100)
        self.booking = Booking("B1", "G1", 101, "2025-06-01", "2025-06-05")

    def test_booking_creation(self):
        self.assertEqual(self.booking.id, "B1")
        self.assertEqual(self.booking.guest_id, "G1")
        self.assertEqual(self.booking.room_number, 101)
        self.assertEqual(self.booking.status, BookingStatus.CONFIRMED)
        self.assertFalse(self.booking.paid)

    def test_update_booking(self):
        self.booking.update_status(BookingStatus.CHECKED_IN)
        self.assertEqual(self.booking.status, BookingStatus.CHECKED_IN)

    def test_mark_as_paid(self):
        self.booking.mark_as_paid()
        self.assertTrue(self.booking.paid)

    def test_invalid_checkout_without_payment(self):
        self.booking.update_status(BookingStatus.CHECKED_OUT)
        self.assertNotEqual(self.booking.status, BookingStatus.CHECKED_OUT)

    def test_checkout_after_payment(self):
        self.booking.mark_as_paid()
        self.booking.update_status(BookingStatus.CHECKED_OUT)
        self.assertEqual(self.booking.status, BookingStatus.CHECKED_OUT)

    def test_total_price_calculation(self):
        self.assertEqual(self.booking.calculate_total_price(), 4 * 100)

    def test_cancel_booking(self):
        self.booking.cancel_booking()
        self.assertEqual(self.booking.status, BookingStatus.CANCELLED)
        self.assertTrue(self.room.available)

    def test_simple(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
