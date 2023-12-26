import os
import unittest
import sqlite3
from datetime import datetime, timedelta

# Replace with the actual path where your functions are located
from server.operators.db import make_match, get_db_connection

class TestMakeMatchFunction(unittest.TestCase):
    test_db = 'test_iron_farm.db'

    @classmethod
    def setUpClass(cls):
        """Create a fresh test database before any tests start."""
        cls.initialize_test_db()
        cls.insert_test_data()

    @classmethod
    def initialize_test_db(cls):
        """Set up a clean test database."""
        conn = sqlite3.connect(cls.test_db)
        cur = conn.cursor()

        # Create necessary tables
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                       user_id INTEGER PRIMARY KEY,
                       email TEXT UNIQUE)''')

        cur.execute('''CREATE TABLE IF NOT EXISTS VolunteerActivity (
                       ActivityID INTEGER PRIMARY KEY,
                       Date TEXT NOT NULL)''')

        cur.execute('''CREATE TABLE IF NOT EXISTS user_to_volunteer (
                       UserID INTEGER,
                       ActivityID INTEGER,
                       PRIMARY KEY(UserID, ActivityID),
                       FOREIGN KEY(UserID) REFERENCES users(user_id),
                       FOREIGN KEY(ActivityID) REFERENCES VolunteerActivity(ActivityID))''')

        conn.commit()
        conn.close()

    @classmethod
    def insert_test_data(cls):
        """Insert sample data for testing."""
        conn = sqlite3.connect(cls.test_db)
        cur = conn.cursor()

        # Inserting a sample user and activities
        cur.execute("INSERT INTO users (email) VALUES ('user@example.com')")
        cls.sample_user_id = cur.lastrowid

        # Inserting activities: one for today, one for tomorrow
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        cur.execute("INSERT INTO VolunteerActivity (Date) VALUES (?)", (today,))
        cls.activity_today_id = cur.lastrowid
        cur.execute("INSERT INTO VolunteerActivity (Date) VALUES (?)", (tomorrow,))
        cls.activity_tomorrow_id = cur.lastrowid

        conn.commit()
        conn.close()

    def test_make_match_success(self):
        """Test making a match successfully."""
        result = make_match(self.sample_user_id, self.activity_tomorrow_id, self.test_db)
        self.assertTrue(result)

    def test_make_match_failure_same_day(self):
        """Test failure when trying to make a match for the same day."""
        # First, make a successful match for today
        make_match(self.sample_user_id, self.activity_today_id, self.test_db)

        # Then, try to make another match for today
        result = make_match(self.sample_user_id, self.activity_today_id, self.test_db)
        self.assertFalse(result)

    def test_make_match_no_activity(self):
        """Test failure when trying to make a match with a non-existent activity."""
        result = make_match(self.sample_user_id, 9999, self.test_db)  # Assuming 9999 is a non-existent activity ID
        self.assertFalse(result)

    @classmethod
    def tearDownClass(cls):
        """Delete the test database file after all tests are done."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

if __name__ == '__main__':
    unittest.main()
