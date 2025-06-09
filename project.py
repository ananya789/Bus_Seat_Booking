import psycopg2
from psycopg2 import Error
from config import DB_CONFIG

class BookingSystem:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("Successfully connected to the database!")
            self.seats = self.initialize_seats()
            self.mark_booked_seats()
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise Exception("Could not connect to database")

    def initialize_seats(self):
        count = 1
        seats = []
        for i in range(15):
            if i < 14:
                seats.append(
                    [str(count + k) for k in range(2)] + [""] * 2 + 
                    [str(count + 2 + k) for k in range(4)]
                )
                count += 6
            else:
                seats.append([str(count + k) for k in range(7)])
        return seats

    def mark_booked_seats(self):
        try:
            # Get all booked seats from the database
            self.cursor.execute("SELECT seat_numbers FROM bookings")
            booked_seats = self.cursor.fetchall()
            
            # Flatten the list of booked seats
            all_booked = []
            for booking in booked_seats:
                all_booked.extend(booking[0])
            
            # Mark seats as booked in the seating arrangement
            for i in range(len(self.seats)):
                for j in range(len(self.seats[i])):
                    if self.seats[i][j] in all_booked:
                        self.seats[i][j] = "*"
        except Error as e:
            print(f"Error marking booked seats: {e}")

    def verify_admin(self, username, password):
        query = """
        SELECT COUNT(*) FROM admin_users 
        WHERE username = %s AND password = %s
        """
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()[0] > 0

    def add_city_and_stops(self, city_name, stops):
        try:
            # Insert city
            self.cursor.execute(
                "INSERT INTO cities (city_name) VALUES (%s) RETURNING id",
                (city_name,)
            )
            city_id = self.cursor.fetchone()[0]
            
            # Insert stops
            for stop in stops:
                self.cursor.execute(
                    "INSERT INTO stops (city_id, stop_name) VALUES (%s, %s)",
                    (city_id, stop)
                )
            self.conn.commit()
            return True
        except Error as e:
            print(f"Error adding city and stops: {e}")
            self.conn.rollback()
            return False

    def check_seat_availability(self, seat_number, pickup, drop):
        self.cursor.execute("""
            SELECT COUNT(*) FROM bookings 
            WHERE %s = ANY(seat_numbers)
            AND pickup_location = %s 
            AND drop_location = %s
        """, (seat_number, pickup, drop))
        return self.cursor.fetchone()[0] == 0

    def save_booking(self, pickup, drop, seats, names, total_fare):
        try:
            self.cursor.execute("""
                INSERT INTO bookings 
                (pickup_location, drop_location, seat_numbers, passenger_names, total_fare)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (pickup, drop, seats, names, total_fare))
            booking_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return booking_id
        except Error as e:
            print(f"Error saving booking: {e}")
            self.conn.rollback()
            return None

    def get_available_routes(self):
        self.cursor.execute("""
            SELECT c.city_name, array_agg(s.stop_name) 
            FROM cities c 
            JOIN stops s ON c.id = s.city_id 
            GROUP BY c.city_name
        """)
        return dict(self.cursor.fetchall())

    def show_seating_arrangement(self):
        print("\nSeating Arrangement:")
        for row in self.seats:
            print(" ".join(seat if seat else "  " for seat in row))
        print()

    def calculate_fare(self, num_seats):
        base_fare = num_seats * 100
        tax = base_fare * 0.16
        return base_fare + tax

    def show_booking_details(self, booking_id):
        try:
            self.cursor.execute("""
                SELECT pickup_location, drop_location, seat_numbers, 
                       passenger_names, total_fare, booking_date
                FROM bookings WHERE id = %s
            """, (booking_id,))
            booking = self.cursor.fetchone()
            
            if booking:
                print("\n=== Booking Details ===")
                print(f"Booking ID: {booking_id}")
                print(f"Pickup Location: {booking[0]}")
                print(f"Drop Location: {booking[1]}")
                print(f"Seat Numbers: {', '.join(booking[2])}")
                print("Passenger Names:")
                for i, name in enumerate(booking[3], 1):
                    print(f"{i}. {name}")
                print(f"Total Fare: ${booking[4]:.2f}")
                print(f"Booking Date: {booking[5]}")
                print("=====================")
        except Error as e:
            print(f"Error retrieving booking details: {e}")

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

def main():
    try:
        booking_system = BookingSystem()
        
        while True:
            print("\n=== Bus Booking System ===")
            mode = input("Select mode: [1] User [2] Admin [3] Exit: ")
            
            if mode == "1":
                # User operations
                routes = booking_system.get_available_routes()
                if not routes:
                    print("No routes available!")
                    continue
                
                print("\nAvailable Routes:")
                for city, stops in routes.items():
                    print(f"{city}: {', '.join(stops)}")
                
                pickup = input("\nEnter pickup location: ")
                drop = input("Enter drop location: ")
                
                try:
                    num_seats = int(input("Enter number of seats (1-91): "))
                    if not (1 <= num_seats <= 91):
                        print("Invalid number of seats!")
                        continue
                except ValueError:
                    print("Please enter a valid number!")
                    continue
                
                booking_system.show_seating_arrangement()
                
                # Book seats
                booked_seats = []
                passenger_names = []
                
                for i in range(num_seats):
                    while True:
                        seat_num = input(f"Enter seat number for passenger {i+1}: ")
                        if booking_system.check_seat_availability(seat_num, pickup, drop):
                            booked_seats.append(seat_num)
                            name = input(f"Enter name for passenger {i+1}: ")
                            passenger_names.append(name)
                            # Update the visual seating arrangement
                            for row_idx in range(len(booking_system.seats)):
                                for col_idx in range(len(booking_system.seats[row_idx])):
                                    if booking_system.seats[row_idx][col_idx] == seat_num:
                                        booking_system.seats[row_idx][col_idx] = "*"
                            break
                        else:
                            print("Seat already booked or invalid! Please choose another seat.")
                
                booking_system.show_seating_arrangement()
                total_fare = booking_system.calculate_fare(num_seats)
                print(f"\nTotal fare: ${total_fare:.2f}")
                
                confirm = input("Confirm booking (y/n)? ").lower()
                if confirm == 'y':
                    booking_id = booking_system.save_booking(pickup, drop, booked_seats, passenger_names, total_fare)
                    if booking_id:
                        print("Booking successful!")
                        booking_system.show_booking_details(booking_id)
                    else:
                        print("Booking failed!")

            elif mode == "2":
                username = input("Enter admin username: ")
                password = input("Enter admin password: ")
                
                if booking_system.verify_admin(username, password):
                    print("\nAdmin login successful!")
                    while True:
                        print("\n1. Add new city and stops")
                        print("2. Logout")
                        admin_choice = input("Enter choice: ")
                        
                        if admin_choice == "1":
                            city_name = input("Enter city name: ")
                            num_stops = int(input("Enter number of stops to add: "))
                            stops = []
                            for i in range(num_stops):
                                stop = input(f"Enter stop {i+1}: ")
                                stops.append(stop)
                            
                            if booking_system.add_city_and_stops(city_name, stops):
                                print("City and stops added successfully!")
                            else:
                                print("Failed to add city and stops.")
                        
                        elif admin_choice == "2":
                            break
                else:
                    print("Invalid credentials!")

            elif mode == "3":
                print("Thank you for using the Bus Booking System!")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()