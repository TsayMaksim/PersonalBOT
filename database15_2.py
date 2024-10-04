import sqlite3

connection = sqlite3.connect('mydb', check_same_thread=False)
sql = connection.cursor()


sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, number TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS loc (tg_id INTEGER, lat REAL, lon REAL);')


def register(tg_id, name, number):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);', (tg_id, name, number))
    connection.commit()


def register_loc(tg_id, lat, lon,):
    sql.execute('INSERT INTO loc VALUES (?, ?, ?);', (tg_id, lat, lon))
    connection.commit()


def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?;', (tg_id,)).fetchone():
        return True
    else:
        return False


def get_loc_lat(tg_id):
    res_lat = sql.execute('SELECT lat FROM loc WHERE tg_id=?;', (tg_id,)).fetchone()
    return res_lat[0]


def get_loc_lon(tg_id):
    res_lon = sql.execute('SELECT lon FROM loc WHERE tg_id=?;', (tg_id,)).fetchone()
    return res_lon[0]

def get_username(tg_id):
    res_name = sql.execute('SELECT name FROM users WHERE tg_id=?;', (tg_id,)).fetchone()
    return res_name[0]