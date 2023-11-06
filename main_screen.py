import tkinter as tk
from tkinter import ttk
from tkinter import *
import sys
import datetime
from tkinter import messagebox
from datetime import datetime
import datetime
import time
from functions import check_internet
from element_window_extended import element_window_extended
from element_window_small import element_window_small
from DBManager import DBManager
from DataFormObject import DataForm
from DataStoreManager import *

#from move_to import move_task_to
#from new_task import new_task
#from adhoc_task import adhoc_task
#from catch_idea import catch_idea
#from add_remark import add_remark
#from add_event import add_event
#from tasks_list_database import tasks_list
#from delegated_tasks_list_database import delegated_tasks_list
#from ideas_list_database import ideas_list
#from deadlines_reminder import remind_my_deadlines, remind_deadlines_delegated
#from catchbox_reminder import remind_full_catchbox
#from birthdays import birthday_list
#from birthday_reminder import remind_birthdays
#from projects_list_database import projects_list
#from check_undone_tasks import check_undone_tasks, check_undone_delegated_tasks, check_udnone_projects
#from events_database import events_list
#from remarks_database import remarks_list
#from maybe_sometimes_list import maybe_sometimes_list

db_manager.create_db()


current_date = datetime.datetime.now()
date_string = current_date.strftime("%d/%m/%Y")
tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
tomorrow_date = tomorrow.strftime('%d/%m/%Y')
chosen_date = None
chosen_deadline = None
element_id = None
project_name = None
db = 'data'
db_manager = DBManager()
data = DataForm()
data_store_manager = DataStoreManager()

def check_connection():
    check_internet(top_frame_left, top_frame_right)
    root.after(10000, check_connection)

def show_number_of_day_element(category):
        number_elements = data_store_manager.count_number_of_day_element(category)
        if category == 'task':
            frame = middle_frame_left
            XX = 140
            YY = 6
            fg_color = "#00A205"
        elif category == 'remark':
            frame = bottom_frame_left
            XX = 165
            YY = 6
            fg_color = "#8801B3"

        elif category == 'event':
            frame = bottom_frame_right
            XX = 150
            YY = 6
            fg_color = "#A8A803"

        number_of_elements_label = tk.Label(
            frame,
            text = f"{str(number_elements)}     ",
            font = ("Arial", "12", "bold"),
            background = "#2F3030",
            foreground = fg_color
        )
        number_of_elements_label.place(x = XX, y = YY)
        progress_bar_of_day()

def show_total_number_of_elements(category, delegated, done, frame, XX, YY):
    number_elements = db_manager.count_total_number_of_elements(category, delegated, done)
    number_elements_label = tk.Label(
        frame,
        text = f"{number_elements}   ",
        font = ('Arial', '12', 'bold'),
        background = "#2F3030",
        foreground = "#FFFFFF"
    )
    number_elements_label.place(x = XX, y = YY)

def task_done():
    selection = treeview.selection()
    if selection:
        element_name = treeview.item(selection, 'values')[0]        
        element_id = data_store_manager.get_element_id_from_data_tuple(element_name)
        data.element_id = element_id
        data.element = element_name
        db_manager.update_db_fields(data)
        data_store_manager.make_day_data_tuple()
        data_store_manager.insert_data_to_treeview(treeview, 'task')
        show_number_of_day_element('task')
    else:
        messagebox.showwarning("Error", "No task selected. Please select a task to be done.")

def do_task_tomorrow():
    try:
        selection = treeview.selection()
        if selection:
            element_name = treeview.item(selection, 'values')[0]
            element_id = data_store_manager.get_element_id_from_data_tuple(element_name)
            data.element_id = element_id
            data.element = element_name
            data.date = tomorrow_date
            db_manager.update_db_fields(data)
            messagebox.showinfo("Info", "Task moved to tomorrow.")
            data_store_manager.make_day_data_tuple()
            data_store_manager.insert_data_to_treeview(treeview, 'task')
            show_number_of_day_element('task')
            progress_bar_of_day()
        else:
            messagebox.showwarning("ERROR", "Select an element.")
    except Exception as e:
        messagebox.showerror("ERROR", f"ERROR: {e}")

