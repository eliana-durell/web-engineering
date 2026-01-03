import datetime
from datetime import datetime as dt
import os
from .swen344_db_utils import *
import hashlib
import secrets

def rebuild_tables():
    exec_sql_file('src/db/library.sql')

def get_users():
    """
    Description: get users table
    Args: N/A
    Access: N/A
    Returned: 
        JSON object containing 
        all user's id, full_name, username, email, status
    """
    sql = "SELECT row_to_json(users) FROM \
            (SELECT id, full_name, username, email, active as status FROM users) \
            users;"
    return exec_get_all(sql)

def get_inventory():
    """
    Description: get inventory table
    Args: N/A
    Access: N/A
    Returned: 
        JSON object containing
        all book id, library id, available count, checkout count
    """
    sql = "SELECT row_to_json(inventory) FROM \
            (SELECT book_id, library_id, available_count, checkout_count FROM inventory) \
            inventory;"
    return exec_get_all(sql)

def get_history():
    """
    Description: get history table
    Args: N/A
    Access: N/A
    Returned: 
        JSON object containing 
        all user id, book id, library id, status tag, checkout date, due date, return date
    """
    sql = "SELECT row_to_json(history) FROM \
            (SELECT user_id, book_id, library_id, status_tag as status, TO_CHAR(checkout_date, 'YYYY-MM-DD') as checkout_date, \
                TO_CHAR(due_date, 'YYYY-MM-DD') as due_date, TO_CHAR(return_date, 'YYYY-MM-DD') as return_date \
                FROM history) \
        history;"
    return exec_get_all(sql)

def get_libraries():
    """
    Description: get libraries table
    Args: N/A
    Access: N/A
    Returned: 
        JSON object containing 
        all id, library name
    """
    sql = "SELECT row_to_json(libraries) FROM \
            (SELECT id, lib_name as library \
                FROM libraries) \
        libraries;"
    return exec_get_all(sql)

def search_for_book(library, title, author, genre):
    """
    Description: a user can get all books or search for a book by library, title, author, or genre
    Args:
        library - String, the name of the library
        title - String, the title of the book
        author - String, the author(s) of the book
        genre - String, the genre of the book
    Access: N/A
    Returned: 
        if there are books available, 
            then JSON object containing the library, title, author, genre, and available count
        if there are no book, 
            then an JSON object
    """
    sql = "SELECT row_to_json(inventory) FROM \
            (SELECT l.lib_name as library, b.title, b.author, b.genre, i.available_count \
            FROM inventory i \
            JOIN libraries l ON l.id=i.library_id \
            JOIN books b ON b.id=i.book_id"
    addAnd = False
    sqlAnd = " AND "
    params = []
    if library or title or author or genre: #select by search criteria
        sql = sql + " WHERE "
        if library:
            params.append(library)
            sql = sql + "l.lib_name LIKE %s"
            addAnd = True
        if title:
            if addAnd:
                sql = sql + sqlAnd
            params.append(title)
            sql = sql + "b.title LIKE %s"
            addAnd = True
        if author:
            if addAnd:
                sql = sql + sqlAnd
            params.append(author)
            sql = sql + "b.author LIKE %s"
            addAnd = True
        if genre:
            if addAnd:
                sql = sql + sqlAnd
            params.append(genre)
            sql = sql + "b.genre LIKE %s"
    else: #select all books (rest-2)
        sql = sql + " WHERE title IS NOT NULL" 
    sql = sql + " ORDER BY l.lib_name ASC) inventory;"
    result = exec_get_all(sql, params)
    if(result):
        return result
    else: 
        return {}

#rest 2
def compute_hash(password):
    """
    Description: one-way hashes a password
    Args:
        password - String, the user's password
    Access: System only
    Returned: 
        a sha512 hashed password in hexidecimal
    """
    hash = hashlib.sha512()
    encoded_pwd = password.encode('utf-8')
    hash.update(encoded_pwd)
    return hash.hexdigest()

def generate_session_key():
    """
    Description: generates a session key for the logged in user
    Args: N/A
    Access: System only
    Returned: 
        returns a random 128-bit number
    """
    return secrets.randbits(128)

