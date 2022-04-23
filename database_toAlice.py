import sqlite3

connection = sqlite3.connect('users_a.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Users
              (user_id TEXT, Token TEXT)''')
connection.commit()
connection.close()


def new_user(user_id, token):
    connection_new = sqlite3.connect('users_a.db')
    cursor_new = connection_new.cursor()
    cursor_new.execute(f'''INSERT INTO Users(user_id,Token) VALUES('{user_id}','{token}')''')
    connection_new.commit()
    connection_new.close()


def get_token(user_id):
    con = sqlite3.connect("users_a.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT Token FROM Users
                WHERE user_id = {user_id}""").fetchall()
    con.close()
    return result