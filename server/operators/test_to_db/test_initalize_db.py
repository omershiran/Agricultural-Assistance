import sqlite3
import unittest
import os

from server.operators.db import initialize_db  # Ensure this path is correct


class TestDatabaseInitialization(unittest.TestCase):
    test_db = 'test_iron_farm.db'  # Specify the test database file

    @classmethod
    def setUpClass(cls):
        """Set up database once before any tests are run."""
        initialize_db(cls.test_db)

    def setUp(self):
        """Set up the database before each test."""
        print("Setting up database...")

    def test_tables_created(self):
        """Test that all tables are created."""
        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()

        tables = ["users", "business", "VolunteerActivity", "user_to_volunteer"]
        for table in tables:
            with self.subTest(table=table):
                print(f"Checking table: {table}")
                try:
                    cur.execute(f'SELECT * FROM {table}')
                except sqlite3.OperationalError as e:
                    self.fail(f"{table} table does not exist. Error: {e}")

        conn.close()

    def test_trigger_after_user_volunteer_insert(self):
        """Test that VolunteersNeeded decrements by 1 when a new user_to_volunteer is inserted."""
        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()

        # Assuming there is already some data in the VolunteerActivity and users tables
        # Insert a test volunteer activity and a user
        cur.execute("INSERT INTO users (firstname, LastName, email, password, phone_number) VALUES (?, ?, ?, ?, ?)",
                    ('Test', 'User', 'test@example.com', 'pass123', '1234567890'))
        user_id = cur.lastrowid  # Get the ID of the inserted user

        cur.execute("INSERT INTO business (user_id, business_name, region) VALUES (?, ?, ?)",
                    (user_id, 'Test Business', 'Test Region'))
        business_id = cur.lastrowid  # Get the ID of the inserted business

        cur.execute(
            "INSERT INTO VolunteerActivity (BusinessID, city, StartTime, EndTime, IsPhysical, NumberOfVolunteers, VolunteersNeeded, type_volunteer, ActivityDescription) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (business_id, 'Test City', '2021-01-01 09:00:00', '2021-01-01 12:00:00', 1, 10, 10, 'Test Type',
             'Test Description'))
        activity_id = cur.lastrowid  # Get the ID of the inserted activity

        # Insert a new user_to_volunteer record to trigger the decrement of VolunteersNeeded
        cur.execute("INSERT INTO user_to_volunteer (UserID, ActivityID) VALUES (?, ?)", (user_id, activity_id))

        # Now, check if the VolunteersNeeded has decremented
        cur.execute("SELECT VolunteersNeeded FROM VolunteerActivity WHERE ActivityID = ?", (activity_id,))
        volunteers_needed = cur.fetchone()[0]

        self.assertEqual(volunteers_needed, 9, "VolunteersNeeded did not decrement by 1 as expected")

        conn.close()

    def test_indexes_created(self):
        """Test that indexes are created correctly."""
        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()

        # Dictionary of expected indexes and the table they should be on
        expected_indexes = {
            'idx_type_of_volunteer': 'VolunteerActivity',
            'idx_start_time': 'VolunteerActivity',
            'idx_locate': 'VolunteerActivity'
        }

        for index_name, table_name in expected_indexes.items():
            with self.subTest(index=index_name):
                cur.execute("PRAGMA index_list('{}')".format(table_name))
                indexes = cur.fetchall()

                # Check if the index is in the list of indexes for the table
                found = any(index_name in row for row in indexes)
                self.assertTrue(found, f"Index {index_name} on table {table_name} does not exist.")

        conn.close()

    @classmethod
    def tearDownClass(cls):
        """Delete the test database file after all tests are done."""
        print("Cleaning up: Deleting test database file.")
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)


if __name__ == '__main__':
    unittest.main()
