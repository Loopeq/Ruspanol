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


connection.commit()