import csv
import datetime
from src.swen344_db_utils import *

def rebuildTables():
    """
    Description: execute the sql file and create database
    Args: N/A
    Access: N/A
    Returned: N/A
    """
    exec_sql_file("db-egd1486/library.sql")
    
def get_users():
    """
    Description: get users table
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT * FROM users;"
    return exec_get_all(sql)

def get_books():
    """
    Description: get books table
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT * FROM books;"
    return exec_get_all(sql)

def get_inventory():
    """
    Description: get inventory table
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT * FROM inventory;"
    return exec_get_all(sql)

def get_history():
    """
    Description: get history table
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT * FROM history;"
    return exec_get_all(sql)

def get_user_history_books(userFirstName, userLastName):
    """
    Description: get a user's history of checked out books
    Args:
        userFirstName - String, the user's first name
        userLastName - String, the user's last name
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT h.book_id \
            FROM history h \
            JOIN users u ON h.user_id=u.id \
            WHERE u.first_name=%s AND u.last_name=%s;"
    return exec_get_all(sql, (userFirstName, userLastName))

def get_user_history_books_by_alphabet(userFirstName, userLastName):
    """
    Description: get a user's history of checked out books, sorted by book title ascending
    Args:
        userFirstName - String, the user's first name
        userLastName - String, the user's last name
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT b.title AS title \
            FROM books b \
            JOIN history h ON h.book_id=b.id \
            JOIN users u ON h.user_id=u.id \
            WHERE u.first_name=%s AND u.last_name=%s \
            ORDER BY title ASC;"
    return exec_get_all(sql, (userFirstName, userLastName))

def get_history_books_by_name():
    """
    Description: get the book titles of the checked out books - order by user's first name
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT u.first_name AS name, b.title AS title \
            FROM books b \
            JOIN history h ON h.book_id=b.id \
            JOIN users u ON h.user_id=u.id \
            ORDER BY u.first_name ASC, b.title ASC;"
    return exec_get_all(sql)

def get_books_in_category(category):
    """
    Description: get the name of books in a category
    Args:
        category - String, the book category
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT b.title \
        FROM books b \
        WHERE b.category=%s;"
    return exec_get_all(sql, (category,))

def get_count_books_in_category(category):
    """
    Description: get total amount of books in a category
    Args:
        category - String, the book category
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT COUNT(b.title) \
        FROM books b \
        WHERE b.category=%s;"
    return exec_get_all(sql, (category,))

def get_inventory_total_books():
    """
    Description: get the total amount of books in the inventory 
        (total count of each book across all libraries)
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT b.title, SUM(i.available_count + i.checkout_count) AS total_count \
        FROM inventory i \
        JOIN books b ON b.id=i.book_id \
        GROUP BY b.title \
        ORDER BY b.title;"
    return exec_get_all(sql)

def get_total_available_books():
    """
    Description: get the total amount of books that are available in the inventory
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT SUM(available_count) \
        FROM inventory;"
    return exec_get_all(sql)
    
def get_available_books_by_category():
    """
    Description: get the total amount of books that are available in the inventory, order by category
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT b.category AS category, SUM(i.available_count) AS total_count \
        FROM books b \
        JOIN inventory i ON i.book_id=b.id \
        GROUP BY b.category \
        ORDER BY b.category ASC;"
    return exec_get_all(sql)
    
# DB2
def create_user(userFirstName, userLastName, email):
    """
    Description: insert a new user into the user table
    Args: 
        userFirstName - String, the user's first name
        userLastName - String, the user's last name
        email - String, the user's email
            note: active - Boolean, default is true
    Access: assumes the entry is not already in the database
    Returned: 
        the id of the created user
    """
    sql = "INSERT INTO users (first_name, last_name, email, active) \
        VALUES (%s, %s, %s, DEFAULT) \
        RETURNING id;"
    return exec_insert_returning(sql, (userFirstName, userLastName, email))

def remove_user(email):
    """
    Description: deactivate the user's account
    Args: 
        email - String, the user's email
            note: active - Boolean, default is true
    Access: assumes that emails are unique to each user
    Returned: 
        the user's id, the user's email, the status of the account
    """
    sql = "UPDATE users \
        SET active=FALSE \
        WHERE email=%s \
        RETURNING id, email, active;"
    return exec_returning_all(sql, (email,))

def get_user_id(userFirstName, userLastName):
    """
    Description: get the user id
    Args:
        userFirstName - String, the user's first name
        userLastName - String, the user's last name
    Access: N/A
    Returned: 
        the id of the user
    """
    sql = "SELECT id \
    FROM users \
    WHERE first_name=%s AND last_name=%s;"
    user_id = exec_get_one(sql, (userFirstName, userLastName))
    return user_id

