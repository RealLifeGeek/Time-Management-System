import sqlite3

db = 'data'

def check_all_db_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()
        if not rows:
            print("No data found in the database.")
        else:
            for row in rows:
                print(row)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

check_all_db_data()