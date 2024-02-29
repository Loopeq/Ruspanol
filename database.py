import sqlite3

connection = sqlite3.connect('espanol.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Sections (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Subsections (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
section_id INTEGER REFERENCES Sections(id) ON UPDATE CASCADE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Words (
id INTEGER PRIMARY KEY,
russian TEXT NOT NULL,
espanol TEXT NOT NULL,
subsection_id INTEGER REFERENCES Subsections(id) ON UPDATE CASCADE
)
''')


def get_sections():
    cursor.execute("SELECT * FROM Sections")
    return [dict(row) for row in cursor.fetchall()]

def get_subsections(section_id):
    cursor.execute("SELECT * FROM Subsections WHERE section_id = ?", (section_id,))
    return [dict(row) for row in cursor.fetchall()]

def get_subsection(subsection_id):
    cursor.execute("SELECT * FROM Subsections WHERE id = ?", (subsection_id,))
    return [dict(row) for row in cursor.fetchall()]

def get_words(subsection_id):
    cursor.execute("SELECT * FROM Words WHERE subsection_id = ?", (subsection_id,))
    return [dict(row) for row in cursor.fetchall()]

connection.commit()