def refresh_main_screen():
    data_store_manager.make_day_data_tuple()
    data_store_manager.insert_data_to_treeview(treeview, 'task')
    data_store_manager.insert_data_to_treeview(treeview_remarks, 'remark')
    data_store_manager.insert_data_to_treeview(treeview_events, 'event')
    show_number_of_day_element('task')
    show_number_of_day_element('remark')
    show_number_of_day_element('event')
    #remind_my_deadlines()
    #remind_deadlines_delegated()
    show_total_number_of_elements(db, 'task', '', 'No', right_frame, 200, 162)
    show_total_number_of_elements(db, 'task', 'Yes', 'No', right_frame, 200, 202)
    show_total_number_of_elements(db, 'project', 'None', 'No', right_frame, 200, 242)
    show_total_number_of_elements(db, 'idea', 'None', 'No', right_frame, 200, 282)
    show_total_number_of_elements(db, 'people', 'None', 'No', right_frame, 200, 442)
    #check_undone_tasks()
    #check_undone_delegated_tasks()
    #check_udnone_projects()
    #remind_full_catchbox()
    #remind_birthdays()
    #root.after(10000, refresh_main_screen)

def delete_task_from_database():
    selection = treeview.selection()
    if selection:
        element_name = treeview.item(selection, 'values')[0]
        element_id = data_store_manager.get_element_id_from_data_tuple(element_name)
        db_manager.set_element_id(element_id)
        answer = messagebox.askyesno("DELETE", "DELETE from database?")
        if answer:
            db_manager.delete_from_db()
            data_store_manager.make_day_data_tuple()
            data_store_manager.insert_data_to_treeview(treeview, 'task')
            show_number_of_day_element('task')
        else:
            pass
    else:
        messagebox.showwarning("ERROR", "Select an element")

def delete_remark_from_database():
    selection = treeview_remarks.selection()
    if selection:
        element_name = treeview_remarks.item(selection, 'values')[0]
        element_id = data_store_manager.get_element_id_from_data_tuple(element_name)
        db_manager.set_element_id(element_id)
        answer = messagebox.askyesno("DELETE", "DELETE from database?")
        if answer:
            db_manager.delete_from_db()
            data_store_manager.make_day_data_tuple()
            data_store_manager.insert_data_to_treeview(treeview_remarks, 'remark')
            show_number_of_day_element('remark')
        else:
            pass
    else:
        messagebox.showwarning("ERROR", "Select an element")

def delete_event_from_database():
    selection = treeview_events.selection()
    if selection:
        element_name = treeview_events.item(selection, 'values')[0]
        element_id = data_store_manager.get_element_id_from_data_tuple(element_name)
        db_manager.set_element_id(element_id)
        answer = messagebox.askokcancel("DELETE", "DELETE from database?")
        if answer:
            db_manager.delete_from_db()
            data_store_manager.make_day_data_tuple()
            data_store_manager.insert_data_to_treeview(treeview_events, 'event')
            show_number_of_day_element('event')
        else:
            pass
    else:
        messagebox.showwarning("ERROR", "Select an element")

def progress_bar_of_day():
    try:
        number_tasks_done = db_manager.count_total_number_of_elements('task', '', 'DONE')
        number_tasks_to_fulfill = db_manager.count_total_number_of_elements('task', 'None', 'No')
        total_number_tasks = number_tasks_done + number_tasks_to_fulfill
        if total_number_tasks != 0:
            task_value = 100/total_number_tasks
            task_done_value = number_tasks_done * task_value
            value = 0 + task_done_value
        else:
            value = 0

        style_progressbar = ttk.Style(root)
        style_progressbar.theme_use("clam")
        style_progressbar.configure("green.Horizontal.TProgressbar", background= '#0003C8')
        today_progress_bar = ttk.Progressbar(top_header_frame_left, style = "green.Horizontal.TProgressbar",  orient="horizontal", length=249, mode="determinate")
        today_progress_bar.place(x = 0, y = 80)
        today_progress_bar["value"] = value

        if total_number_tasks == 0:
            style_progressbar.configure("green.Horizontal.TProgressbar", background= '#20EE00', troughcolor='#20EE00')
        else:
            if value == 0:
                style_progressbar.configure("green.Horizontal.TProgressbar", background= '#970000', troughcolor='#666666')
            elif 1 <= value <= 30:
                style_progressbar.configure("green.Horizontal.TProgressbar", background= '#970000', troughcolor='#666666')
            elif 31 <= value <= 60:
                style_progressbar.configure("green.Horizontal.TProgressbar", background= '#F08C05',  troughcolor='#666666')
            elif 61 <= value <= 99:
                style_progressbar.configure("green.Horizontal.TProgressbar", background= '#BFEE00',  troughcolor='#666666')
            else:
                style_progressbar.configure("green.Horizontal.TProgressbar", background= '#20EE00',  troughcolor='#666666')

    except Exception as e:
        messagebox.showerror("ERROR", f"Progress bar error: {e}")

