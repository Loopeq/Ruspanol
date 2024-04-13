from data.core import cursor, connection
from data.wrapper import get_rows

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


def get_user_sections(user_id: str):
    cursor.execute("SELECT * FROM User_Sections WHERE user_id = ?", (user_id, ))
    return get_rows(cursor)


def insert_user_section(user_id: str, section_title: str):
    user_section = get_user_sections(user_id)
    users_section_title = [obj["section_title"] for obj in user_section]
    if section_title not in users_section_title:
        cursor.execute("INSERT INTO User_Sections (section_title, user_id) VALUES (?, ?)", (section_title, user_id, ))
    connection.commit()

def get_user_section_by_id(us_id: str):
    cursor.execute("SELECT * FROM User_Sections WHERE id=?", (us_id,))
    return get_rows(cursor)

def get_user_section_id(user_id: str, section_title: str):
    cursor.execute("SELECT id FROM User_Sections WHERE user_id = ? AND section_title = ?", (user_id, section_title, ) )
    return get_rows(cursor)

def insert_words_to_user_section(data: list[dict]):
    cursor.executemany("""INSERT INTO User_Sections_Words (espanol, russian, us_id) 
                            VALUES 
                            (?, ?, ?)
                            """, data)
    connection.commit()

def get_us_words(us_id: str):
    cursor.execute("SELECT * FROM User_Sections_Words WHERE us_id = ?", (us_id, ))
    return get_rows(cursor)

def get_us_word_by_id(id: str):
    cursor.execute("SELECT * FROM User_Sections_Words WHERE id = ?", (id, ))
    return get_rows(cursor)

def delete_user_section(us_id: str):
    cursor.execute("DELETE FROM User_Sections WHERE id = ?", (us_id,))
    cursor.execute("DELETE FROM User_Sections_Words WHERE us_id = ?", (us_id, ))
    connection.commit()

def get_user_id_by_us_id(us_id: str):
    cursor.execute("SELECT user_id FROM User_Sections WHERE id = ?", (us_id,))
    return get_rows(cursor)

def delete_word_by_id(word_id: str, us_id: str):
    cursor.execute("DELETE FROM User_Sections_Words WHERE id = ? AND us_id = ?", (word_id, us_id,))
    connection.commit()