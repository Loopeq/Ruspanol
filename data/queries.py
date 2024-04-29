from data.core import cursor, connection
from data.wrapper import get_rows


def insert_user(user_id: int):
    cursor.execute("INSERT INTO Users (user_id) VALUES(?)", (user_id, ))
    connection.commit()


def insert_history(user_id: int, message: str, is_user: bool = True):
    cursor.execute("INSERT INTO UsersHist (user_id, message, is_user) VALUES(?, ?, ?)", (user_id, message, int(is_user)))
    connection.commit()


def get_history(user_id: int) -> tuple[dict, int]:
    cursor.execute("SELECT * FROM UsersHist WHERE user_id = ?", (user_id,))
    rows = get_rows(cursor)
    cursor.execute("SELECT COUNT(*) as count FROM UsersHist WHERE user_id = ?", (user_id, ))
    count = get_rows(cursor)[0]["count"]
    return rows, count


def delete_history(user_id: int):
    cursor.execute("DELETE FROM UsersHist WHERE user_id = ?", (user_id, ))
    connection.commit()
