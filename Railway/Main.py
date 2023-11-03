import calendar
import datetime
from tabulate import tabulate
from random import *
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


# main login page
def login_pg():
    print()
    print("+---SELECT THE DESIRED OPTION---+")
    print("|            1.Login            |")
    print("|       2.Forgot Password       |")
    print("|      3.Register Account       |")
    print("+-------------------------------+")
    print("Enter your desired option (1/2/3)")
    choice_1 = int(input(">"))
    return choice_1


# login function
def login(db, cursor):
    username = input("Enter Your Username : ")
    pass_word = input("Enter Your Password : ")
    cursor.execute("SELECT * FROM users WHERE Username = %s AND Password = %s", (username, pass_word))
    user = cursor.fetchall()
    if user:
        print("=============== SUCCESSFULLY LOGGED IN ===============")
    else:
        print("Invalid credentials. Please try again.")
        login(db, cursor)


# password function
def password(user, phno, db, cursor):
    ps_wd = input("Enter Password       : ")
    confirm_pass_word = input("Enter Password Again : ")
    if ps_wd == confirm_pass_word:
        cursor.execute("INSERT INTO users (Username, Password, Phone_No) VALUES (%s, %s, %s)", (user, ps_wd, phno))
        db.commit()
        return True
    else:
        return False


