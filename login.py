import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="railway_db"
)
cursor = db.cursor(buffered=True)


# main login page
def login_pg():
    print("+---SELECT THE DESIRED OPTION---+")
    print("|            1.Login            |")
    print("|       2.Forgot Password       |")
    print("|      3.Register Account       |")
    print("+-------------------------------+")
    choice_1 = int(input(">"))
    return choice_1


# login function
def login():
    username = input("Enter Your Username : ")
    pass_word = input("Enter Your Password : ")
    cursor.execute("SELECT * FROM users WHERE Username = %s AND Password = %s", (username, pass_word))
    user = cursor.fetchall()
    if user:
        print("=============== SUCCESSFULLY LOGGED IN ===============")
    else:
        print("Invalid credentials. Please try again.")
        login()


# password function
def password(user, phno):
    ps_wd = input("Enter Password       : ")
    confirm_pass_word = input("Enter Password Again : ")
    if ps_wd == confirm_pass_word:
        cursor.execute("INSERT INTO users (Username, Password, Phone_No) VALUES (%s, %s, %s)", (user, ps_wd, phno))
        db.commit()
        return True
    else:
        return False


# register account function
def register():
    username = input("Enter Your Username  : ")
    cursor.execute("SELECT * FROM users WHERE Username = %s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        print("Username already taken. Please choose another.")
        register()
    else:
        phone_no = input("Enter Your Phone No. : ")
        if password(username, phone_no):
            print("================ ACCOUNT SUCCESSFULLY REGISTERED =================")
        else:
            print("Passwords do not match. Try again")
            password(username, phone_no)


# forgot password function
def forgot_password():
    username = input("Enter Your Username  : ")
    phone_no = input("Enter Your Phone No. :")
    cursor.execute("SELECT * FROM users WHERE Username = %s AND Phone_No = %s", (username, phone_no))
    user = cursor.fetchone()
    cursor.execute("DELETE FROM users WHERE Username = %s", (username,))
    db.commit()
    if user:
        if password(username, phone_no):
            print("=============== PASSWORD SUCCESSFULLY CHANGED ===============")
        else:
            print("Passwords do not match. Try again")
            password(username, phone_no)
    else:
        print("Invalid credentials. Please try again")

login_pg()
login()
register()
forgot_password()
