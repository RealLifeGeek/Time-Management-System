import datetime
import sqlite3
from tkinter import messagebox
from functions import generate_element_id
# Created on : 14. 10. 2023, 14:26:26
# Author     : prohi


class DBManager():  
    conn = None
    cursor = None
    element_id = None
    db = 'data'
    
    def __init__(self, db, element_id):
        self.conn = sqlite3.connect(db + '.db')
        self.cursor = self.conn.cursor()

        self.db = db
        self.element_id = element_id

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def create_db(self):
        try:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.db} (id INTEGER PRIMARY KEY, element_ID TEXT, element TEXT, date TEXT, deadline TEXT, field1 TEXT, field2 TEXT, field3 TEXT, project TEXT, delegated TEXT, cooperating TEXT, field4 TEXT, field5 TEXT, remarks TEXT, keywords TEXT, category TEXT, done TEXT)')

        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def delete_from_db(self):
        try:
            self.cursor.execute(f"SELECT id FROM {self.db} WHERE element_ID=?", (self.element_id,))
            row = self.cursor.fetchone()
            row_id = row[0]
            self.cursor.execute(f"DELETE FROM {self.db} WHERE id = ?", (row_id,))
            self.conn.commit()
            messagebox.showinfo("SUCCESS", "Successfully DELETED!")
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()

    def save_to_db(self, element_id, element, date, deadline, field1, field2, field3, project, delegated, 
                            cooperating, field4, field5, remarks, keywords, category, done):
        try:
            query = f"INSERT INTO {self.db} (element_ID, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (element_id, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done)
            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("SUCCESS", "Successfully SAVED!")
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()

    def update_db_field(self, column_name, text):
        try:
            conn = sqlite3.connect({self.db} + '.db')
            cursor = conn.cursor()
            cursor.execute(f'UPDATE {self.db} SET {column_name}={text} WHERE element_ID=?', (self.element_id,))
        except Exception as e:
            messagebox.showwarning("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def get_elementid_from_database(self, column_name, text):
        try:
            self.cursor.execute(f"SELECT element_ID FROM {self.db} WHERE {column_name}=?", (text,))
            self.element_id = self.cursor.fetchone()
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()


            
        