def search_user(email=None):
    """
    Description: looks to see if a user exists
    Args: 
        email - String, the user's email
    Access: System only
    Returned:
        True if the user exists
        False if the user doesn't exist
    """
    if email != None:
        sql = "SELECT id \
            FROM users \
            WHERE email=%s;"
        result = exec_get_one(sql, (email,))
        if result:
            return True
        return False

def create_user(full_name, username, email, password):
    """
    Description: creates a new user 
        !NOTE: email is unchangeable after creation
    Args: 
        full_name - String, the user's full name
        username - String, the user's display name
        email - String, the user's email
            Note: active - Boolean, default is true
        password - String, password for login
    Access: N/A
    Returned: 
        JSON object containing
        status message or the id of the created user, the username, and the email
    """
    userExists = search_user(email) #email because session key doesn't exist on creation, email unqiue
    if userExists:
        return dict(Status="User already exists")
    
    hashed_pwd = compute_hash(password)
    sql = "INSERT INTO users (full_name, username, email, active, hashed_password) \
            VALUES (%s, %s, %s, DEFAULT, %s) \
            RETURNING id, username, email;"
    result = exec_returning_all(sql, (full_name, username, email, hashed_pwd))
    return dict(id=result[0], username=result[1], email=result[2])

def edit_user(full_name, username, email, password, session_key):
    """
    Description: edit a user in the user table
       !NOTE: email is unchangeable 
    Args: 
        full_name - String, the user's full name
        username - String, the user's display name
        email - String, the user's email
        password - String, password for login
        session-key - Integer, the user's own session_key
    Access: Logged in users, assumes there is at least 1 param being changed
    Returned: 
        JSON object containing
        status message or the user's full name, username and email
    """
    message = authenticate_user(email, session_key)
    if message != "Passed":
        return dict(Status=message)
    #else user passed login authentication
    params = []
    addComma = False
    comma = ", "
    sql = "UPDATE users SET "
    if full_name:
        sql = sql + "full_name=%s"
        params.append(full_name)
        addComma = True
    if username:
        if addComma:
            sql = sql + comma
        sql = sql + "username=%s"
        params.append(username)
        addComma = True
    if password: 
        if addComma:
            sql = sql + comma
        sql = sql + "hashed_password=%s"
        params.append(compute_hash(password))
    sql = sql + " WHERE session_key=%s RETURNING full_name, username, email;"
    params.append(session_key)
    result = exec_returning_all(sql, params)
    return dict(full_name=result[0], username=result[1], email=result[2])
    
def remove_user(email, session_key):
    """
    Description: delete the user's account
    Args: 
        email - String, the user's email
        session-key - Integer, the user's own session_key
    Access: Logged in users
    Returned: 
        JSON object containing
        status message 
    """
    message = authenticate_user(email, session_key)
    if message != "Passed":
        return dict(Status=message)
    #else user passed login authentication
    sql = "DELETE FROM users \
        WHERE email=%s AND session_key=%s;"
    exec_commit(sql, (email, session_key))
    
    logout_user(email, session_key) #ensures no more further transactions
    return dict(Status="Deleted user")

def login_user(username, password):
    """
    Description: logs in a user given credentials
    Args: 
        username - String, the user's display name
        password - String, the user's password
    Access: N/A
    Returned: 
        JSON object containing
        status message with/without user's session key
    """
    cmp_hashed_pwd = compute_hash(password)
    sql = "SELECT hashed_password \
        FROM users \
        WHERE username=%s;"
    result = exec_get_one(sql, (username, ))
    if result == None:
        return dict(Status="Login failed") #invalid username
    hashed_pwd = result[0]
    if hashed_pwd == cmp_hashed_pwd:
        session_key = generate_session_key()
        sql = "UPDATE users \
            SET session_key=%s \
            WHERE username=%s;"
        exec_commit(sql, (session_key, username))
        return dict(Status="Login succeeded", session_key=session_key)
    else:
        return dict(Status="Login failed") #invalid password
    
def logout_user(email, session_key):
    """
    Description: logs out a user 
    Args:
        email - String, the user's email
        session-key - Integer, the user's own session_key
    Access: Logged in users
    Returned: 
        JSON object containing
        status message 
    """
    message = authenticate_user(email, session_key)
    if message != "Passed":
        return dict(Status=message)
    #else user passed login authentication
    sql = "UPDATE users \
        SET session_key=%s \
        WHERE email=%s;"
    exec_commit(sql, (None, email, ))
    return dict(Status="Logout succeeded")

