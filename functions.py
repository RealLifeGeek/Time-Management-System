import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import random
import string
import requests

chosen_date = None
chosen_deadline = None
now = datetime.now()
today = now.strftime('%d/%m/%Y')


def create_database(db):
    try:    
        conn = sqlite3.connect(db + '.db')
        cursor = conn.cursor()

        cursor.execute(f'CREATE TABLE IF NOT EXISTS {db} (id INTEGER PRIMARY KEY, element_ID TEXT, element TEXT, date TEXT, deadline TEXT, field1 TEXT, field2 TEXT, field3 TEXT, project TEXT, delegated TEXT, cooperating TEXT, field4 TEXT, field5 TEXT, remarks TEXT, keywords TEXT, category TEXT, done TEXT)')
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("ERROR", f"ERROR: {e}")
        
def delete_from_database(db, element_id):
    try:
        conn = sqlite3.connect(db + '.db')
        cursor = conn.cursor()

        cursor.execute(f"SELECT id FROM {db} WHERE element_ID=?", (element_id,))
        row = cursor.fetchone()
        row_id = row[0]
        cursor.execute(f"DELETE FROM {db} WHERE id = ?", (row_id,))
        conn.commit()
        messagebox.showinfo("SUCCESS", "Successfully DELETED!")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("ERROR",f"ERROR: {e}")

def save_to_database(db, element_id, element, date, deadline, field1, field2, field3, project, delegated, 
                         cooperating, field4, field5, remarks, keywords, category, done):
    try:
        conn = sqlite3.connect(db + '.db')
        cursor = conn.cursor()
        query = f"INSERT INTO {db} (element_ID, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (element_id, element, date, deadline, field1, field2, field3, project, delegated, cooperating, field4, field5, remarks, keywords, category, done)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("SUCCESS", "Successfully SAVED!")
    except Exception as e:
        messagebox.showerror("ERROR",f"ERROR: {e}")

def generate_element_id(db, letter_sign):
    while True:
        letters = letter_sign
        random_number = ''.join(random.choice(string.digits) for i in range(2))
        element_id = f"{letters}{random_number}_{today}"
        if not element_id_already_exists(db, element_id):
            return element_id

def element_id_already_exists(db, id):
    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {db} WHERE element_ID=?", (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is not None:
        return True
    else:
        return False

