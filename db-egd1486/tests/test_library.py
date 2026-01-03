import datetime
import unittest
from src.library import *
from src.swen344_db_utils import connect

class TestLibrary(unittest.TestCase):
    def setUp(self):
        """Build the tables"""
        rebuildTables()

    def test_rebuild_tables(self):
        """Tables have rows"""
        result = get_users()
        self.assertNotEqual([], result, "no rows in users table")
        self.assertTrue(len(result) == 6, "not the correct amount of rows in users table")
        
        result = get_books()
        self.assertNotEqual([], result, "no rows in books table")
        self.assertTrue(len(result) == 7, "not the correct amount of rows in books table")
        
        result = get_inventory()
        self.assertNotEqual([], result, "no rows in inventory table")
        self.assertTrue(len(result) == 17, "not the correct amount of rows in inventory table")
        
        result = get_history()
        self.assertNotEqual([], result, "no rows in history table")
        self.assertTrue(len(result) == 9, "not the correct amount of rows in history table")
        
        result = get_libraries()
        self.assertNotEqual([], result, "no rows in history table")
        self.assertTrue(len(result) == 4, "not the correct amount of rows in history table")
        
    # idempotent. If something is idempotent then we can run it multiple times in a row and get the same effect. 
    # Unit tests should always be idempotent and not be impacted by side effects.
    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuildTables()
        rebuildTables()
        result = get_users()
        self.assertNotEqual([], result, "no rows in users table")
    
    # When we list the books that Art has checked out, it returns an empty list.
        # DB3 changed to Stevie Wonder
    def test_user_history_books(self):
        """List history of checked out books of a User"""
        result = get_user_history_books("Stevie", "Wonder")
        self.assertEqual([], result, "history of checked out books")
        
        result = get_user_history_books("Jackie", "Gleason")
        self.assertNotEqual([], result, "no checked out books")
        
    # When we list the books that Jackie Gleason has checked out, it correctly lists them in alphabetical order.
    def test_user_history_books_alphabet(self):
        """List history of checked out books alphabetically of a User"""
        result = get_user_history_books_by_alphabet("Jackie", "Gleason")
        self.assertEqual([('Beneath Hollow Skies',), ('Frankenstein',), ('Voices from the Edge: Climate Stories from the Front Lines',)], 
                         result, "unordered alphabetical checked out books")
    
    # When a librarian lists history of checked out books, it lists everyone’s checked out books ordered by user name
    def test_history_books_by_name(self):
        """List history of checked out books in order by user's name"""
        result = get_history_books_by_name()
        self.assertEqual([('Ada', 'Beneath Hollow Skies'),
                            ('Ada', 'The Echoes of Glass'),
                            ('Art', 'The Echoes of Glass'),
                            ('Frank', 'Frankenstein'),
                            ('Frank', 'The Hidden Cost of Convenience'),
                            ('Jackie', 'Beneath Hollow Skies'),
                            ('Jackie', 'Frankenstein'),
                            ('Jackie', 'Voices from the Edge: Climate Stories from the Front Lines'),
                            ('Mary', 'Beneath Hollow Skies')], 
                            result, "unordered user's history checked out books")
        
    # The librarian can list all the non-fiction books in inventory, along with the quantity.
    def test_books_in_category(self):
        """List all books in a category"""
        result = get_books_in_category("Non-Fiction")
        self.assertNotEqual([], result, "not the correct category")
        self.assertAlmostEqual([('Wired for Wonder: The Neuroscience of Curiosity',), 
                                ('The Hidden Cost of Convenience',), 
                                ('Voices from the Edge: Climate Stories from the Front Lines',)],
                               result, "not the correct category of books")
   
    # The librarian can list all the non-fiction books in inventory, along with the quantity.
    def test_count_books_in_category(self):
        """Get total number of books by category"""
        result = get_count_books_in_category("Non-Fiction")
        self.assertTrue(result[0][0] == 3, "not the correct number of books in category")
        
    def test_inventory_total_books(self):
        """Get total number of books in inventory"""
        result = get_inventory_total_books()
        self.assertEqual([('Beneath Hollow Skies', 5),
                          ('Frankenstein', 5),
                          ('The Echoes of Glass', 5),
                          ('The Hidden Cost of Convenience', 5),
                          ('The Lantern Keeper’s Promise', 5), 
                          ('Voices from the Edge: Climate Stories from the Front Lines', 5),
                          ('Wired for Wonder: The Neuroscience of Curiosity', 5)],
                         result, "not the correct number of total books in inventory")
    
    def test_total_available_books(self):
        """Get total number of available books"""
        result = get_total_available_books()
        self.assertTrue(result[0][0] == 29, "not the correct number of total available books")
        
    def test_available_books_by_category(self):
        """Get total number of available books by category"""
        result = get_available_books_by_category()
        self.assertEqual([('Fiction', 16), ('Non-Fiction', 13)], 
                        result, "not the correct number of available books by category")
    
    """DB2"""
    # Christopher Marlowe and Francis Bacon each sign up for a new account
    def test_create_user(self):
        """Creating a user"""
        result = create_user("Christopher", "Marlowe", "cmarlowe@gmail.com")
        self.assertIsNotNone(result, "user was not created")
        result = create_user("Francis", "Bacon", "francisb@outlook.com")
        self.assertIsNotNone(result, "user was not created")
    
    # Mary Shelley searches for “The Last Man” 
    # and after finding no copies in the library, deletes her account.
    def test_search_for_book_by_title(self):
        result = search_for_book_by_title("The Last Man")
        self.assertEqual(result, 0, "book was found in inventory")
    
    # Mary Shelley searches for “The Last Man” 
    # and after finding no copies in the library, deletes her account.
    def test_remove_user(self):
        """Removing a user"""
        result = remove_user("mshelly@hotmail.com")
        self.assertEqual((2, 'mshelly@hotmail.com', False), result, "did not remove user")
    
    # Art Garfunkel returns a copy of “Frankenstein” three days after he borrowed it.
    def test_checkout_book(self):
        """Checking out a book"""
        # over due books and account active
        result = checkout_book("Art", "Garfunkel", "Frankenstein", "Mary Shelley", datetime.date(2025, 1, 1), "Fairport")
        self.assertFalse(result, "checked out book")
        
        # over due books and account not active
        result = checkout_book("Frank", "Wonder", "Frankenstein", "Mary Shelley", datetime.date(2025, 1, 1), "Fairport")
        self.assertFalse(result, "checked out book")
        
        #set up 
        return_book("Art", "Garfunkel", "The Echoes of Glass", "Maren Elwood",  datetime.date(2022, 10, 1), "Towns of Penfield")

        # no overdue books and account active 
        result = checkout_book("Art", "Garfunkel", "Frankenstein", "Mary Shelley", datetime.date(2025, 1, 1), "Fairport")
        self.assertEqual( ((4, 7, 2, 'checked_out', datetime.date(2025, 1, 1),  datetime.date(2025, 1, 15), None), (7, 2, 1, 2)),
                         result, "did not check out book")
        
         # no overdue books and the users account is not active
        result = checkout_book("Stevie", "Wonder", "Frankenstein", "Mary Shelley", datetime.date(2025, 1, 1), "Fairport")
        self.assertFalse(result, "checked out book")
   
    # Art Garfunkel returns a copy of “Frankenstein” three days after he borrowed it.
    def test_return_book(self):
        """Returning a book"""
        # late return and account is inactive (account inactive due to trying to check out a book)
        result = return_book("Frank", "Wonder", "The Hidden Cost of Convenience", "Marcus Leung", datetime.date(2025, 1, 4), "Fairport")
        self.assertEqual(((5, 5, 2, 'late_return', datetime.date(2014, 4, 5), datetime.date(2025, 1, 4)), (5, 2, 3, 0)),
                         result, "did not return book")
        
        #set up
        rebuildTables()
         # on time return and account is inactive (account inactive due to trying to check out a book)
        result = return_book("Frank", "Wonder", "The Hidden Cost of Convenience", "Marcus Leung", datetime.date(2014, 4, 7), "Fairport")
        self.assertEqual(((5, 5, 2, 'returned', datetime.date(2014, 4, 5), datetime.date(2014, 4, 7)), (5, 2, 3, 0)),
                         result, "did not return book")
        
        #setup 
        return_book("Art", "Garfunkel", "The Echoes of Glass", "Maren Elwood", datetime.date(2022, 10, 1), "Towns of Penfield")
        # on time return and account is active
        checkout_book("Art", "Garfunkel", "Frankenstein", "Mary Shelley", datetime.date(2025, 1, 1), "Fairport")
        result = return_book("Art", "Garfunkel", "Frankenstein", "Mary Shelley",  datetime.date(2025, 1, 4), "Fairport")
        self.assertEqual(((4, 7, 2, 'returned', datetime.date(2025, 1, 1), datetime.date(2025, 1, 4)), (7, 2, 2, 1)),
                         result, "did not return book")
        
        #setup
        rebuildTables()
        return_book("Art", "Garfunkel", "The Echoes of Glass", "Maren Elwood", datetime.date(2022, 10, 1), "Towns of Penfield")
        # late return and account is active
        checkout_book("Art", "Garfunkel", "Frankenstein", "Mary Shelley", datetime.date(2025, 1, 1), "Fairport")
        result = return_book("Art", "Garfunkel", "Frankenstein", "Mary Shelley",  datetime.date(2025, 2, 4), "Fairport")
        self.assertEqual(((4, 7, 2, 'late_return', datetime.date(2025, 1, 1), datetime.date(2025, 2, 4)), (7, 2, 2, 1)),
                         result, "did not return book")
    
    # Jackie Gleason wants to reserve a copy of a book
    # The request fails when reserving incorrectly and succeeds when doing it correctly.
    def test_reserve_book(self):
        """"Reserving a book"""
        result = reserve_book("Jackie", "Gleason", "The Echoes of Glass", "Maren Elwood", "Towns of Penfield")
        self.assertEqual((3, 1, 1), result, "not able to reserve the book")
        result = reserve_book("Jackie", "Gleason", "The Lantern Keeper’s Promise", "Eira Monroe", "Fairport")
        self.assertEqual((3,), result, "able to reserve the book")    
    
    # All .csv books loaded successfully into database 
    # (your unittest should check for the count of items)
    def test_read_csv(self):
        """Reading csv file and inserting into DB"""
        read_csv()
        
        result = get_users()
        self.assertTrue(len(result) == 6, "row count has updated in users table")
        
        result = get_books()
        self.assertTrue(len(result) == 26, "row count has not updated in books table")
        
        result = get_inventory()
        self.assertTrue(len(result) == 36, "row count has not updated in inventory table")
        
        result = get_history()
        self.assertTrue(len(result) == 9, "row count has updated in history table")
        
        result = get_libraries()
        self.assertTrue(len(result) == 4, "not the correct amount of rows in history table")
        
    # The librarian gets a list of all books checked out (sorted by book type/ author); they need to see at least the details of:
    # Who checked it out and when; returned date (or if it’s not returned); remaining copies
    def test_get_list_of_checkout_books(self):
        """Get list of checked out books, sorted"""
        result = get_list_checkout_books()
        self.assertEqual([('Ada', 'Beneath Hollow Skies', datetime.date(2020, 3, 2), datetime.date(2020, 3, 8), 3),
                        ('Ada', 'The Echoes of Glass', datetime.date(2022, 9, 30), datetime.date(2022, 10, 1), 4),
                        ('Art', 'The Echoes of Glass', datetime.date(2022, 9, 30), None, 4), 
                        ('Frank', 'Frankenstein', datetime.date(2012, 8, 2), datetime.date(2012, 8, 30), 4),
                        ('Frank', 'The Hidden Cost of Convenience', datetime.date(2014, 4, 5), None, 4),
                        ('Jackie', 'Beneath Hollow Skies', datetime.date(2019, 10, 19), datetime.date(2019, 10, 21), 3),
                        ('Jackie', 'Frankenstein', datetime.date(2019, 10, 2), None, 4), 
                        ('Jackie', 'Voices from the Edge: Climate Stories from the Front Lines', datetime.date(2023, 5, 21), None, 4),
                        ('Mary', 'Beneath Hollow Skies', datetime.date(2020, 1, 5), datetime.date(2020, 1, 15), 3)],
                    result, "incorrect list of checked out books")
        
    """DB3"""
    def test_get_user_id(self):
        """Get a user id"""
        result = get_user_id("Ada", "Lovelace")
        self.assertEqual((1,), result, "not the correct user id")
        
    def test_get_book_id(self):
        """Get a book id"""
        result = get_book_id("The Hidden Cost of Convenience", "Marcus Leung")
        self.assertEqual((5,), result, "not the correct book id")
        
    def test_get_library_id(self):
        """Get a library id"""
        result = get_library_id("Pittsford")
        self.assertEqual((4,), result, "not the correct library id")
        
    def test_create_due_date(self):
        """Create due date for book"""
        checkout_date = datetime.date(2020, 1, 1)
        due_date = datetime.date(2020, 1, 15)
        result = create_due_date(checkout_date)
        self.assertEqual(due_date, result, "dates do not match")
        
    def test_check_overdue_books_by_user(self):
        """Check overdue books for a specific user"""
        result = check_overdue_books_by_user(3, datetime.date(2023, 7, 1))
        self.assertEqual([(6, datetime.date(2023, 5, 21), datetime.date(2023, 6, 5), None),
                            (7, datetime.date(2019, 10, 2), datetime.date(2019, 10, 16), None)],
                         result, "there were no overdue books for this user")

    def test_user_account_status(self):
        """Check User Account Status"""
        result = get_user_account_status(5) #Frank Wonder
        self.assertFalse(result, "account is activated")
        
        result = get_user_account_status(1) #Ada Lovelace
        self.assertTrue(result, "account is deactivated")
    
    def test_add_book(self):
        """Add a book to existing books"""
        result = add_book("The Winds of Winter", "George R.R. Martin", "Fiction", "Fantasy", datetime.date(2025, 1, 1),
                          "The epic struggle for power across Westeros and Essos as winter descends, old alliances fracture, and supernatural threats loom ever closer.")
        self.assertEqual(8, result, "did not create the book correctly")

    # “The Winds of Winter”, by George R.R. Martin - is added to inventory with each library only having 1 copy
    # A good samaritan donates 3 additional copies of the ‘The Winds of Winter’ to Fairport 
    # Another good samaritan donates 2 copies of “The Wines of Winter” by WineExpress to Pittsford and Henrietta. 
    def test_add_book_to_library(self):
        """Add # copies of a book to a library"""
        add_book("The Winds of Winter", "George R.R. Martin", "Fiction", "Fantasy", datetime.date(2025, 1, 1),
                "The epic struggle for power across Westeros and Essos as winter descends, old alliances fracture, and supernatural threats loom ever closer.")
        
        result = add_book_to_library("The Winds of Winter", "George R.R. Martin", 1, "Towns of Penfield")
        self.assertEqual((8, 1, 1), result, "did not insert the book correctly into the library")
        
        result = add_book_to_library("The Winds of Winter", "George R.R. Martin", 1, "Fairport")
        self.assertEqual((8, 2, 1), result, "did not insert the book correctly into the library")
        
        result = add_book_to_library("The Winds of Winter", "George R.R. Martin", 1, "Henrietta")
        self.assertEqual((8, 3, 1), result, "did not insert the book correctly into the library")
        
        result = add_book_to_library("The Winds of Winter", "George R.R. Martin", 1, "Pittsford")
        self.assertEqual((8, 4, 1), result, "did not insert the book correctly into the library")
        #
        result = add_book_to_library("The Winds of Winter", "George R.R. Martin", 3, "Fairport")
        self.assertEqual((8, 2, 4), result, "did not insert the book correctly into the library")
        #
        add_book("The Wines of Winter", "WineExpress", "Non-Fiction", "Food & Drink", datetime.date(2025, 1, 1),
         "A rich and flavorful journey through the best winter wines, curated by WineExpress to warm the coldest nights and pair with seasonal feasts.")

        result = add_book_to_library("The Wines of Winter", "WineExpress", 1, "Pittsford")
        self.assertEqual((9, 4, 1), result, "did not insert the book correctly into the library")
        
        result = add_book_to_library("The Wines of Winter", "WineExpress", 1, "Henrietta")
        self.assertEqual((9, 3, 1), result, "did not insert the book correctly into the library")
        
    def test_check_overdue_books_all_users(self):
        """Check overdue books for all users"""
        result = check_overdue_books_all_users(datetime.date(2025, 6, 11))
        self.assertEqual([(3, 6, datetime.date(2023, 5, 21), datetime.date(2023, 6, 5)),
                        (3, 7, datetime.date(2019, 10, 2), datetime.date(2019, 10, 16)),
                        (4, 1, datetime.date(2022, 9, 30), datetime.date(2022, 10, 14)), 
                        (5, 5, datetime.date(2014, 4, 5), datetime.date(2014, 4, 19))],
                         result, "did not get correct amount of overdue books")
    
    # The Fairport Librarian runs a report listing overdue books per user.
    def test_overdue_books_by_library(self):
        """Get overdue books by library"""
        result = get_overdue_books_by_library("Fairport", datetime.date(2019, 10, 30))
        self.assertEqual([('Jackie', 'Frankenstein', datetime.date(2019, 10, 2), datetime.date(2019, 10, 16)), 
                          ('Frank', 'The Hidden Cost of Convenience', datetime.date(2014, 4, 5), datetime.date(2014, 4, 19))],
                         result, "not the correct listing of overdue books")
    
    # The county librarian runs a report listing all books in all libraries
    # orderby library name and book title include count of books at each location
    def test_all_books_in_libraries(self):
        """Get all the books in all the libraries"""
        result = get_all_books_in_libraries()
        self.assertEqual([('Fairport', 'Frankenstein', 3),
                        ('Fairport', 'The Echoes of Glass', 3),
                        ('Fairport', 'The Hidden Cost of Convenience', 3),
                        ('Fairport', 'The Lantern Keeper’s Promise', 3),
                        ('Henrietta', 'Beneath Hollow Skies', 1),
                        ('Henrietta', 'Frankenstein', 2),
                        ('Henrietta', 'The Echoes of Glass', 1), 
                        ('Henrietta', 'The Hidden Cost of Convenience', 2), 
                        ('Henrietta', 'Wired for Wonder: The Neuroscience of Curiosity', 2), 
                        ('Pittsford', 'Beneath Hollow Skies', 1),
                        ('Pittsford', 'The Lantern Keeper’s Promise', 1),
                        ('Pittsford', 'Voices from the Edge: Climate Stories from the Front Lines', 4), 
                        ('Towns of Penfield', 'Beneath Hollow Skies', 3),
                        ('Towns of Penfield', 'The Echoes of Glass', 1),
                        ('Towns of Penfield', 'The Lantern Keeper’s Promise', 1), 
                        ('Towns of Penfield', 'Voices from the Edge: Climate Stories from the Front Lines', 1),
                        ('Towns of Penfield', 'Wired for Wonder: The Neuroscience of Curiosity', 3)],
                         result, "not the correct amount of books in libraries")
    
    #  A user should be able to get a listing of their own lending history including their late history.
    def test_user_lending_history(self):
        """Get a user's lending history"""
        result = get_user_lending_history(3, datetime.date(2023, 6, 1)) #Jackie Gleason
        self.assertEqual([('Pittsford', 'Beneath Hollow Skies', 'K.J. Harrow', datetime.date(2019, 10, 19), datetime.date(2019, 11, 3), datetime.date(2019, 10, 21), 'returned'),
                        ('Towns of Penfield', 'Voices from the Edge: Climate Stories from the Front Lines', 'Sarita Javed', datetime.date(2023, 5, 21), datetime.date(2023, 6, 5), None, 'checked_out')],
                         result, "not the correct lending history")
    
    #  A user should be able to get a listing of their own lending history including their late history.
    def test_user_late_history(self):
        """Get a user's late history"""
        result = get_user_late_history(3, datetime.date(2023, 6, 1)) #Jackie Gleason
        self.assertEqual([('Fairport', 'Frankenstein', 'Mary Shelley', datetime.date(2019, 10, 2), datetime.date(2019, 10, 16), None, 'overdue')],
                         result, "not the correct late history")
        
    # Also, a librarian can get a comprehensive list of all late books and histories
    def test_all_lending_history(self):
        """Get all users lending history"""
        result = get_all_lending_history(datetime.date(2023, 6, 1))
        self.assertEqual([('Ada', 'Lovelace', 'Henrietta', 'Beneath Hollow Skies', 'K.J. Harrow', datetime.date(2020, 3, 2), datetime.date(2020, 3, 16), datetime.date(2020, 3, 8), 'returned'),
                        ('Ada', 'Lovelace', 'Towns of Penfield', 'The Echoes of Glass', 'Maren Elwood', datetime.date(2022, 9, 30), datetime.date(2022, 10, 14), datetime.date(2022, 10, 1), 'returned'),
                        ('Jackie', 'Gleason', 'Pittsford', 'Beneath Hollow Skies', 'K.J. Harrow', datetime.date(2019, 10, 19), datetime.date(2019, 11, 3), datetime.date(2019, 10, 21), 'returned'),
                        ('Jackie', 'Gleason', 'Towns of Penfield', 'Voices from the Edge: Climate Stories from the Front Lines', 'Sarita Javed', datetime.date(2023, 5, 21), datetime.date(2023, 6, 5), None, 'checked_out'), 
                        ('Mary', 'Shelley', 'Pittsford', 'Beneath Hollow Skies', 'K.J. Harrow', datetime.date(2020, 1, 5), datetime.date(2020, 1, 19), datetime.date(2020, 1, 15), 'returned')],
                         result, "not the correct amount of entries in lending history")
    
    # Also, a librarian can get a comprehensive list of all late books and histories
    def test_all_late_history(self):
        """Get all users late history"""
        result = get_all_late_history(datetime.date(2023, 6, 1))
        self.assertEqual([('Art', 'Garfunkel', 'Towns of Penfield', 'The Echoes of Glass', 'Maren Elwood', datetime.date(2022, 9, 30), datetime.date(2022, 10, 14), None, 'overdue'), 
                        ('Frank', 'Wonder', 'Fairport', 'The Hidden Cost of Convenience', 'Marcus Leung', datetime.date(2014, 4, 5), datetime.date(2014, 4, 19), None, 'overdue'),
                        ('Frank', 'Wonder', 'Fairport', 'Frankenstein', 'Mary Shelley', datetime.date(2012, 8, 2), datetime.date(2012, 8, 16), datetime.date(2012, 8, 30), 'late_return'),
                        ('Jackie', 'Gleason', 'Fairport', 'Frankenstein', 'Mary Shelley', datetime.date(2019, 10, 2), datetime.date(2019, 10, 16), None, 'overdue')],
                         result, "not the correct amount of entries in late history")
    
    #A new book - the long awaited Game of Thrones installment, “The Winds of Winter”, by George R.R. Martin 
    # - is added to inventory with each library only having 1 copy. 
    # The follow checkouts occur @ Fairport.
        # Mary checks it out on Jan. 2nd and returns in in 8 days.
        # Ada checks it out on Jan 13th and returns it in 18 days.
        # Ada tries to check out another book 15 days after checking out “The Winds of Winter”, 
            # but her request is rejected due to the late status of her currently checked out book.
        # Jackie checks it out on March 1st and returns it in 30 days.
    def test_checkout_return_series(self):
        """Fairport checkout and return series"""
        #set up 
        add_book("The Winds of Winter", "George R.R. Martin", "Fiction", "Fantasy", datetime.date(2025, 1, 1),
                "The epic struggle for power across Westeros and Essos as winter descends, old alliances fracture, and supernatural threats loom ever closer.")
        add_book_to_library("The Winds of Winter", "George R.R. Martin", 1, "Towns of Penfield")
        add_book_to_library("The Winds of Winter", "George R.R. Martin", 1, "Fairport")
        add_book_to_library("The Winds of Winter", "George R.R. Martin", 1, "Henrietta")
        add_book_to_library("The Winds of Winter", "George R.R. Martin", 1, "Pittsford")
        #testing
        result = checkout_book("Mary", "Shelley", "The Winds of Winter", "George R.R. Martin", datetime.date(2025, 1, 2), "Fairport")
        self.assertEqual(((2, 8, 2, 'checked_out', datetime.date(2025, 1, 2), datetime.date(2025, 1, 16), None), (8, 2, 0, 1)),
                         result, "did not check out book")
         
        result = return_book("Mary", "Shelley", "The Winds of Winter", "George R.R. Martin", datetime.date(2025, 1, 10), "Fairport" )
        self.assertEqual(((2, 8, 2, 'returned', datetime.date(2025, 1, 2), datetime.date(2025, 1, 10)), (8, 2, 1, 0)),
                         result, "did not return book")
        
        result = checkout_book("Ada", "Lovelace", "The Winds of Winter", "George R.R. Martin", datetime.date(2025, 1, 13), "Fairport")
        self.assertEqual(((1, 8, 2, 'checked_out', datetime.date(2025, 1, 13), datetime.date(2025, 1, 27), None), (8, 2, 0, 1)),
                         result, "did not check out book")
        
        result = checkout_book("Ada", "Lovelace", "The Lantern Keeper’s Promise", "Eira Monroe", datetime.date(2025, 1, 28), "Fairport")
        self.assertFalse(result, "checked out book")
        #check if account was deactivated
        user_id = get_user_id("Ada", "Lovelace")
        result = get_user_account_status(user_id)
        self.assertFalse(result, "account was not deactivated")
        
        result = return_book("Ada", "Lovelace", "The Winds of Winter", "George R.R. Martin", datetime.date(2025, 1, 31), "Fairport")
        self.assertEqual(((1, 8, 2, 'late_return', datetime.date(2025, 1, 13), datetime.date(2025, 1, 31)), (8, 2, 1, 0)),
                         result, "did not return book")
        
        #set up 
        return_book("Jackie", "Gleason", "Voices from the Edge: Climate Stories from the Front Lines", "Sarita Javed", datetime.date(2023, 6, 1), "Towns of Penfield")
        return_book("Jackie", "Gleason", "Frankenstein", "Mary Shelley", datetime.date(2019, 10, 3), "Fairport")
        
        result = checkout_book("Jackie", "Gleason", "The Winds of Winter", "George R.R. Martin", datetime.date(2025, 3, 1), "Fairport")
        self.assertEqual(((3, 8, 2, 'checked_out', datetime.date(2025, 3, 1), datetime.date(2025, 3, 15), None), (8, 2, 0, 1)),
                         result, "did not check out book")

        result = return_book("Jackie", "Gleason", "The Winds of Winter", "George R.R. Martin", datetime.date(2025, 3, 31), "Fairport" )
        self.assertEqual(((3, 8, 2, 'late_return', datetime.date(2025, 3, 1), datetime.date(2025, 3, 31)), (8, 2, 1, 0)),
                         result, "did not return book")

    """DB4"""
    # There will be a late-fee charge if the book is past due. 
    # A per day penalty of $0.25 for the first week, and $2.00 per day after that
    def test_calculate_late_fee(self):
        """Calculate late fee"""
        # return before due date
        result = calculate_late_fee(datetime.date(2020, 1, 2), datetime.date(2020, 1, 1))
        self.assertEqual(0.0, result, "incorrect late fee")
        
        # under 1 week
        result = calculate_late_fee(datetime.date(2020, 1, 1), datetime.date(2020, 1, 7))
        self.assertEqual(1.5, result, "incorrect late fee")
        
        # exactly 1 week
        result = calculate_late_fee(datetime.date(2020, 1, 1), datetime.date(2020, 1, 8))
        self.assertEqual(1.75, result, "incorrect late fee")
        
        # over 1 week
        result = calculate_late_fee(datetime.date(2020, 1, 1), datetime.date(2020, 1, 9))
        self.assertEqual(3.75, result, "incorrect late fee")
     
    def test_report_book_late_fees(self):
        """"Report late book fees"""
        report_book_late_fees(datetime.date(2021, 1, 1))
        
    def test_report_user_info(self):
        """Report user information"""
        report_user_info(datetime.date(2021, 1, 1))
     
    def test_report_checked_out_books_by_library(self):
        """Report checked out books by library"""
        report_checked_out_books_by_library()
    
    def test_report_checked_out_books_days(self):
        """"Report checked out books include days borrowed"""
        report_checked_out_books_days()
     
     
     