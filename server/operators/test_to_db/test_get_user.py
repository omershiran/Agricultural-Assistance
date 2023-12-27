import unittest
import sqlite3
import os

# Replace with the actual path where your get_user function is located.
from server.operators.db import get_user

class TestGetUserFunction(unittest.TestCase):
    test_db = 'test_iron_farm.db'

    @classmethod
    def setUpClass(cls):
        """Create a fresh test database before any tests start."""
        cls.initialize_test_db()

    @classmethod
    def initialize_test_db(cls):
        """Set up a clean test database."""
        conn = sqlite3.connect(cls.test_db)
        cur = conn.cursor()

        # Create the users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                firstname TEXT,
                LastName TEXT,
                email TEXT UNIQUE,
                password TEXT,
                phone_number TEXT
            );
        ''')

        # Create the business table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS business (
                BusinessID INTEGER PRIMARY KEY,
                user_id INTEGER,
                business_name TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        ''')

        # Commit changes and close connection
        conn.commit()
        conn.close()

    def test_get_user_success_with_business(self):
        """Test retrieving a user with an associated business."""
        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()

        # Insert a user
        cur.execute("INSERT INTO users (firstname, LastName, email, password, phone_number) VALUES (?, ?, ?, ?, ?)",
                    ('John', 'Doe', 'john.doe@example.com', 'password123', '555-555-5555'))
        user_id = cur.lastrowid

        # Insert a business associated with the user
        cur.execute("INSERT INTO business (user_id, business_name) VALUES (?, ?)", (user_id, 'John Doe Inc.'))
        conn.commit()

        # Test getting the user
        success, retrieved_user_id, business_id = get_user('john.doe@example.com', 'password123', self.test_db)
        self.assertTrue(success)
        self.assertEqual(retrieved_user_id, user_id)
        self.assertIsNotNone(business_id)

        conn.close()

    def test_get_user_success_no_business(self):
        """Test retrieving a user with no associated business."""
        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()

        # Insert a user without a business
        cur.execute("INSERT INTO users (firstname, LastName, email, password, phone_number) VALUES (?, ?, ?, ?, ?)",
                    ('Jane', 'Doe', 'jane.doe@example.com', 'password123', '555-555-5555'))
        user_id = cur.lastrowid
        conn.commit()

        # Test getting the user
        success, retrieved_user_id, business_id = get_user('jane.doe@example.com', 'password123', self.test_db)
        self.assertTrue(success)
        self.assertEqual(retrieved_user_id, user_id)
        self.assertIsNone(business_id)

        conn.close()

    def test_get_user_failure(self):
        """Test retrieving a user that does not exist."""
        success, user_id, business_id = get_user('nonexistent@example.com', 'password', self.test_db)
        self.assertFalse(success)
        self.assertIsNone(user_id)
        self.assertIsNone(business_id)

    @classmethod
    def tearDownClass(cls):
        """Delete the test database file after all tests are done."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

if __name__ == '__main__':
    unittest.main()