def exit_tms():
    answer = messagebox.askokcancel("Close TMS", "Do you want to close TMS?")
    if answer:
        sys.exit()
    else:
        pass

def show_new_task_window():
    task_window = element_window_extended(
        root, 'Task', db, None
    )
    task_window.create_window()

def show_existing_task_window():
    selection = treeview.selection()
    if selection:
        element_name = treeview.item(selection, 'values')[0]
        element_id = data_store_manager.get_element_id_from_data_tuple(element_name)
    else:
        messagebox.showwarning("ERROR", f"Select an element")
    task_window = element_window_extended(
        root, 'Task View', db, element_id
    )
    task_window.create_window()
    task_window.insert_values()

def show_new_event_window():
    event_window = element_window_extended(
        root, 'Event', db, None
    )
    event_window.create_window()

def show_existing_event_window():
    selection = treeview_events.selection()
    if selection:
        element_name = treeview_events.item(selection, 'values')[0]
        element_id = data_store_manager.get_element_id_from_data_tuple(element_name)
    else:
        messagebox.showwarning("ERROR", f"Select an element")
    event_window = element_window_extended(
        root, "Event View", db, element_id
    )
    event_window.create_window()
    event_window.insert_values()

def show_new_remark_window():
    remark_window = element_window_extended(
        root, "Remark", db, None
    )
    remark_window.create_window()

def show_existing_remark_window():
    selection = treeview_remarks.selection()
    if selection:
        element_name = treeview_remarks.item(selection, 'values')[0]
        element_id = data_store_manager.get_element_id_from_data_tuple(element_name)
    else:
        messagebox.showwarning("ERROR", f"Select an element")
    remark_window = element_window_extended(
        root, "Remark View", db, element_id
    )
    remark_window.create_window()
    remark_window.insert_values()

def show_new_idea_window():
    idea_window = element_window_small(
        root, 'Idea', db, None
    )
    idea_window.create_window()

