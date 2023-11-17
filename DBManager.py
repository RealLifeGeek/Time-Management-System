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
        db = 'data'
        self.db = db

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
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.db} (id INTEGER PRIMARY KEY,'
                                'element_ID TEXT, element TEXT, date TEXT, deadline TEXT, field1 TEXT,'
                                'field2 TEXT, field3 TEXT, project TEXT, delegated TEXT, cooperating TEXT, field4 TEXT,'
                                'field5 TEXT, remarks TEXT, keywords TEXT, category TEXT, done TEXT)')
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

    def save_to_db(self, data):
        try:
            self.open_db()
            answer = messagebox.askyesno("SAVE", "Save element?")
            if answer:
                query = f"INSERT INTO {self.db} (element_ID, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
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
                query = f"UPDATE {self.db} SET element = ?, date = ?, deadline = ?, field1 = ?, field2 = ?, field3 = ?, project = ?, delegated = ?, cooperating = ?, " \
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

    def get_day_data_tuple(self):        # Day data for DataStoreManager - MainScreen
        self.open_db()
        try:
            self.cursor.execute(f"SELECT * FROM {self.db} WHERE date=?", (date_string,))
            rows = self.cursor.fetchall()
            print('Creating new day_data_tuple: DBManager')
            return rows
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def get_list_data_tuple(self):        # List data for DataStoreManager - ListWindow
        self.open_db()
        try:
            self.cursor.execute(f"SELECT * FROM {self.db}")
            rows = self.cursor.fetchall()
            print('Creating new list_data_tuple: DBManager')
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
            self.cursor.execute(f"SELECT * FROM {self.db} WHERE element_ID=?", (id,))
            result = self.cursor.fetchone()

            if result is not None:
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def project_name_already_exist(self, project_name):
        self.open_db()
        try:
            self.cursor.execute(f"SELECT element_ID FROM {self.db} WHERE project=? AND category = 'project'", (project_name,))
            rows = self.cursor.fetchone()
            print('ROWS in db: ' + str(rows))

            if rows is not None:
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()

    def count_total_number_of_elements(self, category, delegated, done):
        self.open_db()
        try:
            if category == 'task' and delegated == '':
                self.cursor.execute(f'SELECT element FROM {self.db} WHERE category = "task" AND delegated = "" AND done = ?', (done,))
            elif category == 'task' and delegated != '':
                self.cursor.execute(f'SELECT element FROM {self.db} WHERE category = "task" AND delegated != "" AND done = ?', (done,))
            else:
                self.cursor.execute(f'SELECT element FROM {self.db} WHERE category = ?', (category,))
            rows = self.cursor.fetchall()
            elements = [str(row[0]) for row in rows]
            number_elements = int(len(elements))
            return number_elements
        except Exception as e:
            messagebox.showwarning("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()