def authenticate_user(email, session_key):
    """
    Description: authenticate a user before a transaction
    Args:
        email - String, the user's email
        session-key - Integer, the user's own session_key
    Access: System only
    Returned: 
        status message 
    """
    if not session_key: 
        return "User must be logged in"
    
    #check that the user exists and is only editing their account
    sql = "SELECT email \
        FROM users \
        WHERE session_key=%s;"
    cmp_email = exec_get_one(sql, (session_key, ))
    if not cmp_email: 
        return "Session key is invalid" #not tied to any user
    if (email != cmp_email[0]):
        return "Users can only edit their own account" #the given key and its user do not match the given user
    return "Passed"

def get_user_history_books(username, session_key):
    """
    Description: get a user's history of checked out books, sorted by book title ascending
    Args:
        username - String, the user's display name
        session-key - Integer, the user's own session_key
    Access: Logged in users
    Returned: 
        JSON object containing
        status message or library name, book title, book author, checkout date, return date, due date
    """
    #doing this so the email isn't exposed in the URL
    sql = "SELECT email \
        FROM users \
        WHERE username=%s"
    email = exec_get_one(sql, (username, ))[0]
    
    message = authenticate_user(email, session_key)
    if message != "Passed":
        return dict(Status=message)
    #else user passed login authentication
    sql = "SELECT row_to_json(history) FROM \
            (SELECT l.lib_name AS library, b.title, b.author, h.checkout_date, h.due_date, h.return_date \
            FROM history h \
            JOIN books b ON b.id=h.book_id \
            JOIN users u ON u.id=h.user_id \
            JOIN libraries l ON l.id=h.library_id \
            WHERE u.email=%s \
            ORDER BY l.lib_name ASC, b.title ASC) \
        history;"
    result = exec_get_all(sql, (email, ))
    if result:
        return result
    return {}

#the following functions are for checkout and reserve book
def get_user_id(username):
    """
    Description: get the user id
    Args:
        username - String, the user's display name
    Access: System only
    Returned: 
        the id of the user
    """
    sql = "SELECT id \
    FROM users \
    WHERE username=%s;"
    user_id = exec_get_one(sql, (username, ))
    return user_id

def get_book_id(title, author):
    """
    Description: get the book id
    Args:
        title - String, the title of the book
        author - String, the author(s) of the book
    Access: System only
    Returned: 
        the id of the book
    """
    sql = "SELECT id \
        FROM books \
        WHERE title=%s AND author=%s;"
    book_id = exec_get_one(sql, (title, author))
    return book_id

def get_library_id(lib_name):
    """
    Description: get the library id
    Args:
        lib_name - String, the name of the library
    Access: System only
    Returned: 
        the id of the library
    """
    sql = "SELECT id \
        FROM libraries \
        WHERE lib_name=%s;"
    library_id = exec_get_one(sql, (lib_name,))
    return library_id

def get_user_account_status(user_id):
    """
    Description: Get the specified user's account status
    Args:
        user_id - Unique Integer, the specific user
    Access: System only
    Returned:
        the specified user's account status (TRUE or FALSE)
    """
    sql = "SELECT active \
    FROM users \
    WHERE id=%s;"
    return exec_get_one(sql, (user_id,))[0]

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

def deactivate_user(email):
    """
    Description: deactivate the user's account
    Args: 
        email - String, the user's email
    Access: System only
    Returned: N/A
    """
    sql = "UPDATE users \
        SET active=FALSE \
        WHERE email=%s"
    exec_commit(sql, (email,))
    
def create_due_date(checkout_date):
    """
    Description: calculate the due date (2 weeks after the checkout date)
    Args:
        checkout_date - datetime, the checkout date
    Access: System only
    Returned:
        due_date - String, the due date 
    """
    date = dt.strptime(checkout_date, "%Y-%m-%d")
    added_time = datetime.timedelta(weeks=2)
    due_date = date + added_time
    new_date = due_date.strftime( "%Y-%m-%d")
    return new_date