def show_new_adhoc_task_window():
    adhoc_task_window = element_window_small(
        root, 'Adhoc Task', db, None
    )
    adhoc_task_window.create_window()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry ("800x600")
    root.title("Time Management System 1.1: Main Screen")
    root.resizable(0,0)
    root.configure(bg = "#212121")

    root.protocol("WM_DELETE_WINDOW", exit_tms)

    right_frame = tk.Frame(
        None,
        width = 230,
        height = 600,
        background = "#2F3030"
    )
    right_frame.place(x = 570, y = 0)

    header_label = tk.Label(
        right_frame,
        text = "TMS 1.1",
        font = ('Montserrat', '40'),
        background = "#2F3030",
        foreground = "#474747"
    )
    header_label.place(x = 15, y = 50)

    refresh_button_img = PhotoImage(
    file = r"C:\Users\kalvo\OneDrive\Dokumenty\Python\New_Project\TMS_ver4\Pictures\refresh_icon2.png"
    )
    small_refresh_button_img = refresh_button_img.subsample(2)

    refresh_button = tk.Button(
        right_frame,
        image = small_refresh_button_img,
        font = ('Arial', '8', 'bold'),
        width = 35,
        command = refresh_main_screen,
        background = '#DBDBDB',
        foreground = '#000000'
    )
    refresh_button.place(x = 170, y = 10)

    empty_inbox_img = PhotoImage(
    file = r"C:\Users\kalvo\OneDrive\Dokumenty\Python\New_Project\TMS_ver4\Pictures\empty_inbox2.png"
    )
    small_empty_inbox_img = empty_inbox_img.subsample(2)

    notification_button = tk.Button(
        right_frame,
        image = small_empty_inbox_img,
        font = ('Arial', '8', 'bold'),
        width = 35,
        command = None,
        background = '#DBDBDB',
        foreground = '#000000'
    )
    notification_button.place(x = 120, y = 10)

    task_list_button = tk.Button(
        right_frame,
        text = "MY TASKS",
        font = ('Arial', '11'),
        width = 19,
        command = None,
        background = '#00248B',
        foreground = '#FFFFFF'
    )
    task_list_button.place(x = 16, y = 160)

    delegated_tasks_list_button = tk.Button(
        right_frame,
        text = "DELEGATED TASKS",
        font = ('Arial', '11'),
        width = 19,
        command = None,
        background = '#00248B',
        foreground = '#FFFFFF'
    )
    delegated_tasks_list_button.place(x = 16, y = 200)

    project_list_button = tk.Button(
        right_frame,
        text = "PROJECTS",
        font = ('Arial', '11'),
        width = 19,
        command = None,
        background = '#00248B',
        foreground = '#FFFFFF'
    )
    project_list_button.place(x = 16, y = 240)

    catch_box_button = tk.Button(
        right_frame,
        text = "CATCH-BOX",
        font = ('Arial', '11'),
        width = 19,
        command = None,
        background = '#00248B',
        foreground = '#FFFFFF'
    )
    catch_box_button.place(x = 16, y = 280)

    calendar_button = tk.Button(
        right_frame,
        text = "CALENDAR",
        font = ('Arial', '11'),
        width = 19,
        command = None,
        background = '#00248B',
        foreground = '#FFFFFF'
    )
    calendar_button.place(x = 16, y = 320)

    revision_button = tk.Button(
        right_frame,
        text = "REVISION",
        font = ('Arial', '11'),
        width = 19,
        command = None,
        background = '#00248B',
        foreground = '#FFFFFF'
    )
    revision_button.place(x = 16, y = 360)

    maybe_list_button = tk.Button(
        right_frame,
        text = "MAYBE/SOMETIMES",
        font = ('Arial', '11'),
        width = 19,
        command = None,
        background = '#00248B',
        foreground = '#FFFFFF'
    )
    maybe_list_button.place(x = 16, y = 400)

    birthday_list_button = tk.Button(
        right_frame,
        text = "PEOPLE CARDS",
        font = ('Arial', '11'),
        width = 19,
        command = None,
        background = '#00248B',
        foreground = '#FFFFFF'
    )
    birthday_list_button.place(x = 16, y = 440)

    exit_button = tk.Button(
        right_frame,
        text = "EXIT",
        font = ('Arial', '11'),
        width = 19,
        command = exit_tms,
        background = '#970000',
        foreground = '#FFFFFF'
    )
    exit_button.place(x = 16, y = 480)

    top_frame_left = tk.Frame(
        None,
        width = 270,
        height = 120,
        background = "#2F3030"
    )
    top_frame_left.place(x = 10, y = 10)

    top_header_frame_left = tk.Frame(
        top_frame_left,
        width = 250,
        height = 90,
        background = '#6A6A6A'
    )
    top_header_frame_left.place(x = 8, y = 18)

    my_day_sign = tk.Label(  
        top_header_frame_left,  
        text = "MY DAY",  
        font = ("Open Sans", "30"),  
        background = "#6A6A6A",  
        foreground = "#FFFFFF"  
    )
    my_day_sign.place(x = 45, y = 20)

    top_frame_right = tk.Frame(
        None,
        width = 270,
        height = 120,
        background = "#2F3030"
    )
    top_frame_right.place(x = 290, y = 10)

    top_header_frame_right = tk.Frame(
        top_frame_right,
        width = 250,
        height = 90,
        background = '#6A6A6A'
    )
    top_header_frame_right.place(x = 8, y = 18)

    date_sign = tk.Label(  
        top_header_frame_right,  
        text = "Date",  
        font = ("Open Sans ", "20"),  
        background = "#6A6A6A",  
        foreground = "#FFFFFF"  
    )
    date_sign.place(x = 20, y = 8)

    date_label = tk.Label(  
        top_header_frame_right,  
        text = time.strftime('%d/%m/%y'),  
        font = ("Open Sans ", "20"),  
        background = "#6A6A6A",  
        foreground = "#FFFFFF"  
    )
    date_label.place(x = 95, y = 8)

    weekday_sign = tk.Label(  
    top_header_frame_right,  
        text = "Day",
        font = ("Open Sans ", "20"),  
        background = "#6A6A6A",  
        foreground = "#FFFFFF"  
    )
    weekday_sign.place(x = 20, y = 45)

    weekday_label = tk.Label(  
        top_header_frame_right,  
        text = time.strftime('%A'),  
        font = ("Open Sans ", "20"),  
        background = "#6A6A6A",  
        foreground = "#FFFFFF"  
    )
    weekday_label.place(x = 95, y = 45)

    sign_label = tk.Label(
        right_frame,
        text = 'by VK',
        font = ("Edwardian Script ITC", "25"),
        background = '#2F3030',
        foreground = '#FFFFFF'
    )
    sign_label.place(x = 125, y = 550)

    middle_frame_left = tk.Frame(
        None,
        width = 480,
        height = 235,
        background = "#2F3030"
    )
    middle_frame_left.place(x = 10, y = 155)

    middle_frame_right = tk.Frame(
        None,
        width = 50,
        height = 230,
        background = "#2F3030"
    )
    middle_frame_right.place(x = 510, y = 157)

    done_button_img = PhotoImage(
    file = r"Pictures\done_icon.png"
    )
    small_done_button_img = done_button_img.subsample(2)

    done_button = tk.Button(
        middle_frame_right,
        image = small_done_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = task_done,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    done_button.place(x = 10, y = 20)

    see_task_button_img = PhotoImage(
    file = r"Pictures\magnifier_icon.png"
    )
    small_see_task_button_img = see_task_button_img.subsample(3)

    see_task_button = tk.Button(
        middle_frame_right,
        image = small_see_task_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = show_existing_task_window,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    see_task_button.place(x = 10, y = 60)

    do_tommorrow_button_img = PhotoImage(
    file = r"Pictures\tomorrow_icon.png"
    )
    small_do_tommorrow_button_img = do_tommorrow_button_img.subsample(2)

    do_it_tomorrow_button = tk.Button(
        middle_frame_right,
        image = small_do_tommorrow_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = do_task_tomorrow,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    do_it_tomorrow_button.place(x = 10, y = 100)

    move_to_button_img = PhotoImage(
    file = r"Pictures\change_icon.png"
    )
    small_move_to_button_img = move_to_button_img.subsample(3)

    move_to_button = tk.Button(
        middle_frame_right,
        image = small_move_to_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = None,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    move_to_button.place(x = 10, y = 140)

    delete_button_img = PhotoImage(
    file = r"Pictures\delete_icon.png"
    )
    small_delete_button_img = delete_button_img.subsample(1)

    delete_button = tk.Button(
        middle_frame_right,
        image = small_delete_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = delete_task_from_database,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    delete_button.place(x = 10, y = 180)

    task_treeview_label = tk.Label(
        middle_frame_left,
        text = "Tasks for today:",
        font = ("Open Sans", "12", "bold"),
        background = "#2F3030",
        foreground = "#FFFFFF"
    )
    task_treeview_label.place(x = 10, y = 6)

    treeview = ttk.Treeview(
        middle_frame_left, columns=('Task', 'Time'), height = 8)
    treeview.heading('#0', text='ID')
    treeview.column('#0', width=0, stretch = False)
    treeview.heading('Task', text='Task')
    treeview.column('Task', width=350)
    treeview.heading('Time', text='Time')
    treeview.column('Time', width=100)
    treeview.place (x = 15, y = 35)
    
    bottom_frame_left = tk.Frame(
        None,
        width = 270,
        height = 150,
        background = "#2F3030"
    )
    bottom_frame_left.place(x = 10, y = 400)

    remark_treeview_label = tk.Label(
        bottom_frame_left,
        text = "Remarks for today:",
        font = ("Open Sans", "12", "bold"),
        background = "#2F3030",
        foreground = "#FFFFFF"
    )
    remark_treeview_label.place(x = 10, y = 6)

    treeview_remarks = ttk.Treeview(
        bottom_frame_left, columns=('#1'), height = 4)

    treeview_remarks.heading('#0', text='ID')
    treeview_remarks.column('#0', width=0, stretch = False)
    treeview_remarks.heading('#1', text='Remark')
    treeview_remarks.column('#1', width=210)
    treeview_remarks.place (x = 10, y = 35)

    view_database_button_img = PhotoImage(
    file = r"Pictures\view_list.png"
    )
    small_view_database_button_img = view_database_button_img.subsample(2)

    remarks_database_button = tk.Button(
        bottom_frame_left,
        image = small_view_database_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = None,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    remarks_database_button.place(x = 235, y = 35)

    see_remark_button = tk.Button(
        bottom_frame_left,
        image = small_see_task_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = show_existing_remark_window,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    see_remark_button.place(x = 235, y = 70)

    delete_remark_button = tk.Button(
        bottom_frame_left,
        image = small_delete_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = delete_remark_from_database,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    delete_remark_button.place(x = 235, y = 105)

    bottom_frame_right = tk.Frame(
        None,
        width = 270,
        height = 150,
        background = "#2F3030"
    )
    bottom_frame_right.place(x = 290, y = 400)

    event_treeview_label = tk.Label(
        bottom_frame_right,
        text = "Events for today:",
        font = ("Open Sans", "12", "bold"),
        background = "#2F3030",
        foreground = "#FFFFFF"
    )
    event_treeview_label.place(x = 10, y = 6)

    treeview_events = ttk.Treeview(
        bottom_frame_right, columns=('#1'), height = 4)

    treeview_events.heading('#0', text='ID')
    treeview_events.column('#0', width=0, stretch = False)
    treeview_events.heading('#1', text='Event')
    treeview_events.column('#1', width=210)
    treeview_events.place (x = 10, y = 35)

    event_database_button = tk.Button(
        bottom_frame_right,
        image = small_view_database_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = None,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    event_database_button.place(x = 235, y = 35)
    
    see_event_button = tk.Button(
        bottom_frame_right,
        image = small_see_task_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = show_existing_event_window,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    see_event_button.place(x = 235, y = 70)

    delete_event_button = tk.Button(
        bottom_frame_right,
        image = small_delete_button_img,
        font = ('Arial', '11'),
        width = 27,
        command = delete_event_from_database,
        background = '#DBDBDB',
        foreground = '#FFFFFF'
    )
    delete_event_button.place(x = 235, y = 105)

    very_bottom_frame1 = tk.Frame(
        None,
        width = 230,
        height = 35,
        background = "#2F3030"
    )
    very_bottom_frame1.place(x = 10, y = 565)

    catch_it_button = tk.Button(
        very_bottom_frame1,
        text = "CATCH THE IDEA",
        font = ('Arial', '8', 'bold'),
        width = 14,
        command = show_new_idea_window,
        background = '#4F0082',
        foreground = '#FFFFFF'
    )
    catch_it_button.place(x = 10, y = 5)

    adhoc_task_button = tk.Button(
        very_bottom_frame1,
        text = "ADHOC TASK",
        font = ('Arial', '8', 'bold'),
        width = 13,
        command = show_new_adhoc_task_window,
        background = '#A94102',
        foreground = '#FFFFFF'
    )
    adhoc_task_button.place(x = 125, y = 5)

    very_bottom_frame2 = tk.Frame(
        None,
        width = 110,
        height = 50,
        background = "#2F3030"
    )
    very_bottom_frame2.place(x = 240, y = 555)

    new_task_button = tk.Button(
        very_bottom_frame2,
        text = "NEW TASK",
        font = ('Arial', '9', 'bold'),
        width = 13,
        height = 2,
        command = show_new_task_window,
        background = '#004C01',
        foreground = '#FFFFFF'
    )
    new_task_button.place(x = 5, y = 2)

    very_bottom_frame3 = tk.Frame(
        None,
        width = 220,
        height = 35,
        background = "#2F3030"
    )
    very_bottom_frame3.place(x = 347, y = 565)

    add_remark_button = tk.Button(
        very_bottom_frame3,
        text = " ADD REMARK",
        font = ('Arial', '8', 'bold'),
        width = 13,
        command = show_new_remark_window,
        background = '#9E019A',
        foreground = '#FFFFFF'
    )
    add_remark_button.place(x = 8, y = 5)

    add_event_button = tk.Button(
        very_bottom_frame3,
        text = " ADD EVENT",
        font = ('Arial', '8', 'bold'),
        width = 13,
        command = show_new_event_window,
        background = '#A8A803',
        foreground = '#FFFFFF'
    )
    add_event_button.place(x = 116, y = 5)

    check_connection()
    progress_bar_of_day()
    show_number_of_day_element('task')
    show_number_of_day_element('remark')
    show_number_of_day_element('event')
    data_store_manager.insert_data_to_treeview(treeview, 'task')
    data_store_manager.insert_data_to_treeview(treeview_remarks, 'remark')
    data_store_manager.insert_data_to_treeview(treeview_events, 'event')
    #remind_my_deadlines()
    #remind_deadlines_delegated()
    show_total_number_of_elements(db, 'task', '', 'No', right_frame, 200, 162)
    show_total_number_of_elements(db, 'task', 'Yes', 'No', right_frame, 200, 202)
    show_total_number_of_elements(db, 'project', '', 'No', right_frame, 200, 242)
    show_total_number_of_elements(db, 'idea', 'None', 'No', right_frame, 200, 282)
    show_total_number_of_elements(db, 'people', 'None', 'No', right_frame, 200, 442)
    #check_undone_tasks()
    #check_undone_delegated_tasks()
    #check_udnone_projects()
    #remind_full_catchbox()
    #remind_birthdays()
    #root.after(10000, refresh_main_screen)
    root.mainloop()