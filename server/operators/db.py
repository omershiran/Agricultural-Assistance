import sqlite3
import json
import random
from datetime import datetime


def initialize_db(db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
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
                user_id INTEGER UNIQUE,
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
                Date TEXT NOT NULL,
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
    cur.execute('CREATE INDEX IF NOT EXISTS idx_date ON VolunteerActivity(date);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_locate ON business(city);')
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


def add_user(first_name, last_name, email, password, phone_number, db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
    cur = conn.cursor()
    try:
        # Connect to the SQLite database

        # Insert a new record into the users table
        cur.execute('''
                INSERT INTO users (firstname, LastName, email, password, phone_number)
                VALUES (?, ?, ?, ?, ?)
                ''', (first_name, last_name, email, password, phone_number))

        # Commit the changes and retrieve the new user_id
        conn.commit()
        user_id = cur.lastrowid

        # Close the connection
        conn.close()

        return True, user_id  # Return True and the new user_id

    except sqlite3.IntegrityError as e:
        # Handle any database constraints (e.g., unique email) violation
        print(f"Error adding user: {e}")
        conn.close()
        return False, None  # Return False and None for user_id

    except Exception as e:
        # Handle other exceptions such as database connection errors
        print(f"An error occurred: {e}")
        conn.close()
        return False, None


def get_user(email, password, db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
    cur = conn.cursor()
    try:

        # Query to find the user with the given email and password
        cur.execute('''
            SELECT users.user_id, business.BusinessID FROM users
            LEFT JOIN business ON users.user_id = business.user_id
            WHERE users.email = ? AND users.password = ?
            ''', (email, password))

        # Fetch one result
        result = cur.fetchone()

        # Close the connection
        conn.close()

        # Check if a result was found
        if result:
            user_id, business_id = result
            # Return True with the user_id and business_id (business_id may be None if not associated)
            return True, user_id, business_id
        else:
            return False, None, None  # Return False if no user was found

    except sqlite3.Error as e:
        conn.close()
        # Handle any SQLite errors
        print(f"An error occurred: {e}")
        return False, None, None  # Return False if there's an error


def create_business(business_name, city, user_id, db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
    cur = conn.cursor()
    try:
        cur.execute('''
                INSERT INTO business (business_name, city, user_id)
                VALUES (?, ?, ?)
                ''', (business_name, city, user_id))

        # Commit the changes and retrieve the new business_id
        conn.commit()
        business_id = cur.lastrowid

        # Close the connection
        conn.close()

        return business_id, True  # Return the new business_id and True for success

    except sqlite3.IntegrityError as e:
        # Handle any database constraints violation (e.g., unique business name, if applicable)
        print(f"Integrity Error: {e}")
        conn.close()
        return None, False  # Return None for business_id and False for failure

    except sqlite3.Error as e:
        # Handle any SQLite errors
        print(f"An error occurred: {e}")
        conn.close()
        return None, False


def create_activity(BusinessID, date, is_physical, NumberOfVolunteers, type_volunteer, ActivityDescription,
                    db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
    cur = conn.cursor()
    try:

        # Insert a new record into the VolunteerActivity table
        cur.execute('''
            INSERT INTO VolunteerActivity (BusinessID, Date, IsPhysical, NumberOfVolunteers,VolunteersNeeded, type_volunteer, ActivityDescription)
            VALUES (?, ?, ?, ?, ?, ?,?)
            ''', (
            BusinessID, date, is_physical, NumberOfVolunteers, NumberOfVolunteers, type_volunteer, ActivityDescription))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

        return True  # Return True for success

    except sqlite3.IntegrityError as e:
        # Handle any database constraints violation (e.g., foreign key constraint)
        print(f"Integrity Error: {e}")
        conn.close()
        return False  # Return False for failure

    except sqlite3.Error as e:
        # Handle any SQLite errors
        print(f"An error occurred: {e}")
        conn.close()
        return False  # Return False for failure


def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")  # Enable FK enforcement
    return conn


def get_activity(city=None, start_date=None, end_date=None, is_physical=None, type_volunteer=None,
                 db_name='iron_farm.db'):
    # Establish a connection to the database
    conn = get_db_connection(db_name)
    cur = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    # Base SQL query
    sql = """
    SELECT v.ActivityID, v.BusinessID, v.Date, v.IsPhysical, v.type_volunteer, v.ActivityDescription,v.VolunteersNeeded,b.city 
    FROM VolunteerActivity v 
    inner join Business b 
    on v.BusinessID=b.BusinessID
    WHERE 1=1 AND v.date>?
    """

    # Parameters to include in the query
    params = [today]
    """
    # Add conditions to the SQL query based on function arguments
    if city:
        sql += " AND EXISTS (SELECT 1 FROM business WHERE business.BusinessID = VolunteerActivity.BusinessID AND business.city = ?)"
        params.append(city)
    if start_date:
        sql += " AND Date >= ?"
        params.append(start_date)
    else:
        # Default to today's date if no start_date is provided
        sql += " AND Date >= ?"
        params.append(datetime.now().strftime('%Y-%m-%d'))
    if end_date:
        sql += " AND Date <= ?"
        params.append(end_date)
    if is_physical is not None:
        sql += " AND IsPhysical = ?"
        params.append(is_physical)
    if type_volunteer:
        sql += " AND type_volunteer = ?"
        params.append(type_volunteer)

    # Execute the SQL query with the parameters
    """
    cur.execute(sql, params)

    # Fetch all the results
    results = cur.fetchall()

    # Close the database connection
    conn.close()

    # Return the results
    return results


def make_match(user_id, activity_id, db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
    cur = conn.cursor()

    try:
        # Get the date of the activity user wants to register for
        cur.execute("SELECT Date FROM VolunteerActivity WHERE ActivityID = ?", (activity_id,))
        activity_date = cur.fetchone()
        if not activity_date:
            print("No such activity found.")
            return False

        # Check if the user is already registered for an activity on the same date
        cur.execute("""
        SELECT 1 FROM user_to_volunteer uv
        JOIN VolunteerActivity va ON uv.ActivityID = va.ActivityID
        WHERE uv.UserID = ? AND va.Date = ?
        """, (user_id, activity_date[0]))

        if cur.fetchone():
            # The user is already registered for an activity on this date
            print("User is already registered for an activity on this date.")
            return False

        # Insert the user and activity into the user_to_volunteer table
        cur.execute("INSERT INTO user_to_volunteer (UserID, ActivityID) VALUES (?, ?)", (user_id, activity_id))
        conn.commit()

        return True

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        # Close the connection to the database
        conn.close()


# function to miletzky
def is_business_exist(user_id, business_name, db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
    cur = conn.cursor()

    try:
        # Prepare SQL to check if a business exists with the given user_id and business_name
        cur.execute("SELECT 1 FROM business WHERE user_id = ? AND business_name = ?", (user_id, business_name))

        # Fetch one result
        result = cur.fetchone()

        # Return True if a business exists, False otherwise
        return result is not None

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        # Close the database connection
        conn.close()


def check_mail(mail, db_name='iron_farm.db'):
    conn = get_db_connection(db_name)
    cur = conn.cursor()

    try:
        # Prepare SQL to check if an email exists in the users table
        cur.execute("SELECT 1 FROM users WHERE email = ?", (mail,))

        # Fetch one result
        result = cur.fetchone()

        # Return True if an email exists, False otherwise
        return result is not None

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        # Close the database connection
        conn.close()
def add_user(user_data):
    cursor = connection.cursor()
    insert_user_query = "INSERT INTO users (phone, name, password, email) VALUES (%s, %s, %s, %s, %s)"
    values = (
        user_data['phone'],
        user_data['name'],
        user_data['password'],
        user_data['email']
    )

    cursor.execute(insert_user_query, values)
    connection.commit()
    cursor.close()


def get_user(mail,password):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            sql = f"SELECT * FROM users WHERE mail='{mail}'"
            cursor.execute(sql)
            userId = cursor.fetchall()
            return userId
    except Error as e:
        print("Error fetching users:", e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def mail_password_match(mail, password):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            sql = f"SELECT * FROM users WHERE mail='{mail}' AND password='{password}'"
            cursor.execute(sql)
            user = cursor.fetchall()
            # Return -1 if user doesn't exist or details are wrong, 0 if all good
            return -1 if len(user) == 0 else 0
    except Error as e:
        print("Error fetching users:", e)
        return -1
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