def project_name_already_exist(db, project_name):
    conn = sqlite3.connect(db+ '.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT element_ID FROM {db} WHERE project=?", (project_name,))
    rows = cursor.fetchone()
    cursor.close()
    conn.close()

    if rows is not None:
        return True
    else:
        return False

def update_database_field(db, element_id, column_name, text):
    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()
    try:
        conn = sqlite3.connect({db} + '.db')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE {db} SET {column_name}={text} WHERE element_ID=?', (element_id,))
        conn.commit()
        conn.close() 
    except Exception as e:
        messagebox.showwarning("ERROR", f"ERROR: {e}")
    cursor.close()
    conn.close()

def get_elementid_from_database(db, column_name, text):
    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT element_ID FROM {db} WHERE {column_name}=?", (text,))
    element_id = cursor.fetchone()
    cursor.close()
    conn.close()

    return element_id

def count_number_of_day_element(db, category, date_string):
    try:
        conn = sqlite3.connect(db + '.db')
        cursor = conn.cursor()
        if category == 'task':
            cursor.execute(f'SELECT element, field3 FROM {db} WHERE category = ? AND date = ? AND delegated = ""', (category, date_string))
        else:
            cursor.execute(f'SELECT element FROM {db} WHERE category = ? AND date = ?', (category, date_string))
        rows = cursor.fetchall()
        elements = [str(row[0]) for row in rows]
        number_elements = int(len(elements))
        cursor.close()
        conn.close()
        return number_elements
    except Exception as e:
        messagebox.showerror("ERROR", f"ERROR: {e}")

def count_total_number_of_elements(db, category, delegated, done):
    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()
    try:
        if category == 'task' and delegated == '':
            cursor.execute(f'SELECT element FROM {db} WHERE category = "task" AND delegated = "" AND done = ?', (done,))
        elif category == 'task' and delegated != '':
            cursor.execute(f'SELECT element FROM {db} WHERE category = "task" AND delegated != "" AND done = ?', (done,))
        else:
            cursor.execute(f'SELECT element FROM {db} WHERE category = ?', (category,))
        rows = cursor.fetchall()
        elements = [str(row[0]) for row in rows]
        #my_tasks = [(str(row[0]).replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")
        #                  .replace(",", "").replace("'", "")) for row in rows] 
        number_elements = int(len(elements))
        return number_elements
    except Exception as e:
        messagebox.showwarning("ERROR", f"ERROR: {e}")
    cursor.close()
    conn.close()

def check_internet(frame1, frame2):
    url = "https://www.google.com"
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        online_frame1 = tk.Frame(
            frame1,
            width = 250,
            height = 5,
            background = "#007606"
        )
        online_frame1.place(x = 8, y = 12)

        online_frame2 = tk.Frame(
            frame2,
            width = 250,
            height = 5,
            background = "#007606"
        )
        online_frame2.place(x = 8, y = 12)
    except requests.ConnectionError:
        offline_frame1 = tk.Frame(
            frame1,
            width = 250,
            height = 5,
        background = "#9B0202"
        )
        offline_frame1.place(x = 8, y = 12)

        offline_frame2 = tk.Frame(
            frame2,
            width = 250,
            height = 5,
            background = "#9B0202"
        )
        offline_frame2.place(x = 8, y = 12)

def exit_window(win_name):
    win_name.destroy()

def insert_values_to_task_form(db, element_id, win, frame, row1, row2, row3, row4, row5, row6, row7):
    global chosen_date
    global chosen_deadline

    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM {db} WHERE element_ID=?", (element_id,))
    row = cursor.fetchone()
    row_id = row[0]
    
    element_id_label = tk.Label(
        win,
        text = element_id,
        font = ("Open Sans", "10"),
        background = "#212121",
        foreground = "#FFFFFF"
    )
    element_id_label.place(x = 480, y = 5)

    cursor.execute(f"SELECT element FROM {db} WHERE id = {row_id}")
    result_element = cursor.fetchone()[0]
    row1.insert(0, result_element)

    cursor.execute(f"SELECT date FROM {db} WHERE id = {row_id}")
    chosen_date = cursor.fetchone()[0]
    result_date_label = tk.Label(
        frame,
        text = chosen_date,
        font = ('Montserrat', '12'),
        background = "#2F3030",
        foreground = "#FFFFFF"
    )
    result_date_label.place(x = 180, y = 5)

    cursor.execute(f"SELECT deadline FROM {db} WHERE id = {row_id}")
    chosen_deadline = cursor.fetchone()[0]
    result_deadline_label = tk.Label(
        frame,
        text = chosen_deadline,
        font = ('Montserrat', '12', 'bold'),
        background = "#970000",
        foreground = "#FFFFFF"
    )
    result_deadline_label.place(x = 180, y = 45)

    cursor.execute(f"SELECT field2 FROM {db} WHERE id = {row_id}")
    result_expected_result = cursor.fetchone()[0]
    row2.insert(0, result_expected_result)

    cursor.execute(f"SELECT field3 FROM {db} WHERE id = {row_id}")
    result_time = cursor.fetchone()[0]
    row3.insert(0, result_time)

    cursor.execute(f"SELECT project FROM {db} WHERE id = {row_id}")
    result_project = cursor.fetchone()[0]
    row4.insert(0, result_project)

    cursor.execute(f"SELECT delegated FROM {db} WHERE id = {row_id}")
    result_delegate_to = cursor.fetchone()[0]
    row5.insert(0, result_delegate_to)

    cursor.execute(f"SELECT cooperating FROM {db} WHERE id = {row_id}")
    result_cooperate_with = cursor.fetchone()[0]
    row6.insert(0, result_cooperate_with)

    cursor.execute(f"SELECT keywords FROM {db} WHERE id = {row_id}")
    result_keywords = cursor.fetchone()[0]
    row7.insert(0, result_keywords)

    cursor.close()
    conn.close()

def insert_values_to_event_form(db, element_id, win, frame, row1, row2, row3, row4, row5):
    global chosen_date
    global chosen_deadline

    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM {db} WHERE element_ID=?", (element_id,))
    row = cursor.fetchone()
    row_id = row[0]
    
    element_id_label = tk.Label(
        win,
        text = element_id,
        font = ("Open Sans", "10"),
        background = "#212121",
        foreground = "#FFFFFF"
    )
    element_id_label.place(x = 480, y = 5)

    cursor.execute(f"SELECT element FROM {db} WHERE id=?", (row_id,))
    result_event = cursor.fetchone()[0]
    row1.insert(0, result_event)
    
    cursor.execute(f"SELECT field1 FROM {db} WHERE id=?", (row_id,))
    result_field1 = cursor.fetchone()[0]
    row2.insert(0, result_field1)
    
    cursor.execute(f"SELECT field2 FROM {db} WHERE id=?", (row_id,))
    result_field2 = cursor.fetchone()[0]
    row3.insert(0, result_field2)
    
    cursor.execute(f"SELECT date FROM {db} WHERE id=?", (row_id,))
    chosen_date = cursor.fetchone()[0]
    result_start_date_label = tk.Label(
        frame,
        text = chosen_date,
        font = ('Montserrat', '12', 'bold'),
        background = "#A8A803",
        foreground = "#FFFFFF"
    )
    result_start_date_label.place(x = 180, y = 5)

    cursor.execute(f"SELECT deadline FROM {db} WHERE id=?", (row_id,))
    chosen_deadline = cursor.fetchone()[0]
    result_end_date_label = tk.Label(
        frame,
        text = chosen_deadline,
        font = ('Montserrat', '12', 'bold'),
        background = "#970000",
        foreground = "#FFFFFF"
    )
    result_end_date_label.place(x = 180, y = 45)

    cursor.execute(f"SELECT field3 FROM {db} WHERE id=?", (row_id,))
    result_start_time = cursor.fetchone()[0]
    row4.insert(0, result_start_time)

    cursor.execute(f"SELECT field4 FROM {db} WHERE id=?", (row_id,))
    result_end_time = cursor.fetchone()[0]
    row5.insert(0, result_end_time)

    cursor.close()
    conn.close()

def insert_values_to_remark_form(db, element_id, win, frame, row1, row2, row3):
    global chosen_date

    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM {db} WHERE element_ID=?", (element_id,))
    row = cursor.fetchone()
    row_id = row[0]
        
    element_id_label = tk.Label(
        win,
        text = element_id,
        font = ("Open Sans", "10"),
        background = "#212121",
        foreground = "#FFFFFF"
    )
    element_id_label.place(x = 480, y = 5)

    cursor.execute(f"SELECT element FROM {db} WHERE id=?", (row_id,))
    result_remark = cursor.fetchone()[0]
    row1.insert(0, result_remark)
    
    cursor.execute(f"SELECT field1 FROM {db} WHERE id=?", (row_id,))
    result_field1 = cursor.fetchone()[0]
    row2.insert(0, result_field1)
    
    cursor.execute(f"SELECT field2 FROM {db} WHERE id=?", (row_id,))
    result_field2 = cursor.fetchone()[0]
    row3.insert(0, result_field2)
    
    cursor.execute(f"SELECT date FROM {db} WHERE id=?", (row_id,))
    chosen_date = cursor.fetchone()[0]
    result_date_label = tk.Label(
        frame,
        text = chosen_date,
        font = ('Montserrat', '12'),
        background = "#9E019A",
        foreground = "#FFFFFF"
    )
    result_date_label.place(x = 180, y = 25)

    cursor.close()
    conn.close()

def insert_values_to_idea_form(db, element_id, win, row1, row2, row3):
    conn = sqlite3.connect(db + '.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM {db} WHERE element_ID=?", (element_id,))
    row = cursor.fetchone()
    row_id = row[0]

    idea_id_label = tk.Label(
        win,
        text = element_id,
        font = ("Open Sans", "10"),
        background = "#212121",
        foreground = "#FFFFFF"
    )
    idea_id_label.place(x = 480, y = 5)

    cursor.execute(f"SELECT element FROM {db} WHERE id=?", (row_id,))
    result_idea_or_action = cursor.fetchone()[0]
    row1.insert(0, result_idea_or_action)

    cursor.execute("SELECT keywords FROM ideas WHERE id=?", (row_id,))
    result_keywords = cursor.fetchone()[0]
    row2.insert(0, result_keywords)

    cursor.execute(f"SELECT remarks FROM {db} WHERE id=?", (row_id,))
    result_remark = cursor.fetchone()[0]
    row3.insert(0, result_remark)

    cursor.execute(f"SELECT date FROM {db} WHERE id=?", (row_id,))
    result_date = cursor.fetchone()[0]
    date_label = tk.Label(
        win,
        text = result_date,
        font = ('Montserrat', '15'),
        background = "#212121",
        foreground = "#FFFFFF"
    )
    date_label.place(x = 480, y = 160)
    
    cursor.close()
    conn.close()

#def find_task():
#    search_string = find_task_row.get().strip()
#    if len(search_string) != 0:
#        if search_string == "tomorrow":
#            search_string = tomorrow
#        elif search_string == "yesterday":
#            search_string = yesterday
#        else:
#            pass
#
#        clear_treeview()
#        insert_data_into_treeview()
#        items = treeview.get_children()    
#        for item in items:
#            values = treeview.item(item)['values']
#            if search_string in values[1] or search_string in values[2] or search_string in values[4] or search_string in values[6]:
#                treeview.selection_add(item)
#                treeview.focus(item)
#            elif search_string =="previous":
#                for i in range(1,356):
#                    previous_date = (now - timedelta(days=i)).strftime('%d/%m/%Y')
#                    if previous_date in values[1] or previous_date in values[2] or previous_date in values[4] or previous_date in values[6]: 
#                        treeview.selection_add(item)
#                        treeview.focus(item)
#    else:
#        messagebox.showerror("Error", "Insert task or keyword you are willing to find.")
