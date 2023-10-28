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
