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

class DBDirector:
    def __init__(self):
        self.db_name = 'data'
        self.create_db()

    def open_db(self):
        self.conn = sqlite3.connect(self.db_name + '.db')
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def create_db(self):
        try:
            self.open_db()
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
            messagebox.showerror("ERROR", f"ERROR 101: {e}")
        finally:
            self.close_db()

    def get_hashed_password(self, user_email):
        self.open_db()
        try:
            self.cursor.execute('SELECT hashed_password FROM users WHERE user_email = ?', (user_email,))
            result = self.cursor.fetchone()
            return result
        
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 102: {e}")
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
            messagebox.showerror("ERROR",f"ERROR 103: {e}")
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
            messagebox.showerror("ERROR", f"ERROR 104: {e}")
    
    def get_user_id(self, user_email):
        self.open_db()
        try:
            query = "SELECT user_id FROM users WHERE user_email = ?"
            values = (user_email,)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            user_id = result[0]
            return user_id
            
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 105: {e}")
        
        finally:
            self.close_db()

    def generate_user_id(self):
        while True:
            letters = 'User'
            random_number = ''.join(random.choice(string.digits) for i in range(4))
            element_id = f"_{letters}{random_number}_"
            if not self.user_id_already_exists(element_id):
                return element_id

    def user_id_already_exists(self, id):
        self.open_db()
        try:
            self.cursor.execute(f"SELECT * FROM users WHERE user_id=?", (id,))
            result = self.cursor.fetchone()

            if result is not None:
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 106: {e}")
        finally:
            self.close_db()


class DBManager(DBDirector):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.table_name = f"data_{user_id}"
        self.create_data_db()

    def set_element_id(self, element_id):
        self.element_id = element_id

    def create_data_db(self):
        try:
            self.open_db()
            self.cursor.execute(f'''
                                CREATE TABLE IF NOT EXISTS {self.table_name} (
                                    id INTEGER PRIMARY KEY,
                                    element_ID TEXT,
                                    element TEXT,
                                    date TEXT,
                                    deadline TEXT,
                                    field1 TEXT,
                                    field2 TEXT,
                                    field3 TEXT,
                                    project TEXT,
                                    delegated TEXT,
                                    cooperating TEXT,
                                    field4 TEXT,
                                    field5 TEXT,
                                    remarks TEXT,
                                    keywords TEXT,
                                    category TEXT,
                                    done TEXT,
                                    timestamp_created TEXT,
                                    timestamp_finished TEXT
                                )
                                ''')
            self.cursor.execute(f'''
                                CREATE TABLE IF NOT EXISTS login_logout (
                                    id INTEGER PRIMARY KEY,
                                    user_ID TEXT,
                                    act TEXT,
                                    timestamp TEXT
                                )
                                ''')
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 110: {e}")
        finally:
            self.close_db()

    def delete_from_db(self):
        try:
            self.open_db()
            self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE element_ID=?", (self.element_id,))
            row = self.cursor.fetchone()
            row_id = row[0]
            self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (row_id,))
            self.conn.commit()
            messagebox.showinfo("SUCCESS", "Successfully DELETED!")
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR 111: {e}")
        finally:
            self.close_db()

    def save_to_db(self, data):
        try:
            self.open_db()
            answer = messagebox.askyesno("SAVE", "Save element?")
            if answer:
                query = f"INSERT INTO {self.table_name} (element_ID, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done, timestamp_created, timestamp_finished) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
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
                    data.done,
                    data.timestamp_created,
                    data.timestamp_finished
                )
                self.cursor.execute(query, values)
                self.conn.commit()
                messagebox.showinfo("SUCCESS", "Successfully SAVED!")
            else:
                pass
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR 112: {e}")
        finally:
            self.close_db()
    
    def save_login_logout_time(self, act, timestamp):
        try:
            self.open_db()
            query = f"INSERT INTO login_logout (user_ID, act, timestamp) VALUES (?, ?, ?)"
            values = (
                self.user_id,
                act,
                timestamp
            )
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR 112: {e}")
        finally:
            self.close_db()

    def update_db_fields(self, data):
        try:
            self.open_db()
            answer = messagebox.askyesno("UPDATE", "Update element?")
            if answer:
                query = f"UPDATE {self.table_name} SET element = ?, date = ?, deadline = ?, field1 = ?, field2 = ?, field3 = ?, project = ?, delegated = ?, cooperating = ?, " \
                        "field4 = ?, field5 = ?, remarks = ?, keywords = ?, category = ?, done = ?, timestamp_created = ?, timestamp_finished = ? WHERE element_ID = ?"
                #if data.deadline == date_string or data.deadline == None:
                #    data.deadline = tomorrow_date

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
                    data.timestamp_created,
                    data.timestamp_finished,
                    data.element_id
                )

                self.conn.execute(query, values)
                self.conn.commit()
                messagebox.showinfo("UPDATED", "Successfully UPDATED!")
            else:
                pass
        except Exception as e:
            messagebox.showwarning("ERROR", f"ERROR 113: {e}")
        finally:
            self.close_db()

    def get_list_data_tuple(self):        # List data for DataStoreManager - ListWindow
        self.open_db()
        try:
            self.cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 114: {e}")
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
            self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE element_ID=?", (id,))
            result = self.cursor.fetchone()

            if result is not None:
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 115: {e}")
        finally:
            self.close_db()
