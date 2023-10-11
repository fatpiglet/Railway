import datetime
import calendar
import mysql.connector
from tabulate import tabulate

# Establishing connection to mysql database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="railway_db"
)

# Creating a cursor object to interact with the database
cursor = db.cursor(buffered=True)


def book(db,cursor):
    print("=========BOOKING TICKET==========")
    departure = input("TO:")
    arrival = input("FROM:")
    jdate = input("Enter journey date (DD/MM/YYYY): ")
    day: int = datetime.datetime.strptime(jdate, '%d/%m/%Y').weekday()
    date = calendar.day_abbr[day]
    query = "SELECT Train_name,Train_no,Seats_available,Fare FROM Trains WHERE Days_running LIKE %(p)s  AND Stations LIKE %(q)s AND Stations LIKE %(r)s"
    cursor.execute(query,{"p": "%{}%".format(date), "q": "%{}%".format(departure), "r": "%{}%".format(arrival)})
    row = cursor.fetchall()
    head = ["Train", "Train no.", "Available Seats", "Fare"]
    print(tabulate(row, headers=head, tablefmt="grid"))

book(db,cursor)