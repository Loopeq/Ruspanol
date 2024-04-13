import sqlite3

connection = sqlite3.connect('data/espanol.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()