def get_book_id(title, author):
    """
    Description: get the book id
    Args:
        title - String, the title of the book
        author - String, the author(s) of the book
    Access: N/A
    Returned: 
        the id of the book
    """
    sql = "SELECT id \
        FROM books \
        WHERE title=%s AND author=%s;"
    book_id = exec_get_one(sql, (title, author))
    return book_id

def checkout_book(userFirstName, userLastName, title, author, checkout_date, lib_name):
    """
    Description: if the user has overdue books, they can't checkout and their account is deactivated,
        else the user checks out the book, updates the checkout history and the inventory
    Args:
        userFirstName - String, the user's first name
        userLastName - String, the user's last name
        title - String, the title of the book
        author - String, the author(s) of the book
        checkout_date - datetime, the checkout date
        lib_name - String, the specific library name where the book is
    Access: assumes that the book exists and there are available copies of the book
    Returned: 
        User can't checkout - False
        User can checkout - the user's id, book's id, the library's id, the updated status of the book, 
        the checkout date, the return date, and the updated inventory numbers for the book
    """
    user_id = get_user_id(userFirstName, userLastName)
    book_id = get_book_id(title, author)
    library_id = get_library_id(lib_name)
    #check if the account status is active
    isActive = get_user_account_status(user_id)
    if not isActive:
        return False
    #check if the user has any books overdue
    overdue_books = check_overdue_books_by_user(user_id, checkout_date)
    hasOverdueBooks = False
    if overdue_books != None and overdue_books != []:
        hasOverdueBooks = True
    #if they have overdue books, deactivate their account, can't checkout
    if hasOverdueBooks:
        sql0 = "SELECT email \
            FROM users \
            WHERE id=%s;"
        email = exec_get_one(sql0, (user_id, ))
        #check if the account isn't already deactivated
        isActive = get_user_account_status(user_id)
        if isActive:
            remove_user(email)
        return False #"Can't checkout book because you have overdue books."
    #else no overdue books and can checkout
    sql1 = "INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) \
        VALUES (%s, %s, %s, %s, %s, %s, NULL) \
        RETURNING user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date;"
    due_date = create_due_date(checkout_date)
    result1 = exec_returning_all(sql1, (user_id, book_id, library_id, "checked_out", checkout_date, due_date))
    sql2 = "UPDATE inventory \
        SET available_count=available_count-1, checkout_count=checkout_count+1 \
        WHERE book_id=%s AND library_id=%s\
        RETURNING book_id, library_id, available_count, checkout_count;"
    result2 = exec_returning_all(sql2, (book_id, library_id))
    return result1, result2

def return_book(userFirstName, userLastName, title, author, return_date, lib_name):
    """
    Description: the user returns the book, updates the checkout history and the inventory, 
        if it is returned late a message will be printed
    Args:
        userFirstName - String, the user's first name
        userLastName - String, the user's last name
        title - String, the title of the book
        author - String, the author(s) of the book
        return_date - datetime, the return date
        lib_name - String, the specific library name where the book is
    Access: assumes the user has previously checked out the book
    Returned:
        the user's id, the book's id, the library's id, the updated status of the book, the checkout date, the return date, 
        and the updated inventory numbers for the book
    """
    user_id = get_user_id(userFirstName, userLastName)
    book_id = get_book_id(title, author)
    library_id = get_library_id(lib_name)
    #get the due date
    sql0 = "SELECT due_date \
        FROM history \
        WHERE user_id=%s AND book_id=%s;"
    due_date = exec_get_one(sql0, (user_id, book_id))[0]
    #check if the book has been returned past the due date
    status_tag = "returned"
    if due_date < return_date:
        status_tag = "late_return"
        day_diff = str((return_date - due_date).days)
        late_fee = str(calculate_late_fee(due_date, return_date))
        print()
        print("You returned your book " + day_diff + " days late. You have a late fee of $" + late_fee)
    #check if the user has an overdue books
    overdue_books = check_overdue_books_by_user(user_id, return_date)
    hasOverdueBooks = False
    if overdue_books != None and overdue_books != []:
        hasOverdueBooks = True
    #if no overdue books and the users account is not active
    if not hasOverdueBooks:
        #check if the user's account is active already
        isActive = get_user_account_status(user_id)
        if not isActive:
            sql0 = "UPDATE users \
                SET active=TRUE \
                WHERE id=%s;"
            exec_commit(sql0, (user_id, ))
    sql1 = "UPDATE history \
        SET status_tag=%s, return_date=%s \
        WHERE user_id=%s AND book_id=%s AND library_id=%s \
        RETURNING user_id, book_id, library_id, status_tag, checkout_date, return_date;"
    result1 = exec_returning_all(sql1, (status_tag, return_date, user_id, book_id, library_id))
    sql2 = "UPDATE inventory \
        SET available_count=available_count+1, checkout_count=checkout_count-1 \
        WHERE book_id=%s AND library_id=%s\
        RETURNING book_id, library_id, available_count, checkout_count;"
    result2 = exec_returning_all(sql2, (book_id, library_id))
    return result1, result2

