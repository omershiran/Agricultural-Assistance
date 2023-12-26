import unittest
import sqlite3
import os

# Replace with the actual path where your create_business function is located.
from server.operators.db import create_business

class TestCreateBusinessFunction(unittest.TestCase):
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
                business_name TEXT,
                city TEXT,
                user_id INTEGER UNIQUE,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        ''')



        # Commit changes and close connection
        conn.commit()
        conn.close()

    def test_create_business_success(self):
        """Test creating a business successfully."""
        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (firstname, LastName, email, password, phone_number) VALUES (?, ?, ?, ?, ?)",
                    ('John', 'Doe', 'john.success@example.com', 'password123', '555-555-5555'))
        user_id = cur.lastrowid
        conn.commit()

        business_id, success = create_business('Doe Enterprises', 'New City', user_id, self.test_db)
        self.assertTrue(success)
        self.assertIsNotNone(business_id)
        conn.close()

    def test_create_business_failure(self):
        """Test handling failure when creating a business (e.g., duplicate name)."""
        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (firstname, LastName, email, password, phone_number) VALUES (?, ?, ?, ?, ?)",
                    ('Jane', 'Doe', 'jane.failure@example.com', 'password123', '555-555-5555'))
        user_id = cur.lastrowid
        conn.commit()

        # First, create a business successfully
        create_business('Doe Enterprises', 'New City', user_id, self.test_db)

        # Then, try creating another business with the same name (assuming business_name needs to be unique)
        business_id, success = create_business('Doe Enterprises', 'Old City', user_id, self.test_db)
        self.assertFalse(success)
        self.assertIsNone(business_id)
        conn.close()
    @classmethod
    def tearDownClass(cls):
        """Delete the test database file after all tests are done."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

if __name__ == '__main__':
    unittest.main()
