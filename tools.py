import sqlite3
import MySQLdb

def get_product_ids():
    db = "http://127.0.0.1:3306"
    conn = sqlite3.connect(db)
    c = conn.cursor()
    query = ""
    c.execute(query)
    product_ids = c.fetchall()
    conn.close()


def get_user_preferences():
    pass
