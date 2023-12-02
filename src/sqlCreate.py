import sqlite3 as sq


class DataBase:
    def __init__(self):
        with sq.connect("../database/priemka.db") as con:
            self.cur = con.cursor()
            self.cur.execute("PRAGMA foreign_keys=on;")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            login TEXT,
            fullname TEXT,
            status TEXT,
            password TEXT
            )""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS applicants(
                user_id INTEGER,
                attestat VARCHAR(20),
                sub1 INTEGER,
                sub2 INTEGER,
                sub3 INTEGER,
                state TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )""")
            attestat1 = "018 56789"





data = DataBase()
#DataBase.registration()
#DataBase.log_in()
