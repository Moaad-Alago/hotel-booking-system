from datetime import datetime,timedelta
from models_guests.guest import Guest
from models_rooms.room import Room

from enum import Enum

class BookingStatus(Enum):
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked in"
    CHECKED_OUT = "checked out"
    CANCELLED = "cancelled"


class Booking:
    bookings = {}
    booking_counter = 1

    def __init__(self, booking_id, guest_id, room_number, check_in_date, check_out_date):
        self.id = booking_id
        self.guest_id = guest_id
        self.room_number = room_number
        self.cancellation_fee = 0.0

        try:
            if isinstance(check_in_date, str):
                self.check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d").replace(hour=12, minute=0)
            else:
                self.check_in_date = check_in_date.replace(hour=12, minute=0)

            if isinstance(check_out_date, str):
                self.check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d").replace(hour=12, minute=0)
            else:
                self.check_out_date = check_out_date.replace(hour=12, minute=0)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            raise ValueError("Invalid date format. Booking not created.")

        if self.check_out_date <= self.check_in_date:
            print("Check-out date must be after check-in date.")
            raise ValueError("Invalid dates: Check-out before check-in.")

        self.status = BookingStatus.CONFIRMED
        self.paid = False

        self.guest = Guest.guests.get(guest_id)
        self.room = Room.rooms.get(room_number)

        if self.guest and isinstance(self.guest.bookings, list) and self.id not in self.guest.bookings:
            self.guest.bookings.append(self.id)
            print(f"Added booking {self.id} to guest {self.guest.name}")

        Booking.bookings[self.id] = self



    def mark_room_unavailable(self):
        if self.room:
            self.room.available = False
    def mark_room_available(self):
        if self.room:
            self.room.available = True

    def change(self, check_in_date=None, check_out_date=None, status=None):
        if check_in_date is not None:
            self.check_in_date = check_in_date
        if check_out_date is not None:
            self.check_out_date= check_out_date
        if status is not None:
            self.status = status

    @staticmethod
    def update(booking_id, check_in_date=None, check_out_date=None):
        booking = Booking.bookings.get(booking_id)
        if booking:
            booking.change(check_in_date, check_out_date)
            return True
        return False

    def booking_info(self):
        guest = Guest.guests.get(self.guest_id)
        print('====================================')
        print(f"Booking ID: {self.id}")
        print(f"Guest ID: {self.guest_id}")
        print(f"Full Name: {guest.name if guest else 'Unknown'}")
        print(f"Room ID: {self.room_number}")
        print(f"Check-in: {self.check_in_date}")
        print(f"Check-out: {self.check_out_date}")
        print(f"Status: {self.status}")
        print('====================================')

    @staticmethod
    def get_booking_info(booking_id):
        booking = Booking.bookings.get(booking_id)
        if booking:
            booking.booking_info()
        else:
            print("Booking not found.")



    def cancel_booking(self):
        if self.status == BookingStatus.CANCELLED:
            print("Booking is already cancelled.")
            return

        now = datetime.now()
        time_diff = self.check_in_date - now

        if time_diff > timedelta(hours=48):
            self.cancellation_fee = 0.0
        elif time_diff > timedelta(hours=24):
            self.cancellation_fee = self.calculate_total_price() * 0.5
        else:
            self.cancellation_fee = self.calculate_total_price() * 0.8

        self.status = BookingStatus.CANCELLED
        room = Room.rooms.get(self.room_number)
        if room:
            room.available = True

        print(f"Booking cancelled successfully. Cancellation fee: {self.cancellation_fee}")



    @staticmethod
    def delete_booking(booking_id):
        if booking_id in Booking.bookings:
            del Booking.bookings[booking_id]
            return True
        return False


    @staticmethod
    def list_bookings():
        return list(Booking.bookings.values())
    

    def mark_as_paid(self):
        self.paid = True



    def update_status(self, new_status):

        valid_transitions = [BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN, BookingStatus.CHECKED_OUT]

        if not isinstance(new_status, BookingStatus):
            print("Invalid status type passed.")
            return False

        if new_status == self.status:
            print("New status is the same as current status.")
            return False

        if new_status not in valid_transitions:
            print("Invalid booking status.")
            return False

        if new_status == BookingStatus.CHECKED_OUT and not self.paid:
            print("Cannot checkout before payment...")
            return False

        self.cancellation_fee = 0.0
        self.status = new_status
        return True

    def to_dict(self):
        room = Room.rooms.get(self.room_number)
        room_price = room.price if room else None
        total_price = self.calculate_total_price() if room else None

        return {
            'booking_id': self.id,
            'guest_id': self.guest_id,
            'guest_name': self.guest.name if isinstance(self.guest, Guest) else str(self.guest_id),
            'room_number': self.room_number,
            'check_in_date': self.check_in_date.strftime("%Y-%m-%d"),
            'check_out_date': self.check_out_date.strftime("%Y-%m-%d"),
            'status': self.status.value,
            'paid': self.paid,
            'room_price': room_price,
            'total_price': total_price,
            'cancellation_fee': self.cancellation_fee
        }

    
    @staticmethod
    def from_dict(data):
        booking = Booking(
            booking_id=data['booking_id'],
            guest_id=data['guest_id'],
            room_number=data['room_number'],
            check_in_date=datetime.fromisoformat(data['check_in_date']),
            check_out_date=datetime.fromisoformat(data['check_out_date'])
        )

        
        status_str = data.get('status', 'confirmed').strip().lower()
        status_map = {
            "confirmed": BookingStatus.CONFIRMED,
            "checked in": BookingStatus.CHECKED_IN,
            "checked out": BookingStatus.CHECKED_OUT,
        }
        booking.status = status_map.get(status_str, BookingStatus.CONFIRMED)

        booking.paid = data.get('paid', False)
        return booking

    def calculate_total_price(self):
        room = Room.rooms.get(self.room_number) 
        if room:
            nights = (self.check_out_date - self.check_in_date).days
            return nights * room.price
        else:
            print(f"Room {self.room_number} not found for booking {self.id}")
            return 0.0

