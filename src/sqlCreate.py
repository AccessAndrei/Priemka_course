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
                applicant_id INTEGER UNIQUE,
                attestat VARCHAR(20),
                sub1 INTEGER,
                sub2 INTEGER,
                sub3 INTEGER,
                original INTEGER,
                FOREIGN KEY (applicant_id) REFERENCES users(id)
            )""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS directions(
                direction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_of_direction TEXT,
                name TEXT,
                amount int
            )""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS admission_results(
                applicant_id INTEGER,
                direction_id INTEGER,
                checked INTEGER,
                FOREIGN KEY (applicant_id) REFERENCES users(id),
                FOREIGN KEY (direction_id) REFERENCES directions(direction_id)
            )""")

            #attestat1 = "018 56789"





data = DataBase()
#DataBase.registration()
#DataBase.log_in()
