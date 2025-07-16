# Hotel Booking System 🏨

A Python-based hotel booking system designed to simulate and manage hotel operations, including guest management, room assignment, and booking records. This project showcases OOP design, CLI interaction, JSON-based data handling, and basic testing.

---

## 📂 Project Structure

<pre>
.
├── data/             → JSON data files (guests, rooms, bookings)
├── data_loader/      → Handles data loading and saving
├── factories/        → Guest creation logic (Factory pattern)
├── manager/          → Central data management logic (Singleton)
├── models_bookings/  → Booking models and logic
├── models_guests/    → Guest models (VIP, Member, etc.)
├── models_rooms/     → Room models
├── services/         → Business logic
├── validators/       → Input validation
├── tests/            → Unit tests
├── cli.py            → Command-line interface
├── run_tests.py      → Script to run tests
└── test_results.log  → Logs from test results
</pre>

---

##  Features

- Guest registration (Regular, VIP, Member)
- Room booking and availability checking
- Booking search and listing
- Persistent data storage using JSON
- Clean and simple command-line interface (CLI)
- Unit tests to validate system logic

---

##  Technologies Used

- **Python 
- **Object-Oriented Programming (OOP)**
- **JSON for data persistence**
- **Command-Line Interface (CLI)**
- **Built-in `unittest` framework**

---

##  Notes

This project was created as part of a learning journey in software development.  
Future improvements may include a graphical user interface (GUI), database support (e.g. SQLite), and user authentication.

---

##  Contributions

Feel free to fork the project, suggest improvements, or open an issue!


