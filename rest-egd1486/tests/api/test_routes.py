import json
import unittest
from tests.test_utils import *


class TestRoutes(unittest.TestCase):

    def setUp(self):  
        """Initialize DB using API call"""
        post_rest_call(self, 'http://127.0.0.1:4999/manage/init')
        print("DB Should be reset now")
    
    def test_users(self):
        """List Users"""
        expected = [[{'id': 1, 'full_name': 'Ada Lovelace', 'username': 'ada_love', 'email': 'adalovelace@gmail.com', 'status': True}],
                    [{'id': 2, 'full_name': 'Mary Shelley', 'username': 'franks_mom', 'email': 'mshelly@hotmail.com', 'status': True}], 
                    [{'id': 3, 'full_name': 'Jackie Gleason', 'username': 'jackie_G', 'email': 'jg@bookies.com', 'status': True}],
                    [{'id': 4, 'full_name': 'Art Garfunkel', 'username': 'art', 'email': 'artgarfunkel@go.com', 'status': True}],
                    [{'id': 5, 'full_name': 'Frank Wonder', 'username': 'Frank_Wonder', 'email': 'frankywonder@mail.com', 'status': False}], 
                    [{'id': 6, 'full_name': 'Stevie Wonder', 'username': 'Stevie_Wonder', 'email': 'steviewonder@gmail.com', 'status': False}]]
        actual = get_rest_call(self, 'http://127.0.0.1:4999/users')
        self.assertEqual(expected, actual, "incorrect users")
        
        result = get_rest_call(self, 'http://127.0.0.1:4999/users')
        self.assertNotEqual([], result, "no rows in users table")
        self.assertTrue(len(result) == 6, "not the correct amount of rows in users table")
        
    def test_search_books(self):
        """Search books"""
        #search by library
        expected = [[{'library': 'Fairport', 'title': 'The Echoes of Glass', 'author': 'Maren Elwood', 'genre': 'Mystery', 'available_count': 3}], 
                    [{'library': 'Fairport', 'title': 'The Lantern Keeper’s Promise', 'author': 'Eira Monroe', 'genre': 'Drama', 'available_count': 3}], 
                    [{'library': 'Fairport', 'title': 'The Hidden Cost of Convenience', 'author': 'Marcus Leung', 'genre': 'Social Studies', 'available_count': 2}], 
                    [{'library': 'Fairport', 'title': 'Frankenstein', 'author': 'Mary Shelley', 'genre': 'Gothic Horror', 'available_count': 2}]]
        actual = get_rest_call(self, 'http://127.0.0.1:4999/books?library=Fairport') 
        self.assertEqual(expected, actual, "incorrect listed books")  
        
        #search by library, title
        expected = [[{'library': 'Henrietta', 'title': 'Frankenstein', 'author': 'Mary Shelley', 'genre': 'Gothic Horror', 'available_count': 2}]]
        actual = get_rest_call(self, 'http://127.0.0.1:4999/books?library=Henrietta&title=Frankenstein') 
        self.assertEqual(expected, actual, "incorrect listed books")  
        
        #search by library, title, author
        expected = [[{'library': 'Pittsford', 'title': 'Beneath Hollow Skies', 'author': 'K.J. Harrow', 'genre': 'Post-Apocalyptic', 'available_count': 0}]]
        actual = get_rest_call(self, 'http://127.0.0.1:4999/books?library=Pittsford&title=Beneath Hollow Skies&author=K.J. Harrow') 
        self.assertEqual(expected, actual, "incorrect listed books")  
        
        #search by library, title, author, genre
        expected = [[{'library': 'Towns of Penfield', 'title': 'The Lantern Keeper’s Promise', 'author': 'Eira Monroe', 'genre': 'Drama', 'available_count': 1}]]
        actual = get_rest_call(self, 'http://127.0.0.1:4999/books?library=Towns of Penfield&title=The Lantern Keeper’s Promise&author=Eira Monroe&genre=Drama') 
        self.assertEqual(expected, actual, "incorrect listed books")  
        
        #search by library, genre
        expected = [[{'library': 'Henrietta', 'title': 'Wired for Wonder: The Neuroscience of Curiosity', 'author': 'Dr. Alicia Renn', 'genre': 'Science', 'available_count': 2}]]
        actual = get_rest_call(self, 'http://127.0.0.1:4999/books?library=Henrietta&genre=Science') 
        self.assertEqual(expected, actual, "incorrect listed books")  
        
        #search by title
        expected = [[{'library': 'Pittsford', 'title': 'Voices from the Edge: Climate Stories from the Front Lines', 'author': 'Sarita Javed', 'genre': 'Environmental', 'available_count': 4}], 
                    [{'library': 'Towns of Penfield', 'title': 'Voices from the Edge: Climate Stories from the Front Lines', 'author': 'Sarita Javed', 'genre': 'Environmental', 'available_count': 0}]]
        actual = get_rest_call(self, 'http://127.0.0.1:4999/books?title=Voices from the Edge: Climate Stories from the Front Lines') 
        self.assertEqual(expected, actual, "incorrect listed books")  
        
        #search not existent book
        expected = {}
        actual = get_rest_call(self, 'http://127.0.0.1:4999/books?library=Pittsford&author=Marcus Leung') 
        self.assertEqual(expected, actual, "incorrect listed books")  
        
        #search all books
        expected = [[{'library': 'Fairport', 'title': 'The Hidden Cost of Convenience', 'author': 'Marcus Leung', 'genre': 'Social Studies', 'available_count': 2}],
[{'library': 'Fairport', 'title': 'The Echoes of Glass', 'author': 'Maren Elwood', 'genre': 'Mystery', 'available_count': 3}], 
[{'library': 'Fairport', 'title': 'Frankenstein', 'author': 'Mary Shelley', 'genre': 'Gothic Horror', 'available_count': 2}], 
[{'library': 'Fairport', 'title': 'The Lantern Keeper’s Promise', 'author': 'Eira Monroe', 'genre': 'Drama', 'available_count': 3}], 
[{'library': 'Henrietta', 'title': 'Wired for Wonder: The Neuroscience of Curiosity', 'author': 'Dr. Alicia Renn', 'genre': 'Science', 'available_count': 2}], 
[{'library': 'Henrietta', 'title': 'Beneath Hollow Skies', 'author': 'K.J. Harrow', 'genre': 'Post-Apocalyptic', 'available_count': 0}], 
[{'library': 'Henrietta', 'title': 'The Hidden Cost of Convenience', 'author': 'Marcus Leung', 'genre': 'Social Studies', 'available_count': 2}], 
[{'library': 'Henrietta', 'title': 'The Echoes of Glass', 'author': 'Maren Elwood', 'genre': 'Mystery', 'available_count': 1}],
[{'library': 'Henrietta', 'title': 'Frankenstein', 'author': 'Mary Shelley', 'genre': 'Gothic Horror', 'available_count': 2}], 
[{'library': 'Pittsford', 'title': 'Beneath Hollow Skies', 'author': 'K.J. Harrow', 'genre': 'Post-Apocalyptic', 'available_count': 0}], 
[{'library': 'Pittsford', 'title': 'The Lantern Keeper’s Promise', 'author': 'Eira Monroe', 'genre': 'Drama', 'available_count': 1}], 
[{'library': 'Pittsford', 'title': 'Voices from the Edge: Climate Stories from the Front Lines', 'author': 'Sarita Javed', 'genre': 'Environmental', 'available_count': 4}], 
[{'library': 'Towns of Penfield', 'title': 'The Lantern Keeper’s Promise', 'author': 'Eira Monroe', 'genre': 'Drama', 'available_count': 1}],
[{'library': 'Towns of Penfield', 'title': 'Beneath Hollow Skies', 'author': 'K.J. Harrow', 'genre': 'Post-Apocalyptic', 'available_count': 3}],
[{'library': 'Towns of Penfield', 'title': 'The Echoes of Glass', 'author': 'Maren Elwood', 'genre': 'Mystery', 'available_count': 0}],
[{'library': 'Towns of Penfield', 'title': 'Wired for Wonder: The Neuroscience of Curiosity', 'author': 'Dr. Alicia Renn', 'genre': 'Science', 'available_count': 3}], 
[{'library': 'Towns of Penfield', 'title': 'Voices from the Edge: Climate Stories from the Front Lines', 'author': 'Sarita Javed', 'genre': 'Environmental', 'available_count': 0}]]
        actual = get_rest_call(self, 'http://127.0.0.1:4999/books') 
        self.assertEqual(expected, actual, "incorrect listed books")  
        
