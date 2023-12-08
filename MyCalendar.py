import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import datetime
import time
import calendar
from DBManager import *
from DataFormObject import *
from DataStoreManager import *
from element_window_extended import *
from element_window_small import *
from ProjectWindow import *
from PersonalCardWindow import *
from dateutil.relativedelta import relativedelta

current_date = datetime.now()
date_string = current_date.strftime("%d/%m/%Y")
tomorrow = datetime.today() + timedelta(days=1)
tomorrow_date = tomorrow.strftime('%d/%m/%Y')
db_manager = DBManager()
data_store_manager = DataStoreManager()
data = DataForm()

month_and_year = current_date.strftime("%B %Y")

class MyCalendar:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.geometry("1000x695+200+0")
        self.window.configure(bg="#212121")
        self.window.title('Calendar')
        self.window.resizable(0,0)
      
        style = ttk.Style()
        style.theme_use('clam')

        self.month_and_year = current_date
        self.month_and_year_str = current_date.strftime("%B %Y")

        self.first_month_date = self.set_month_beggining()
        self.selected_date_unformated = None
        self.selected_date = None
        self.heading = 'forward'
        self.frame_name = None
        self.button_name = None
        self.frame_names = []
        self.button_names = []
        self.first_date_check = []

        self.task_frames = []
        self.remark_frames = []
        self.event_frames = []
        self.deadline_frames = []
        self.birthday_frames = []

    def set_month_beggining(self):
        user_selected_month = self.month_and_year
        selected_date = user_selected_month.replace(day=1)
        formated_date = selected_date.strftime("%d/%m/%Y") + '\n' + selected_date.strftime('%A')
        return selected_date

    def plus_day_date(self):
        self.selected_date_unformated = self.selected_date_unformated + timedelta(days=1)
        selected_date = self.selected_date_unformated.strftime('%d/%m/%Y') + '\n' + self.selected_date_unformated.strftime('%A')
        return selected_date
    
    def count_number_month_days(self):
        year = int(self.month_and_year.strftime('%Y'))
        month = int(self.month_and_year.strftime('%m'))
        days_in_month = calendar.monthrange(year, month)[1]
        return days_in_month

    def change_month_beggining(self):
        self.date_date = self.set_month_beggining()


    def create_frame(self, frame_sign, XX, YY):
        self.frame_name = 'date_frame' + str(frame_sign)
        self.frame_name = tk.Frame(
            self.window,
            width=125,
            height=110,
            background="#2F3030"
        )
        self.frame_name.place(x=XX, y=YY)

        self.button_name = 'date_button' + str(frame_sign)
        self.button_name = tk.Button(
            self.frame_name,
            text= '',
            font=('Arial', '10', 'bold'),
            width=13,
            background='#001B81',
            foreground='#FFFFFF'
        )
        self.button_name.place(x=5, y=5)
        self.button_name.bind("<Button-1>", self.show_calendar_date_window)

        self.frame_names.append(self.frame_name)
        self.button_names.append(self.button_name)

        self.task_frame = 'task_frame' + str(frame_sign)
        self.task_frame = tk.Frame(
            self.frame_name,
            width=115,
            height=5,
            background= '#0CC800'
        )
        self.task_frame.place_forget()
        self.task_frames.append(self.task_frame)

        self.remark_frame = 'remark_frame' + str(frame_sign)
        self.remark_frame = tk.Frame(
            self.frame_name,
            width=115,
            height=5,
            background='#9E019A'
        )
        self.remark_frame.place_forget()
        self.remark_frames.append(self.remark_frame)

        self.event_frame = 'event_frame' + str(frame_sign)
        self.event_frame = tk.Frame(
            self.frame_name,
            width=115,
            height=5,
            background='#A8A803'
        )
        self.event_frame.place_forget()
        self.event_frames.append(self.event_frame)

        self.deadline_frame = 'deadline_frame' + str(frame_sign)
        self.deadline_frame = tk.Frame(
            self.frame_name,
            width=115,
            height=5,
            background='#970000'
        )
        self.deadline_frame.place_forget()
        self.deadline_frames.append(self.deadline_frame)

        self.birthday_frame = 'birthday_frame' + str(frame_sign)
        self.birthday_frame = tk.Frame(
            self.frame_name,
            width=115,
            height=5,
            background='#47A0FF'
        )
        self.birthday_frame.place_forget()
        self.birthday_frames.append(self.birthday_frame)

        return self.frame_name
    
    def create_notification_bars(self, i):
        list_data_tuple = data_store_manager.make_list_data_tuple()
        searched_date = (str(self.selected_date))[:10]
        searched_birthday = (str(self.selected_date))[:5]

        for data_row in list_data_tuple:
            if data_row[15] == 'task' and data_row[3] == searched_date:
                self.task_frames[i].place(relx=0.5, y=60, anchor='center')
                break
            else:
                self.task_frames[i].place_forget()

        for data_row in list_data_tuple:
            if data_row[15] == 'remark' and data_row[3] == searched_date:
                self.remark_frames[i].place(relx = 0.5, y = 70, anchor = 'center')
                break
            else:
                self.remark_frames[i].place_forget()

        for data_row in list_data_tuple:
            if data_row[15] == 'event':
                start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                event_date_string = datetime.strptime(self.selected_date[:10], "%d/%m/%Y")
                if start_date <= event_date_string and end_date >= event_date_string:
                    self.event_frames[i].place(relx = 0.5, y = 80, anchor = 'center')
                    break
                else:
                    self.event_frames[i].place_forget()
        
        for data_row in list_data_tuple:
            if data_row[15] == 'task' and data_row[4] == searched_date:
                self.deadline_frames[i].place(relx = 0.5, y = 90, anchor = 'center')
                break
            elif data_row[15] == 'project' and data_row[4] == searched_date:
                self.deadline_frames[i].place(relx = 0.5, y = 90, anchor = 'center')
                break
            else:
                self.deadline_frames[i].place_forget()

        for data_row in list_data_tuple:
            if data_row[15] == 'personal card' and data_row[3] == searched_birthday:
                self.birthday_frames[i].place(relx = 0.5, y = 100, anchor = 'center')
                break
            else:
                self.birthday_frames[i].place_forget()

    def show_date_frames(self):
        x = 15
        y = 75
        gap = 135
        number_days_in_month = self.count_number_month_days()

        for i in range(0, 7):
            if i == 0:
                if len(self.first_date_check) == 0:
                    self.selected_date_unformated = self.set_month_beggining()
                    self.selected_date = self.selected_date_unformated.strftime("%d/%m/%Y") + '\n' + self.selected_date_unformated.strftime('%A')
                    self.first_date_check.append(self.selected_date)
                else:
                    if self.heading == 'forward':
                        self.selected_date = self.plus_day_date()
                    else:
                        if i == 0:
                            self.selected_date_unformated = self.set_month_beggining()
                            self.selected_date = self.selected_date_unformated.strftime("%d/%m/%Y") + '\n' + self.selected_date_unformated.strftime('%A')
                        else:
                            self.selected_date = self.plus_day_date()

            else:
                self.selected_date = self.plus_day_date()

            if len(self.frame_names) == i:
                frame = self.create_frame(i, x, y)
            else:
                pass
            #self.delete_notification_bars()
            self.button_names[i].configure(text=self.selected_date)
            self.create_notification_bars(i)
            x += gap
        
        x = 15
        y = 200
        for i in range(7, 14):
            self.selected_date = self.plus_day_date()

            if len(self.frame_names) == i:
                frame = self.create_frame(i, x, y)
            else:
                pass
            #self.delete_notification_bars()
            self.create_notification_bars(i)
            self.button_names[i].configure(text=self.selected_date)
            x += gap

        x = 15
        y = 325
        for i in range(14, 21):
            self.selected_date = self.plus_day_date()

            if len(self.frame_names) == i:
                frame = self.create_frame(i, x, y)
            else:
                pass
            #self.delete_notification_bars()
            self.create_notification_bars(i)
            self.button_names[i].configure(text=self.selected_date)
            x += gap

        x = 15
        y = 450
        for i in range(21, 28):
            self.selected_date = self.plus_day_date()

            if len(self.frame_names) == i:
                frame = self.create_frame(i, x, y)
            else:
                pass
            #self.delete_notification_bars()
            self.create_notification_bars(i)
            self.button_names[i].configure(text=self.selected_date)
            x += gap

        x = 15
        y = 575
        if number_days_in_month == 28:
            for i in range(28, 31):
                self.frame_names[i].place_forget()

        elif number_days_in_month == 29:
            for i in range(28, 29):
                self.frame_name.place_forget()
                self.selected_date = self.plus_day_date()

                if len(self.frame_names) == i:
                    frame = self.create_frame(i, x, y)
                else:
                    self.frame_name.place(x=x, y=y)
                #self.delete_notification_bars()
                self.create_notification_bars(i)
                self.button_names[i].configure(text=self.selected_date)
                x += gap
            for i in range(29, 31):
                self.frame_names[i].place_forget()

        elif number_days_in_month == 30:
            for i in range(28, 30):
                self.frame_name.place_forget()
                self.selected_date = self.plus_day_date()

                if len(self.frame_names) == i:
                    frame = self.create_frame(i, x, y)
                else:
                    self.frame_names[i].place(x=x, y=y)
                #self.delete_notification_bars()
                self.create_notification_bars(i)
                self.button_names[i].configure(text=self.selected_date)
                x += gap
            for i in range(30, 31):
                self.frame_name.place_forget()

        elif number_days_in_month == 31:
            for i in range(28, 31):
                self.selected_date = self.plus_day_date()
                if len(self.frame_names) == i:
                    frame = self.create_frame(i, x, y)
                else:
                    self.frame_names[i].place(x=x, y=y)
                #self.delete_notification_bars()
                self.create_notification_bars(i)
                self.button_names[i].configure(text=self.selected_date)
                x += gap
        self.heading = None

    def previous_month(self):
        self.heading = 'backward'
        self.month_and_year = self.month_and_year - relativedelta(months=1)
        self.month_and_year_str = self.month_and_year.strftime("%B %Y")
        self.header_label.configure(text = self.month_and_year_str)
        self.show_date_frames()

    def next_month(self):
        self.heading = 'forward'
        self.month_and_year = self.month_and_year + relativedelta(months=1)
        self.month_and_year_str = self.month_and_year.strftime("%B %Y")
        self.header_label.configure(text = self.month_and_year_str)
        self.show_date_frames()

    def show_calendar_date_window(self, event):
        clicked_button = event.widget
        date_and_day = clicked_button.cget('text')
        date = date_and_day[:10]
        day = date_and_day[11:]
        calendar_date_window = CalendarDateWindow(self.window, date, day)

        calendar_date_window.create_window()

    def exit(self):
        self.window.destroy()

    def create_window(self):
        self.header_label = tk.Label(
            self.window,
            text = self.month_and_year_str,
            font = ('Montserrat', '23'),
            background = "#212121",
            foreground = '#FFFFFF'
        )
        self.header_label.place (x = 60, y = 15)

        previous_month_button = tk.Button(
            self.window,
            text = '<',
            font = ('Arial', '15', 'bold'),
            width = 2,
            command = self.previous_month,
            background = '#0091C3',
            foreground = '#FFFFFF'
        )
        previous_month_button.place(x = 15, y = 15)

        next_month_button = tk.Button(
            self.window,
            text = '>',
            font = ('Arial', '15', 'bold'),
            width = 2,
            command = self.next_month,
            background = '#0091C3',
            foreground = '#FFFFFF'
        )
        next_month_button.place(x = 300, y = 15)

        description_label_task = tk.Label(
            self.window,
            text = "TASK",
            font = ('Montserrat', '10'),
            background = "#212121",
            foreground = '#FFFFFF'
        )
        description_label_task.place(x = 400, y = 15)

        description_bar_task = tk.Frame(
            self.window,
            width=80,
            height=5,
            background= '#0CC800'
        )
        description_bar_task.place(x = 480, y = 20)

        description_label_remark = tk.Label(
            self.window,
            text = "REMARK",
            font = ('Montserrat', '10'),
            background = "#212121",
            foreground = '#FFFFFF'
        )
        description_label_remark.place(x = 400, y = 40)
        
        description_bar_remark = tk.Frame(
            self.window,
            width=80,
            height=5,
            background='#9E019A'
        )
        description_bar_remark.place(x = 480, y = 45)

        description_label_event = tk.Label(
            self.window,
            text = "EVENT",
            font = ('Montserrat', '10'),
            background = "#212121",
            foreground = '#FFFFFF'
        )
        description_label_event.place(x = 580, y = 15)

        description_bar_event = tk.Frame(
            self.window,
            width=80,
            height=5,
            background='#A8A803'
        )
        description_bar_event.place(x = 660, y = 20)

        description_label_deadline = tk.Label(
            self.window,
            text = "DEADLINE",
            font = ('Montserrat', '10'),
            background = "#212121",
            foreground = '#FFFFFF'
        )
        description_label_deadline.place(x = 580, y = 40)

        description_bar_deadline = tk.Frame(
            self.window,
            width=80,
            height=5,
            background='#970000'
        )
        description_bar_deadline.place(x = 660, y = 45)

        description_label_birhtday = tk.Label(
            self.window,
            text = "BIRTHDAY",
            font = ('Montserrat', '10'),
            background = "#212121",
            foreground = '#FFFFFF'
        )
        description_label_birhtday.place(x = 780, y = 15)

        description_bar_birhtday = tk.Frame(
            self.window,
            width=80,
            height=5,
            background='#47A0FF'
        )
        description_bar_birhtday.place(x = 860, y = 20)


        exit_button = tk.Button(
            self.window,
            text = "EXIT",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.exit,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        exit_button.place(x = 850, y = 660)

        self.show_date_frames()


class CalendarDateWindow:
        def __init__(self, parent, date, day):
            self.window = tk.Toplevel(parent)
            self.window.geometry("800x560+50+50")
            self.window.configure(bg="#212121")
            self.window.title('DAY VIEW')
            self.window.resizable(0,0)
        
            style = ttk.Style()
            style.theme_use('clam')

            self.list_data_tuple = data_store_manager.make_list_data_tuple()
            self.date = date
            self.day = day
            self.text = 'TASKS'
            self.rows = []

        def fill_initial_data_to_treeview(self):

            self.treeview.delete(*self.treeview.get_children())
            self.rows.clear()
            birthday_date = self.date[:5]

            for data_row in self.list_data_tuple:
                if self.text == 'TASKS':
                    if data_row[15] == 'task' and data_row[3] == self.date:
                        if data_row[1] not in self.rows:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[16]))
                            self.rows.append(data_row[1])
            
                if data_row[15] == 'personal card' and data_row[3] == birthday_date:
                    print('birthday!')
                    if data_row[1] not in self.rows:
                            self.treeview_birthdays.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4]))
                            self.rows.append(data_row[1])
        
        def insert_data_to_treeview(self, event):
            clicked_button = event.widget
            self.text = clicked_button.cget('text')

            self.treeview.delete(*self.treeview.get_children())
            self.rows.clear()
            self.treeview_label.configure(text = self.text + ': ')

            for data_row in self.list_data_tuple:
                if self.text == 'TASKS':
                    if data_row[15] == 'task' and data_row[3] == self.date:
                        if data_row[1] not in self.rows:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[16]))
                            self.rows.append(data_row[1])

                elif self.text == 'DEADLINES':
                    if data_row[15] == 'task' and data_row[4] == self.date:
                        if data_row[1] not in self.rows:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[16]))
                            self.rows.append(data_row[1])
                    if data_row[15] == 'project' and data_row[4] == self.date:
                        if data_row[1] not in self.rows:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[16]))
                            self.rows.append(data_row[1])

                elif self.text == 'REMARKS':
                    if data_row[15] == 'remark' and data_row[3] == self.date:
                        if data_row[1] not in self.rows:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[16]))
                            self.rows.append(data_row[1])

                elif self.text == 'EVENTS':
                    if data_row[15] == 'event':
                        start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                        end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                        date_string = datetime.strptime(self.date, "%d/%m/%Y")
                        if start_date <= date_string and end_date >= date_string:
                            if data_row[1] not in self.rows:
                                self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                                self.rows.append(data_row[1])
        
        def exit(self):
            self.window.destroy()

        def create_window(self):
            right_frame = tk.Frame(
                self.window,
                width = 230,
                height = 600,
                background = "#2F3030"
            )
            right_frame.place(x = 570, y = 0)

            header_label = tk.Label(
                right_frame,
                text = 'CALENDAR',
                font = ('Montserrat', '25'),
                background = "#2F3030",
                foreground = "#474747"
            )
            header_label.place(x = 15, y = 50)

            task_button = tk.Button(
                right_frame,
                text = "TASKS",
                font = ('Arial', '11'),
                width = 19,
                background = '#00248B',
                foreground = '#FFFFFF'
            )
            task_button.place(x = 16, y = 160)
            task_button.bind("<Button-1>", self.insert_data_to_treeview)

            deadline_button = tk.Button(
                right_frame,
                text = "DEADLINES",
                font = ('Arial', '11'),
                width = 19,
                command = None,
                background = '#00248B',
                foreground = '#FFFFFF'
            )
            deadline_button.place(x = 16, y = 200)
            deadline_button.bind("<Button-1>", self.insert_data_to_treeview)

            remark_button = tk.Button(
                right_frame,
                text = "REMARKS",
                font = ('Arial', '11'),
                width = 19,
                command = None,
                background = '#00248B',
                foreground = '#FFFFFF'
            )
            remark_button.place(x = 16, y = 240)
            remark_button.bind("<Button-1>", self.insert_data_to_treeview)

            event_button = tk.Button(
                right_frame,
                text = "EVENTS",
                font = ('Arial', '11'),
                width = 19,
                command = None,
                background = '#00248B',
                foreground = '#FFFFFF'
            )
            event_button.place(x = 16, y = 280)
            event_button.bind("<Button-1>", self.insert_data_to_treeview)

            exit_button = tk.Button(
                right_frame,
                text = "EXIT",
                font = ('Arial', '11'),
                width = 19,
                command = self.exit,
                background = '#970000',
                foreground = '#FFFFFF'
            )
            exit_button.place(x = 16, y = 480)

            top_frame_left = tk.Frame(
                self.window,
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
                text = "DAY VIEW",  
                font = ("Open Sans", "30"),  
                background = "#6A6A6A",  
                foreground = "#FFFFFF"  
            )
            my_day_sign.place(x = 25, y = 20)

            top_frame_right = tk.Frame(
                self.window,
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
                text = self.date,  
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
                text = self.day,  
                font = ("Open Sans ", "20"),  
                background = "#6A6A6A",  
                foreground = "#FFFFFF"  
            )
            weekday_label.place(x = 95, y = 45)

            middle_frame = tk.Frame(
                self.window,
                width = 550,
                height = 235,
                background = "#2F3030"
            )
            middle_frame.place(x = 10, y = 155)

            self.treeview_label = tk.Label(
                middle_frame,
                text = self.text + ': ',
                font = ("Open Sans", "12", "bold"),
                background = "#2F3030",
                foreground = "#FFFFFF"
            )
            self.treeview_label.place(x = 10, y = 6)

            self.treeview = ttk.Treeview(
                middle_frame, columns=('#1', '#2', '#3', '#4', '#5', '#6'), height = 8)
            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Element ID')
            self.treeview.column('#1', width=0, stretch = False)
            self.treeview.heading('#2', text='Element')
            self.treeview.column('#2', width=200)
            self.treeview.heading('#3', text='Date')
            self.treeview.column('#3', width=80)
            self.treeview.heading('#4', text='Deadline')
            self.treeview.column('#4', width=80)
            self.treeview.heading('#5', text='Delegated')
            self.treeview.column('#5', width=80)
            self.treeview.heading('#6', text='Done')
            self.treeview.column('#6', width=80)

            self.treeview.place (x = 15, y = 35)

            bottom_frame = tk.Frame(
                self.window,
                width = 550,
                height = 150,
                background = "#2F3030"
            )
            bottom_frame.place(x = 10, y = 400)

            birthday_treeview_label = tk.Label(
                bottom_frame,
                text = "Birthday:",
                font = ("Open Sans", "12", "bold"),
                background = "#2F3030",
                foreground = "#FFFFFF"
            )
            birthday_treeview_label.place(x = 10, y = 6)

            self.treeview_birthdays = ttk.Treeview(
                bottom_frame, columns=('#1','#2', '#3', '#4'), height = 4)

            self.treeview_birthdays.heading('#0', text='ID')
            self.treeview_birthdays.column('#0', width=0, stretch = False)
            self.treeview_birthdays.heading('#1', text='Element ID')
            self.treeview_birthdays.column('#1', width=0, stretch = False)
            self.treeview_birthdays.heading('#2', text='Name')
            self.treeview_birthdays.column('#2', width=305)
            self.treeview_birthdays.heading('#3', text='Date')
            self.treeview_birthdays.column('#3', width=110)
            self.treeview_birthdays.heading('#4', text='Year')
            self.treeview_birthdays.column('#4', width=110)

            self.treeview_birthdays.place (x = 10, y = 35)

            self.fill_initial_data_to_treeview()