def reserve_book(userFirstName, userLastName, title, author, lib_name):
    """
    Description: the user reserves a book at the specified library
    Args: 
        userFirstName - String, the user's first name
        userLastName - String, the user's last name
        title - String, the title of the book
        author - String, the author(s) of the book
        lib_name - String, the specific library name where the book is
    Access: N/A
    Returned: 
        on success, the user's id, the book's id, and the library's id
        on fail, the book id
    """
    user_id = get_user_id(userFirstName, userLastName)
    book_id = get_book_id(title, author)
    library_id = get_library_id(lib_name)
    
    sql = "SELECT available_count \
        FROM inventory \
        WHERE book_id = %s AND library_id=%s;"
    result1 = exec_get_all(sql, (book_id, library_id))
    #check that there are no available copies
    if result1 == [(0,)]: 
        sql2 = "INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) \
        VALUES (%s, %s, %s, %s, NULL, NULL, NULL) \
        RETURNING user_id, book_id, library_id;"
        return exec_returning_all(sql2, (user_id, book_id, library_id, "reserved"))
    else: #has available copies
        return book_id
    
def read_csv():
    """
    Description: reads a csv, parses it, and inserts the data into the database (for multi library system)
    Args: N/A
    Access: N/A
    Returned: N/A
    """
    path = "db-egd1486/data.csv"
    full_path = os.path.join(os.path.dirname(__file__), f'../../{path}')
    with open(full_path, 'r') as file:
        content = csv.reader(file, quotechar='"')
        books_lst = []
        copies_lst = []
        for line in content:
            if (line[0] == "Title"):
                continue #skip first line of csv
            # title, authors, category, genre, publish_date, summary
            books_lst.append([line[0], line[1], line[3], line[4], line[2]])
            copies_lst.append(line[5]) #copies
        #insert into books
        sql1 = "INSERT INTO books (title, author, category, genre, publish_date, summary) \
            VALUES (%s, %s, %s, %s, NULL, %s) RETURNING id;"
        book_ids_lst = exec_list(sql1, books_lst)
        #get list of libraries
        sql2 = "SELECT id FROM libraries;"
        libraries_list = exec_get_all(sql2)
        #create list for inventory
        inventory_lst = []
        c = 0
        for i in range(len(book_ids_lst)):
            inventory_lst.append([book_ids_lst[i], copies_lst[i], libraries_list[c]])
            if c == 3:
                c = 0
            else: 
                c = c + 1
        #insert into inventory
        sql2 = "INSERT INTO inventory (book_id, available_count, checkout_count, library_id) \
            VALUES (%s, %s, 0, %s) RETURNING book_id;"
        exec_list(sql2, inventory_lst)

# # another way (for single system library)
# import pandas as pd
# def read_csv():
#     path = "db-egd1486/data.csv"
#     full_path = os.path.join(os.path.dirname(__file__), f'../../{path}')
#     data = pd.read_csv(full_path, sep=',', quotechar='"')
#     iterate = len(data['Title'])
#     for i in range(iterate):
#         title = data['Title'][i]
#         authors = data['Author(s)'][i]
#         summary = data['Comments'][i]
#         category = data['Category'][i]
#         genre = data['Sub-category'][i]
#         copies = int(data['Copies'][i])
#         sql1 = "INSERT INTO books (title, author, category, genre, publish_date, summary) \
#             VALUES (%s, %s, %s, %s, NULL, %s) RETURNING id;"
#         book_id = exec_insert_returning(sql1, (title, authors, category, genre, summary))
#         sql2 = "INSERT INTO inventory (book_id, available_count, checkout_count) \
#             VALUES (%s, %s, 0);"
#         exec_commit(sql2, (book_id, copies))
#     return 

def search_for_book_by_title(title):
    """
    Description: a user can search for a book by title
    Args:
        title - String, the title of the book
    Access: N/A
    Returned: 
        if the book is available, then the number of available copies
        if the book isn't available, then 0
    """
    sql1 = "SELECT id \
        FROM books \
        WHERE title=%s;"
    book_id = exec_get_one(sql1, (title,))
    if book_id:
        sql2 = "SELECT available_count \
            FROM inventory \
            WHERE book_id=%s;"
        result = exec_get_one(sql2, (book_id,))
        return result
    else: 
        return 0

def get_list_checkout_books():
    """
    Description: gets list of checked out books sorted by genre and author
    Args: N/A
    Access: N/A
    Returned:
        the user's first name, the book's title, the checkout date, the return date (if exists), the available copy count
    """
    sql = "SELECT u.first_name, b.title, checkout_date, return_date, SUM(i.available_count) as total_copies \
        FROM history h \
        JOIN users u ON h.user_id=u.id \
        JOIN books b ON h.book_id=b.id \
        JOIN inventory i ON h.book_id=i.book_id \
        GROUP BY u.first_name, b.title, checkout_date, return_date \
        ORDER BY u.first_name ASC, b.title ASC;" 
    return exec_get_all(sql)

