import sqlite3 as sq


class DataBase:
    def __init__(self):
        with sq.connect("../database/priemka.db") as con:
            self.cur = con.cursor()
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            fullname TEXT,
            status TEXT
            )""")
data = DataBase()