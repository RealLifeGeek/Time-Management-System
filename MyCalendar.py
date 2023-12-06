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

        button_name = 'date_button' + str(frame_sign)
        button_name = tk.Button(
            self.frame_name,
            text= '',
            font=('Arial', '10', 'bold'),
            width=13,
            command=None,
            background='#001B81',
            foreground='#FFFFFF'
        )
        button_name.place(x=5, y=5)

        self.frame_names.append(self.frame_name)
        self.button_names.append(button_name)

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

    #def delete_notification_bars(self):
    #    self.task_frame.place_forget()
    #    self.remark_frame.place_forget()
    #    self.event_frame.place_forget()
    #    self.deadline_frame.place_forget()
    #    self.birthday_frame.place_forget()

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