# DB3
def get_library_id(lib_name):
    """
    Description: get the library id
    Args:
        lib_name - String, the name of the library
    Access: N/A
    Returned: 
        the id of the library
    """
    sql = "SELECT id \
        FROM libraries \
        WHERE lib_name=%s;"
    library_id = exec_get_one(sql, (lib_name,))
    return library_id

def get_libraries():
    """
    Description: get libraries table
    Args: N/A
    Access: N/A
    Returned: psycopg2 result set
    """
    sql = "SELECT * FROM libraries;"
    return exec_get_all(sql)

def create_due_date(checkout_date):
    """
    Description: calculate the due date (2 weeks after the checkout date)
    Args:
        checkout_date - datetime, the checkout date
    Access: N/A
    Returned:
        due_date - datetime, the due date 
    """
    added_time = datetime.timedelta(weeks=2)
    due_date = checkout_date + added_time
    return due_date

def check_overdue_books_by_user(user_id, today_date):
    """
    Description: Check if any of the specificed user's books are overdue
    Args: 
        user_id - Unique Integer, the specific user
        today_date - datetime, today's date
    Access: only users can check their own account
    Returned: 
        the book id, the checkout date, the due date, and the return date
    """
    sql = "UPDATE history \
        SET status_tag='overdue' \
        WHERE due_date < %s AND user_id=%s AND status_tag='checked_out' \
        RETURNING book_id, checkout_date, due_date, return_date"
    return exec_returning_many(sql, (today_date, user_id))

def get_user_account_status(user_id):
    """
    Description: Get the specified user's account status
    Args:
        user_id - Unique Integer, the specific user
    Access: N/A
    Returned:
        the specified user's account status (TRUE or FALSE)
    """
    sql = "SELECT active \
    FROM users \
    WHERE id=%s;"
    return exec_get_one(sql, (user_id,))[0]

def add_book(title, author, category, genre, publish_date, summary):
    """
    Description: add book to book table
    Args:
        title - String, the title of the book
        author - String, the author(s) of the book
        category - String, the category of the book, Fiction or Non-Fiction
        genre - String, the genre of the book
        publish_date - datetime, when the book was published
        summary - String, one line description of the book
    Access: N/A
    Returned: 
        the id of the book
    """
    sql = "INSERT INTO books (title, author, category, genre, publish_date, summary) \
        VALUES (%s, %s, %s, %s, %s, %s) \
        RETURNING id;"
    return exec_insert_returning(sql, (title, author, category, genre, publish_date, summary))

def add_book_to_library(title, author, available_count, lib_name):
    """
    Description: add copies of a book to different libraries
    Args: 
        title - String, the title of the book
        author - String, the author(s) of the book
        available_count - Integer, the number of copies
        lib_name - String, the library name
    Access: assumes the book id and library id exist
    Returned:
        the book id, the library id, and the number of copies
    """
    book_id = get_book_id(title, author)
    library_id = get_library_id(lib_name)
    
    #check if the book already exists in the specific library
    sql0 = "SELECT book_id, library_id \
        FROM inventory \
        WHERE book_id=%s AND library_id=%s;"
    existingBook = exec_get_all(sql0, (book_id, library_id))
    
    if existingBook == []: #doesn't exist
        sql1 = "INSERT INTO inventory (book_id, available_count, checkout_count, library_id) \
        VALUES (%s, %s, %s, %s) \
        RETURNING book_id, library_id, available_count;"
        return exec_returning_all(sql1, (book_id, available_count, 0, library_id))
    #already exists
    sql1 = "UPDATE inventory \
        SET available_count=available_count+%s \
        WHERE book_id=%s AND library_id=%s \
        RETURNING book_id, library_id, available_count;"
    return exec_returning_all(sql1, (available_count, book_id, library_id))

def check_overdue_books_all_users(today_date):
    """
    Description: Check all the checked out books and see if they've overdue
    Args:
        today_date - datetime, today's date
    Access: N/A
    Returned: 
        the user ids, the book ids, the checkout dates, and the due dates
    """ 
    sql = "UPDATE history \
    SET status_tag='overdue' \
    WHERE due_date < %s AND status_tag='checked_out' \
    RETURNING user_id, book_id, checkout_date, due_date"
    return exec_returning_many(sql, (today_date, ))

