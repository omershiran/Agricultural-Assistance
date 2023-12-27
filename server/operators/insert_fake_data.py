import sqlite3
from datetime import datetime, timedelta
import random

from server.operators.db import get_db_connection


def insert_random_activities_no_faker_fixed_v2(db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
    cur = conn.cursor()
    try:
                # Clearing existing data before repopulating
        cur.executescript('''
            DELETE FROM user_to_volunteer;
            DELETE FROM VolunteerActivity;
            DELETE FROM business;
            DELETE FROM users;
        ''')
        conn.commit()

        # Sample data sets
        first_names = ["John", "Jane", "Alex", "Alice", "Bob", "Sara", "Michael", "Rachel", "Tom", "Laura"]
        last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Taylor", "Anderson"]
        company_names = ["Alpha Co", "Beta Ltd", "Gamma Corp", "Delta Inc", "Epsilon LLC", "Zeta GmbH", "Eta SA", "Theta Pty", "Iota AG", "Kappa NV"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
        activity_types = ["Environmental", "Community", "Educational"]
        descriptions = ["Help clean up local parks.", "Assist in a community kitchen.", "Teach coding to kids.", "Participate in urban tree planting.", "Help organize a charity run.", "Lead a neighborhood watch group.", "Support a local art event.", "Contribute to a beach clean-up.", "Work at a local animal shelter.", "Tutor students in a local school."]

        # Inserting users and businesses
        user_ids = []
        for i in range(10):
            cur.execute("INSERT INTO users (firstname, LastName, email, password, phone_number) VALUES (?, ?, ?, ?, ?)",
                        (first_names[i], last_names[i], f"user{i}@mail.com", "pass1234", f"555-010{i}"))
            user_id = cur.lastrowid  # Store user ID for business association
            user_ids.append(user_id)
            cur.execute("INSERT INTO business (user_id, business_name, city) VALUES (?, ?, ?)",
                        (user_id, company_names[i], cities[i]))

        conn.commit()  # Commit the users and businesses

        # Inserting random activities associated with the businesses
        for i in range(10):
            business_id = i + 1  # Use sequential business IDs from earlier insertion
            cur.execute('''
                INSERT INTO VolunteerActivity (BusinessID, Date, IsPhysical, NumberOfVolunteers, VolunteersNeeded, type_volunteer, ActivityDescription)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    business_id,
                    (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
                    random.randint(0, 1),
                    random.randint(5, 20),
                    random.randint(1, 10),
                    activity_types[i % len(activity_types)],
                    descriptions[i % len(descriptions)]
                ))

        conn.commit()  # Commit the activities
    except sqlite3.OperationalError as e:
        print(f"An operational error occurred: {e}")
    finally:
        if conn:
            conn.close()  # Ensure the connection is closed

# Run the function to insert ten random activities without using Faker and with corrected user-business associations and error handling
insert_random_activities_no_faker_fixed_v2()
