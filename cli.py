from datetime import datetime
from models_rooms.room import Room
from models_guests.guest import Guest
from models_guests.MemberGuest import MemberGuest
from models_guests.VIPGuest import VIPGuest
from models_bookings.booking import Booking, BookingStatus
from models_bookings.invoice import Invoice
from services.payment_service import PaymentService
from validators.input_validators import InputValidator 
from manager.manager_singleton import SingletonMeta
from factories.guest_factory import GuestFactory
from data_loader.rooms_data import load_rooms, save_rooms
from data_loader.guest_data import load_guests, save_guests
from data_loader.booking_data import load_bookings, save_bookings

load_rooms()
load_guests()
load_bookings()


class RoomCLI:
    VALID_FEATURES = ["Balcony", "Jacuzzi", "Smoking", "Sea View", "Accessible", "PetFriendly"]

    def add_room(self):
        number = InputValidator.validate_numeric_string("Enter room number: ")
        if number in Room.rooms:
            print(f"Room number {number} already exists! Please enter a different number.")
            return

        room_type = InputValidator.choose_option("Enter room type (single/double/suite): ", ["single", "double", "suite"])
        price = float(InputValidator.validate_int_input("Enter room price: "))

      
        features_input = input(
            f"Enter room features (comma-separated): {', '.join(self.VALID_FEATURES)}\n> "
        )
        features = []
        if features_input:
            features = [f.strip().title() for f in features_input.split(",") if f.strip()]
            invalid = [f for f in features if f not in self.VALID_FEATURES]
            if invalid:
                print(f"Invalid features: {', '.join(invalid)}. These will be ignored.")
                features = [f for f in features if f in self.VALID_FEATURES]

        Room(number, room_type, price, features=features)
        save_rooms()
        print("Room added successfully.")

    def view_all_rooms(self):
        print("\n--- All Rooms ---")
        for room in Room.list_rooms():
            print(room)

    def update_room(self):
        room_number = InputValidator.validate_numeric_string("Enter Room Number to update: ")
        
        room = Room.rooms.get(room_number)
        if not room:
            print("Room not found.")
            return

        room_type = InputValidator.choose_option_withSkip(
            "Enter new type -- Single | Double | Suite -- (leave blank to skip): ",
            ["single", "double", "suite"]
        )
        price = InputValidator.validate_int_input_update("Enter new price (leave blank to skip): ") or None

        availability_input_raw = InputValidator.choose_option_withSkip(
            "Enter new availability (Available/Taken/Maintenance): ",
            list(Room.availability.keys())
        )
        availability_input = Room.availability.get(availability_input_raw) if availability_input_raw else None

       
        features = None
        update_features = input(
            f"Enter features (comma-separated) to update or leave blank to skip: {', '.join(self.VALID_FEATURES)}\n> "
        )

        if update_features:
            features_list = [f.strip().title() for f in update_features.split(",") if f.strip()]
            invalid = [f for f in features_list if f not in self.VALID_FEATURES]

            if invalid:
                print(f"Invalid features: {', '.join(invalid)}. These will be ignored.")
                features_list = [f for f in features_list if f in self.VALID_FEATURES]

            if not features_list:
                print("No valid features provided. Skipping feature update.")
            else:
                action = ""
                while action not in ["1", "2"]:
                    action = input("Do you want to (1) Add to existing features or (2) Replace all features?\n> ").strip()
                    if action not in ["1", "2"]:
                        print("Invalid input. Please enter 1 to add or 2 to replace.")

                if action == "1":
                    features = list(set(room.features + features_list))
                elif action == "2":
                    features = features_list

        
        room.update_room(
            room_type=room_type,
            price=float(price) if price else None,
            available=availability_input,
            features=features
        )

        save_rooms()
        print("Room updated successfully.")


