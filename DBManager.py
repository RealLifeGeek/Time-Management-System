import sqlite3
import datetime
from tkinter import messagebox
# Created on : 14. 10. 2023, 14:26:26
# Author     : prohi

current_date = datetime.datetime.now()
date_string = current_date.strftime("%d/%m/%Y")
tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
tomorrow_date = tomorrow.strftime('%d/%m/%Y')

class DBManager():   
    def __init__(self):
        db = 'data'
        self.db = db
        self.open_db()

    def set_element_id(self, element_id):
        self.element_id = element_id

    def open_db(self):
        self.conn = sqlite3.connect(self.db + '.db')
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def create_db(self):
        try:
            self.open_db()
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.db} (id INTEGER PRIMARY KEY, element_ID TEXT, element TEXT, date TEXT, deadline TEXT, field1 TEXT, field2 TEXT, field3 TEXT, project TEXT, delegated TEXT, cooperating TEXT, field4 TEXT, field5 TEXT, remarks TEXT, keywords TEXT, category TEXT, done TEXT)')

        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def delete_from_db(self):
        try:
            self.open_db()
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
            self.open_db()
            query = f"INSERT INTO {self.db} (element_ID, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (element_id, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done)
            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("SUCCESS", "Successfully SAVED!")
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()

    def update_db_fields(self, element_id, element, date, deadline, field1, field2, field3, project, delegated,
                         cooperating, field4, field5, remarks, keywords, category, done):
        if deadline == date_string:
            deadline = tomorrow_date
        else:
            pass
        try:
            self.open_db()

            query = f"UPDATE {self.db} SET element = ?, date = ?, deadline = ?, field1 = ?, field2 = ?, field3 = ?, project = ?, delegated = ?, cooperating = ?, field4 = ?, field5 = ?, remarks = ?, keywords = ?, category = ?, done = ? WHERE element_ID = ?"
            values = (element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done, element_id)
            self.conn.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("UPDATED", "Successfully UPDATED!")

        except Exception as e:
            messagebox.showwarning("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def get_elementid_from_db(self, column_name, text):
        try:
            self.open_db()
            self.cursor.execute(f"SELECT element_ID FROM {self.db} WHERE {column_name}=?", (text,))
            self.element_id = self.cursor.fetchone()
            return self.element_id
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()


            
        