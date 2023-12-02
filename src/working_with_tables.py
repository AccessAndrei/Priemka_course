import sqlite3

with sqlite3.connect('../database/priemka.db') as db:
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS applicants")