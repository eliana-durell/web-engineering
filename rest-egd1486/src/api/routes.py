from flask_restful import Resource
from flask_restful import request, reqparse
from db import library_db
    
class User(Resource):
    # List All Users
    def get(self):
        return library_db.get_users()

    # Add a user (with all their information).
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("full_name", str)
        parser.add_argument("username", str)
        parser.add_argument("email", str)
        parser.add_argument("password", str)
        args = parser.parse_args()
        
        full_name = args["full_name"]
        username = args["username"]
        email = args["email"]
        password = args["password"]
        return library_db.create_user(full_name, username, email, password)
    
    # Edit a users information. 
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("full_name", str)
        parser.add_argument("username", str)
        parser.add_argument("email", str)
        parser.add_argument("password", str)
        args = parser.parse_args()
        
        full_name = args["full_name"]
        username = args["username"]
        email = args["email"]
        password = args["password"]
        try:
            session_key = request.headers.get("Session-Key")
        except: 
            session_key = None
        
        return library_db.edit_user(full_name, username, email, password, session_key) 
    
    # Remove a user. 
    def delete(self):
        email = request.args.get("email")
        session_key = request.headers.get("Session-Key")
        return library_db.remove_user(email, session_key)
   
class Book(Resource):
    # List All Books or by search criteria 
    def get(self):
        library = request.args.get("library")
        title = request.args.get("title")
        author = request.args.get("author")
        genre = request.args.get("genre")
        return library_db.search_for_book(library, title, author, genre)

class Inventory(Resource):
    # List all the inventory
    def get(self):
        return library_db.get_inventory()

class History(Resource):
    # List all user transactions in the library
    def get(self):
        return library_db.get_history()

class Libraries(Resource):
    # List all libraries
    def get(self):
        return library_db.get_libraries()

#rest-2
class Login(Resource):
    # A user can login to the library DB.
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", str)
        parser.add_argument("password", str)
        args = parser.parse_args()
        
        username = args["username"]
        password = args["password"]
        return library_db.login_user(username, password)

class Logout(Resource):
    # A user can logout of the library DB.
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", str)
        args = parser.parse_args()
        email = args["email"]
        try:
            session_key = request.headers.get("Session-Key")
        except: 
            session_key = None
        return library_db.logout_user(email, session_key)
    
class Checkout(Resource):
    # List all checkouts for a given user.
    def get(self):
        username = request.args.get("username")
        try:
            session_key = request.headers.get("Session-Key")
        except: 
            session_key = None
        return library_db.get_user_history_books(username, session_key)
    
     # A logged in user can checkout
    def post(self):
        title = request.args.get("title")
        author = request.args.get("author")
        checkout_date = request.args.get("checkout_date")
        lib_name = request.args.get("lib_name")
        
        parser = reqparse.RequestParser()
        parser.add_argument("username", str)
        args = parser.parse_args()
        username = args["username"]
        try:
            session_key = request.headers.get("Session-Key")
        except: 
            session_key = None
        return library_db.checkout_book(session_key, username, title, author, checkout_date, lib_name)
    
class Reserve(Resource):
    # A logged in user can reserve a book. 
    def post(self):
        title = request.args.get("title")
        author = request.args.get("author")
        lib_name = request.args.get("lib_name")
        
        parser = reqparse.RequestParser()
        parser.add_argument("username", str)
        args = parser.parse_args()
        username = args["username"]
        try:
            session_key = request.headers.get("Session-Key")
        except: 
            session_key = None
        return library_db.reserve_book(session_key, username, title, author, lib_name)
