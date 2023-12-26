import sqlite3
import json
import random


def initialize_db(db_name='iron_farm.db'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Create users table
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

    # Create business table
    cur.execute('''
            CREATE TABLE IF NOT EXISTS business (
                user_id INTEGER,
                BusinessID INTEGER PRIMARY KEY,
                business_name TEXT,
                city TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
    # Create VolunteerActivity table
    cur.execute('''
            CREATE TABLE IF NOT EXISTS VolunteerActivity (
                ActivityID INTEGER PRIMARY KEY,
                BusinessID INTEGER,
                StartTime TEXT NOT NULL,
                EndTime TEXT NOT NULL,
                IsPhysical INTEGER NOT NULL,
                NumberOfVolunteers INTEGER NOT NULL,
                VolunteersNeeded INTEGER NOT NULL,
                type_volunteer TEXT,
                ActivityDescription TEXT,
                FOREIGN KEY(BusinessID) REFERENCES business(BusinessID)
            )
        ''')

    # Create user_to_volunteer table
    cur.execute('''
            CREATE TABLE IF NOT EXISTS user_to_volunteer (
                UserID INTEGER,
                ActivityID INTEGER,
                FOREIGN KEY(UserID) REFERENCES users(user_id),
                FOREIGN KEY(ActivityID) REFERENCES VolunteerActivity(ActivityID)
            )
        ''')

    # Create indexes for the VolunteerActivity table
    cur.execute('CREATE INDEX IF NOT EXISTS idx_type_of_volunteer ON VolunteerActivity(type_volunteer);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_start_time ON VolunteerActivity(StartTime);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_locate ON VolunteerActivity(city);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_email_user ON users(email);')

    # Create a trigger for after an insert on user_to_volunteer
    cur.execute('''
            CREATE TRIGGER IF NOT EXISTS AfterUserVolunteerActivityInsert
            AFTER INSERT ON user_to_volunteer
            BEGIN
                UPDATE VolunteerActivity
                SET VolunteersNeeded = VolunteersNeeded - 1
                WHERE ActivityID = NEW.ActivityID
                AND VolunteersNeeded > 0;
            END;
        ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