def get_overdue_books_by_library(lib_name, today_date):
    """
    Description: Get overdue books in a specified library
    Args:
        lib_name - String, the specific library name where the book is
        today_date - datetime, today's date
    Access: N/A
    Returned:
        the user names, the book titles, the checkout dates, and the due dates
    """
    library_id = get_library_id(lib_name)
    check_overdue_books_all_users(today_date)
    
    sql = "SELECT u.first_name, b.title, h.checkout_date, h.due_date \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN users u on u.id=h.user_id \
        WHERE h.status_tag='overdue' AND h.library_id=%s \
        ORDER BY h.user_id ASC, b.title ASC;"
    return exec_get_all(sql, (library_id, ))

def get_all_books_in_libraries():
    """
    Description: Get a list of all books in all libraries including count,
        ordered by library name then book title
    Args: N/A
    Access: N/A
    Returned: 
        the library name, the book title, and the total amount of each book
    """
    sql = "SELECT l.lib_name, b.title, i.available_count+i.checkout_count AS total_count  \
        FROM inventory i \
        JOIN libraries l ON l.id=i.library_id \
        JOIN books b on b.id=i.book_id \
        ORDER BY l.lib_name ASC, b.title ASC;"
    return exec_get_all(sql)

def get_user_lending_history(user_id, today_date):
    """
    Description: Get a specified user's lending history (checked out books and on time returned books)
    Args:
        user_id - Unique Integer, the specific user
    Access: only users can check their own account
    Returned:
        the library name, the book title, the book author, the date the book was checked out,
        the due date, the return date if the book was returned, and the status of the book (checked out or returned)
    """
    check_overdue_books_all_users(today_date)
    sql = "SELECT l.lib_name, b.title, b.author, h.checkout_date, h.due_date, h.return_date, h.status_tag \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN libraries l on l.id=h.library_id \
        WHERE h.user_id=%s AND (h.status_tag='checked_out' OR h.status_tag='returned') \
        ORDER BY l.lib_name ASC, b.title ASC;"
    return exec_get_all(sql, (user_id, ))

def get_user_late_history(user_id, today_date):
    """
    Description: Get a specified user's late history (overdue books or late returned books)
    Args: 
        user_id - Unique Integer, the specific user
    Access: only users can check their own account
    Returned: 
        the library name, the book title, the book author, the date the book was checked out,
        the due date, the return date if the book was returned, and the status of the book (overdue or late_return)
    """
    check_overdue_books_all_users(today_date)
    sql = "SELECT l.lib_name, b.title, b.author, h.checkout_date, h.due_date, h.return_date, h.status_tag \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN libraries l on l.id=h.library_id \
        WHERE h.user_id=%s AND (h.status_tag='overdue' OR h.status_tag='late_return') \
        ORDER BY l.lib_name ASC, b.title ASC;"
    return exec_get_all(sql, (user_id, ))

def get_all_lending_history(today_date):
    """
    Description: Get a list of all users lending history (checked out or returned)
    Args: N/A
    Access: N/A
    Returned:
        the users first name and last name, the library name, the book title, the book author, 
        the date the book was checked out, the due date, the return date if the book was returned, 
        and the status of the book (checked out or returned)
    """
    check_overdue_books_all_users(today_date)
    sql = "SELECT u.first_name, u.last_name, l.lib_name, b.title, b.author, h.checkout_date, h.due_date, h.return_date, h.status_tag \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN libraries l on l.id=h.library_id \
        JOIN users u on u.id=h.user_id \
        WHERE h.status_tag='checked_out' OR h.status_tag='returned' \
        ORDER BY u.first_name ASC, l.lib_name ASC;"
    return exec_get_all(sql)

def get_all_late_history(today_date):
    """
    Description: Get a list of all users lending history (overdue or late return)
    Args: N/A
    Access: N/A
    Returned:
        the users first name and last name, the library name, the book title, the book author, 
        the date the book was checked out, the due date, the return date if the book was returned, 
        and the status of the book (overdue or late_return)
    """
    check_overdue_books_all_users(today_date)
    sql = "SELECT u.first_name, u.last_name, l.lib_name, b.title, b.author, h.checkout_date, h.due_date, h.return_date, h.status_tag \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN libraries l on l.id=h.library_id \
        JOIN users u on u.id=h.user_id \
        WHERE h.status_tag='overdue' OR h.status_tag='late_return' \
        ORDER BY u.first_name ASC, l.lib_name ASC;"
    return exec_get_all(sql)

# DB4
def calculate_late_fee(due_date, today_date):
    """
    Description: calculate the late fee, per day penalty of $0.25 for the first week, and $2.00 per day after that
    Args:
        due_date - datetime, the due date
        today_date - datetime, today's date or the return date
    Access: N/A
    Returned:
        the late fee
    """
    difference = today_date - due_date 
    day_diff = difference.days
    if day_diff < 0:
        return 0.0
    
    late_fee = 0
    if day_diff < 8: #first week
        late_fee = late_fee + (0.25 * day_diff)
    else:  #calc for past 1 week
        late_fee = late_fee + (0.25 * 7)
        day_diff = day_diff - 7 #get rid of first week
        late_fee = late_fee + (2 * day_diff)
    return late_fee