# register account function
def register(db, cursor):
    def registered(ph_no):
        if password(username, ph_no, db, cursor) is False:
            print("Passwords do not match. Try again")
            registered(ph_no)
            return False
        else:
            print("================ ACCOUNT SUCCESSFULLY REGISTERED =================")
            return True

    username = input("Enter Your Username  : ")

    cursor.execute("SELECT * FROM users WHERE Username = %s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        print("Username already taken. Please choose another.")
        register(db, cursor)
    else:
        phone_no = input("Enter Your Phone No. : ")
        if registered(phone_no) is False:
            pass


# forgot password function
def forgot_password(db, cursor):
    def changed():
        if password(username, phone_no, db, cursor) is False:
            print("Passwords do not match. Try again")
            changed()
            return False
        else:
            print("=============== PASSWORD SUCCESSFULLY CHANGED ===============")
            return True

    username = input("Enter Your Username  : ")
    phone_no = input("Enter Your Phone No. : ")
    cursor.execute("SELECT * FROM users WHERE Username = %s AND Phone_No = %s", (username, phone_no))
    user = cursor.fetchone()
    db.commit()
    if user:
        cursor.execute("DELETE FROM users WHERE Username = %s", (username,))
        if changed() is False:
            pass
    else:
        print("Invalid credentials. Please try again")
        forgot_password(db, cursor)


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

        def generate_pnr():
            pnr1 = ''
            for i in range(6):
                pnr1 += ''.join(choice('0123456789'))
            cursor.execute("SELECT PNR FROM tickets WHERE PNR = %s", (pnr1,))
            if cursor.rowcount > 0:
                generate_pnr()
            else:
                return pnr1

        pnr2 = generate_pnr()

        while passenger_no > 0:
            passenger_name = input('Enter Passenger Name: ')
            passenger_age = int(input('Enter Passenger Age: '))
            passenger_gender = input('Enter Passenger Gender(M/F): ')
            passenger_details += [
                (pnr2, passenger_name, passenger_age, passenger_gender, jdate, dep, arr, train, train2, f), ]
            passenger_details1 += [[passenger_name, passenger_age, passenger_gender]]
            passenger_no -= 1
        print()
        print('YOUR PNR is :', pnr2)
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
            query3 = (
                "INSERT INTO tickets (PNR, Name, Age, Gender, Journey_date, Departure, Arrival, Train_no, Train_name, "
                "Fare ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.executemany(query3, passenger_details)  # inserts multiple records into tickets table
            print()
            db.commit()
            return True
        else:
            print('Enter passenger details again!!!')
            book(db, cursor)
            db.commit()
            return True

    print()
    if not row:
        print("NO AVAILABLE TRAINS!!!")
        print()
    else:
        header = ["Train", "Train no.", "Available Seats", "Fare"]
        print(tabulate(row, headers=header))
        if ins_passenger():
            return True


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

        def check_upi():  # user to check whether upi is correct
            upi = input('Enter full UPI id: ')
            print('Check whether UPI id is correct')
            print(upi)
            upi_check = input('Enter Y if UPI is correct')
            if upi_check.upper() == 'Y':
                return True
            else:
                check_upi()
                return True

        if check_upi():
            print('deductible amount is ', total_fare)
            confirm_pay = input('Confirm payment (Y/N)')
            if confirm_pay.upper() == 'Y':
                print('Rs.', total_fare, 'deducted from your account')
            else:
                payment()
    elif opt == 2:
        def card_no():
            card_number = input('Enter card no: ')
            if len(card_number) == 16:
                return True
            else:
                print('Invalid card number')
                card_no()
                return True

        def cvv():
            cvv_no = input('Enter CVV number: ')
            if len(cvv_no) == 3:
                return True
            else:
                print('Invalid CVV number')
                cvv()
                return True

        def holder_name():
            name = input("Enter Cardholder's name: ")
            if len(name) != 0:
                return True
            else:
                print('Invalid Name')
                holder_name()
                return True

        print('===========CARD===========')

        def check_card():  # user to check whether card is correct
            if card_no() and holder_name() and cvv():
                input('Enter Expiry date (MM/DD): ')
                return True
            else:
                check_card()
                return True

        if check_card():
            print('deductible amount is ', total_fare)
            confirm_pay = input('Confirm payment (Y/N)')
            if confirm_pay.upper() == 'Y':
                print('Rs.', total_fare, 'deducted from your account')
            else:
                payment()
    elif opt == 3:
        print('Redirecting to main menu!!!')


def cancel(db, cursor):
    print('=========TICKET CANCELLATION=========')
    pnr3 = input('Enter PNR number: ')
    cursor.execute('SELECT * FROM tickets WHERE PNR = %s', (pnr3,))
    row = cursor.fetchall()
    if not row:
        print('No available tickets with the given pnr')
    else:
        header = ['PNR', 'Name', 'Age', 'Gender', 'Journey_date', 'Departure', 'Arrival', 'Train no.', 'Train name',
                  'Fare']
        print(tabulate(row, headers=header))
    tkt_cancel = int(input('Enter number of tickets you want to cancel: '))
    for i in range(tkt_cancel):
        passenger_name = input('Enter passenger name: ')
        confirm = input('Confirm cancellation (Y/N): ')
        if confirm.upper() == 'Y':
            cursor.execute('DELETE FROM tickets WHERE PNR = %s AND Name = %s', (pnr3, passenger_name))
            print(passenger_name, "'s ticket has been cancelled", sep='')
            db.commit()
        else:
            return False


def pnr(cursor):
    print('==============CHECK PNR==============')
    pnr4 = input('Enter PNR: ')
    cursor.execute('SELECT * FROM tickets WHERE PNR = %s', (pnr4,))
    row = cursor.fetchall()
    if not row:
        print('No available tickets with the given pnr')
    else:
        header = ['PNR', 'Name', 'Age', 'Gender', 'Journey_date', 'Departure', 'Arrival', 'Train no.', 'Train name',
                  'Fare']
        print(tabulate(row, headers=header))


print("========================== WELCOME TO IRCTC ==========================")
print()


def loginpage():
    login_page = login_pg()
    if login_page == 1:
        print("========================= LOGIN =========================")
        login(db, cursor)
    elif login_page == 2:
        print("==================== FORGOT PASSWORD ====================")
        forgot_password(db, cursor)
        loginpage()
    elif login_page == 3:
        print("==================== REGISTRATION ====================")
        register(db, cursor)
        loginpage()
    else:
        print('INVALID OPTION PLEASE CHOOSE AGAIN')
        loginpage()


def menu():
    print("+-------------MENU-------------+")
    print("|         1. CHECK PNR         |")
    print("|        2. BOOK TICKET        |")
    print("|       3. CANCEL TICKET       |")
    print("|     4. EXIT FROM PROGRAM     |")
    print("+------------------------------+")
    print("Enter your desired option (1/2/3/4)")
    choice_2 = int(input(">"))
    if choice_2 == 1:
        pnr(cursor)
        menu()
    elif choice_2 == 2:
        if book(db, cursor):
            payment()
        menu()
    elif choice_2 == 3:
        if cancel(db, cursor):
            menu()
        else:
            menu()
    elif choice_2 == 4:
        print('Exiting from Program!!!')
        exit()


loginpage()
menu()
