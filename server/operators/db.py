import sqlite3
import json
import random

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



def initialize_db():
    pass