import unittest
from models_rooms.room import Room

class TestRoom(unittest.TestCase):

    def setUp(self):
        Room.rooms = {}
        self.room = Room(101, "Single", 100, available=True)

    def test_room_initialization(self):
        self.assertEqual(self.room.number, 101)
        self.assertEqual(self.room.room_type, "Single")
        self.assertEqual(self.room.price, 100)
        self.assertEqual(self.room.available, True)
        self.assertIn(101, Room.rooms)

    def test_update_room(self):
        self.room.update_room(number=102, room_type="Double", price=150, available=False)
        self.assertEqual(self.room.number, 102)
        self.assertEqual(self.room.room_type, "Double")
        self.assertEqual(self.room.price, 150)
        self.assertEqual(self.room.available, False)

    def test_delete_room(self):
        self.assertTrue(Room.delete_room(101))
        self.assertNotIn(101, Room.rooms)
        self.assertFalse(Room.delete_room(999))  # غير موجود

    def test_list_rooms(self):
        another_room = Room(102, "Double", 200, available=True)
        rooms = Room.list_rooms()
        self.assertEqual(len(rooms), 2)
        self.assertIn(self.room, rooms)
        self.assertIn(another_room, rooms)

    def test_to_dict(self):
        expected = {
            "number": 101,
            "room_type": "Single",
            "price": 100,
            "available": True
        }
        self.assertEqual(self.room.to_dict(), expected)

    def test_from_dict(self):
        data = {
            "number": 103,
            "room_type": "Suite",
            "price": 300,
            "available": False
        }
        room = Room.from_dict(data)
        self.assertEqual(room.number, 103)
        self.assertEqual(room.room_type, "Suite")
        self.assertEqual(room.price, 300)
        self.assertEqual(room.available, False)

    def test_repr(self):
        expected = "ROOM 101\nType:Single, Price:$100, Available: Available\n"
        self.assertEqual(repr(self.room), expected)

if __name__ == '__main__':
    unittest.main()
