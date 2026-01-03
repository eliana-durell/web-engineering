import unittest
from tests.test_utils import *

# validate the integrity of the database 
# (checking that the database is in the correct structure and state)
class TestLibrarySchema(unittest.TestCase):

    def test_rebuild_tables(self):
        """Rebuild the tables"""
        post_rest_call(self, 'http://127.0.0.1:4999/manage/init')
        
        result = get_rest_call(self, 'http://127.0.0.1:4999/users')
        self.assertNotEqual([], result, "no rows in users table")
        
        result = get_rest_call(self, 'http://127.0.0.1:4999/books')
        self.assertNotEqual([], result, "no rows in books table")
        
        result = get_rest_call(self, 'http://127.0.0.1:4999/inventory')
        self.assertNotEqual([], result, "no rows in inventory table")
        
        result = get_rest_call(self, 'http://127.0.0.1:4999/history')
        self.assertNotEqual([], result, "no rows in history table")
        
        result = get_rest_call(self, 'http://127.0.0.1:4999/libraries')
        self.assertNotEqual([], result, "no rows in history table")

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        post_rest_call(self, 'http://127.0.0.1:4999/manage/init')
        post_rest_call(self, 'http://127.0.0.1:4999/manage/init')
        
        result = get_rest_call(self, 'http://127.0.0.1:4999/users')
        self.assertNotEqual([], result, "no rows in users table")
        self.assertTrue(len(result) == 6, "not the correct amount of rows in users table")
