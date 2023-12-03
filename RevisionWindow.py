import tkinter as tk
from tkinter import ttk
import datetime
from DBManager import *
from DataStoreManager import *
from DataFormObject import *
from element_window_extended import *
from element_window_small import*
from ProjectWindow import *
from PersonalCardWindow import *

current_date = datetime.now()
date_string = current_date.strftime("%d/%m/%Y")
tomorrow = datetime.today() + timedelta(days=1)
tomorrow_date = tomorrow.strftime('%d/%m/%Y')
db_manager = DBManager()
data_store_manager = DataStoreManager()
data = DataForm()

class RevisionWindow:

    def __init__(self, parent, title):
        self.window = tk.Toplevel(parent)
        self.window.geometry('800x600+300+50')
        self.window.title(str(title).upper() + ' REVISION')
        self.window.option_add('*Dialog.msg.title.bg', '#000000')
        self.window.configure(bg = "#AFAFAF")
        self.window.resizable(0,0)

        self.title = title
        self.title_list_day_week = ['MY TASKS', 'DELEGATED TASKS', 'SHARED TASKS', 'MY PROJECTS', 'DELEGATED PROJECTS', 
                           'SHARED PROJECTS', 'EVENTS', 'REMARKS', 'MAYBE/SOMETIMES', 'BIRTHDAYS']
        self.title_list_month = ['DEADLINES', 'EVENTS']
        self.current_index = 0

        if self.title == 'day' or self.title == 'week':
            self.current_title = 'MY TASKS'
        elif self.title == 'month':
            self.current_title = 'DEADLINES'
        else:
            print('Wrong self.title in RevisionWindow')

    def insert_data_to_revision_treeview(self):
        self.list_data_tuple = data_store_manager.make_list_data_tuple()
        self.treeview.delete(*self.treeview.get_children())

        if self.title == 'day': # tasks date +1, deadline + 7 days; projects deadline + 7 days, events +1 day, remarks +1 day, maybe/sometimes all, birthdays + 7 days 
            for data_row in self.list_data_tuple:
                if self.current_title == 'MY TASKS':
                    if data_row[15] == 'task' and data_row[3] == current_date and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                    if data_row[15] == 'task' and data_row[3] == tomorrow_date and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                    for i in range(1,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'task' and data_row[4] == future_date and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                
                elif self.current_title == 'DELEGATED TASKS':
                    if data_row[15] == 'task' and data_row[3] == current_date and data_row[9] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                    if data_row[15] == 'task' and data_row[3] == tomorrow_date and data_row[9] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                    for i in range(1,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'task' and data_row[4] == future_date and data_row[9] != "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                
                elif self.current_title == 'SHARED TASKS':
                    if data_row[15] == 'task' and data_row[3] == current_date and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                    if data_row[15] == 'task' and data_row[3] == tomorrow_date and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        for i in range(1,7):
                            future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")

                elif self.current_title == 'MY PROJECTS':
                    for i in range(0,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'project' and data_row[4] == future_date and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'DELEGATED PROJECTS':
                    for i in range(0,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'project' and data_row[4] == future_date and data_row[9] != "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'SHARED PROJECTS':
                    for i in range(0,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'project' and data_row[4] == future_date and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'EVENTS':
                    if data_row[15] == 'event':
                        start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                        end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                        future_date = (current_date + timedelta(days=1)).strftime("%d/%m/%Y")
                        future_date_string = datetime.strptime(future_date, "%d/%m/%Y")
                        if start_date <= future_date_string and end_date >= future_date_string:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'REMARKS':
                    if data_row[15] == 'remark' and data_row[3] == tomorrow_date:
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'MAYBE/SOMETIMES':
                    if data_row[15] == 'maybe/sometimes':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'BIRTHDAYS':
                    for i in range(0,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m")
                        if data_row[15] == 'personal card' and data_row[3] == future_date:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

        elif self.title == 'week':
            for data_row in self.list_data_tuple:
                if self.current_title == 'MY TASKS':
                    if data_row[15] == 'task'and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                
                elif self.current_title == 'DELEGATED TASKS':
                    if data_row[15] == 'task'and data_row[9] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'SHARED TASKS':
                    if data_row[15] == 'task'and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'MY PROJECTS':
                    if data_row[15] == 'project'and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'DELEGATED PROJECTS':
                    if data_row[15] == 'project'and data_row[9] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'SHARED PROJECTS':
                    if data_row[15] == 'project'and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'EVENTS':
                    if data_row[15] == 'event':
                        start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                        end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                        for i in range(0,30):
                            future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                            future_date_string = datetime.strptime(future_date, "%d/%m/%Y")
                            if start_date <= future_date_string and end_date >= future_date_string:
                                self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'REMARKS':
                    for i in range(0,30):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'remark' and data_row[3] == future_date:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'MAYBE/SOMETIMES':
                    if data_row[15] == 'maybe/sometimes':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

                elif self.current_title == 'BIRTHDAYS':
                    if data_row[15] == 'personal card':
                        for i in range(0,30):
                            future_date = (current_date + timedelta(days=i)).strftime("%d/%m")
                            if data_row[3] == future_date:
                                self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))

        elif self.title == 'month':
            for data_row in self.list_data_tuple:
                if self.current_title == 'DEADLINES':
                    for i in range(0,30):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'task' and data_row[4] == future_date and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                elif self.current_title == 'EVENTS':
                    if data_row[15] == 'event':
                        start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                        end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                        for i in range(0,30):
                            future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                            future_date_string = datetime.strptime(future_date, "%d/%m/%Y")
                            if start_date <= future_date_string and end_date >= future_date_string:
                                self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
        else:
            print('Wrong self.current_title in RevisionWindow: function Insert_data_to_treeview')


    def next(self):
        if self.title == 'day' or self.title == 'week':
            if self.current_index < len(self.title_list_day_week):
                self.current_title = self.title_list_day_week[self.current_index]
                self.current_index += 1
            else:
                self.current_index += 0
                self.finish_button.place(relx = 0.5, y = 550, anchor = 'center')
        elif self.title == 'month':
            self.treeview_label.configure(text = 'DEADLINES')
            if self.current_index < len(self.title_list_month):
                self.current_title = self.title_list_month[self.current_index]
                self.current_index += 1
            else:
                self.current_index += 0
                self.finish_button.place(relx = 0.5, y = 550, anchor = 'center')
        else:
            print('Wrong self.title in RevisionWindow: function Next')
        
        self.treeview_label.configure(text = str(self.current_title) + ':')
        self.insert_data_to_revision_treeview()
        if self.current_title == 'MY TASKS' or self.current_title == 'DELEGATED TASKS' or self.current_title == 'SHARED TASKS' or self.current_title == 'MY PROJECTS' or self.current_title == 'DELEGATED PROJECTS' or self.current_title == 'SHARED PROJECTS' or self.current_title == 'DEADLINES':
            self.done_button.place(x = 15, y = 400)
        else:
            self.done_button.place_forget()

    def back(self):
        if self.current_index > 0:
            self.current_index -= 1
            if self.title == 'day' or self.title == 'week':
                self.current_title = self.title_list_day_week[self.current_index]
            elif self.title == 'month':
                self.current_title = self.title_list_month[self.current_index]
            else:
                print('Wrong self.title in RevisionWindow: function Back')
            
            self.treeview_label.configure(text = str(self.current_title) + ':')
            self.insert_data_to_revision_treeview()
            if self.current_title == 'MY TASKS' or self.current_title == 'DELEGATED TASKS' or self.current_title == 'SHARED TASKS' or self.current_title == 'MY PROJECTS' or self.current_title == 'DELEGATED PROJECTS' or self.current_title == 'SHARED PROJECTS' or self.current_title == 'DEADLINES':
                self.done_button.place(x = 15, y = 400)
            else:
                self.done_button.place_forget()
        else:
            self.current_index -= 0

    def exit(self):
        self.window.destroy()

    def show_new_idea_window(self):
        idea_window = element_window_small(
            self.window, 'Idea', None
        )
        idea_window.create_window()
    
    def create_window(self):
        header_label = tk.Label(
            self.window,
            text = str(self.title).upper() + " REVISION",
            font = ('Montserrat', '25', 'bold'),
            background = "#AFAFAF",
            foreground = "#2D4A54"
        )
        header_label.place(relx = 0.5, y = 35, anchor = 'center')

        self.treeview_label = tk.Label(
            self.window,
            text = "MY TASKS: ",
            font = ('Montserrat', '14', 'bold'),
            background = "#AFAFAF",
            foreground = "#2D4A54"
        )
        self.treeview_label.place(x = 15, y = 75)

        if self.title == 'month':
            self.treeview_label.configure(text = 'DEADLINES: ')


        self.treeview = ttk.Treeview(
            self.window, 
            columns=('#1', '#2', '#3', '#4', '#5', '#6'),
            height = 13
        )

        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=0, stretch = False)
        self.treeview.heading('#1', text='Element ID')
        self.treeview.column('#1', width=120)
        self.treeview.heading('#2', text='Element')
        self.treeview.column('#2', width=180)
        self.treeview.heading('#3', text='Date')
        self.treeview.column('#3', width=80)
        self.treeview.heading('#4', text='Deadline')
        self.treeview.column('#4', width=80)
        self.treeview.heading('#5', text='Delegated')
        self.treeview.column('#5', width=150)
        self.treeview.heading('#6', text='Cooperating')
        self.treeview.column('#6', width=150)

        self.treeview.place (x = 15, y = 105)

        self.done_button = tk.Button(
            self.window,
            text = "DONE",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = None,
            background = '#004C01',
            foreground = '#FFFFFF'
        )
        self.done_button.place(x=15, y=400)

        view_button = tk.Button(
            self.window,
            text = "VIEW",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = None,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        view_button.place(x=130, y = 400)

        delete_button = tk.Button(
            self.window,
            text = "DELETE",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = None,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        delete_button.place(x=245, y = 400)

        back_button = tk.Button(
            self.window,
            text = "BACK",
            font = ('Arial', '15', 'bold'),
            width = 15,
            command = self.back,
            background = '#6700DC',
            foreground = '#FFFFFF'
        )
        back_button.place(x=80, y = 470)

        add_idea_button = tk.Button(
            self.window,
            text = "CATCH THE IDEA",
            font = ('Arial', '15', 'bold'),
            width = 15,
            command = self.show_new_idea_window,
            background = '#4F0082',
            foreground = '#FFFFFF'
        )
        add_idea_button.place(relx = 0.5, y = 490, anchor = 'center')

        next_button = tk.Button(
            self.window,
            text = "NEXT",
            font = ('Arial', '15', 'bold'),
            width = 15,
            command = self.next,
            background = '#06CA00',
            foreground = '#FFFFFF'
        )
        next_button.place(x=530, y = 470)

        self.finish_button = tk.Button(
            self.window,
            text = "FINISH REVISION",
            font = ('Arial', '15', 'bold'),
            width = 15,
            command = self.exit,
            background = '#000000',
            foreground = '#FFFFFF'
        )
        self.finish_button.place_forget()

        self.insert_data_to_revision_treeview()