"""import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="railway_db"
)
cursor = db.cursor(buffered=True)
"""


# main login page
def login_pg():
    print()
    print("+---SELECT THE DESIRED OPTION---+")
    print("|            1.Login            |")
    print("|       2.Forgot Password       |")
    print("|      3.Register Account       |")
    print("+-------------------------------+")
    print("Enter your desired option (1/2/3/4")
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
