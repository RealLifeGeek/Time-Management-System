import sqlite3
import datetime
from tkinter import messagebox
import tkinter as tk
# Created on : 14. 10. 2023, 14:26:26
# Author     : prohi
# Updated     : RealLifeGeek

current_date = datetime.datetime.now()
date_string = current_date.strftime("%d/%m/%Y")
tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
tomorrow_date = tomorrow.strftime('%d/%m/%Y')

class DBManager:   
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

    def save_to_db(self, data):
        try:
            self.open_db()
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
        except Exception as e:
            messagebox.showerror("ERROR",f"ERROR: {e}")
        finally:
            self.close_db()

    def update_db_fields(self, data):
        try:

            self.open_db()
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
    
    def insert_values_to_task_form(self, element_id, win, row1, row2, row3, row4, row5, row6, row7, row8, row9):
        self.open_db()

        self.cursor.execute(f"SELECT id FROM {self.db} WHERE element_ID=?", (element_id,))
        row = self.cursor.fetchone()
        row_id = row[0]
        
        element_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 480, y = 5)

        self.cursor.execute(f"SELECT element FROM {self.db} WHERE id = {row_id}")
        result_element = self.cursor.fetchone()[0]
        row1.insert(0, result_element)

        self.cursor.execute(f"SELECT date FROM {self.db} WHERE id = {row_id}")
        chosen_date = self.cursor.fetchone()[0]
        row2.insert(0, chosen_date)

        self.cursor.execute(f"SELECT deadline FROM {self.db} WHERE id = {row_id}")
        chosen_deadline = self.cursor.fetchone()[0]
        row3.insert(0, chosen_deadline)

        self.cursor.execute(f"SELECT field2 FROM {self.db} WHERE id = {row_id}")
        result_expected_result = self.cursor.fetchone()[0]
        row4.insert(0, result_expected_result)

        self.cursor.execute(f"SELECT field3 FROM {self.db} WHERE id = {row_id}")
        result_time = self.cursor.fetchone()[0]
        row5.insert(0, result_time)

        self.cursor.execute(f"SELECT project FROM {self.db} WHERE id = {row_id}")
        result_project = self.cursor.fetchone()[0]
        row6.insert(0, result_project)

        self.cursor.execute(f"SELECT delegated FROM {self.db} WHERE id = {row_id}")
        result_delegate_to = self.cursor.fetchone()[0]
        row7.insert(0, result_delegate_to)

        self.cursor.execute(f"SELECT cooperating FROM {self.db} WHERE id = {row_id}")
        result_cooperate_with = self.cursor.fetchone()[0]
        row8.insert(0, result_cooperate_with)

        self.cursor.execute(f"SELECT keywords FROM {self.db} WHERE id = {row_id}")
        result_keywords = self.cursor.fetchone()[0]
        row9.insert(0, result_keywords)

        self.close_db()

    def insert_values_to_event_form(self, element_id, win, row1, row2, row3, row4, row5, row6, row7):
        self.open_db()

        self.cursor.execute(f"SELECT id FROM {self.db} WHERE element_ID=?", (element_id,))
        row = self.cursor.fetchone()
        row_id = row[0]
        
        element_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 480, y = 5)

        self.cursor.execute(f"SELECT element FROM {self.db} WHERE id=?", (row_id,))
        result_event = self.cursor.fetchone()[0]
        row1.insert(0, result_event)
        
        self.cursor.execute(f"SELECT field1 FROM {self.db} WHERE id=?", (row_id,))
        result_field1 = self.cursor.fetchone()[0]
        row2.insert(0, result_field1)
        
        self.cursor.execute(f"SELECT field2 FROM {self.db} WHERE id=?", (row_id,))
        result_field2 = self.cursor.fetchone()[0]
        row3.insert(0, result_field2)
        
        self.cursor.execute(f"SELECT date FROM {self.db} WHERE id=?", (row_id,))
        chosen_date = self.cursor.fetchone()[0]
        row4.insert(0, chosen_date)

        self.cursor.execute(f"SELECT deadline FROM {self.db} WHERE id=?", (row_id,))
        chosen_deadline = self.cursor.fetchone()[0]
        row5.insert(0, chosen_deadline)

        self.cursor.execute(f"SELECT field3 FROM {self.db} WHERE id=?", (row_id,))
        result_start_time = self.cursor.fetchone()[0]
        row6.insert(0, result_start_time)

        self.cursor.execute(f"SELECT field4 FROM {self.db} WHERE id=?", (row_id,))
        result_end_time = self.cursor.fetchone()[0]
        row7.insert(0, result_end_time)

        self.close_db()

    def insert_values_to_remark_form(self, element_id, win, row1, row2, row3, row4):
        self.open_db()

        self.cursor.execute(f"SELECT id FROM {self.db} WHERE element_ID=?", (element_id,))
        row = self.cursor.fetchone()
        row_id = row[0]
            
        element_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 480, y = 5)

        self.cursor.execute(f"SELECT element FROM {self.db} WHERE id=?", (row_id,))
        result_remark = self.cursor.fetchone()[0]
        row1.insert(0, result_remark)
        
        self.cursor.execute(f"SELECT field1 FROM {self.db} WHERE id=?", (row_id,))
        result_field1 = self.cursor.fetchone()[0]
        row2.insert(0, result_field1)
        
        self.cursor.execute(f"SELECT field2 FROM {self.db} WHERE id=?", (row_id,))
        result_field2 = self.cursor.fetchone()[0]
        row3.insert(0, result_field2)
        
        self.cursor.execute(f"SELECT date FROM {self.db} WHERE id=?", (row_id,))
        chosen_date = self.cursor.fetchone()[0]
        row4.insert(0, chosen_date)

        self.close_db()

    def insert_values_to_idea_form(self, element_id, win, row1, row2, row3):
        self.open_db()

        self.cursor.execute(f"SELECT id FROM {self.db} WHERE element_ID=?", (element_id,))
        row = self.cursor.fetchone()
        row_id = row[0]

        idea_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        idea_id_label.place(x = 480, y = 5)

        self.cursor.execute(f"SELECT element FROM {self.db} WHERE id=?", (row_id,))
        result_idea_or_action = self.cursor.fetchone()[0]
        row1.insert(0, result_idea_or_action)

        self.cursor.execute("SELECT keywords FROM ideas WHERE id=?", (row_id,))
        result_keywords = self.cursor.fetchone()[0]
        row2.insert(0, result_keywords)

        self.cursor.execute(f"SELECT remarks FROM {self.db} WHERE id=?", (row_id,))
        result_remark = self.cursor.fetchone()[0]
        row3.insert(0, result_remark)

        self.cursor.execute(f"SELECT date FROM {self.db} WHERE id=?", (row_id,))
        result_date = self.cursor.fetchone()[0]
        date_label = tk.Label(
            win,
            text = result_date,
            font = ('Montserrat', '15'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        date_label.place(x = 480, y = 160)
        
        self.close_db()

    def get_day_data_tuple(self):        # Day data for DayDataManager
        self.open_db()
        try:
            self.cursor.execute(f"SELECT * FROM {self.db} WHERE date=?", (date_string,))
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
        finally:
            self.close_db()




            
        