# Return and print the results of the Late Fees API, 
# which would summarize the results for all users with checkout/ return data and late fees.
def report_book_late_fees(today_date):
    # get data
    sql = "SELECT ARRAY_AGG (b.title || ' by ' || b.author ORDER BY b.title ASC) AS title, \
            ARRAY_AGG (u.first_name || ' ' || u.last_name ORDER BY u.first_name ASC) AS name, \
            h.checkout_date, h.return_date, h.due_date \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN users u ON u.id=h.user_id \
        GROUP BY h.checkout_date, h.return_date, h.due_date \
        ORDER BY title ASC, name ASC;"
    data = exec_get_all(sql) #lst of tuples (lst, lst, datetime, datetime, datetime)
    title_author_lst = []
    name_lst = []
    dates_lst = []
    due_date_lst = []
    for i in range(len(data)):
        title_author_lst.append(data[i][0][0])
        name_lst.append(data[i][1][0])
        dates_lst.append((data[i][2], data[i][3]))
        due_date_lst.append(data[i][4])
    #calc late fee
    late_fee_lst = []
    for i in range(len(due_date_lst)):
        late_fee_lst.append(calculate_late_fee(due_date_lst[i], today_date))
    #set up for printing - calculate spaces
    max_len_book = 0
    max_len_name = 0
    for i in range(len(title_author_lst)):
        curr_len_book = len(title_author_lst[i])
        curr_len_name = len(name_lst[i]) 
        if curr_len_book > max_len_book:
            max_len_book = curr_len_book
        if curr_len_name > max_len_name:
            max_len_name = curr_len_name
    book_spaces = " " * (int((max_len_book - 4) / 2) + 1)
    name_spaces = " " * (int((max_len_name - 4) / 2) + 1)
    #header print
    print()
    print(book_spaces + "book" + book_spaces + "|" + name_spaces + "name" + name_spaces + "| checkout_date " + "| returned_date" + " | late_fees ")
    book_line = "-" * (max_len_book + 2)
    name_line = "-" * (max_len_name + 2)
    print(book_line + "+" + name_line + "+" + ("-" * 15) + "+" + ("-" * 15) + "+" + ("-" * 11))
    #setup
    date_spaces = " " * 4
    #print data rows
    for i in range(len(dates_lst)):
        book_spaces = ((max_len_book + 1) - len(title_author_lst[i])) * " "
        name_spaces = ((max_len_name + 1) - len(name_lst[i])) * " "
        #dates
        checkout_date = " " + dates_lst[i][0].strftime('%Y/%m/%d')
        returned_date = dates_lst[i][1]
        if returned_date == None:
            returned_date = 11 * " "
        else:
            returned_date = " " + returned_date.strftime('%Y/%m/%d')
        #fees
        fee_spaces = (11 - len((str(late_fee_lst[i])))) * " "
        fee_str = str(late_fee_lst[i])
        fee_change = fee_str.split(".")[1]
        extra_zero = ""
        if len(fee_change) == 1:
            fee_spaces = (10 - len((str(late_fee_lst[i])))) * " "
            extra_zero = "0"
        #print data row
        print(" " + title_author_lst[i] + book_spaces + "| " + name_lst[i] + name_spaces + "|" + checkout_date + date_spaces + "|" + returned_date + date_spaces + "|" + fee_spaces + str(late_fee_lst[i]) + extra_zero)
    print()
    
