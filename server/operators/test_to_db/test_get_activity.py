import os
import unittest
import sqlite3
from datetime import datetime, timedelta

# Replace with the actual path where your get_activity function is located.
from server.operators.db import get_activity  # Ensure correct import path

class TestGetActivityFunction(unittest.TestCase):
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

        # Assuming you have 'business' and 'VolunteerActivity' tables
        cur.execute('''CREATE TABLE IF NOT EXISTS business (
                       BusinessID INTEGER PRIMARY KEY,
                       business_name TEXT,
                       city TEXT)''')

        cur.execute('''CREATE TABLE IF NOT EXISTS VolunteerActivity (
                       ActivityID INTEGER PRIMARY KEY,
                       BusinessID INTEGER,
                       Date TEXT NOT NULL,
                       IsPhysical INTEGER NOT NULL,
                       type_volunteer TEXT,
                       VolunteersNeeded INTEGER NOT NULL,
                       ActivityDescription TEXT,
                       FOREIGN KEY(BusinessID) REFERENCES business(BusinessID))''')

        conn.commit()
        conn.close()

    @classmethod
    def insert_test_data(cls):
        """Insert sample data for testing."""
        conn = sqlite3.connect(cls.test_db)
        cur = conn.cursor()

        # Inserting a sample business
        cur.execute("INSERT INTO business (business_name, city) VALUES (?, ?)", ('Doe Enterprises', 'SampleCity'))
        business_id = cur.lastrowid

        # Inserting sample activities
        cur.execute(
            "INSERT INTO VolunteerActivity (BusinessID, Date, IsPhysical, type_volunteer, ActivityDescription,VolunteersNeeded) VALUES (?, ?, ?, ?, ?,?)",
            (business_id, '2024-01-01', 1, 'Type1', 'Sample Activity 1', 5))
        cur.execute(
            "INSERT INTO VolunteerActivity (BusinessID, Date, IsPhysical, type_volunteer, ActivityDescription,VolunteersNeeded) VALUES (?, ?, ?, ?, ?,?)",
            (business_id, datetime.now().strftime('%Y-%m-%d'), 0, 'Type2', 'Sample Activity 2', 3))

        conn.commit()
        conn.close()



    def test_get_activity_by_date_range(self):
        """Test getting activities filtered by a date range."""
        activities = get_activity(start_date="2024-01-01", end_date="2024-12-31", db_name=self.test_db)
        self.assertIsNotNone(activities)
        # Ensure that the returned activities fall within the specified date range
        self.assertTrue(any('2024-01-01' <= activity[2] <= '2024-12-31' for activity in activities))

    def test_get_activity_default_date(self):
        """Test getting activities with default date (today)."""
        today = datetime.now().strftime('%Y-%m-%d')
        activities = get_activity(db_name=self.test_db)
        self.assertIsNotNone(activities)
        # Ensure that the returned activities are from today onwards by default
        for activity in activities:
            print(activity[2])
        self.assertTrue(all(activity[2] >= today for activity in activities))

    def test_get_activity_by_physical_and_type(self):
        """Test getting activities filtered by physicality and type."""
        activities = get_activity(is_physical=1, type_volunteer="Type1", db_name=self.test_db)
        self.assertIsNotNone(activities)
        # Ensure that the returned activities match the specified physicality and type
        self.assertTrue(any(activity[3] == 1 and activity[4] == "Type1" for activity in activities))

    @classmethod
    def tearDownClass(cls):
        """Delete the test database file after all tests are done."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

if __name__ == '__main__':
    unittest.main()
