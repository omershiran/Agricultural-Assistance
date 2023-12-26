import unittest
import sqlite3
import os

# Replace with the actual path where your create_activity function is located.
from server.operators.db import create_activity

class TestCreateActivityFunction(unittest.TestCase):
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

        # Create the necessary tables: users, business, and VolunteerActivity
        # Make sure these definitions match your schema
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
        cur.execute('''
            CREATE TABLE IF NOT EXISTS business (
                BusinessID INTEGER PRIMARY KEY,
                user_id INTEGER,
                business_name TEXT,
                city TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS VolunteerActivity (
                ActivityID INTEGER PRIMARY KEY,
                BusinessID INTEGER,
                Date TEXT NOT NULL,
                IsPhysical INTEGER NOT NULL,
                NumberOfVolunteers INTEGER NOT NULL,
                VolunteersNeeded INTEGER NOT NULL,
                type_volunteer TEXT,
                ActivityDescription TEXT,
                FOREIGN KEY(BusinessID) REFERENCES business(BusinessID)
            );
        ''')

        # Insert a test user and a test business to associate with activities
        cur.execute("INSERT INTO users (firstname, LastName, email, password, phone_number) VALUES (?, ?, ?, ?, ?)",
                    ('John', 'Doe', 'john.doe@example.com', 'password123', '555-555-5555'))
        user_id = cur.lastrowid

        cur.execute("INSERT INTO business (user_id, business_name, city) VALUES (?, ?, ?)",
                    (user_id, 'Doe Enterprises', 'New City'))
        cls.test_business_id = cur.lastrowid

        # Commit changes and close connection
        conn.commit()
        conn.close()

    def test_create_activity_success(self):
        """Test creating an activity successfully."""
        success = create_activity(
            self.test_business_id,
            '2022-01-01',
            1,
            10,
            'Type1',
            'Description of activity',
            self.test_db
        )
        self.assertTrue(success)

    def test_create_activity_failure(self):
        """Test handling failure when creating an activity with invalid data."""
        # Example: Using an invalid BusinessID
        success = create_activity(
            9999,  # assuming 9999 is an invalid BusinessID
            '2022-01-01',
            1,
            10,
            'Type1',
            'Description of activity',
            self.test_db
        )
        self.assertFalse(success)

    @classmethod
    def tearDownClass(cls):
        """Delete the test database file after all tests are done."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

if __name__ == '__main__':
    unittest.main()
