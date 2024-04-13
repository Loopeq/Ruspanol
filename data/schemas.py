from data.core import cursor, connection


cursor.execute('''
CREATE TABLE IF NOT EXISTS Sections (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL UNIQUE,
level TEXT NOT NULL
ru_trans TEXT
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS User_Sections (
id INTEGER PRIMARY KEY,
user_id INTEGER REFERENCES Users(user_id) ON UPDATE CASCADE,
section_title TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS User_Sections_Words(
id INTEGER PRIMARY KEY,
espanol TEXT NOT NULL,
russian TEXT NOT NULL,
us_id INTEGER REFERENCES User_Sections(id) ON UPDATE CASCADE
)
""")

connection.commit()