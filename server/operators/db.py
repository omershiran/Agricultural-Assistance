import sqlite3
import json
import random

def initialize_db():
    pass



def initialize_voice_db():
    voice_conn = sqlite3.connect('voices.db')
    voice_cursor=voice_conn.cursor()
    
    voice_cursor.execute("""CREATE TABLE IF NOT EXISTS voices (
            username TEXT,
            date INTEGER,
            id INTEGER,
            question_name TEXT,
            index INTEGER,
            text TEXT

    )""")

    voice_conn.commit()
    voice_conn.close()



def voice_save(username, date, id, question_name, index, text):
    
    voices_conn = sqlite3.connect('voices.db')
    voices_cursor=voices_conn.cursor()
    voices_cursor.execute("""INSERT INTO voices  (username, date, id, question_name, index, text) VALUES (?,?,?,?,?,?);""", (username, date, id, question_name, index, text))
    voices_conn.commit()
    voices_conn.close()


def get_voice_as_text_chat(username,id):
    pass