# User information for all activity. 
# This includes the user name, books checked out, due dates, return dates and late fees.
# Organize by library, user, books and date
def report_user_info(today_date):
    # get data
    sql = "SELECT l.lib_name, ARRAY_AGG (b.title || ' by ' || b.author ORDER BY b.title ASC) AS title, \
            ARRAY_AGG (u.first_name || ' ' || u.last_name ORDER BY u.first_name ASC) AS name, \
            h.checkout_date, h.return_date, h.due_date \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN users u ON u.id=h.user_id \
        JOIN libraries l ON l.id=h.library_id \
        GROUP BY h.checkout_date, h.return_date, h.due_date, l.lib_name \
        ORDER BY l.lib_name ASC, name ASC, title ASC, h.checkout_date ASC;"
    data = exec_get_all(sql) #lst of tuples (lst, lst, datetime, datetime, datetime)
    title_author_lst = []
    name_lst = []
    dates_lst = []
    due_date_lst = []
    library_lst = []
    for i in range(len(data)):
        library_lst.append(data[i][0])
        title_author_lst.append(data[i][1][0])
        name_lst.append(data[i][2][0])
        dates_lst.append((data[i][3], data[i][4]))
        due_date_lst.append(data[i][5])
    #calc late fee
    late_fee_lst = []
    for i in range(len(due_date_lst)):
        late_fee_lst.append(calculate_late_fee(due_date_lst[i], today_date))
    #set up for printing - calculate spaces
    max_len_library = 0
    max_len_book = 0
    max_len_name = 0
    for i in range(len(title_author_lst)):
        curr_len_library = len(library_lst[i])
        curr_len_book = len(title_author_lst[i])
        curr_len_name = len(name_lst[i]) 
        if curr_len_library > max_len_library:
            max_len_library = curr_len_library
        if curr_len_book > max_len_book:
            max_len_book = curr_len_book
        if curr_len_name > max_len_name:
            max_len_name = curr_len_name
    library_spaces = " " * (int((max_len_library - 8) / 2) + 1 + 1)
    book_spaces = " " * (int((max_len_book - 4) / 2) + 1)
    name_spaces = " " * (int((max_len_name - 4) / 2) + 1)
    #header print
    print()
    print(library_spaces + "library" + library_spaces + "|" + book_spaces + "book" + book_spaces + "|" + name_spaces + "name" + name_spaces + "| checkout_date " + "| returned_date" + " | late_fees ")
    library_line = "-" * (max_len_library + 1 + 1)
    book_line = "-" * (max_len_book + 2)
    name_line = "-" * (max_len_name + 2)
    print(library_line + "+" + book_line + "+" + name_line + "+" + ("-" * 15) + "+" + ("-" * 15) + "+" + ("-" * 11))
    #setup
    date_spaces = " " * 4
    #print data rows
    for i in range(len(dates_lst)):
        library_spaces = ((max_len_library) - len(library_lst[i])) * " "
        book_spaces = ((max_len_book + 1) - len(title_author_lst[i])) * " "
        name_spaces = ((max_len_name + 1) - len(name_lst[i])) * " "
        #dates
        checkout_date = " " + dates_lst[i][0].strftime('%Y/%m/%d')
        returned_date = dates_lst[i][1]
        if returned_date == None:
            returned_date = 11 * " "
        else:
            returned_date = " " + returned_date.strftime('%Y/%m/%d')
        #fees
        fee_spaces = (11 - len((str(late_fee_lst[i])))) * " "
        fee_str = str(late_fee_lst[i])
        fee_change = fee_str.split(".")[1]
        extra_zero = ""
        if len(fee_change) == 1:
            fee_spaces = (10 - len((str(late_fee_lst[i])))) * " "
            extra_zero = "0"
        #print data row
        print(" " + library_lst[i] + library_spaces + " | " + title_author_lst[i] + book_spaces + "| " + name_lst[i] + name_spaces + "|" + checkout_date + date_spaces + "|" + returned_date + date_spaces + "|" + fee_spaces + str(late_fee_lst[i]) + extra_zero)
    print()

# Present a table style listing of each book and who has checked out the book
# Make the output user friendly by have all the book info (title/ author) in ONE column in the output.
# e.g The Winds of Winter by George R.R. Martin. HINT: using the PostgreSQL command array_agg might help.
def report_checked_out_books_by_library():
    # get data
    sql = "SELECT l.lib_name, ARRAY_AGG (b.title || ' by ' || b.author ORDER BY b.title ASC) AS title, \
            ARRAY_AGG (u.first_name || ' ' || u.last_name ORDER BY u.first_name ASC) AS name, \
            h.checkout_date, h.return_date \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN users u ON u.id=h.user_id \
        JOIN libraries l ON l.id=h.library_id \
        GROUP BY h.checkout_date, h.return_date, h.due_date, l.lib_name \
        ORDER BY l.lib_name ASC, name ASC, title ASC, h.checkout_date ASC;"
    data = exec_get_all(sql) #lst of tuples (lst, lst, datetime, datetime, datetime)
    title_author_lst = []
    name_lst = []
    dates_lst = []
    library_lst = []
    for i in range(len(data)):
        library_lst.append(data[i][0])
        title_author_lst.append(data[i][1][0])
        name_lst.append(data[i][2][0])
        dates_lst.append((data[i][3], data[i][4]))
    #set up for printing - calculate spaces
    max_len_library = 0
    max_len_book = 0
    max_len_name = 0
    for i in range(len(title_author_lst)):
        curr_len_library = len(library_lst[i])
        curr_len_book = len(title_author_lst[i])
        curr_len_name = len(name_lst[i]) 
        if curr_len_library > max_len_library:
            max_len_library = curr_len_library
        if curr_len_book > max_len_book:
            max_len_book = curr_len_book
        if curr_len_name > max_len_name:
            max_len_name = curr_len_name
    library_spaces = " " * (int((max_len_library - 8) / 2) + 1 + 1)
    book_spaces = " " * (int((max_len_book - 4) / 2) + 1)
    name_spaces = " " * (int((max_len_name - 4) / 2) + 1)
    #header print
    print()
    print(library_spaces + "library" + library_spaces + "|" + book_spaces + "book" + book_spaces + "|" + name_spaces + "name" + name_spaces + "| checkout_date " + "| returned_date ")
    library_line = "-" * (max_len_library + 1 + 1)
    book_line = "-" * (max_len_book + 2)
    name_line = "-" * (max_len_name + 2)
    print(library_line + "+" + book_line + "+" + name_line + "+" + ("-" * 15) + "+" + ("-" * 15))
    #setup
    date_spaces = " " * 4
    #print data rows
    for i in range(len(dates_lst)):
        library_spaces = ((max_len_library) - len(library_lst[i])) * " "
        book_spaces = ((max_len_book + 1) - len(title_author_lst[i])) * " "
        name_spaces = ((max_len_name + 1) - len(name_lst[i])) * " "
        #dates
        checkout_date = " " + dates_lst[i][0].strftime('%Y/%m/%d')
        returned_date = dates_lst[i][1]
        if returned_date == None:
            returned_date = 11 * " "
        else:
            returned_date = " " + returned_date.strftime('%Y/%m/%d')
        #print data row
        print(" " + library_lst[i] + library_spaces + " | " + title_author_lst[i] + book_spaces + "| " + name_lst[i] + name_spaces + "|" + checkout_date + date_spaces + "|" + returned_date + date_spaces)
    print()    