class GuestCLI:

    def register_guest(self):
        guest_id = InputValidator.validate_numeric_string("Enter guest ID: ")
        if guest_id in Guest.guests:
            print(f"Guest with ID {guest_id} already exists!")
            return
        name = InputValidator.validate_alpha_string("Enter full name: ")
        mail = input("Enter email: ")
        phone = InputValidator.validate_numeric_string("Enter phone number: ")

        guest_type = InputValidator.choose_option("Enter guest type (Regular/VIP/Member): ",["Regular","VIP","Member"]).lower()

        from factories.guest_factory import GuestFactory
        guest = GuestFactory.create_guest(guest_type, guest_id, name, mail, phone)
        save_guests()
        print(f"{guest.get_guest_type()} guest '{guest.name}' registered successfully.")

    def view_guest(self):
        guest_id = InputValidator.validate_numeric_string("Enter guest ID: ")
        info = Guest.get_guest_info(guest_id)
        print(info if info else "Guest not found.")

    def update_guest(self):
        guest_id = InputValidator.validate_numeric_string("Enter guest ID to update: ")
        name = InputValidator.validate_alpha_string_update("Enter new name (leave blank to skip): ") or None
        phone_number = InputValidator.validate_numeric_string_update("Enter new phone (leave blank to skip): ") or None
        guest_type = InputValidator.choose_option_withSkip("Enter new Type (Regular/VIP/Member): (leave blank to skip): ",["Regular","VIP","Member"]) or None
        email = input("Enter new Email (leave blank to skip): ") or None
        if Guest.update(guest_id, name=name, phone_number=phone_number, guest_type=guest_type,email=email):
            save_guests()
            print("Guest updated.")
        else:
            print("Guest not found.")

    def remove_guest(self):
        guest_id = input("Enter guest ID to delete: ")
        if Guest.delete_guest(guest_id):
            save_guests()
            print("Guest deleted.")
        else:
            print("Guest not found.")

    def update_preferences(self):
        guest_id = input("Enter guest ID: ")
        guest = Guest.guests.get(guest_id)
        if guest:
            preferences = input("Enter preferences (e.g., room type, allergies, etc.): ")
            guest.update_preferences(preferences)
            save_guests()
            print("Preferences updated.")
        else:
            print("Guest not found.")

    def update_notes(self):
        guest_id = input("Enter guest ID: ")
        guest = Guest.guests.get(guest_id)
        if guest:
            notes = input("Enter notes for guest (e.g., VIP details, special requests): ")
            guest.update_notes(notes)
            save_guests()
            print("Notes updated.")
        else:
            print("Guest not found.")

    def view_all_guests(self):
        if not Guest.guests:
            print("No guests found.")
            return
        for guest in Guest.guests.values():
            print(f"{guest.guest_info()}\n")


