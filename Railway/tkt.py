"""
import mysql.connector

# Establishing connection to mysql database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="railway_db"
)

# Creating a cursor object to interact with the database
cursor = db.cursor(buffered=True)
"""

import calendar
import datetime
from tabulate import tabulate

total_fare = 0


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
    d1 = '%' + departure.upper() + '%'  # returns for sql query
    arrival = input("FROM:")
    a1 = '%' + arrival.upper() + '%'  # returns for sql query
    jdate = input("Enter journey date (YYYY-MM-DD): ")  # gives journey date  Eg: 2023-10-15
    print()

    def fare(train):  # function return the fare of a train
        d = 0
        query1 = 'SELECT Distance FROM ' + train + ' WHERE Station_code LIKE %s OR Station_code LIKE %s'  # query for returning distance btw the stations
        parameter1 = (d1, a1)
        cursor.execute(query1, parameter1)
        for i in cursor.fetchall():
            for j in i:
                d = j - d
        abs(d)  # returns only positive value of the fare
        d = d * 0.48
        cursor.execute('UPDATE Trains SET fare = %s WHERE Train = %s', (d, train))  # updates fare into trains table
        return d

    fare('train_0001')
    fare('train_0002')
    date: int = datetime.datetime.strptime(jdate, '%Y-%m-%d').weekday()
    day = calendar.day_abbr[date]  # returns the day when date is given Eg:Wed
    da1 = '%' + day + '%'  # returns for sql query

    query2: str = ('SELECT Train_name,Train_no,Seats_available,Fare FROM Trains WHERE Days_running LIKE %s  AND '
                   'Stations LIKE %s AND Stations LIKE %s')  # returns train name, train no., seats available and fare by checking the day and stations when the trains is running
    parameter2 = (da1, d1, a1)
    cursor.execute(query2, parameter2)
    row = cursor.fetchall()  # returns all the trains on given date and btw stations
    if not row:
        print("NO AVAILABLE TRAINS!!!")
        return True
    else:
        header = ["Train", "Train no.", "Available Seats", "Fare"]
        print(tabulate(row, headers=header))

    def ins_passenger():  # function for inserting the passenger details into table
        train = int(input('Enter train no: '))  # contains train no
        passenger_details = []  # for query
        passenger_details1 = []  # for displaying
        passenger_no = int(input('Enter number of Passengers: '))
        cursor.execute('SELECT Train FROM Trains WHERE Train_no = %s', (train,))
        train1 = cursor.fetchone()
        train1 = ''.join(train1)  # gives the train table name
        cursor.execute('SELECT Station_name FROM ' + train1 + ' WHERE Station_code = %s', (arrival,))
        arr = cursor.fetchone()
        arr = ''.join(arr)  # gives to station name
        cursor.execute('SELECT Station_name FROM ' + train1 + ' WHERE Station_code = %s', (departure,))
        dep = cursor.fetchone()
        dep = ''.join(dep)  # gives from station name
        cursor.execute('SELECT Train_name FROM Trains WHERE Train_no = %s', (train,))
        train2 = cursor.fetchone()
        train2 = ''.join(train2)  # gives train name
        global total_fare
        f = round(fare(train1))
        total_fare = f * passenger_no  # gives total fare

        while passenger_no > 0:
            passenger_name = input('Enter Passenger Name: ')
            passenger_age = int(input('Enter Passenger Age: '))
            passenger_gender = input('Enter Passenger Gender(M/F/O): ')
            passenger_details += [
                (passenger_name, passenger_age, passenger_gender, jdate, dep, arr, train, train2, f), ]
            passenger_details1 += [[passenger_name, passenger_age, passenger_gender]]
            passenger_no -= 1
        print()
        header1 = ['Train No.', 'Train Name', 'From', 'To', 'Total Fare']
        main_details = [[train, train2, dep, arr, total_fare]]
        print(tabulate(main_details, headers=header1, tablefmt='github'), end='\n')
        header2 = ['Passenger Name', 'Passenger Age', 'Passenger Gender']
        print()
        print(tabulate(passenger_details1, headers=header2, tablefmt='github'), end='\n')
        print()
        confirm = input('Confirm ticket (Y/N): ')
        print()
        if confirm.upper() == 'Y':
            query3 = ("INSERT INTO tickets (Name, Age, Gender, Journey_date, Departure, Arrival, Train_no, Train_name, "
                      "Fare ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.executemany(query3, passenger_details)  # inserts multiple records into tickets table
            print()
        else:
            print('Enter passenger details again!!!')
            ins_passenger()

    print()
    ins_passenger()
    db.commit()


def payment():
    print('Choose payment method: ')
    print('+-----------------------+')  # displays payment methods
    print('|         1.UPI         |')
    print('|     2.CREDIT CARD     |')
    print('|    3.CANCEL PAYMENT   |')
    print('+-----------------------+')
    opt = int(input('>'))  # input payment method
    print()
    if opt == 1:
        print('============UPI===========')

        def check():  # user to check whether upi is correct
            upi = input('Enter full UPI id: ')
            print('Check whether UPI id is correct')
            print()
            print(upi)
            print()
            upi_check = input('Enter Y if UPI is correct')
            print()
            if upi_check.upper() == 'Y':
                return True
            else:
                check()
                return True
        if check():
            print()
            print('deductible amount is ', total_fare)
            print()
            confirm_pay = input('Confirm payment (Y/N)')
            print()
            if confirm_pay.upper() == 'Y':
                print('Rs.', total_fare, 'deducted from your account')
            else:
                payment()
    elif opt == 2:
        print()


payment()
