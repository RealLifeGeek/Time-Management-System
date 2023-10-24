import sqlite3
db = 'data'

def check_all_elements(db):
    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {db}")
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    conn.close()



check_all_elements(db)