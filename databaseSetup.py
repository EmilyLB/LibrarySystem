import sqlite3
from sqlite3 import Error
from datetime import date

# This file is only used if the database file needs to be setup or edited. I have added in values into the database already so it does not need to be run.

# Connect to database
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Gets information from the database
def get_entry(conn, get_entry_sql):
    try:
        c = conn.cursor()
        c.execute(get_entry_sql)

        results = c.fetchall()

        for res in results:
            print(res)
    except Error as e:
        print(e)

# Adds to the database
def add_entry(conn, add_sql):
    try:
        c = conn.cursor()
        c.execute(add_sql)
        conn.commit()
    except Error as e:
        print(e)

def populateDatabase(conn):

    # I left these commands here so that you can see how I was adding to and removing items from the database

    sql_add_book = """INSERT INTO Books
                        (book_title, book_description)
                        VALUES
                        ('The Wheel of Time Book 1', 'Fantasy')"""
    
    # add_entry(conn, sql_add_book)

    sql_add_user = """INSERT INTO Users
                        (first_name, last_name, email, password)
                        VALUES
                        ('Emily', 'Lopez', 'anemail@address.com', 'password22')"""
    # add_entry(conn, sql_add_user)

    sql_add_outgoing = """INSERT INTO Outgoing
                            (user_ID, book_ID, return_date)
                            VALUES
                            (1, 3, '2023-08-30')"""
    # add_entry(conn, sql_add_outgoing)

    sql_delete = """DELETE FROM Users WHERE user_ID=3"""
    # add_entry(conn, sql_delete)


def main():
    database = ".\librarydb.sqlite"

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS Users (
                                    user_ID integer PRIMARY KEY AUTOINCREMENT,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    email text NOT NULL,
                                    password text NOT NULL
    );"""

    sql_create_books_table = """CREATE TABLE IF NOT EXISTS Books (
                                    book_ID integer PRIMARY KEY AUTOINCREMENT,
                                    book_title text NOT NULL,
                                    book_description text NOT NULL
    );"""

    sql_create_outgoing_table = """CREATE TABLE IF NOT EXISTS Outgoing (
                                    outgoing_ID integer PRIMARY KEY AUTOINCREMENT,
                                    user_ID integer NOT NULL,
                                    book_ID integer NOT NULL,
                                    return_Date text NOT NULL,
                                    FOREIGN KEY (user_ID) REFERENCES Users (user_ID),
                                    FOREIGN KEY (book_ID) REFERENCES Books (book_ID)
    );"""


    conn = create_connection(database)
    create_table(conn, sql_create_users_table)
    create_table(conn, sql_create_books_table)
    create_table(conn, sql_create_outgoing_table)

    # populateDatabase(conn) - Only needed when needing to edit the database




if __name__ == '__main__':
    main()