# Generate a report that lists each book that has been checked out, the number of days for which it was checked out,
# and at the end, prints the average number of days it takes for a book to be returned
# Title                  User            Checkout        Return       Days borrowed
def report_checked_out_books_days():
    # get data
    sql = "SELECT b.title, \
            ARRAY_AGG (u.first_name || ' ' || u.last_name ORDER BY u.first_name ASC) AS name, \
            h.checkout_date, h.return_date \
        FROM history h \
        JOIN books b ON b.id=h.book_id \
        JOIN users u ON u.id=h.user_id \
        GROUP BY b.title, h.checkout_date, h.return_date, h.due_date \
        ORDER BY b.title ASC, name ASC;"
    data = exec_get_all(sql) #lst of tuples (lst, lst, datetime, datetime, datetime)
    title_author_lst = []
    name_lst = []
    dates_lst = []
    for i in range(len(data)):
        title_author_lst.append(data[i][0])
        name_lst.append(data[i][1][0])
        dates_lst.append((data[i][2], data[i][3]))
    #set up for printing - calculate spaces
    max_len_book = 0
    max_len_name = 0
    for i in range(len(title_author_lst)):
        curr_len_book = len(title_author_lst[i])
        curr_len_name = len(name_lst[i]) 
        if curr_len_book > max_len_book:
            max_len_book = curr_len_book
        if curr_len_name > max_len_name:
            max_len_name = curr_len_name
    book_spaces = " " * (int(max_len_book - 4 + 1))
    name_spaces = " " * (int(max_len_name - 4 + 1))
    #header print
    print()
    print("Title" + book_spaces + " User" + name_spaces + "  Checkout" + "     " + "Return" + "       " + "Days borrowed")
    #setup
    date_spaces = " " * 2
    avg_day_lst = []
    #print data rows
    for i in range(len(dates_lst)):
        book_spaces = ((max_len_book + 1 + 1) - len(title_author_lst[i])) * " "
        name_spaces = ((max_len_name + 1) - len(name_lst[i])) * " "
        #dates and days
        checkout_date = "  " + dates_lst[i][0].strftime('%Y/%m/%d')
        returned_date = dates_lst[i][1]
        days_borrowed = "None"
        if returned_date == None:
            returned_date = 11 * " "
            avg_day_lst.append(0)
        else:
            returned_date = " " + returned_date.strftime('%Y/%m/%d')
            days = (dates_lst[i][1] - dates_lst[i][0]).days
            days_borrowed = str(days)
            avg_day_lst.append(days)
        #print data row
        print(title_author_lst[i] + book_spaces + " " + name_lst[i] + name_spaces + checkout_date + date_spaces + returned_date + date_spaces + " " + days_borrowed)
    print()
    #print average return time
    day_total = 0
    for i in range(len(avg_day_lst)):
        day_total = day_total + avg_day_lst[i]
    avg_day = str(round(day_total / len(avg_day_lst), 2))
    print("Average return time = " + avg_day + " days")
    print()
    

    
    
    
# A useful, single sentence about what the method does.
# Name of each argument, what it means, and any default value
# Access control assumptions you are making
# What is returned? (e.g. python dict? psycopg2 result set?)
"""
Description:
Args:
Access: 
Returned:
"""
# access call examples
# "Assumes the caller is an authenticated user."
# "Only admin users should call this function."
# "Should only be called within a transaction context."
# "Must not be called directly from external APIs."