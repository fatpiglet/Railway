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


def book(db, cursor):
    data1 = [['AGRA', 'AGC'], ['BHOPAL', 'BPL'], ['BHUSAWAL', 'BSL'], ['CHENNAI', 'MS'], ['COIMBATORE', 'CBE'],
             ['ERNAKULAM', 'ERS'], ['JHANSI', 'JHS'], ['KALYAN', 'KYN']]
    data2 = [['KANPUR', 'CNB'], ['LUCKNOW', 'LJN'], ['MADGAON', 'MAQ'], ['MANGALORE', 'MAJN'], ['NAGPUR', 'NGP'],
             ['NEW DELHI', 'NDLS'], ['SHORANUR', 'SRR'], ['VIJAYAWADA', 'BZA'], ['WARANGAL', 'WL']]
    header = ['Station', 'Station Code']
    table1 = tabulate(data1, headers=header, tablefmt='github')
    table2 = tabulate(data2, headers=header, tablefmt='github')
    print('+--------------------------------------------------------------+')
    print('|                  PLEASE ENTER STATION CODE                   |')
    print(tabulate([[table1, table2]], headers='', tablefmt="simple"))
    print()
    print("======================== BOOKING TICKET ========================")
    print()
    departure = input("TO:")
    arrival = input("FROM:")
    jdate = input("Enter journey date (DD/MM/YYYY): ")
    print()

    def fare(train):
        d = 0
        query1 = 'SELECT Distance FROM ' + train + ' WHERE Station_code LIKE %(q)s OR Station_code LIKE %(r)s'
        parameter1 = {"q": "%{}%".format(departure.upper()), "r": "%{}%".format(arrival.upper())}
        cursor.execute(query1, parameter1)
        for i in cursor.fetchall():
            for j in i:
                d = j - d
        abs(d)
        d = d * 0.48
        cursor.execute('UPDATE Trains SET fare = %s WHERE Train = %s', (d, train))
        return d

    fare('train_0001')
    fare('train_0002')
    date: int = datetime.datetime.strptime(jdate, '%d/%m/%Y').weekday()
    day = calendar.day_abbr[date]

    query2: str = ('SELECT Train_name,Train_no,Seats_available,Fare FROM Trains WHERE Days_running LIKE %(p)s  AND '
                   'Stations LIKE %(q)s AND Stations LIKE %(r)s')
    parameter2 = {"p": "%{}%".format(day), "q": "%{}%".format(departure.upper()), "r": "%{}%".format(arrival.upper())}
    cursor.execute(query2, parameter2)
    row = cursor.fetchall()
    if not row:
        print("NO AVAILABLE TRAINS")
        return True
    else:
        head = ["Train", "Train no.", "Available Seats", "Fare"]
        print(tabulate(row, headers=head))


book(db, cursor)