class BookingCLI:
    def create_booking(self):
        
        while True:
            booking_id = input("Enter booking ID: ")
            if booking_id in Booking.bookings:
                print(f"Booking with ID {booking_id} already exists!")
            elif not booking_id.strip():
                print("Booking ID cannot be empty.")
            else:
                break

        
        guest_id = InputValidator.validate_numeric_string("Enter guest ID: ")

        
        while True:
            room_number = InputValidator.validate_numeric_string("Enter room number: ")
            room = Room.rooms.get(room_number)

            if not room:
                print("Enter valid Room number.")
                continue

            if not room.available:
                print("Room is not available. Please choose another room.")
                continue
            break


        
        while True:
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            try:
                datetime.strptime(check_in, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        
        while True:
            check_out = input("Enter check-out date (YYYY-MM-DD): ")
            try:
                datetime.strptime(check_out, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        
        try:
            booking = Booking(booking_id, guest_id, room_number, check_in, check_out)
        except Exception as e:
            print(f"Error creating booking: {e}")
            return

        save_bookings()
        save_guests()
        save_rooms()
        print("Booking created.")


    def view_all_bookings(self):
        print("\n--- All Bookings ---")
        for booking in Booking.list_bookings():
            guest = Guest.guests.get(booking.guest_id)
            print(f"Booking ID: {booking.id}, Guest: {guest.name if guest else 'Unknown'}, Room: {booking.room_number}, Dates: {booking.check_in_date} to {booking.check_out_date}, Status: {booking.status.value}")



    def update_booking(self):
        booking_id = input("Enter Booking ID to update: ")
        booking = Booking.bookings.get(booking_id)
        if not booking:
            print("Booking not found.")
            return

        check_in_input = input("New check-in date (YYYY-MM-DD) or blank: ").strip()
        check_out_input = input("New check-out date (YYYY-MM-DD) or blank: ").strip()

        check_in = None
        check_out = None

        try:
            if check_in_input:
                check_in = datetime.strptime(check_in_input, "%Y-%m-%d")
            if check_out_input:
                check_out = datetime.strptime(check_out_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        if Booking.update(booking_id, check_in, check_out):
            save_bookings()
            print("Booking updated.")
        else:
            print("Booking not found.")

    def cancel_or_delete_booking(self):
        booking_id = input("Enter Booking ID to process: ")
        booking = Booking.bookings.get(booking_id)
        if not booking:
            print("Booking not found.")
            return

        print("What would you like to do?")
        print("1. Cancel Booking (Apply cancellation fee)")
        print("2. Delete Booking (Remove permanently)")
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            booking.cancel_booking()
            save_bookings()
            print("Booking has been cancelled. Cancellation fee applied.")
        elif choice == "2":
            Booking.delete_booking(booking_id)
            save_bookings()
            print("Booking has been deleted from the system.")
        else:
            print("Invalid choice.")


    def view_guest_booking_history(self):
        guest_name = input("Guest Name: ")
        guest = next((g for g in Guest.guests.values() if g.name.lower() == guest_name.lower()), None)

        if not guest:
            print("Guest not found.")
            return

        print("=== Bookings for", guest.name, "===")

        if not guest.bookings:
            print("No bookings found.")
            return

        for booking_id in guest.bookings:
            booking = Booking.bookings.get(booking_id)
            if booking:
                room_type = booking.room.room_type if booking.room else "Unknown"
                paid_status = "Yes" if booking.paid else "No"
                status = booking.status.value if hasattr(booking.status, 'value') else booking.status
                print(f"Booking ID: {booking.id}, Room: {room_type}, Check-in: {booking.check_in_date.date()}, Check-out: {booking.check_out_date.date()}, Status: {status}, Paid: {paid_status}")
            else:
                print(f"Booking {booking_id} not found.")

    def update_booking_status(self):
        booking_id = input("Enter Booking ID to update: ")
        booking = Booking.bookings.get(booking_id)
        if not booking:
            print("Booking not found.")
            return

        print("New Status Options: confirmed, checked in, checked out")
        status_input = input("Enter new status: ").strip().lower()


        status_map = {
            "confirmed": BookingStatus.CONFIRMED,
            "checked in": BookingStatus.CHECKED_IN,
            "checked out": BookingStatus.CHECKED_OUT,
        }

        new_status_enum = status_map.get(status_input)
        if not new_status_enum:
            print("Invalid status. Please enter one of the valid options.")
            return

        result = booking.update_status(new_status_enum)

        if result:
        
            if new_status_enum == BookingStatus.CHECKED_IN:
                booking.mark_room_unavailable()
            elif new_status_enum in [BookingStatus.CHECKED_OUT,BookingStatus.CONFIRMED]:
                booking.mark_room_available()

            save_bookings()
            save_rooms()
            save_guests()
            print("Booking status updated successfully.")
        else:
            print("Failed to update booking.")







    def mark_booking_paid(self):
        booking_id = input("Enter Booking ID to mark as paid: ")
        booking = Booking.bookings.get(booking_id)
        if not booking:
            print("Booking not found.")
            return
        
        if booking.paid:
            print("Booking is already marked as paid.")
        else:
            PaymentService.mark_as_paid(booking)
            save_bookings()
            print("Payment marked as completed.")

    def search_bookings_by_date(self):
        date_str = input("Enter Date (YYYY-MM-DD): ")
        try:
            search_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        print("\n=== Bookings on", search_date, "===")
        found = False
        for booking in Booking.bookings.values():
            check_in = booking.check_in_date.date() if not isinstance(booking.check_in_date, str) else datetime.strptime(booking.check_in_date, "%Y-%m-%d").date()
            check_out = booking.check_out_date.date() if not isinstance(booking.check_out_date, str) else datetime.strptime(booking.check_out_date, "%Y-%m-%d").date()

            if check_in <= search_date <= check_out:
                guest_name = booking.guest.name if booking.guest else "Unknown"
                room_type = booking.room.room_type if booking.room else "Unknown"
                print(f"Guest: {guest_name}, Room: {room_type}, Status: {booking.status}")
                found = True

        if not found:
            print("No bookings found.")

    def search_bookings_by_guest(self):
        guest_name = input("Guest Name: ")
        guest = next((g for g in Guest.guests.values() if g.name.lower() == guest_name.lower()), None)
        if not guest:
            print("Guest not found.")
            return

        print("=== Bookings for", guest.name, "===")
        if not guest.bookings:
            print("No bookings found.")
            return

        for booking_id in guest.bookings:
                booking = Booking.bookings.get(booking_id)
                if booking:
                        room = Room.rooms.get(booking.room_number)
                        room_type = room.room_type if room else "Unknown"
                        print(f"Room: {room_type}, Check-in: {booking.check_in_date.date()}, Check-out: {booking.check_out_date.date()}, Status: {booking.status}")
                else:
                        print(f"Booking {booking_id} not found.")

      
class ReportCLI(metaclass=SingletonMeta):
    def view_all_rooms_and_status(self):
        print("\n--- All Rooms and Status ---")
        for room in Room.list_rooms():
            print(f"Room Number: {room.number}, Type: {room.room_type}, Price: {room.price}, Available: {room.available}")

    def view_occupancy_rate(self):
        print("\n--- Occupancy Rate ---")
        total = len(Room.rooms)
        occupied = len([r for r in Room.rooms.values() if r.available == False])
        rate = (occupied / total * 100) if total else 0
        print(f"Occupied: {occupied}/{total} ({rate:.2f}%)")

    def view_upcoming_bookings(self):
        print("\n--- Today's Bookings ---")
        today = datetime.today().date()
        today_found = False
        upcoming_found = False

        for booking in Booking.bookings.values():
            check_in = booking.check_in_date.date()
            guest_name = booking.guest.name if booking.guest else "Unknown"
            room_type = booking.room.room_type if booking.room else "Unknown"

            if check_in == today:
                print(f"[Today] Booking ID: {booking.id}, Guest: {guest_name}, Room: {room_type}, Check-in: {booking.check_in_date.date()}, Check-out: {booking.check_out_date.date()}, Status: {booking.status}")
                today_found = True

        if not today_found:
            print("No bookings for today.")

        print("\n--- Upcoming Bookings ---")
        for booking in Booking.bookings.values():
            check_in = booking.check_in_date.date()
            guest_name = booking.guest.name if booking.guest else "Unknown"
            room_type = booking.room.room_type if booking.room else "Unknown"

            if check_in > today:
                print(f"[Upcoming] Booking ID: {booking.id}, Guest: {guest_name}, Room: {room_type}, Check-in: {booking.check_in_date.date()}, Check-out: {booking.check_out_date.date()}, Status: {booking.status}")
                upcoming_found = True

        if not upcoming_found:
            print("No upcoming bookings.")


class HotelCLI:
    def __init__(self):
        self.room_cli = RoomCLI()
        self.guest_cli = GuestCLI()
        self.booking_cli = BookingCLI()
        self.report_cli = ReportCLI()
        load_rooms()
        load_guests()
        load_bookings()

    def run(self):
        while True:
            print("\n--- Hotel Management System ---")
            print("1. Room Management")
            print("2. Guest Management")
            print("3. Booking Management")
            print("4. Manager Reports")
            print("5. Generate Invoice")
            print("6. Exit")
            choice = input("Select an option: ")
            if choice == "1":
                self.room_menu()
            elif choice == "2":
                self.guest_menu()
            elif choice == "3":
                self.booking_menu()
            elif choice == "4":
                self.report_menu()
            elif choice == "5":
                self.generate_invoice()
            elif choice == "6":
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

    def room_menu(self):
        while True:
            print("\n--- Room Management ---")
            print("1. Add Room")
            print("2. View All Rooms")
            print("3. Update Room Details")
            print("4. Remove Room")
            print("5. Check Room Availability")
            print("6. Back to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.room_cli.add_room()
            elif choice == "2":
                self.room_cli.view_all_rooms()
            elif choice == "3":
                self.room_cli.update_room()
            elif choice == "4":
                self.room_cli.remove_room()
            elif choice == "5":
                self.room_cli.check_room_availability()
            elif choice == "6":
                break
            else:
                print("Invalid choice.")

    def guest_menu(self):
        while True:
            print("\n--- Guest Management ---")
            print("1. Register Guest")
            print("2. View Guest Details")
            print("3. Update Guest Information")
            print("4. Remove Guest")
            print("5. Add & Update Preferences")
            print("6. Add & Update Notes")
            print("7. View All Guests")
            print("8. Back to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.guest_cli.register_guest()
            elif choice == "2":
                self.guest_cli.view_guest()
            elif choice == "3":
                self.guest_cli.update_guest()
            elif choice == "4":
                self.guest_cli.remove_guest()
            elif choice == "5":
                self.guest_cli.update_preferences()
            elif choice == "6":
                self.guest_cli.update_notes()
            elif choice == "7":
                self.guest_cli.view_all_guests()
            elif choice == "8":
                break
            else:
                print("Invalid choice.")

    def booking_menu(self):
        while True:
            print("\n--- Booking Management ---")
            print("1. Create Booking")
            print("2. View All Bookings")
            print("3. Update Booking Dates")
            print("4. Cancel Or Delete Booking")
            print("5. View Guest Booking History")
            print("6. Update Booking Status")
            print("7. Mark Booking as Paid")
            print("8. Search Bookings by Date")
            print("9. Search Bookings by Guest Name")
            print("10. Back to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.booking_cli.create_booking()
            elif choice == "2":
                self.booking_cli.view_all_bookings()
            elif choice == "3":
                self.booking_cli.update_booking()
            elif choice == "4":
                self.booking_cli.cancel_or_delete_booking()
            elif choice == "5":
                self.booking_cli.view_guest_booking_history()
            elif choice == "6":
                self.booking_cli.update_booking_status()
            elif choice == "7":
                self.booking_cli.mark_booking_paid()
            elif choice == "8":
                self.booking_cli.search_bookings_by_date()
            elif choice == "9":
                self.booking_cli.search_bookings_by_guest()
            elif choice == "10":
                break
            else:
                print("Invalid choice.")

    def report_menu(self):
        while True:
            print("\n--- Manager Reports ---")
            print("1. View All Rooms and Status")
            print("2. View Occupancy Rate")
            print("3. View Upcoming Bookings")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.report_cli.view_all_rooms_and_status()
            elif choice == "2":
                self.report_cli.view_occupancy_rate()
            elif choice == "3":
                self.report_cli.view_upcoming_bookings()
            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def generate_invoice(self):
        guest_name = input("Guest Name: ")
        guest = next((g for g in Guest.guests.values() if g.name.lower() == guest_name.lower()), None)

        if not guest:
            print("Guest not found.")
            return

        print("=== Bookings for", guest.name, "===")
        if not guest.bookings:
            print("No bookings found.")
            return

        for booking_id in guest.bookings:
            booking = Booking.bookings.get(booking_id)
            if booking:
                room = Room.rooms.get(booking.room_number)  
                room_type = room.room_type if room else 'Unknown'
                print(f"Booking ID: {booking.id}, Room: {room_type}, Check-in: {booking.check_in_date.date()}, Check-out: {booking.check_out_date.date()}, Status: {booking.status}")
            else:
                print(f"Booking {booking_id} not found.")

        booking_id = input("Enter Booking ID to generate invoice for: ")
        booking = Booking.bookings.get(booking_id)
        if not booking:
            print("Booking not found.")
            return

        invoice = Invoice(booking)
        invoice.print_invoice()


if __name__ == "__main__":
    cli = HotelCLI()
    cli.run()
