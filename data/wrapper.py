from sqlite3 import Cursor

def get_rows(cursor: Cursor):
    return [dict(row) for row in cursor.fetchall()]