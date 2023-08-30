import sqlite3
from sqlite3 import Error
from datetime import date
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import getpass

# Run this file to access the library system. Interact with the system from the command line.

# Connecting to sqlite database
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        # print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Checking user credentials against those stored in database
def validateUser(username, password):
    # Validate the login credentials
    conn = create_connection(".\librarydb.sqlite")
    try:
        c = conn.cursor()
        c.execute("SELECT user_ID FROM Users WHERE email=? AND password=?", (username, password))
        res = c.fetchall()
        if res != []:
            # Valid user
            return True, str(res[0][0])
        else:
            return False, ""
    except Error as e:
        print(e)
        return False, ""

# Commands that can be used whilst a user is logged in    
def accountInstructions():
    print("Valid instructions: ")
    print("- To view all books in the database, enter: 1")
    print("- To view all currently available books, enter: 2")
    print("- To view all books due to be returned today, enter: 3")
    print("- To view all books currently on loan, enter: 4")
    print("- To view the books you currently have on loan, enter: 5")
    print("- To view books that have a picture, enter: 6")
    print("- To view this information again, enter: 7")
    print("- To logout, enter: 8")

# Used when the SQL query does not require variables
def simpleSQLQuery_getting_books(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        for res in results:
            print("Book Title:",res[0])
            print("Book Description:",res[1])
            print()
    except Error as e:
        print(e)

# Add a new user to the database
def add_user(fName, lName, email, password):
    # Add user
    conn = create_connection(".\librarydb.sqlite")
    c = conn.cursor()
    c.execute("INSERT INTO Users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
              (fName, lName, email, password))
    conn.commit()
    
    # Get user_ID
    _,userID = validateUser(email, password)
    return userID

# Output all books currently on loan
def get_all_books_on_loan(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM Outgoing")
        outgoingInfo = c.fetchall()
        for i in range(len(outgoingInfo)):
            # Find borrower info
            c.execute("SELECT first_name, last_name, email FROM Users WHERE user_ID=?", (str(outgoingInfo[i][1])))
            borrower = c.fetchall()
            # Find book info
            c.execute("SELECT book_title, book_description FROM Books WHERE book_ID=?", (str(outgoingInfo[i][2])))
            book = c.fetchall()
            # Output info to user
            print("Book Title:", book[0][0])
            print("Book Description:", book[0][1])
            print("Return Date:", outgoingInfo[i][3])
            # Find correct borrower information
            print("Borrower Details: first name = "+borrower[0][0]+", last name = "+borrower[0][1]+", email address = "+borrower[0][2])
            print()
    except Error as e:
        print(e)

# Output all books currently loaned to logged in user
def get_user_loaned_books(conn, userID):
    try:
        c = conn.cursor()
        c.execute("SELECT book_ID, return_date FROM Outgoing WHERE user_ID=?", (userID))
        results = c.fetchall()
        for res in results:
            c.execute("SELECT book_title, book_description FROM Books WHERE book_ID=?", (str(res[0])))
        booksDue = c.fetchall()
        for i in range(len(booksDue)):
            print("Book Title:", booksDue[i][0])
            print("Book Description:", booksDue[i][1])
            print("Return Date:",results[i][1])
            print()
    except Error as e:
        print(e)

# Output all books out on loan, due today
def get_all_books_due_today(conn):
    today_date = date.today()
    try:
        c = conn.cursor()
        c.execute("SELECT user_ID, book_ID, return_date FROM Outgoing WHERE return_date=?", (today_date,))
        results = c.fetchall()
        ids = []
        userIDs = []
        for res in results:
            userIDs.append(res[0])
            ids.append(res[1])
        for id in ids:
            c.execute("SELECT book_title, book_description FROM Books WHERE book_ID=?", (id,))
        books_due = c.fetchall()
        for uID in userIDs:
            c.execute("SELECT first_name, last_name, email FROM Users WHERE user_ID=?", (uID,))
        users = c.fetchall()
        for i in range(len(books_due)):
            print("Book Title:", books_due[i][0])
            print("Book Description:", books_due[i][1])
            print("Return Date:", today_date)
            print("Borrower Details: first name="+users[i][0]+", last name="+users[i][1]+", email address="+users[i][2])
            print()
    except Error as e:
        print(e)

# Output books that have a picture and show picture
def view_books_with_picture(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT book_title, book_description FROM Books")
        bookTitles = c.fetchall()
        images = os.listdir('.\Images')
        for title in bookTitles:
            name = str(title[0])+'.jpg'
            for image in images:
                if name == image:
                    print("Book Title:",title[0])
                    print("Book Description:",title[1])
                    print()
                    name = "Images/"+name
                    image = mpimg.imread(name)
                    imgplot = plt.imshow(image)
                    plt.show()
                    break
    except Error as e:
        print(e)

# Get user command in account page
def get_command():
    try:
        command = int(input("What would you like to do?: "))
    except:
        print("Please enter a number from 1-8. If you need to see the valid instructions again, enter 7.")
    
    return command

# Main body of the program - user can access this when they have logged in
def accountPage(userID):
    logout = False
    print("\n******************Account Page******************\n")
    accountInstructions()

    conn = create_connection(".\librarydb.sqlite")

    while not logout:

        command = get_command()

        if command == 1:
            query = """SELECT book_title, book_description FROM Books"""
            simpleSQLQuery_getting_books(conn, query)
        elif command == 2:
            # View all currently available books
            query = """SELECT book_title, book_description FROM Books WHERE book_ID NOT IN (SELECT book_ID FROM Outgoing)"""
            simpleSQLQuery_getting_books(conn, query)
        elif command == 3:
            # View all books due back today
            get_all_books_due_today(conn)
        elif command == 4:
            # View all books currently on loan
            get_all_books_on_loan(conn)
        elif command == 5:
            # View books logged in user currently has on loan
            get_user_loaned_books(conn, userID)
        elif command == 6:
            # View books that have a picture
            view_books_with_picture(conn)
        elif command == 7:
            # View instructions again
            accountInstructions()
        elif command == 8:
            logout = True

    return logout

def main():
    print("******************Welcome to Viable Data Library System******************\n")

    leave = False

    while not leave:
        checkIfExistingUser = input("Do you have an account? (y/n): ")
        if checkIfExistingUser == "y":
            # Login page
            username = input("Please enter your username: ")
            password = getpass.getpass("Please enter you password: ") # Hide input
            # Check details
            valid, userID = validateUser(username, password)
            if valid:
                leave = accountPage(userID)
            else:
                print("Incorrect username or password.")

        else:
            checkSignUp = input("Would you like to sign up? (y/n): ")
            if checkSignUp == "y":
                # Sign up page
                fName = input("Please enter your first name: ")
                lName = input("Please enter your last name: ")
                email = input("Please enter your email address (this will be your username): ")
                password = input("Please enter your password: ")
                # Add user to database and move to account page
                userID = add_user(fName, lName, email, password)
                leave = accountPage(userID)
            else:
                leave = True


if __name__ == '__main__':
    main()