#rest 2
# In all cases of failure, the API must return a reasonable error,
# and your unit test must display a human readable message for the error.
    def test_create_user(self):
        """Create a user"""
        expected = {'id': 7, 'username': 'br1990', 'email': 'brcyrus@gmail.com'}
        data = dict(full_name='Billy Ray', username='br1990', email='brcyrus@gmail.com', password='hannahMontana')
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'} #setting content type
        actual = post_rest_call(self, 'http://127.0.0.1:4999/users', json_data, hdr)
        self.assertEqual(expected, actual, "User not created")
        
        expected = {'Status': 'User already exists'}
        data = dict(full_name='Ada Lovelace', username='ada_love', email='adalovelace@gmail.com', password='hannahMontana')
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'} #setting content type
        actual = post_rest_call(self, 'http://127.0.0.1:4999/users', json_data, hdr)
        self.assertEqual(expected, actual, "User created")
        
    def test_edit_user(self):
        """Edit a user"""
        #need to login first
        data = dict(username="ada_love", password="math!science?")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']

        #edit own account
        expected = {'full_name': 'Adam Lovelace', 'username': 'adam_lovelace', 'email': 'adalovelace@gmail.com'}
        data = dict(full_name='Adam Lovelace', username='adam_lovelace', email='adalovelace@gmail.com', password='hacked!')
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = put_rest_call(self, 'http://127.0.0.1:4999/users', json_data, hdr)
        self.assertEqual(expected, actual, "could not edit information")
        
        #testing authentication also
        #no session key / not logged in
        expected = {'Status': 'User must be logged in'}
        data = dict(full_name='Ada Lovelace', username='ada_love', password='match!science?')
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        actual = put_rest_call(self, 'http://127.0.0.1:4999/users', json_data, hdr)
        self.assertEqual(expected, actual, "could edit information")
        
        #session key invalid (doesn't match to a user)
        fake_session_key = 43258
        expected = {'Status': 'Session key is invalid'}
        data = dict(full_name='Adam Lovelace', username='adam_lovelace', email='adam_lovelace@gmail.com', password='not!hacked')
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{fake_session_key}'}
        actual = put_rest_call(self, 'http://127.0.0.1:4999/users', json_data, hdr)
        self.assertEqual(expected, actual, "could edit information")
    
        #given session key doesn't match given user's session key
        expected = {'Status': 'Users can only edit their own account'}
        data = dict(full_name='Adam Lovelace', username='adam_lovelace', email='adam_lovelace@gmail.com', password='not!hacked')
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = put_rest_call(self, 'http://127.0.0.1:4999/users', json_data, hdr)
        self.assertEqual(expected, actual, "could edit information")
    
    def test_remove_user(self):
        """Delete a user"""
        #need to login first
        data = dict(username="ada_love", password="math!science?")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']
        
        expected = {'Status': 'Deleted user'}
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = delete_rest_call(self, 'http://127.0.0.1:4999/users?email=adalovelace@gmail.com', hdr)
        self.assertEqual(expected, actual, "user still exists")
        
        #try to edit account
        expected = {'Status': 'Session key is invalid'}
        data = dict(full_name='Adam Lovelace', username='adam_lovelace', email='adalovelace@gmail.com', password='hacked!')
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = put_rest_call(self, 'http://127.0.0.1:4999/users', json_data, hdr)
        self.assertEqual(expected, actual, "could edit information")
        
    def test_login_user(self):
        """Login user"""
        expected = "Login succeeded"
        data = dict(username="ada_love", password="math!science?")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        self.assertEqual(expected, actual["Status"], "Error logging in")
        
        #non existent user
        expected = {'Status': 'Login failed'}
        data = dict(username="barley_tom", password="breadmaker")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        self.assertEqual(expected, actual, "Logged in")
        
        # wrong password
        expected = {'Status': 'Login failed'}
        data = dict(username="ada_love", password="no!password")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        self.assertEqual(expected, actual, "Logged in")
        
    def test_logout_user(self):
        """Logout user"""
        #need to login first
        data = dict(username="ada_love", password="math!science?")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']
        
        expected = {'Status': 'Logout succeeded'}
        data = dict(email="adalovelace@gmail.com")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-key': f'{session_key}'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/logout', json_data, hdr)
        self.assertEqual(expected, actual, "Error logging out")
        #tested authentication cases in test_edit_users
        
        #try to edit account
        expected = {'Status': "Session key is invalid"}
        data = dict(full_name='Adam Lovelace', username='adam_lovelace', email='adalovelace@gmail.com', password='hacked!')
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = put_rest_call(self, 'http://127.0.0.1:4999/users', json_data, hdr)
        self.assertEqual(expected, actual, "could edit information")
        
    def test_user_history_books(self):
        """List user's checkouts"""
        #need to login first
        data = dict(username="ada_love", password="math!science?")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']
        
        expected = [[{'library': 'Henrietta', 'title': 'Beneath Hollow Skies', 'author': 'K.J. Harrow', 'checkout_date': '2020-03-02', 'return_date': '2020-03-08', 'due_date': '2020-03-16'}], 
                    [{'library': 'Towns of Penfield', 'title': 'The Echoes of Glass', 'author': 'Maren Elwood', 'checkout_date': '2022-09-30', 'return_date': '2022-10-01', 'due_date': '2022-10-14'}]]
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = get_rest_call(self, 'http://127.0.0.1:4999/checkout?username=ada_love', params={}, get_header=hdr)
        self.assertEqual(expected, actual, "incorrect check out books")
        
        #need to login first
        data = dict(username="Stevie_Wonder", password="3blindmice")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']
        
        expected = {}
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = get_rest_call(self, 'http://127.0.0.1:4999/checkout?username=Stevie_Wonder', params={}, get_header=hdr)
        self.assertEqual(expected, actual, "incorrect check out books")
        
    def test_checkout_book(self):
        """Checkout a book""" 
        #need to login first
        data = dict(username="ada_love", password="math!science?")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']   
        # no overdue books and account active 
        expected = [{'username': 'ada_love', 'title': 'Frankenstein', 'author': 'Mary Shelley', 'library': 'Henrietta', 'status_tag': 'checked_out', 'checkout_date': '2025-07-02', 'due_date': '2025-07-16', 'return_date': None}]
        data = dict(username="ada_love")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/checkout?title=Frankenstein&author=Mary Shelley&checkout_date=2025-07-02&lib_name=Henrietta', json_data, hdr)
        self.assertEqual(expected, actual, "did not checkout book")
        
        #need to login first
        data = dict(username="Frank_Wonder", password="5wonders")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']
        # over due books and account not active
        expected = {'Status': 'Account is still deactivated due to overdue books'}
        data = dict(username="Frank_Wonder")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/checkout?title=Frankenstein&author=Mary Shelley&checkout_date=2025-07-02&lib_name=Henrietta', json_data, hdr)
        self.assertEqual(expected, actual, "checked out book")
        
        #need to login first
        data = dict(username="art", password="vangogh")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']
        # over due books and account active
        expected = {'Status': 'Account is deactivated due to overdue books'}
        data = dict(username="art")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/checkout?title=Frankenstein&author=Mary Shelley&checkout_date=2025-07-02&lib_name=Henrietta', json_data, hdr)
        self.assertEqual(expected, actual, "checked out book")
        # Note - not testing case: no overdue books and the users account is not active
        # due to when a user removes their account it now deletes (rather than deactivate)
        
    def test_reserve_book(self):
        """Reserve a book"""
        data = dict(username="jackie_G", password="baseball")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json'}
        result = post_rest_call(self, 'http://127.0.0.1:4999/login', json_data, hdr)
        session_key = result['session_key']

        expected = [{'username': 'jackie_G', 'title': 'The Echoes of Glass', 'author': 'Maren Elwood', 'library': 'Towns of Penfield', 'status_tag': 'reserved', 'checkout_date': None, 'due_date': None, 'return_date': None}]
        data = dict(username="jackie_G")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/reserve?title=The Echoes of Glass&author=Maren Elwood&lib_name=Towns of Penfield', json_data, hdr)
        self.assertEqual(expected, actual, "did not reserve book")
        
        expected = [{'library': 'Fairport', 'title': 'The Lantern Keeper’s Promise', 'available_count': 3}]
        data = dict(username="jackie_G")
        json_data = json.dumps(data)
        hdr = {'Content-Type': 'application/json', 'Session-Key': f'{session_key}'}
        actual = post_rest_call(self, 'http://127.0.0.1:4999/reserve?title=The Lantern Keeper’s Promise&author=Eira Monroe&lib_name=Fairport', json_data, hdr)
        self.assertEqual(expected, actual, "reserved book")
   