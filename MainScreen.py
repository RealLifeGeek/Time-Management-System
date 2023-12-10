import tkinter as tk
from tkinter import ttk
from tkinter import *
import sys
import time
import datetime
from datetime import datetime, timedelta
from tkinter import messagebox
from functions import check_internet
from element_window_extended import *
from element_window_small import *
from list_window import *
from DBManager import DBManager
from DataFormObject import DataForm
from DataStoreManager import *
from NotificationWindow import *
from RevisionChoiceWindow import *
from MyCalendar import *

class MainScreen:
    current_date = datetime.now()
    date_string = current_date.strftime("%d/%m/%Y")
    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow_date = tomorrow.strftime('%d/%m/%Y')
    db = 'data'
    db_manager = DBManager()
    data = DataForm()
    data_store_manager = DataStoreManager()

    def __init__(self, root):
        #self.root = tk.Toplevel()
        self.root = root
        self.root.geometry ("800x600+300+50")
        self.root.title("Main Screen")
        self.root.resizable(0,0)
        self.root.configure(bg = "#212121")

        self.root.protocol("WM_DELETE_WINDOW", self.exit_tms)

        self.tooltip_window = None
        self.refresh_button_img = None

    def check_connection(self):
        check_internet(self.top_frame_left, self.top_frame_right)
        self.root.after(10000, self.check_connection)

    def show_number_of_day_element(self, category):
            number_elements = data_store_manager.count_number_of_day_element(category)
            if category == 'task':
                frame = self.middle_frame_left
                XX = 140
                YY = 6
                fg_color = "#00A205"
            elif category == 'remark':
                frame = self.bottom_frame_left
                XX = 165
                YY = 6
                fg_color = "#8801B3"

            elif category == 'event':
                frame = self.bottom_frame_right
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

    def show_total_number_of_elements(self, category, delegated, done, ProgressBar_bool, frame, XX, YY):
        number_elements = data_store_manager.count_total_number_of_elements(category, delegated, done, ProgressBar_bool)
        number_elements_label = tk.Label(
            frame,
            text = f"{number_elements}   ",
            font = ('Arial', '12', 'bold'),
            background = "#2F3030",
            foreground = "#FFFFFF"
        )
        number_elements_label.place(x = XX, y = YY)

    def task_done(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
            data_row = data_store_manager.get_data_row_from_list_data_tuple(element_id)

            data.element_id = element_id
            data.element = data_row[2]
            data.date = data_row[3]
            data.deadline = data_row[4]
            data.field1 = data_row[5]
            data.field2 = data_row[6]
            data.field3 = data_row[7]
            data.project = data_row[8]
            data.delegated = data_row[9]
            data.cooperating = data_row[10]
            data.field4 = data_row[11]
            data.field5 = data_row[12]
            data.remarks = data_row[13]
            data.keywords = data_row[14]
            data.category = data_row[15]
            data.done = 'DONE'

            db_manager.update_db_fields(data)
            data_store_manager.make_list_data_tuple()
            data_store_manager.insert_day_data_to_treeview(self.treeview, 'task')
            self.show_number_of_day_element('task')
        else:
            messagebox.showwarning("Error", "Select an element")

    def do_task_tomorrow(self):
        try:
            selection = self.treeview.selection()
            if selection:
                element_id = self.treeview.item(selection, 'values')[0]
                data_row = data_store_manager.get_data_row_from_list_data_tuple(element_id)

                data.element_id = element_id
                data.element = data_row[2]
                data.date = tomorrow_date
                data.deadline = data_row[4] or data.date
                data.field1 = data_row[5]
                data.field2 = data_row[6]
                data.field3 = data_row[7]
                data.project = data_row[8]
                data.delegated = data_row[9]
                data.cooperating = data_row[10]
                data.field4 = data_row[11]
                data.field5 = data_row[12]
                data.remarks = data_row[13]
                data.keywords = data_row[14]
                data.category = data_row[15]
                data.done = data_row[16]

                db_manager.update_db_fields(data)
                messagebox.showinfo("Info", "Task moved to tomorrow.")
                data_store_manager.make_list_data_tuple()
                #data_store_manager.make_day_data_tuple()
                data_store_manager.insert_day_data_to_treeview(self.treeview, 'task')
                self.show_number_of_day_element('task')
                self.progress_bar_of_day()
            else:
                messagebox.showwarning("ERROR", "Select an element.")
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")

    def refresh_main_screen(self):
        data_store_manager.make_list_data_tuple()
        data_store_manager.insert_day_data_to_treeview(self.treeview, 'task')
        data_store_manager.insert_day_data_to_treeview(self.treeview_remarks, 'remark')
        data_store_manager.insert_day_data_to_treeview(self.treeview_events, 'event')
        self.show_number_of_day_element('task')
        self.show_number_of_day_element('remark')
        self.show_number_of_day_element('event')
        self.progress_bar_of_day()
        self.show_total_number_of_elements('task', '', 'No', 'No', self.right_frame, 200, 162)
        self.show_total_number_of_elements('task', 'Yes', 'No', 'No', self.right_frame, 200, 202)
        self.show_total_number_of_elements('project', 'None', 'No', 'No', self.right_frame, 200, 242)
        self.show_total_number_of_elements('idea', 'None', 'No', 'No', self.right_frame, 200, 282)
        self.show_total_number_of_elements('maybe/sometimes', '', 'No', 'No', self.right_frame, 200, 322)
        self.show_total_number_of_elements('personal card', 'None', 'No', 'No', self.right_frame, 200, 362)
        self.check_notifications()

    def delete_task_from_database(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
            db_manager.set_element_id(element_id)
            answer = messagebox.askyesno("DELETE", "DELETE from database?")
            if answer:
                db_manager.delete_from_db()
                data_store_manager.make_list_data_tuple()
                data_store_manager.insert_day_data_to_treeview(self.treeview, 'task')
                self.show_number_of_day_element('task')
            else:
                pass
        else:
            messagebox.showwarning("ERROR", "Select an element")

    def delete_remark_from_database(self):
        selection = self.treeview_remarks.selection()
        if selection:
            element_id = self.treeview_remarks.item(selection, 'values')[0]
            db_manager.set_element_id(element_id)
            answer = messagebox.askyesno("DELETE", "DELETE from database?")
            if answer:
                db_manager.delete_from_db()
                data_store_manager.make_list_data_tuple()
                data_store_manager.insert_day_data_to_treeview(self.treeview_remarks, 'remark')
                self.show_number_of_day_element('remark')
            else:
                pass
        else:
            messagebox.showwarning("ERROR", "Select an element")

    def delete_event_from_database(self):
        selection = self.treeview_events.selection()
        if selection:
            element_id = self.treeview_events.item(selection, 'values')[0]
            db_manager.set_element_id(element_id)
            answer = messagebox.askokcancel("DELETE", "DELETE from database?")
            if answer:
                db_manager.delete_from_db()
                data_store_manager.make_list_data_tuple()
                data_store_manager.insert_day_data_to_treeview(self.treeview_events, 'event')
                self.show_number_of_day_element('event')
            else:
                pass
        else:
            messagebox.showwarning("ERROR", "Select an element")

    def progress_bar_of_day(self):
        try:
            number_tasks_done = data_store_manager.count_total_number_of_elements('task', '', 'DONE', 'Yes')
            number_tasks_to_fulfill = data_store_manager.count_total_number_of_elements('task', '', 'No', 'Yes')
            total_number_tasks = number_tasks_done + number_tasks_to_fulfill
            if total_number_tasks != 0:
                task_value = 100/total_number_tasks
                task_done_value = number_tasks_done * task_value
                value = 0 + task_done_value
            else:
                value = 0

            style_progressbar = ttk.Style(self.root)
            style_progressbar.theme_use("clam")
            style_progressbar.configure("green.Horizontal.TProgressbar", background= '#0003C8')
            today_progress_bar = ttk.Progressbar(self.top_header_frame_left, style = "green.Horizontal.TProgressbar",  orient="horizontal", length=249, mode="determinate")
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

    def exit_tms(self):
        answer = messagebox.askokcancel("Close TMS", "Do you want to close TMS?")
        if answer:
            sys.exit()
        else:
            pass

    def show_notificaton_window(self):
        self.notification_dot_label.place_forget()
        notification_window = NotificationWindow(self.root)
        notification_window.create_window()

    def show_new_task_window(self):
        task_window = element_window_extended(
            self.root, 'Task', None
        )
        task_window.create_window()

    def show_existing_task_window(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
        else:
            messagebox.showwarning("ERROR", f"Select an element")
        task_window = element_window_extended(
            self.root, 'Task View', element_id
        )
        task_window.create_window()
        task_window.insert_values()

    def show_new_event_window(self):
        event_window = element_window_extended(
            self.root, 'Event', None
        )
        event_window.create_window()

    def show_existing_event_window(self):
        selection = self.treeview_events.selection()
        if selection:
            element_id = self.treeview_events.item(selection, 'values')[0]
        else:
            messagebox.showwarning("ERROR", f"Select an element")
        event_window = element_window_extended(
            self.root, "Event View", element_id
        )
        event_window.create_window()
        event_window.insert_values()

    def show_new_remark_window(self):
        remark_window = element_window_extended(
            self.root, "Remark", None
        )
        remark_window.create_window()

    def show_existing_remark_window(self):
        selection = self.treeview_remarks.selection()
        if selection:
            element_id = self.treeview_remarks.item(selection, 'values')[0]
        else:
            messagebox.showwarning("ERROR", f"Select an element")
        remark_window = element_window_extended(
            self.root, "Remark View", element_id
        )
        remark_window.create_window()
        remark_window.insert_values()

    def show_new_idea_window(self):
        idea_window = element_window_small(
           self.root, 'Idea', None
        )
        idea_window.create_window()

    def show_new_adhoc_task_window(self):
        adhoc_task_window = element_window_small(
            self.root, 'Adhoc Task', None
        )
        adhoc_task_window.create_window()

    def show_tasks_list_window(self):
        tasks_list_window = ListWindow(self.root, 'My Tasks')
        tasks_list_window.create_window()

    def show_delegated_tasks_list_window(self):
        delegated_tasks_list_window = ListWindow(self.root, 'Delegated Tasks')
        delegated_tasks_list_window.create_window()

    def show_projects_list_window(self):
        projects_list_window = ListWindow(self.root, 'Projects')
        projects_list_window.create_window()

    def show_maybe_sometimes_list_window(self):
        maybe_sometimes_list_window = ListWindow(self.root, 'Maybe/Sometimes')
        maybe_sometimes_list_window.create_window()

    def show_ideas_list_window(self):
        ideas_list_window = ListWindow(self.root, 'Ideas')
        ideas_list_window.create_window()

    def show_events_list_window(self):
        events_list_window = ListWindow(self.root, 'Events')
        events_list_window.create_window()

    def show_remarks_list_window(self):
        remarks_list_window = ListWindow(self.root, 'Remarks')
        remarks_list_window.create_window()

    def show_events_list_window(self):
        events_list_window = ListWindow(self.root, 'Events')
        events_list_window.create_window()

    def show_personal_cards_list_window(self):
        personal_cards_list_window = ListWindow(self.root, 'Personal Cards')
        personal_cards_list_window.create_window()

    def show_revision_choice_window(self):
        revision_choice_window = RevisionChoiceWindow(self.root)
        revision_choice_window.create_window()

    def show_calendar_window(self):
        calendar_window = MyCalendar(self.root)
        calendar_window.create_window()

    def check_notifications(self):
        number_undone_tasks = data_store_manager.count_number_undone_elements('tasks', None, None, None)
        number_undone_delegated_tasks = data_store_manager.count_number_undone_elements('delegated tasks', None, None, None)
        number_undone_projects = data_store_manager.count_number_undone_elements('projects', None, None, None)
        number_closing_deadlines = data_store_manager.count_closing_deadlines(None, None, None)
        number_birthdays = data_store_manager.count_birthday()
        number_pending_ideas = data_store_manager.count_pending_ideas(None, None, None)
        result_number = number_undone_tasks + number_undone_delegated_tasks + number_undone_projects + number_closing_deadlines + number_birthdays + number_pending_ideas

        if result_number != 0:
            self.notification_dot_label.config(text="!")
            self.notification_dot_label.place(x=135, y=15)
            messagebox.showinfo('NOTIFICATION', 'Check notifications' )
        else:
            pass
            self.notification_dot_label.place_forget()

    def show_tooltip(self, event):
        hovered_button = event.widget

        if self.tooltip_window is None:
            self.tooltip_window = tk.Toplevel(self.root)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            label = tk.Label(self.tooltip_window, text="", padx=5, pady=3)
            label.pack()
            if hovered_button == self.done_button:
                label.configure(text = 'Task Done')
            elif hovered_button == self.see_task_button:
                label.configure(text = 'Task View')
            elif hovered_button == self.do_it_tomorrow_button:
                label.configure(text = 'Do Task Tomorrow')
            elif hovered_button == self.move_to_button:
                label.configure(text = 'Move Task to')
            elif hovered_button == self.delete_button:
                label.configure(text ='Delete Task' )
            elif hovered_button == self.refresh_button:
                label.configure(text = 'Refresh Screen')
            elif hovered_button == self.notification_button:
                label.configure(text = 'Notifications')
            elif hovered_button == self.remarks_database_button:
                label.configure(text = 'List of Remarks')
            elif hovered_button == self.see_remark_button:
                label.configure(text = 'Remark View')
            elif hovered_button == self.delete_remark_button:
                label.configure(text = 'Delete Remark')
            elif hovered_button == self.event_database_button:
                label.configure(text = 'List of Events')
            elif hovered_button == self.see_event_button:
                label.configure(text = 'Event View')
            elif hovered_button == self.delete_event_button:
                label.configure(text = 'Delete Event')

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def create_window(self):

        self.right_frame = tk.Frame(
            self.root,
            width = 230,
            height = 600,
            background = "#2F3030"
        )
        self.right_frame.place(x = 570, y = 0)

        header_label = tk.Label(
            self.right_frame,
            text = "TMS 1.1",
            font = ('Montserrat', '40'),
            background = "#2F3030",
            foreground = "#474747"
        )
        header_label.place(x = 15, y = 50)

        self.refresh_button_img = PhotoImage(
        file = r"Pictures\refresh_icon2.png"
        )
        self.small_refresh_button_img = self.refresh_button_img.subsample(2)

        self.refresh_button = tk.Button(
            self.right_frame,
            image = self.small_refresh_button_img,
            font = ('Arial', '8', 'bold'),
            width = 35,
            command = self.refresh_main_screen,
            background = '#DBDBDB',
            foreground = '#000000'
        )
        self.refresh_button.place(x = 170, y = 10)
        self.refresh_button.bind("<Enter>", self.show_tooltip)
        self.refresh_button.bind("<Leave>", self.hide_tooltip)

        self.empty_inbox_img = PhotoImage(
        file = r"Pictures\empty_inbox2.png"
        )
        self.small_empty_inbox_img = self.empty_inbox_img.subsample(2)

        self.notification_button = tk.Button(
            self.right_frame,
            image = self.small_empty_inbox_img,
            font = ('Arial', '8', 'bold'),
            width = 35,
            command = self.show_notificaton_window,
            background = '#DBDBDB',
            foreground = '#000000'
        )
        self.notification_button.place(x = 120, y = 10)
        self.notification_button.bind("<Enter>", self.show_tooltip)
        self.notification_button.bind("<Leave>", self.hide_tooltip)

        self.notification_dot_label = tk.Label(
            self.right_frame,
            text="!",
            font=('Montserrat', '12', 'bold'),
            background="#000000",
            foreground="#F90017"
        )
        self.notification_dot_label.place(x=135, y=15)

        task_list_button = tk.Button(
            self.right_frame,
            text = "MY TASKS",
            font = ('Arial', '11'),
            width = 19,
            command = self.show_tasks_list_window,
            background = '#00248B',
            foreground = '#FFFFFF'
        )
        task_list_button.place(x = 16, y = 160)

        delegated_tasks_list_button = tk.Button(
            self.right_frame,
            text = "DELEGATED TASKS",
            font = ('Arial', '11'),
            width = 19,
            command = self.show_delegated_tasks_list_window,
            background = '#00248B',
            foreground = '#FFFFFF'
        )
        delegated_tasks_list_button.place(x = 16, y = 200)

        project_list_button = tk.Button(
            self.right_frame,
            text = "PROJECTS",
            font = ('Arial', '11'),
            width = 19,
            command = self.show_projects_list_window,
            background = '#00248B',
            foreground = '#FFFFFF'
        )
        project_list_button.place(x = 16, y = 240)

        catch_box_button = tk.Button(
            self.right_frame,
            text = "CATCH-BOX",
            font = ('Arial', '11'),
            width = 19,
            command = self.show_ideas_list_window,
            background = '#00248B',
            foreground = '#FFFFFF'
        )
        catch_box_button.place(x = 16, y = 280)

        calendar_button = tk.Button(
            self.right_frame,
            text = "CALENDAR",
            font = ('Arial', '11'),
            width = 19,
            command = self.show_calendar_window,
            background = '#00248B',
            foreground = '#FFFFFF'
        )
        calendar_button.place(x = 16, y = 400)

        revision_button = tk.Button(
            self.right_frame,
            text = "REVISION",
            font = ('Arial', '11'),
            width = 19,
            command = self.show_revision_choice_window,
            background = '#00248B',
            foreground = '#FFFFFF'
        )
        revision_button.place(x = 16, y = 440)

        maybe_list_button = tk.Button(
            self.right_frame,
            text = "MAYBE/SOMETIMES",
            font = ('Arial', '11'),
            width = 19,
            command = self.show_maybe_sometimes_list_window,
            background = '#00248B',
            foreground = '#FFFFFF'
        )
        maybe_list_button.place(x = 16, y = 320)

        personal_cards_button = tk.Button(
            self.right_frame,
            text = "PERSONAL CARDS",
            font = ('Arial', '11'),
            width = 19,
            command = self.show_personal_cards_list_window,
            background = '#00248B',
            foreground = '#FFFFFF'
        )
        personal_cards_button.place(x = 16, y = 360)

        exit_button = tk.Button(
            self.right_frame,
            text = "EXIT",
            font = ('Arial', '11'),
            width = 19,
            command = self.exit_tms,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        exit_button.place(x = 16, y = 480)

        self.top_frame_left = tk.Frame(
            self.root,
            width = 270,
            height = 120,
            background = "#2F3030"
        )
        self.top_frame_left.place(x = 10, y = 10)

        self.top_header_frame_left = tk.Frame(
            self.top_frame_left,
            width = 250,
            height = 90,
            background = '#6A6A6A'
        )
        self.top_header_frame_left.place(x = 8, y = 18)

        my_day_sign = tk.Label(  
            self.top_header_frame_left,  
            text = "MY DAY",  
            font = ("Open Sans", "30"),  
            background = "#6A6A6A",  
            foreground = "#FFFFFF"  
        )
        my_day_sign.place(x = 45, y = 20)

        self.top_frame_right = tk.Frame(
            self.root,
            width = 270,
            height = 120,
            background = "#2F3030"
        )
        self.top_frame_right.place(x = 290, y = 10)

        top_header_frame_right = tk.Frame(
            self.top_frame_right,
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
            self.right_frame,
            text = 'by VK',
            font = ("Edwardian Script ITC", "25"),
            background = '#2F3030',
            foreground = '#FFFFFF'
        )
        sign_label.place(x = 125, y = 550)

        self.middle_frame_left = tk.Frame(
            self.root,
            width = 480,
            height = 235,
            background = "#2F3030"
        )
        self.middle_frame_left.place(x = 10, y = 155)

        middle_frame_right = tk.Frame(
            None,
            width = 50,
            height = 230,
            background = "#2F3030"
        )
        middle_frame_right.place(x = 510, y = 157)

        self.done_button_img = PhotoImage(
        file = r"Pictures\done_icon.png"
        )
        self.small_done_button_img = self.done_button_img.subsample(2)

        self.done_button = tk.Button(
            middle_frame_right,
            image = self.small_done_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.task_done,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.done_button.place(x = 10, y = 20)
        self.done_button.bind("<Enter>", self.show_tooltip)
        self.done_button.bind("<Leave>", self.hide_tooltip)

        see_task_button_img = PhotoImage(
        file = r"Pictures\magnifier_icon.png"
        )
        small_see_task_button_img = see_task_button_img.subsample(3)

        self.see_task_button = tk.Button(
            middle_frame_right,
            image = small_see_task_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.show_existing_task_window,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.see_task_button.place(x = 10, y = 60)
        self.see_task_button.bind("<Enter>", self.show_tooltip)
        self.see_task_button.bind("<Leave>", self.hide_tooltip)

        self.do_tommorrow_button_img = PhotoImage(
        file = r"Pictures\tomorrow_icon.png"
        )
        self.small_do_tommorrow_button_img = self.do_tommorrow_button_img.subsample(2)

        self.do_it_tomorrow_button = tk.Button(
            middle_frame_right,
            image = self.small_do_tommorrow_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.do_task_tomorrow,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.do_it_tomorrow_button.place(x = 10, y = 100)
        self.do_it_tomorrow_button.bind("<Enter>", self.show_tooltip)
        self.do_it_tomorrow_button.bind("<Leave>", self.hide_tooltip)

        self.move_to_button_img = PhotoImage(
        file = r"Pictures\change_icon.png"
        )
        self.small_move_to_button_img = self.move_to_button_img.subsample(3)

        self.move_to_button = tk.Button(
            middle_frame_right,
            image = self.small_move_to_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = None,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.move_to_button.place(x = 10, y = 140)
        self.move_to_button.bind("<Enter>", self.show_tooltip)
        self.move_to_button.bind("<Leave>", self.hide_tooltip)

        self.delete_button_img = PhotoImage(
        file = r"Pictures\delete_icon.png"
        )
        self.small_delete_button_img = self.delete_button_img.subsample(1)

        self.delete_button = tk.Button(
            middle_frame_right,
            image = self.small_delete_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.delete_task_from_database,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.delete_button.place(x = 10, y = 180)
        self.delete_button.bind("<Enter>", self.show_tooltip)
        self.delete_button.bind("<Leave>", self.hide_tooltip)

        task_treeview_label = tk.Label(
            self.middle_frame_left,
            text = "Tasks for today:",
            font = ("Open Sans", "12", "bold"),
            background = "#2F3030",
            foreground = "#FFFFFF"
        )
        task_treeview_label.place(x = 10, y = 6)

        self.treeview = ttk.Treeview(
            self.middle_frame_left, columns=('#1', '#2', '#3'), height = 8)
        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=0, stretch = False)
        self.treeview.heading('#1', text='Element ID')
        self.treeview.column('#1', width=0, stretch = False)
        self.treeview.heading('#2', text='Task')
        self.treeview.column('#2', width=350)
        self.treeview.heading('#3', text='Time')
        self.treeview.column('#3', width=100)
        self.treeview.place (x = 15, y = 35)
        
        self.bottom_frame_left = tk.Frame(
            self.root,
            width = 270,
            height = 150,
            background = "#2F3030"
        )
        self. bottom_frame_left.place(x = 10, y = 400)

        remark_treeview_label = tk.Label(
            self.bottom_frame_left,
            text = "Remarks for today:",
            font = ("Open Sans", "12", "bold"),
            background = "#2F3030",
            foreground = "#FFFFFF"
        )
        remark_treeview_label.place(x = 10, y = 6)

        self.treeview_remarks = ttk.Treeview(
            self.bottom_frame_left, columns=('#1','#2'), height = 4)

        self.treeview_remarks.heading('#0', text='ID')
        self.treeview_remarks.column('#0', width=0, stretch = False)
        self.treeview_remarks.heading('#1', text='Element ID')
        self.treeview_remarks.column('#1', width=0, stretch = False)
        self.treeview_remarks.heading('#2', text='Remark')
        self.treeview_remarks.column('#2', width=210)
        self.treeview_remarks.place (x = 10, y = 35)

        self.view_database_button_img = PhotoImage(
        file = r"Pictures\view_list.png"
        )
        self.small_view_database_button_img = self.view_database_button_img.subsample(2)

        self.remarks_database_button = tk.Button(
            self.bottom_frame_left,
            image = self.small_view_database_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.show_remarks_list_window,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.remarks_database_button.place(x = 235, y = 35)
        self.remarks_database_button.bind("<Enter>", self.show_tooltip)
        self.remarks_database_button.bind("<Leave>", self.hide_tooltip)

        self.see_remark_button = tk.Button(
            self.bottom_frame_left,
            image = small_see_task_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.show_existing_remark_window,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.see_remark_button.place(x = 235, y = 70)
        self.see_remark_button.bind("<Enter>", self.show_tooltip)
        self.see_remark_button.bind("<Leave>", self.hide_tooltip)

        self.delete_remark_button = tk.Button(
            self.bottom_frame_left,
            image = self.small_delete_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.delete_remark_from_database,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.delete_remark_button.place(x = 235, y = 105)
        self.delete_remark_button.bind("<Enter>", self.show_tooltip)
        self.delete_remark_button.bind("<Leave>", self.hide_tooltip)

        self.bottom_frame_right = tk.Frame(
            self.root,
            width = 270,
            height = 150,
            background = "#2F3030"
        )
        self.bottom_frame_right.place(x = 290, y = 400)

        event_treeview_label = tk.Label(
            self.bottom_frame_right,
            text = "Events for today:",
            font = ("Open Sans", "12", "bold"),
            background = "#2F3030",
            foreground = "#FFFFFF"
        )
        event_treeview_label.place(x = 10, y = 6)

        self.treeview_events = ttk.Treeview(
            self.bottom_frame_right, columns=('#1', '#2'), height = 4)

        self.treeview_events.heading('#0', text='ID')
        self.treeview_events.column('#0', width=0, stretch = False)
        self.treeview_events.heading('#1', text='Element ID')
        self.treeview_events.column('#1',  width=0, stretch = False)
        self.treeview_events.heading('#2', text='Event')
        self.treeview_events.column('#2', width=210)
        self.treeview_events.place (x = 10, y = 35)

        self.event_database_button = tk.Button(
            self.bottom_frame_right,
            image = self.small_view_database_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.show_events_list_window,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.event_database_button.place(x = 235, y = 35)
        self.event_database_button.bind("<Enter>", self.show_tooltip)
        self.event_database_button.bind("<Leave>", self.hide_tooltip)
        
        self.see_event_button = tk.Button(
            self.bottom_frame_right,
            image = small_see_task_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.show_existing_event_window,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.see_event_button.place(x = 235, y = 70)
        self.see_event_button.bind("<Enter>", self.show_tooltip)
        self.see_event_button.bind("<Leave>", self.hide_tooltip)

        self.delete_event_button = tk.Button(
            self.bottom_frame_right,
            image = self.small_delete_button_img,
            font = ('Arial', '11'),
            width = 27,
            command = self.delete_event_from_database,
            background = '#DBDBDB',
            foreground = '#FFFFFF'
        )
        self.delete_event_button.place(x = 235, y = 105)
        self.delete_event_button.bind("<Enter>", self.show_tooltip)
        self.delete_event_button.bind("<Leave>", self.hide_tooltip)

        very_bottom_frame1 = tk.Frame(
            self.root,
            width = 230,
            height = 35,
            background = "#2F3030"
        )
        very_bottom_frame1.place(x = 10, y = 565)

        add_idea_button = tk.Button(
            very_bottom_frame1,
            text = "CATCH THE IDEA",
            font = ('Arial', '8', 'bold'),
            width = 14,
            command = self.show_new_idea_window,
            background = '#4F0082',
            foreground = '#FFFFFF'
        )
        add_idea_button.place(x = 10, y = 5)

        adhoc_task_button = tk.Button(
            very_bottom_frame1,
            text = "ADHOC TASK",
            font = ('Arial', '8', 'bold'),
            width = 13,
            command = self.show_new_adhoc_task_window,
            background = '#A94102',
            foreground = '#FFFFFF'
        )
        adhoc_task_button.place(x = 125, y = 5)

        very_bottom_frame2 = tk.Frame(
            self.root,
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
            command = self.show_new_task_window,
            background = '#004C01',
            foreground = '#FFFFFF'
        )
        new_task_button.place(x = 5, y = 2)

        very_bottom_frame3 = tk.Frame(
            self.root,
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
            command = self.show_new_remark_window,
            background = '#9E019A',
            foreground = '#FFFFFF'
        )
        add_remark_button.place(x = 8, y = 5)

        add_event_button = tk.Button(
            very_bottom_frame3,
            text = " ADD EVENT",
            font = ('Arial', '8', 'bold'),
            width = 13,
            command = self.show_new_event_window,
            background = '#A8A803',
            foreground = '#FFFFFF'
        )
        add_event_button.place(x = 116, y = 5)

        self.check_connection()
        data_store_manager.make_list_data_tuple()
        self.progress_bar_of_day()
        self.show_number_of_day_element('task')
        self.show_number_of_day_element('remark')
        self.show_number_of_day_element('event')
        data_store_manager.insert_day_data_to_treeview(self.treeview, 'task')
        data_store_manager.insert_day_data_to_treeview(self.treeview_remarks, 'remark')
        data_store_manager.insert_day_data_to_treeview(self.treeview_events, 'event')
        self.show_total_number_of_elements('task', '', 'No', 'No', self.right_frame, 200, 162)
        self.show_total_number_of_elements('task', 'Yes', 'No', 'No', self.right_frame, 200, 202)
        self.show_total_number_of_elements('project', '', 'No', 'No', self.right_frame, 200, 242)
        self.show_total_number_of_elements('idea', 'None', 'No', 'No', self.right_frame, 200, 282)
        self.show_total_number_of_elements('maybe/sometimes', '', 'No', 'No', self.right_frame, 200, 322)
        self.show_total_number_of_elements('personal card', 'None', 'No', 'No', self.right_frame, 200, 362)
        self.check_notifications()
        
        
        self.root.mainloop()