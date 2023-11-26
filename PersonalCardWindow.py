import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
from DBManager import *
from DataStoreManager import *
from DataFormObject import DataForm

db_manager = DBManager()
data_store_manager = DataStoreManager()
data = DataForm()
now = datetime.now()
today = now.strftime('%d/%m')
tomorrow = (now + timedelta(days=1)).strftime('%d/%m')
yesterday = (now - timedelta(days=1)).strftime('%d/%m')


class PersonalCardWindow:

    def __init__(self, parent, element_id):
        self.window = tk.Toplevel(parent)
        self.window.geometry('800x600+200+50')
        self.window.title('Personal Card')
        self.window.option_add('*Dialog.msg.title.bg', '#000000')
        self.window.configure(bg = "#FFFFFF")
        self.window.resizable(0,0)

        if element_id == None:
            element_id = db_manager.generate_element_id('PC')
        else:
            pass
        self.element_id = element_id

    def get_personal_data(self):
            data.element_id = self.element_id
            if self.first_name_row.get() == 'FIRST NAME':
                self.first_name_row.get() == ""
            else:
                pass
            if self.last_name_row.get() == 'LAST NAME':
                self.last_name_row.get() == ''
            else:
                pass
            data.element = self.first_name_row.get() + ' ' + self.last_name_row.get()
            if self.day_date_row.get() == 'dd' or self.month_date_row.get() == 'mm':
                data.date = ''
            else:
                data.date = self.day_date_row.get() + '/' + self.month_date_row.get()
            if self.year_date_row.get() == 'yyyy':
                data.deadline = ''
            else:
                data.deadline = self.year_date_row.get()
            if self.field1_row.get() == 'Field 1':
                data.field1 = ''
            else:
                data.field1 = self.field1_row.get()
            if self.field2_row.get() == 'Field 2':
                data.field2 = ''
            else:
                data.field2 = self.field2_row.get()
            if self.field3_row.get() == 'Field 3':
                data.field3 = ''
            else:
                data.field3 = self.field3_row.get()
            if self.company_row.get() == 'Company name':
                data.cooperating = ''
            else:
                data.cooperating = self.company_row.get()
            if self.title_before_row.get() == 'Title before name':
                data.field4 = ''
            else:
                data.field4 = self.title_before_row.get()
            if self.title_after_row.get() == 'Title after name':
                data.field5 = ''
            else:
                data.field5 = self.title_after_row.get()
            if self.email_row.get() == 'email_adress@default.com':
                data.remarks = ''
            else:
                data.remarks = self.email_row.get()
            if self.phone_number_row.get() == 'Phone number':
                data.keywords = ''
            else:
                data.keywords = self.phone_number_row.get()
            data.category = 'personal card'

    def save_or_edit_card(self):   
        try:
            self.get_personal_data()
            if db_manager.element_id_already_exists(self.element_id):
                db_manager.update_db_fields(data)
            else:
                db_manager.save_to_db(data)
            data_store_manager.make_list_data_tuple()
            self.window.destroy()
        except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")
                self.window.destroy()
        else:
            pass

    def exit(self):
        self.window.destroy()

    def insert_data_to_treeviews(self):
        name = self.first_name_row.get() + ' ' + self.last_name_row.get()
        print('NAME is: ' + name)
        data_store_manager.insert_data_to_personal_card_treeview(self.delegated_task_treeview, 'task', name)
        data_store_manager.insert_data_to_personal_card_treeview(self.cooperating_on_treeview, 'coooperating', name)
        data_store_manager.insert_data_to_personal_card_treeview(self.delegated_projects_treeview, 'project', name)
        self.window.after(10000, self.insert_data_to_treeviews)

    def create_window(self):
        top_frame = tk.Frame(
            self.window,
            width = 800,
            height = 130,
            background = "#D9D0AF"
        )
        top_frame.place(x = 15, y = 0)

        self.first_name_row = tk.Entry(
            top_frame,
            font = ("Open Sans", "18", "bold"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#D9D0AF",
            foreground = "#2D4A54"
        )
        self.first_name_row.place(x = 230, y = 35)

        self.last_name_row = tk.Entry(
            top_frame,
            font = ("Open Sans", "18", "bold"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#D9D0AF",
            foreground = "#2D4A54"
        )
        self.last_name_row.place(x = 260, y = 75)

        left_frame = tk.Frame(
            self.window,
            width = 200,
            height = 585,
            background = "#2D4A54"
        )
        left_frame.place(x = 30, y = 0)

        self.title_before_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10", "bold"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.title_before_row.place(x = 10, y = 180)

        self.title_after_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10", "bold"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.title_after_row.place(x = 10, y = 220)

        birthday_label = tk.Label(
            left_frame,
            text = 'Birthday',
            font = ('Montserrat', '12', 'bold'),
            background = "#2D4A54",
            foreground = "#FFFFFF")
        birthday_label.place(x = 10, y = 260)

        self.day_date_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 4,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.day_date_row.place(x = 10, y = 290)

        slash1_label = tk.Label(
            left_frame,
            text = "/",
            font = ("Open Sans", "16", "bold"),
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        slash1_label.place(x = 45, y = 285)

        self.month_date_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 4,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.month_date_row.place(x = 60, y = 290)

        slash2_label = tk.Label(
            left_frame,
            text = "/",
            font = ("Open Sans", "16", "bold"),
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        slash2_label.place(x = 85, y = 285)

        self.year_date_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 6,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.year_date_row.place(x = 100, y = 290)

        self.company_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.company_row.place(x = 10, y = 340)

        self.field1_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.field1_row.place(x = 10, y = 380)

        self.field2_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.field2_row.place(x = 10, y = 420)

        self.field3_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.field3_row.place(x = 10, y = 460)

        self.email_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.email_row.place(x = 10, y = 500)

        self.phone_number_row = tk.Entry(
            left_frame,
            font = ("Open Sans", "10"),
            width = 25,
            insertbackground = "#FFFFFF",
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        self.phone_number_row.place(x = 10, y = 540)

        delegated_tasks_label = tk.Label(
            self.window,
            text = "DELEGATED TASKS: ",
            font = ('Montserrat', '12', 'bold'),
            background = "#FFFFFF",
            foreground = "#2D4A54"
        )
        delegated_tasks_label.place(x = 250, y = 140)

        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure("Treeview", background = "#FFFFFF", fieldbackground = "#FFFFFF", foreground = "#2D4A54")

        self.delegated_task_treeview = ttk.Treeview(
            self.window, columns=('#1', '#2', '#3', '#4'), height=4)

        self.delegated_task_treeview.heading('#0', text='ID')
        self.delegated_task_treeview.column('#0', width=0, stretch = False)
        self.delegated_task_treeview.heading('#1', text='Element ID')
        self.delegated_task_treeview.column('#1', width=120)
        self.delegated_task_treeview.heading('#2', text='Task')
        self.delegated_task_treeview.column('#2', width=230)
        self.delegated_task_treeview.heading('#3', text='Date')
        self.delegated_task_treeview.column('#3', width=90)
        self.delegated_task_treeview.heading('#4', text='Deadline')
        self.delegated_task_treeview.column('#4', width=90)
        
        self.delegated_task_treeview.place (x = 250, y = 160)

        cooperating_on_label = tk.Label(
            self.window,
            text = "COOPERATING ON: ",
            font = ('Montserrat', '12', 'bold'),
            background = "#FFFFFF",
            foreground = "#2D4A54"
        )
        cooperating_on_label.place(x = 250, y = 280)

        self.cooperating_on_treeview = ttk.Treeview(
            self.window, columns=('#1', '#2', '#3', '#4'), height=4)
        
        self.cooperating_on_treeview.heading('#0', text='ID')
        self.cooperating_on_treeview.column('#0', width=0, stretch = False)
        self.cooperating_on_treeview.heading('#1', text='Element ID')
        self.cooperating_on_treeview.column('#1', width=120)
        self.cooperating_on_treeview.heading('#2', text='Task/Project')
        self.cooperating_on_treeview.column('#2', width=230)
        self.cooperating_on_treeview.heading('#3', text='Date')
        self.cooperating_on_treeview.column('#3', width=90)
        self.cooperating_on_treeview.heading('#4', text='Deadline')
        self.cooperating_on_treeview.column('#4', width=90)
        
        self.cooperating_on_treeview.place (x = 250, y = 300)

        delegated_projects_label = tk.Label(
            self.window,
            text = "DELEGATED PORJECTS: ",
            font = ('Montserrat', '12', 'bold'),
            background = "#FFFFFF",
            foreground = "#2D4A54"
        )
        delegated_projects_label.place(x = 250, y = 420)

        self.delegated_projects_treeview = ttk.Treeview(
            self.window, columns=('#1', '#2', '#3'), height=4)

        self.delegated_projects_treeview.heading('#0', text='ID')
        self.delegated_projects_treeview.column('#0', width=0, stretch = False)
        self.delegated_projects_treeview.heading('#1', text='Element ID')
        self.delegated_projects_treeview.column('#1', width=120)
        self.delegated_projects_treeview.heading('#2', text='Project')
        self.delegated_projects_treeview.column('#2', width=230)
        self.delegated_projects_treeview.heading('#3', text='Deadline')
        self.delegated_projects_treeview.column('#3', width=180)
        
        self.delegated_projects_treeview.place (x = 250, y = 440)

        save_button = tk.Button(
            self.window,
            text = "SAVE",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.save_or_edit_card,
            background = '#004C01',
            foreground = '#FFFFFF'
        )
        save_button.place(x = 690, y = 560)

        exit_submit_button = tk.Button(
            self.window,
            text = "EXIT",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.exit,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        exit_submit_button.place(x = 580, y = 560)

        self.insert_data_to_treeviews()