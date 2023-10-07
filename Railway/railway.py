from Railway.login import *
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
        pnr()
    elif choice_2 == 2:
        book()
    elif choice_2 == 3:
        cancel()
    elif choice_2 == 4:
        exit()
