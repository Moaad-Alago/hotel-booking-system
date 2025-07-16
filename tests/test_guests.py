import unittest
import os
from models_guests.guest import Guest
from data_loader.guest_data import save_guests, load_guests

class TestGuest(unittest.TestCase):

    def setUp(self):
        Guest.guests = {}
        Guest.guest_number = 1
        self.guest = Guest("123", "Ali", "ali@example.com", "0599999999")

    def test_guest_creation(self):
        self.assertEqual(self.guest.id, "123")
        self.assertEqual(self.guest.name, "Ali")
        self.assertEqual(self.guest.email, "ali@example.com")
        self.assertEqual(self.guest.phone_number, "0599999999")
        self.assertEqual(self.guest.number, 1)

    def test_guest_change(self):
        self.guest.change(name="Omar", phone_number="0588888888")
        self.assertEqual(self.guest.name, "Omar")
        self.assertEqual(self.guest.phone_number, "0588888888")

    def test_guest_update_static(self):
        result = Guest.update("123", name="Khaled", phone_number="0577777777")
        self.assertTrue(result)
        self.assertEqual(self.guest.name, "Khaled")
        self.assertEqual(self.guest.phone_number, "0577777777")

    def test_guest_info(self):

        actual = '\n'.join([line.rstrip() for line in self.guest.guest_info().split('\n')])
        expected = (
            "*Guest ID: 123 | Guest NAME: Ali | Guest PHONE: 0599999999 Guest Type: regular\n"
            "Email: ali@example.com\n"
            "| Preferences:\n"
            "| Notes:"
        )
        self.assertEqual(actual, expected)

    def test_get_guest_info_static(self):
        info = Guest.get_guest_info("123")
        self.assertIn("Ali", info)

    def test_delete_guest(self):
        self.assertTrue(Guest.delete_guest("123"))
        self.assertIsNone(Guest.get_guest_info("123"))

    def test_guest_type_and_discount(self):
        self.assertEqual(self.guest.calculate_discount(), 0)
        self.assertEqual(self.guest.get_guest_type().capitalize(), "Regular")

if __name__ == '__main__':
    unittest.main()
