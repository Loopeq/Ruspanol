import sqlite3

connection = sqlite3.connect(r'C:\\Users\\arsen\\PycharmProjects\\espanol\\data\\espanol.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
user_id TEXT NOT NULL UNIQUE
)
''')

cursor.execute("""
CREATE TABLE IF NOT EXISTS UsersHist(
id INTEGER PRIMARY KEY,
user_id INTEGER NOT NULL,
message TEXT NOT NULL,
is_user INT NOT NULL, 
FOREIGN KEY (user_id) REFERENCES users(id))
""")

connection.commit()