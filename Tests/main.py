import mysql.connector

# Establishing connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mario!#%^!@13",
    database="railway_db"
)

# Creating a cursor object to interact with the database
cursor = db.cursor()


def show_available_trains():
    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    for train in trains:
        print(train)


def make_reservation(user_id, train_id, seat_count):
    # Check if seats are available
    cursor.execute("SELECT available_seats FROM trains WHERE id = %s", (train_id,))
    available_seats = cursor.fetchone()[0]

    if available_seats >= seat_count:
        # Update available seats
        updated_seats = available_seats - seat_count
        cursor.execute("UPDATE trains SET available_seats = %s WHERE id = %s", (updated_seats, train_id))

        # Create reservation entry
        cursor.execute("INSERT INTO reservations (user_id, train_id, seat_count) VALUES (%s, %s, %s)",
                       (user_id, train_id, seat_count))
        db.commit()
        print("Reservation successful!")
    else:
        print("Seats not available for reservation.")


def main():
    while True:
        print("1. Show available trains")
        print("2. Make a reservation")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_available_trains()
        elif choice == "2":
            user_id = int(input("Enter your user ID: "))
            train_id = int(input("Enter the train ID: "))
            seat_count = int(input("Enter the number of seats: "))
            make_reservation(user_id, train_id, seat_count)
        elif choice == "3":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

# Closing the database connection
db.close()
