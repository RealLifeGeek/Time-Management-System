import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox
from functions import generate_element_id, project_name_already_exist, element_id_already_exists
from DBManager import *
from DataFormObject import *
from DayDataManager import *

chosen_date = None
chosen_deadline = None
element_id = None
db_manager = DBManager()
day_data_manager = DayDataManager()
data = DataForm()


class element_window_extended: # task, remark, event
# for new element use title as 'Task', 'Remark', 'Event'
# for view existing element use title as 'Task View', 'Remark View' or 'Event View'
# for element_id use element_id or None
    def __init__(self, parent, title, db, element_id):
        self.window = tk.Toplevel(parent)
        self.window.geometry("600x400")
        self.window.configure(bg="#212121")
        self.window.title(title)

        self.calendar = Calendar (
            self.window, 
            selectmode = 'day', 
            date_pattern = ('dd/mm/yyyy'), 
            background = "black")
        self.calendar.place(x= 330, y= 160)

        if element_id == None:
            if title == 'Task':
                element_id = generate_element_id(db, 'NT')
            elif title ==  'Remark':
                element_id = generate_element_id(db, 'RE')
            elif title == 'Event':
                element_id = generate_element_id(db, 'EV')
        else:
            pass
        
        self.element_id = element_id
        self.title = title
        self.db = db
        
    def choose_date(self):
        chosen_date = self.calendar.get_date()
        self.date_row.delete(0, "end")
        self.date_row.insert(0, chosen_date)

    def choose_deadline(self):
        chosen_deadline = self.calendar.get_date()
        self.deadline_row.delete(0, "end")
        self.deadline_row.insert(0, chosen_deadline)

    def get_task_data(self):
        data.element_id = self.element_id
        data.element = self.element_description_row.get()
        data.date = self.date_row.get()
        data.deadline = self.deadline_row.get()     
        data.field2 = self.field2_row.get()
        data.field3 = self.field3_row.get()
        data.project = self.project_row.get()
        data.delegated = self.delegated_row.get()
        data.cooperating = self.cooperating_row.get()
        data.keywords = self.keywords_row.get()
        data.category = 'task'

        if data.date != None or data.deadline != None:
            if data.date == None and data.deadline != None:
                data.date = data.deadline
            elif data.date != None and data.deadline == None:
                data.deadline = data.date
        else:
            pass
    
    def get_event_data(self):
        data.element_id = self.element_id
        data.element = self.element_description_row.get()
        data.date = self.date_row.get()
        data.deadline = self.deadline_row.get()
        data.field1 = self.field1_row.get()
        data.field2 = self.field2_row.get()
        data.field3 = self.field3_row.get()
        data.field4 = self.field4_row.get()
        data.category = 'event'

    def get_remark_data(self):
        data.element_id = self.element_id
        data.element = self.element_description_row.get()
        data.date = self.date_row.get()
        data.field1 = self.field1_row.get()
        data.field2 = self.field2_row.get()
        data.category = 'remark'

    def save_or_edit_task(self):
        answer = messagebox.askokcancel("SAVE", "SAVE changes?")
        if answer:
            try:
                self.get_task_data()
                if element_id_already_exists(self.db, self.element_id):
                    db_manager.update_db_fields(data)
                    day_data_manager.make_day_data_tuple()
                else:
                    db_manager.save_to_db(data)
                    day_data_manager.make_day_data_tuple()

                if len(self.project_row.get()) != 0:
                    project_name = self.project_row.get()
                    if not project_name_already_exist(self.db, project_name):
                        data.element_id = generate_element_id(self.db, 'PR')
                        data.element = project_name
                        data.date = data.date
                        data.deadline = data.deadline
                        data.delegated = self.delegated_row.get()
                        data.cooperating = self.cooperating_row.get()
                        data.keywords = self.keywords_row.get()
                        data.category = 'project'

                        db_manager.save_to_db(data)
                else:
                    pass
                self.window.destroy()
            except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")
                self.window.destroy()
        else:
            pass

    def save_or_edit_event(self):
        answer = messagebox.askokcancel("SAVE", "SAVE changes?")
        if answer:
            try:
                self.get_event_data()
                if element_id_already_exists(self.db, self.element_id):
                    db_manager.update_db_fields(data)
                    day_data_manager.make_day_data_tuple()
                else:
                    db_manager.save_to_db(data)
                    day_data_manager.make_day_data_tuple()
                self.window.destroy()
            except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")
                self.window.destroy()
    
    def save_or_edit_remark(self):
        answer = messagebox.askyesno("SAVE", "SAVE changes?")
        if answer:
            try:
                self.get_remark_data()
                if element_id_already_exists(self.db, self.element_id):
                    db_manager.update_db_fields(data)
                    day_data_manager.make_day_data_tuple()
                else:
                    db_manager.save_to_db(data)
                    day_data_manager.make_day_data_tuple()
                self.window.destroy()
            except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")
                self.window.destroy()

    def exit(self):
        self.window.destroy()

    def create_window(self):
        self.header_label = tk.Label(
            self.window,
            text = self.title,
            font = ('Montserrat', '15'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.header_label.place(relx = 0.5, y = 15, anchor = 'center')

        self.task_id_label = tk.Label(
            self.window,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.task_id_label.place(x = 480, y = 5)

        self.top_frame = tk.Frame(
            self.window,
            width = 570,
            height = 100,
            background = "#2F3030"
        )
        self.top_frame.place(x = 15, y = 40)

        self.task_description_label = tk.Label(
            self.top_frame,
            text = "Element Name",
            font = ("Open Sans", "10", "bold"),
            background = "#2F3030",
            foreground = "#000000"
        )
        self.task_description_label.place(x = 10, y = 5)

        self.element_description_row = tk.Entry(
            self.top_frame,
            font = ("Open Sans", "10", "bold"),
            width = 56,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        self.element_description_row.place(x = 150, y = 5)

        if self.title == 'Remark' or self.title == 'Event' or self.title == 'Remark View' or self.title == 'Event View':
            self.field1_label = tk.Label(
                self.top_frame,
                text = "Field1",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.field1_label.place(x = 10, y = 35)
        
            self.field1_row = tk.Entry(
                self.top_frame,
                font = ("Open Sans", "10"),
                width = 56,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
                )
            self.field1_row.place(x = 150, y = 35)
        
        else:
            self.keywords_label = tk.Label(
                self.top_frame,
                text = "Keywords",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.keywords_label.place(x = 10, y = 35)

            self.keywords_row = tk.Entry(
                self.top_frame,
                font = ("Open Sans", "10"),
                width = 56,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
            )
            self.keywords_row.place(x = 150, y = 35)

        if self.title == 'Remark' or self.title == 'Event' or self.title == 'Remark View' or self.title == 'Event View':
            self.field2_label = tk.Label(
                self.top_frame,
                text = "Field2",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.field2_label.place(x = 10, y = 65)

        else:
            self.field2_label = tk.Label(
                self.top_frame,
                text = "Expected Result",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.field2_label.place(x = 10, y = 65)

        self.field2_row = tk.Entry(
            self.top_frame,
            font = ("Open Sans", "10"),
            width = 56,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        self.field2_row.place(x = 150, y = 65)

        self.middle_frame = tk.Frame(
            self.window,
            width = 305,
            height = 80,
            background = "#2F3030"
        )
        self.middle_frame.place(x = 15, y = 155)

        if self.title == 'Event' or self.title == 'Event View':
            self.date_button = tk.Button(
                self.middle_frame,
                text = "Choose Start Date",
                font = ('Arial', '10', 'bold'),
                width = 16,
                command = self.choose_date,
                background = '#464646',
                foreground = '#FFFFFF'
            )
            self.date_button.place(x = 10, y = 5)

            self.date_row = tk.Entry(
                self.middle_frame,
                font = ("Open Sans", "12", "bold"),
                width = 14,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#A8A803"
            )
            self.date_row.place(x = 160, y = 8)

            self.deadline_button = tk.Button(
                self.middle_frame,
                text = "Choose End Date",
                font = ('Arial', '10', 'bold'),
                width = 16,
                command = self.choose_deadline,
                background = '#970000',
                foreground = '#FFFFFF'
            )
            self.deadline_button.place(x = 10, y = 45)

            self.deadline_row = tk.Entry(
                self.middle_frame,
                font = ("Open Sans", "12", "bold"),
                width = 14,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FF0000"
            )
            self.deadline_row.place(x = 160, y = 48)
        
        if self.title == 'Remark' or self.title == 'Remark View':
            self.date_button = tk.Button(
                self.middle_frame,
                text = "Choose Date",
                font = ('Arial', '10', 'bold'),
                width = 16,
                command = self.choose_date,
                background = '#464646',
                foreground = '#FFFFFF'
            )
            self.date_button.place(x = 15, y = 25)
    
            self.date_row = tk.Entry(
                self.middle_frame,
                font = ("Open Sans", "12", "bold"),
                width = 14,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#E100B1"
            )
            self.date_row.place(x = 160, y = 28)

        else:
            self.date_button = tk.Button(
                self.middle_frame,
                text = "Choose Date",
                font = ('Arial', '10', 'bold'),
                width = 16,
                command = self.choose_date,
                background = '#464646',
                foreground = '#FFFFFF'
            )
            self.date_button.place(x = 10, y = 5)
    
            self.date_row = tk.Entry(
                self.middle_frame,
                font = ("Open Sans", "12", "bold"),
                width = 14,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
            )
            self.date_row.place(x = 160, y = 8)

            self.deadline_button = tk.Button(
                self.middle_frame,
                text = "Choose Deadline",
                font = ('Arial', '10', 'bold'),
                width = 16,
                command = self.choose_deadline,
                background = '#464646',
                foreground = '#FFFFFF'
            )
            self.deadline_button.place(x = 10, y = 45)

            self.deadline_row = tk.Entry(
                self.middle_frame,
                font = ("Open Sans", "12", "bold"),
                width = 14,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FF0000"
            )
            self.deadline_row.place(x = 160, y = 48)
        
        if self.title == 'Remark' or self.title == 'Remark View':
            self.save_remark_button = tk.Button(
                self.window,
                text = "SAVE",
                font = ('Arial', '10', 'bold'),
                width = 11,
                command = self.save_or_edit_remark,
                background = '#9E019A',
                foreground = '#FFFFFF'
            )
            self.save_remark_button.place(x = 480, y = 360)

        elif self.title == 'Event' or self.title == 'Event View':
            self.save_event_button = tk.Button(
                self.window,
                text = "SAVE",
                font = ('Arial', '10', 'bold'),
                width = 11,
                command = self.save_or_edit_event,
                background = '#A8A803',
                foreground = '#FFFFFF'
            )
            self.save_event_button.place(x = 480, y = 360)
        
        else:
            self.save_task_button = tk.Button(
                self.window,
                text = "SAVE",
                font = ('Arial', '10', 'bold'),
                width = 11,
                command = self.save_or_edit_task,
                background = '#004C01',
                foreground = '#FFFFFF'
            )
            self.save_task_button.place(x = 480, y = 360)

        self.exit_button = tk.Button(
            self.window,
            text = "EXIT",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.exit,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        self.exit_button.place(x = 370, y = 360)

        if self.title == 'Task' or self.title == 'Task View':
            self.bottom_frame = tk.Frame(
                self.window,
                width = 305,
                height = 65,
                background = "#2F3030"
            )
            self.bottom_frame.place(x = 15, y = 245)

            self.field3_label = tk.Label(
                self.bottom_frame,
                text = "Time",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.field3_label.place(x = 10, y = 5)

            self.field3_row = tk.Entry(
                self.bottom_frame,
                font = ("Open Sans", "10"),
                width = 20,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
            )
            self.field3_row.place(x = 150, y = 5)

            self.project_label = tk.Label(
                self.bottom_frame,
                text = "Project",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.project_label.place(x = 10, y = 35)

            self.project_row = tk.Entry(
                self.bottom_frame,
                font = ("Open Sans", "10"),
                width = 20,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
            )
            self.project_row.place(x = 150, y = 35)
        
        elif self.title == 'Event' or self.title == 'Event View':
            self.bottom_frame = tk.Frame(
                self.window,
                width = 305,
                height = 65,
                background = "#2F3030"
            )
            self.bottom_frame.place(x = 15, y = 265)

            self.field3_label = tk.Label(
                self.bottom_frame,
                text = "Start Time",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.field3_label.place(x = 10, y = 5)

            self.field3_row = tk.Entry(
                self.bottom_frame,
                font = ("Open Sans", "10"),
                width = 20,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
            )
            self.field3_row.place(x = 150, y = 5)

            self.field4_label = tk.Label(
                self.bottom_frame,
                text = "End Time",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.field4_label.place(x = 10, y = 35)

            self.field4_row = tk.Entry(
                self.bottom_frame,
                font = ("Open Sans", "10"),
                width = 20,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
            )
            self.field4_row.place(x = 150, y = 35)
        else:
            pass
        
        if self.title == 'Task' or self.title == 'Task View':
            self.very_bottom_frame = tk.Frame(
                self.window,
                width = 305,
                height = 65,
                background = "#2F3030"
            )
            self.very_bottom_frame.place(x = 15, y = 320)

            self.delegated_label = tk.Label(
                self.very_bottom_frame,
                text = "Delegate to",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.delegated_label.place(x = 10, y = 5)

            self.delegated_row = tk.Entry(
                self.very_bottom_frame,
                font = ("Open Sans", "10"),
                width = 20,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
            )
            self.delegated_row.place(x = 150, y = 5)

            self.cooperating_label = tk.Label(
                self.very_bottom_frame,
                text = "Cooperate with",
                font = ("Open Sans", "10", "bold"),
                background = "#2F3030",
                foreground = "#000000"
            )
            self.cooperating_label.place(x = 10, y = 35)

            self.cooperating_row = tk.Entry(
                self.very_bottom_frame,
                font = ("Open Sans", "10"),
                width = 20,
                insertbackground = "#FFFFFF",
                background = "#000000",
                foreground = "#FFFFFF"
            )
            self.cooperating_row.place(x = 150, y = 35)
        else:
            pass

    def insert_values(self):
        if self.title == 'Task View':
            win = self.window
            row1 = self.element_description_row 
            row2 = self.date_row
            row3 = self.deadline_row
            row4 = self.field2_row 
            row5 = self.field3_row
            row6 = self.project_row
            row7 = self.delegated_row 
            row8 = self.cooperating_row
            row9 = self.keywords_row

            day_data_manager.insert_values_to_task_form(
                self.element_id, win, row1, row2, row3, row4, row5, row6, row7, row8, row9
            )
            
        if self.title == 'Remark View':
            win = self.window
            row1 = self.element_description_row
            row2 = self.field1_row
            row3 = self.field2_row
            row4 = self.date_row

            day_data_manager.insert_values_to_remark_form(
                self.element_id, win, row1, row2, row3, row4
            )

        if self.title == 'Event View':
            win = self.window
            row1 = self.element_description_row
            row2 = self.field1_row
            row3 = self.field2_row
            row4 = self.date_row
            row5 = self.deadline_row
            row6 = self.field3_row
            row7 = self.field4_row

            day_data_manager.insert_values_to_event_form(
                self.element_id, win, row1, row2, row3, row4, row5, row6, row7
            )
        