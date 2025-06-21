# **Bus Seat Booking System**

### **Overview**

The Bus Seat Booking System is a Python-based project that provides a seamless interface for booking bus tickets. It integrates Python and PostgreSQL to manage:
- City routes and stops
- Seat availability
- Booking details for users
- Administrative functionalities, such as adding new cities and stops.

This system also displays a live seating arrangement, marks booked seats, and updates the database dynamically.

---

### **Features**

#### **User Mode**
1. View available city routes and stops.
2. Choose a pickup and drop location.
3. View available seats and book multiple seats for passengers.
4. See total fare and confirm bookings.
5. Real-time updates to the seating arrangement.

#### **Admin Mode**
1. Authenticate with a username and password.
2. Add new cities and stops dynamically.
3. Manage database entries for city routes and stops.

---

### **Technologies Used**
- **Python**
- **PostgreSQL**
- **Psycopg2**: Python library for PostgreSQL integration
- **pgAdmin**: PostgreSQL database management tool

---

### **Setup**

#### **Database Configuration**
1. **Create a PostgreSQL Database**:
   ```sql
   CREATE DATABASE bus_booking;
   ```
2. **Create Tables**:
   ```sql
   -- Admin users table
   CREATE TABLE admin_users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(50) NOT NULL UNIQUE,
       password VARCHAR(50) NOT NULL
   );

   -- Cities table
   CREATE TABLE cities (
       id SERIAL PRIMARY KEY,
       city_name VARCHAR(100) NOT NULL UNIQUE
   );

   -- Stops table
   CREATE TABLE stops (
       id SERIAL PRIMARY KEY,
       city_id INT REFERENCES cities(id),
       stop_name VARCHAR(100) NOT NULL
   );

   -- Bookings table
   CREATE TABLE bookings (
       id SERIAL PRIMARY KEY,
       pickup_location VARCHAR(100),
       drop_location VARCHAR(100),
       seat_numbers TEXT[] NOT NULL,
       passenger_names TEXT[] NOT NULL,
       total_fare DECIMAL(10, 2) NOT NULL,
       booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

3. **Sample Data for Cities and Stops**:
   ```sql
   INSERT INTO cities (city_name) VALUES 
   ('Warangal'), ('Hyderabad'), ('Karimnagar'), ('Nizamabad'), ('Khammam'), ('Mahabubnagar');

   INSERT INTO stops (city_id, stop_name) VALUES
   (1, 'Hanamkonda'), (1, 'Hyderabad'), (1, 'Jangaon'), (1, 'Karimnagar'), (1, 'Parkal'),
   (2, 'Zaheerabad'), (2, 'Sangareddy'), (2, 'Secunderabad'), (2, 'Medchal'), (2, 'Vikarabad'),
   (3, 'Kamareddy'), (3, 'Ramagundam'), (3, 'Nirmal'), (3, 'Siddipet'), (3, 'Mancherial'),
   (4, 'Khammam'), (4, 'Bhadrachalam'), (4, 'Bhainsa'), (4, 'Manuguru'), (4, 'Adilabad'),
   (5, 'Mahabubnagar'), (5, 'Miryalaguda'), (5, 'Kothagudem'), (5, 'Suryapet'), (5, 'Yadagirigutta'),
   (6, 'Mahadevpur'), (6, 'Nalgonda'), (6, 'Nagarkurnool'), (6, 'Gadwal'), (6, 'Medak');
   ```

4. **Add a Default Admin User**:
   ```sql
   INSERT INTO admin_users (username, password) VALUES ('admin', 'admin123');
   ```

---

#### **Run the Application**
1. Clone the repository or download the project files.
2. Configure the database in the `config.py` file:
   ```python
   DB_CONFIG = {
       'dbname': 'bus_booking',
       'user': 'postgres',
       'password': 'your_password',  # Replace with your PostgreSQL password
       'host': 'localhost',
       'port': '5432'
   }
   ```
3. Install dependencies:
   ```bash
   pip install psycopg2
   ```
4. Run the main script:
   ```bash
   python project.py
   ```

---

### **How to Use**

#### **User Mode**
1. Select user mode.
2. View available routes and stops.
3. Enter your pickup and drop locations.
4. Select seats from the available seating arrangement.
5. Confirm the booking and view details.

#### **Admin Mode**
1. Log in with admin credentials.
2. Add new cities and stops.
3. Manage city-stop routes dynamically.

---

### **Folder Structure**
- **config.py**: Configuration file for PostgreSQL connection.
- **db_utils.py**: Utility functions for interacting with PostgreSQL.
- **project.py**: Main application logic, including the `BookingSystem` class and GUI functions.

---

### **Future Enhancements**
1. Add payment gateway integration.
2. Include route-specific fares.
3. Support multi-language localization.

---

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
