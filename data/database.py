import sqlite3

from data.wrapper import get_rows

connection = sqlite3.connect('data/espanol.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Sections (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL UNIQUE,
level TEXT NOT NULL
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS Words (
id INTEGER PRIMARY KEY,
russian TEXT NOT NULL,
espanol TEXT NOT NULL,
section_id INTEGER REFERENCES Sections(id) ON UPDATE CASCADE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
user_id TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users_Progress (
id INTEGER PRIMARY KEY,
complete BOOL DEFAULT false,
user_id INTEGER REFERENCES Users(user_id) ON UPDATE CASCADE,
section_id INTEGER REFERENCES Sections(id) ON UPDATE CASCADE
)
''')






def get_sections():
    cursor.execute("SELECT * FROM Sections")
    return get_rows(cursor=cursor)

def get_section(section_id: int):
    cursor.execute("SELECT * FROM Sections WHERE id = ?", (section_id, ))
    return get_rows(cursor=cursor)

def get_words(section_id):
    cursor.execute("SELECT * FROM Words WHERE section_id = ?", (section_id,))
    return get_rows(cursor=cursor)

def get_word_by_id(word_id):
    cursor.execute("SELECT * FROM Words WHERE id = ? ", (word_id, ))
    return get_rows(cursor=cursor)

def insert_sections(section: dict):
    try:
        cursor.execute("INSERT INTO Sections (title, level) VALUES (?, ?)", (section["title"], section["level"],))
    except Exception as err:
        print(err)
    finally:
        connection.commit()

def insert_words(words: list[tuple]):
    cursor.executemany("""INSERT INTO Words (russian, espanol, section_id) 
                            VALUES 
                            (?, ?, ?)
                            """, words)
    connection.commit()

def insert_user(user_id: str):
    cursor.execute("INSERT INTO Users (user_id) VALUES(?)", (user_id, ))
    connection.commit()

def get_user_progression(user_id: str):
    cursor.execute("SELECT section_id FROM Users_Progress WHERE user_id = ?", (user_id, ))
    return get_rows(cursor)

def insert_user_progression(user_id: str, section_id):
    cursor.execute("INSERT INTO Users_Progress (section_id, user_id, complete) VALUES (?, ?, ?)", (section_id, user_id, True,))
    connection.commit()


connection.commit()