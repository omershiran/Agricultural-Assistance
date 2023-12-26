import unittest
import sqlite3
import os

# Replace 'db_operations' with the actual name of your Python file containing add_user
from server.operators.db import add_user


class TestAddUserFunction(unittest.TestCase):
    test_db = 'test_iron_farm.db'

    @classmethod
    def setUpClass(cls):
        # Set up a fresh test database before all tests start
        cls.initialize_test_db()

    @classmethod
    def initialize_test_db(cls):
        # Connect to a SQLite database (or create it if not exists)
        conn = sqlite3.connect(cls.test_db)
        cur = conn.cursor()

        # Create table structure
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                firstname TEXT,
                LastName TEXT,
                email TEXT UNIQUE,
                password TEXT,
                phone_number TEXT
            )
        ''')

        # Commit changes and close connection
        conn.commit()
        conn.close()

    def test_add_user_success(self):
        """Test adding a user successfully."""
        success, user_id = add_user('John', 'Doe', 'john.doe@example.com', 'password123', '555-555-5555', self.test_db)
        print(success)
        self.assertTrue(success, "Failed to add a user when it should have succeeded.")
        self.assertIsNotNone(user_id, "User ID should not be None after successful insertion.")

    def test_add_user_duplicate_email(self):
        """Test adding a user with a duplicate email."""
        # First insert with unique email
        add_user('Jane', 'Doe', 'jane.doe@example.com', 'password123', '555-555-5556', self.test_db)

        # Attempt to insert another user with the same email
        success, user_id = add_user('Janet', 'Doe', 'jane.doe@example.com', 'password123', '555-555-5557', self.test_db)

        # Assert that the function should return False and None for the user ID
        self.assertFalse(success, "Added a user with a duplicate email when it should have failed.")
        self.assertIsNone(user_id, "User ID should be None when insertion fails.")

    @classmethod
    def tearDownClass(cls):
        # Delete the test database file after all tests are done
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)


if __name__ == '__main__':
    unittest.main()
