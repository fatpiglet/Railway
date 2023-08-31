from login import *
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
