import sqlite3 as sq


class DataBase:
    def __init__(self):
        with sq.connect("../database/priemka.db") as con:
            self.cur = con.cursor()
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            login TEXT,
            fullname TEXT,
            status TEXT,
            password TEXT
            )""")

    @staticmethod
    def registration():
        login = input('login:\n')
        name = input('fullname:\n')
        status = input('Должность:\n')
        password = input('Пароль:\n')
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("""
            SELECT login FROM users WHERE login = ?
            """, [login])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users(login, fullname, status, password) VALUES (?,?,?,?)", [login, name,status, password])
                db.commit()
            else:
                print("Same login exists")
                DataBase.registration()
        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()


    @staticmethod
    def log_in():
        login = input("login:\n")
        password = input('password:\n')
        try:
            db = sq.connect('../database/priemka.db')
            cursor = db.cursor()
            cursor.execute("SELECT login, password FROM users WHERE login = ? AND password = ?", [login, password])
            if (login, password) in cursor.fetchall():
                print('success')
            else:
                print("неверный логин или пароль")

        except sq.Error as e:
            print(e)
        finally:
            cursor.close()
            db.close()


data = DataBase()
#DataBase.registration()
DataBase.log_in()