def get_book_info(user_id, book_id, library_id):
    """
    Description: get book info in a JSON object
    Args: 
        user_id - Unique Integer, the user's id
        book_id - Unique Integer, the book's id
        library_id - Unique Integer, the library's id
    Access: System only
    Returned: 
        JSON object containing
        status message or username, book title, book author, library, checkout date, due date, return date
    """
    sql = "SELECT row_to_json(history) FROM \
            (SELECT u.username, b.title, b.author, l.lib_name as library, h.status_tag, \
                TO_CHAR(h.checkout_date, 'YYYY-MM-DD') as checkout_date, \
                TO_CHAR(h.due_date, 'YYYY-MM-DD') as due_date, \
                TO_CHAR(h.return_date, 'YYYY-MM-DD') as return_date \
            FROM history h \
            JOIN users u ON u.id=h.user_id \
            JOIN books b ON b.id=h.book_id \
            JOIN libraries l ON l.id=h.library_id \
            WHERE user_id=%s AND book_id=%s AND library_id=%s) \
        history;"
    return exec_get_one(sql, (user_id, book_id, library_id))

def checkout_book(session_key, username, title, author, checkout_date, lib_name):
    """
    Description: if the user has overdue books, they can't checkout and their account is deactivated,
        else the user checks out the book, updates the checkout history and the inventory
    Args: 
        session-key - Integer, the user's own session_key
        username - String, the user's display name
        title - String, the title of the book
        author - String, the author(s) of the book
        checkout_date - datetime, the checkout date
        lib_name - String, the specific library name where the book is
    Access: Logged in users, assumes that the book exists and there are available copies of the book
    Returned: 
        JSON object containing
        status message or username, book title, book author, library, checkout date, due date, return date
    """
    sql = "SELECT email \
        FROM users \
        WHERE username=%s;"
    email = exec_get_one(sql, (username, ))[0]
    message = authenticate_user(email, session_key)
    if message != "Passed":
        return dict(Status=message)
    #else user passed login authentication
    
    user_id = get_user_id(username)
    book_id = get_book_id(title, author)
    library_id = get_library_id(lib_name)
    #check if the account status is active
    isActive = get_user_account_status(user_id)
    if not isActive:
        return dict(Status="Account is still deactivated due to overdue books")
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
            deactivate_user(email)
        return dict(Status="Account is deactivated due to overdue books") #"Can't checkout book because you have overdue books."
    #else no overdue books and can checkout
    
    sql1 = "INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) \
        VALUES (%s, %s, %s, %s, %s, %s, NULL) \
        RETURNING user_id, book_id, library_id;"
    due_date = create_due_date(checkout_date)
    params = exec_returning_all(sql1, (user_id, book_id, library_id, "checked_out", checkout_date, due_date))
    result = get_book_info(params[0], params[1], params[2])
    
    sql2 = "UPDATE inventory \
        SET available_count=available_count-1, checkout_count=checkout_count+1 \
        WHERE book_id=%s AND library_id=%s;"
    exec_commit(sql2, (book_id, library_id))
    return result

def reserve_book(session_key, username, title, author, lib_name):
    """
    Description: the user reserves a book at the specified library
    Args: 
        session-key - Integer, the user's own session_key
        username - String, the user's display name
        title - String, the title of the book
        author - String, the author(s) of the book
        lib_name - String, the specific library name where the book is
    Access: Logged in users
    Returned: 
        if there are no available copies
            JSON object containing
            username, book title, book author, library, checkout date, due date, return date
        if there are available copies
            JSON object containing
            library, title, and available count
        else
            JSON object containingstatus message 
    """
    sql = "SELECT email \
        FROM users \
        WHERE username=%s;"
    email = exec_get_one(sql, (username, ))[0]
    message = authenticate_user(email, session_key)
    if message != "Passed":
        return dict(Status=message)
    #else user passed login authentication
    
    user_id = get_user_id(username)
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
        params = exec_returning_all(sql2, (user_id, book_id, library_id, "reserved"))
        return get_book_info(params[0], params[1], params[2])
    else: #has available copies
        sql3 = "SELECT row_to_json(inventory) FROM \
                (SELECT l.lib_name as library, b.title, i.available_count \
                FROM inventory i \
                JOIN books b ON b.id=i.book_id \
                JOIN libraries l ON l.id=i.library_id \
                WHERE book_id=%s AND library_id=%s) \
            inventory;"
        return exec_get_one(sql3, (book_id, library_id))

