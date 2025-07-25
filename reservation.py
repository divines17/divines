import random
from datetime import datetime, timedelta
import json

# Sample data (initially hardcoded)
trains = [
    {
        "train_number": "101",
        "train_name": "Express 101",
        "from_station": "Station A",
        "to_station": "Station B",
        "departure_time": "10:00",
        "classes": {
            "Sleeper": {"price": 300, "available_seats": 5},
            "2AC": {"price": 700, "available_seats": 2},
            "3AC": {"price": 500, "available_seats": 3},
        },
    },
    {
        "train_number": "102",
        "train_name": "Superfast 102",
        "from_station": "Station B",
        "to_station": "Station C",
        "departure_time": "15:00",
        "classes": {
            "Sleeper": {"price": 250, "available_seats": 3},
            "2AC": {"price": 750, "available_seats": 1},
            "3AC": {"price": 550, "available_seats": 2},
        },
    }
]

# Users data stored in-memory (can be extended to JSON for persistence)
users = {
    "john": {"name": "John", "email": "john@example.com", "password": "password123", "bookings": []},
}

# Generate PNR (unique identifier for booking)
def generate_pnr():
    return random.randint(100000, 999999)

# Search for available trains between two stations
def search_trains(from_station, to_station):
    available_trains = [train for train in trains if train["from_station"] == from_station and train["to_station"] == to_station]
    return available_trains

# Reserve seat for the user in the selected class
def reserve_seat(train, seat_class):
    available_seats = train["classes"][seat_class]["available_seats"]
    if available_seats > 0:
        train["classes"][seat_class]["available_seats"] -= 1
        return True
    else:
        return False

# Book a ticket
def book_ticket(user, train, seat_class):
    # Generate a unique PNR
    pnr = generate_pnr()
    
    # Reserve seat
    if reserve_seat(train, seat_class):
        booking = {
            "pnr": pnr,
            "train_name": train["train_name"],
            "seat_class": seat_class,
            "price": train["classes"][seat_class]["price"],
            "booking_time": datetime.now()
        }
        user["bookings"].append(booking)
        print(f"Booking successful! Your PNR is {pnr}.")
        return pnr
    else:
        print(f"No available seats in {seat_class} class on {train['train_name']}.")
        return None

# View user bookings
def view_bookings(user):
    if user["bookings"]:
        for booking in user["bookings"]:
            print(f"PNR: {booking['pnr']}, Train: {booking['train_name']}, Class: {booking['seat_class']}, Price: {booking['price']}")
    else:
        print("No bookings found.")

# Cancel a booking and apply refund logic
def cancel_booking(user, pnr):
    for booking in user["bookings"]:
        if booking["pnr"] == pnr:
            booking_time = booking["booking_time"]
            current_time = datetime.now()
            time_diff = current_time - booking_time

            if time_diff <= timedelta(days=1):
                refund = booking["price"]
                print(f"Full refund of {refund} is issued.")
            elif time_diff <= timedelta(days=3):
                refund = booking["price"] * 0.5
                print(f"Partial refund of {refund} is issued.")
            else:
                print("No refund available after 72 hours.")
            user["bookings"].remove(booking)
            return True
    print(f"No booking found with PNR {pnr}.")
    return False

# User registration
def register_user():
    username = input("Enter username: ")
    if username in users:
        print("Username already exists. Please try again.")
        return
    name = input("Enter your full name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    users[username] = {"name": name, "email": email, "password": password, "bookings": []}
    print(f"Registration successful! Welcome, {name}.")

# User login
def login_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if username in users and users[username]["password"] == password:
        print(f"Login successful! Welcome back, {users[username]['name']}.")
        return users[username]
    else:
        print("Invalid username or password.")
        return None

# Admin panel for managing trains (optional)
def admin_panel():
    print("Admin Panel:")
    while True:
        print("1. Add Train\n2. Remove Train\n3. View All Bookings\n4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            train_number = input("Enter train number: ")
            train_name = input("Enter train name: ")
            from_station = input("Enter from station: ")
            to_station = input("Enter to station: ")
            departure_time = input("Enter departure time (HH:MM): ")
            classes = {
                "Sleeper": {"price": int(input("Sleeper price: ")), "available_seats": int(input("Sleeper seats available: "))},
                "2AC": {"price": int(input("2AC price: ")), "available_seats": int(input("2AC seats available: "))},
                "3AC": {"price": int(input("3AC price: ")), "available_seats": int(input("3AC seats available: "))}
            }
            new_train = {
                "train_number": train_number,
                "train_name": train_name,
                "from_station": from_station,
                "to_station": to_station,
                "departure_time": departure_time,
                "classes": classes
            }
            trains.append(new_train)
            print(f"Train {train_name} added successfully!")
        
        elif choice == '2':
            train_number = input("Enter the train number to remove: ")
            global trains
            trains = [train for train in trains if train["train_number"] != train_number]
            print(f"Train {train_number} removed successfully!")
        
        elif choice == '3':
            for user in users.values():
                view_bookings(user)
        
        elif choice == '4':
            break

# Main Program Flow
def main():
    while True:
        print("Welcome to the Train Reservation System!")
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            user = login_user()
            if user:
                while True:
                    print("\n1. Search Trains\n2. View Bookings\n3. Cancel Booking\n4. Logout")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        from_station = input("Enter departure station: ")
                        to_station = input("Enter arrival station: ")
                        available_trains = search_trains(from_station, to_station)

                        if available_trains:
                            for i, train in enumerate(available_trains, 1):
                                print(f"{i}. Train {train['train_name']} ({train['train_number']}) - Departure: {train['departure_time']}")
                                for seat_class, details in train["classes"].items():
                                    print(f"  {seat_class}: {details['available_seats']} available, Price: {details['price']}")

                            train_choice = int(input("Select a train: ")) - 1
                            seat_class = inpu_
