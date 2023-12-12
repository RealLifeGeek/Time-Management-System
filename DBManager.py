import sqlite3
import datetime
from tkinter import messagebox
import tkinter as tk
import random
import string
# Created on : 14. 10. 2023, 14:26:26
# Author     : prohi
# Updated    : RealLifeGeek

current_date = datetime.datetime.now()
date_string = current_date.strftime("%d/%m/%Y")
tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
tomorrow_date = tomorrow.strftime('%d/%m/%Y')

class DBManager:
    def __init__(self):
        self.db_name = 'data'

    def set_element_id(self, element_id):
        self.element_id = element_id

    def open_db(self):
        self.conn = sqlite3.connect(self.db_name + '.db')
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def create_db(self):
        try:
            self.open_db()
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY,'
                                'element_ID TEXT, element TEXT, date TEXT, deadline TEXT, field1 TEXT,'
                                'field2 TEXT, field3 TEXT, project TEXT, delegated TEXT, cooperating TEXT, field4 TEXT,'
                                'field5 TEXT, remarks TEXT, keywords TEXT, category TEXT, done TEXT)')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    user_firstName TEXT NOT NULL,
                    user_lastName TEXT NOT NULL,
                    user_email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def delete_from_db(self):
        try:
            self.open_db()
            self.cursor.execute(f"SELECT id FROM data WHERE element_ID=?", (self.element_id,))
            row = self.cursor.fetchone()
            row_id = row[0]
            self.cursor.execute(f"DELETE FROM data WHERE id = ?", (row_id,))
            self.conn.commit()
            messagebox.showinfo("SUCCESS", "Successfully DELETED!")
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()

    def save_to_db(self, data):
        try:
            self.open_db()
            answer = messagebox.askyesno("SAVE", "Save element?")
            if answer:
                query = f"INSERT INTO data (element_ID, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                values = (
                    data.element_id,
                    data.element,
                    data.date,
                    data.deadline,
                    data.field1,
                    data.field2,
                    data.field3,
                    data.project,
                    data.delegated,
                    data.cooperating,
                    data.field4,
                    data.field5,
                    data.remarks,
                    data.keywords,
                    data.category,
                    data.done
                )
                self.cursor.execute(query, values)
                self.conn.commit()
                messagebox.showinfo("SUCCESS", "Successfully SAVED!")
            else:
                pass
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()

    def update_db_fields(self, data):
        try:
            self.open_db()
            answer = messagebox.askyesno("UPDATE", "Update element?")
            if answer:
                query = f"UPDATE data SET element = ?, date = ?, deadline = ?, field1 = ?, field2 = ?, field3 = ?, project = ?, delegated = ?, cooperating = ?, " \
                        "field4 = ?, field5 = ?, remarks = ?, keywords = ?, category = ?, done = ? WHERE element_ID = ?"
                if data.deadline == date_string or data.deadline == None:
                    data.deadline = tomorrow_date

                values = (
                    data.element,
                    data.date,
                    data.deadline,
                    data.field1,
                    data.field2,
                    data.field3,
                    data.project,
                    data.delegated,
                    data.cooperating,
                    data.field4,
                    data.field5,
                    data.remarks,
                    data.keywords,
                    data.category,
                    data.done,
                    data.element_id
                )

                self.conn.execute(query, values)
                self.conn.commit()
                messagebox.showinfo("UPDATED", "Successfully UPDATED!")
            else:
                pass
        except Exception as e:
            messagebox.showwarning("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def get_list_data_tuple(self):        # List data for DataStoreManager - ListWindow
        self.open_db()
        try:
            self.cursor.execute(f"SELECT * FROM data")
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def generate_element_id(self, letter_sign):
        while True:
            letters = letter_sign
            random_number = ''.join(random.choice(string.digits) for i in range(2))
            element_id = f"{letters}{random_number}_{date_string}"
            if not self.element_id_already_exists(element_id):
                return element_id

    def element_id_already_exists(self, id):
        self.open_db()
        try:
            self.cursor.execute(f"SELECT * FROM data WHERE element_ID=?", (id,))
            result = self.cursor.fetchone()

            if result is not None:
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    #### LOGIN ###3#

    def get_hashed_password(self, user_email):
        self.open_db()
        try:
            self.cursor.execute('SELECT hashed_password FROM users WHERE user_email = ?', (user_email,))
            result = self.cursor.fetchone()
            return result
        
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def save_user_to_db(self, user):
        try:
            self.open_db()
            if self.check_user_exists(user) is False:
                query = f"INSERT INTO users (user_id, user_firstName, user_lastName, user_email, hashed_password) VALUES (?, ?, ?, ?, ?)"
                values = (
                    user.user_id,
                    user.firstName,
                    user.lastName,
                    user.user_email,
                    user.hashed_password
                )
                self.cursor.execute(query, values)
                self.conn.commit()
                messagebox.showinfo("CONGRATS", "User registred")
            else:
                pass
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()
    
    def check_user_exists(self, user):
        try:
            query = "SELECT * FROM users WHERE user_email = ?"
            values = (user.user_email,)
            self.cursor.execute(query, values)
            rows = self.cursor.fetchall()
            if rows:
                messagebox.showerror("UNABLE", "E-mail address already registered")
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
            