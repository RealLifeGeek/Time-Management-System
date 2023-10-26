import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox
from functions import generate_element_id, project_name_already_exist, element_id_already_exists
from functions import insert_values_to_task_form, insert_values_to_event_form, insert_values_to_remark_form
from DBManager import *

chosen_date = None
chosen_deadline = None
element_id = None
db_manager = DBManager()

class element_window_extended: # task, remark, event
# for new element use title as 'Task', 'Remark', 'Event'
# for view existing element use title as 'Task View', 'Remark View' or 'Event View'
# for element_id use element_id or None
    def __init__(self, parent, title, db, element_id):
        global chosen_date
        global chosen_deadline

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

        chosen_date = self.calendar.get_date()
        self.element_id = element_id
        self.title = title
        self.db = db
        
    def choose_date(self):
        global chosen_date
        
        if self.title == 'Event' or self.title == 'Event View':
            bg = "#A8A803"
        elif self.title == 'Remark' or self.title == 'Remark View':
            bg = "#9E019A"
        else:
            bg = "#2F3030"
        
        chosen_date = self.calendar.get_date()
        self.chosen_date_label = tk.Label(
            self.middle_frame,
            text = chosen_date,
            font = ('Montserrat', '12'),
            background = bg,
            foreground = "#FFFFFF"
        )
        if self.title == 'Remark' or self.title == 'Remark View':
            self.chosen_date_label.place(x = 180, y = 25)
        else:
            self.chosen_date_label.place(x = 180, y = 5)

    def choose_deadline(self):
        global chosen_deadline

        chosen_deadline = self.calendar.get_date()
        self.chosen_deadline_label = tk.Label(
            self.middle_frame,
            text = chosen_deadline,
            font = ('Montserrat', '12', 'bold'),
            background = '#970000',
            foreground = "#FFFFFF"
        )
        self.chosen_deadline_label.place(x = 180, y = 45)

    def save_or_edit_task(self):
        global chosen_date
        global chosen_deadline

        if chosen_date != None or chosen_deadline != None:
            if chosen_date == None and chosen_deadline != None:
                chosen_date = chosen_deadline
            elif chosen_date != None and chosen_deadline == None:
                chosen_deadline = chosen_date
        else:
            pass
    
        answer = messagebox.askokcancel("SAVE", "SAVE changes?")
        if answer:
            try:
                element = self.element_description_row.get()
                date = chosen_date
                deadline = chosen_deadline
                field1 = ''
                field2 = self.field2_row.get()
                field3 = self.field3_row.get()
                project = self.project_row.get()
                delegated = self.delegated_row.get()
                cooperating = self.cooperating_row.get()
                field4 = ''
                field5 = ''
                remarks = ''
                keywords = self.keywords_row.get()
                category = 'task'
                done = 'No'

                if element_id_already_exists(self.db, self.element_id):
                    db_manager.update_db_fields(self.element_id, element, date, deadline, field1, field2, field3, project, delegated,
                                                cooperating, field4, field5, remarks, keywords, category, done)
                else:
                    db_manager.save_to_db(self.element_id, element, date, deadline, field1, field2, field3, project, delegated,
                                     cooperating, field4, field5, remarks, keywords, category, done)

                if len(self.project_row.get()) != 0:
                    project_name = self.project_row.get()
                    if not project_name_already_exist(self.db, project_name):
                        element_id = generate_element_id(self.db, 'PR')
                        element = project
                        date = chosen_date
                        deadline = chosen_deadline
                        field1 = ''
                        field2 = ''
                        field3 = ''
                        project = ''
                        delegated = self.delegated_row.get()
                        cooperating = self.cooperating_row.get()
                        field4 = ''
                        field5 = ''
                        remarks = ''
                        keywords = self.keywords_row.get()
                        category = 'project'
                        done = 'No'

                        db_manager.save_to_db(element_id, element, date, deadline, field1, field2, field3, project, delegated, 
                                                cooperating, field4, field5, remarks, keywords, category, done)
                else:
                    pass
                self.window.destroy()
            except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")
                self.window.destroy()
        else:
            pass

    def save_or_edit_event(self):
        global chosen_date
        global chosen_deadline

        answer = messagebox.askokcancel("SAVE", "SAVE changes?")
        if answer:
            try:
                element = self.element_description_row.get()
                date = chosen_date
                deadline = chosen_deadline
                field1 = self.field1_row.get()
                field2 = self.field2_row.get()
                field3 = self.field3_row.get()
                project = ''
                delegated = ''
                cooperating = ''
                field4 = self.field4_row.get()
                field5 = ''
                remarks = ''
                keywords = ''
                category = 'event'
                done = 'No'

                if element_id_already_exists(self.db, self.element_id):
                    db_manager.update_db_fields(self.db, self.element_id, element, date, deadline, field1, field2, field3, project, delegated,
                                                cooperating, field4, field5, remarks, keywords, category, done)
                else:
                    db_manager.save_to_db(self.db, self.element_id, element, date, deadline, field1, field2, field3, project, delegated,
                                            cooperating, field4, field5, remarks, keywords, category, done)
                self.window.destroy()
            except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")
                self.window.destroy()
    
    def save_or_edit_remark(self):
        global chosen_date

        answer = messagebox.askyesno("SAVE", "SAVE changes?")
        if answer:
            try:
                element = self.element_description_row.get()
                date = chosen_date
                deadline = None
                field1 = self.field1_row.get()
                field2 = self.field2_row.get()
                field3 = ''
                project = ''
                delegated = ''
                cooperating = ''
                field4 = ''
                field5 = ''
                remarks = ''
                keywords = ''
                category = 'remark'
                done = 'No'

                if element_id_already_exists(self.db, self.element_id):
                    db_manager.update_db_fields(self.db, self.element_id, element, date, deadline, field1, field2, field3, project, delegated,
                                                cooperating, field4, field5, remarks, keywords, category, done)
                else:
                    db_manager.save_to_db(self.db, self.element_id, element, date, deadline, field1, field2, field3, project, delegated,
                                            cooperating, field4, field5, remarks, keywords, category, done)
                self.window.destroy()
            except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")
                self.window.destroy()

    def exit(self):
        self.window.destroy()

    def create_window(self):
        global chosen_date
        global chosen_deadline

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
            frame = self.middle_frame 
            row1 = self.element_description_row 
            row2 = self.field2_row 
            row3 = self.field3_row
            row4 = self.project_row
            row5 = self.delegated_row 
            row6 = self.cooperating_row
            row7 = self.keywords_row

            insert_values_to_task_form(
                self.db, self.element_id, win, frame, row1, row2, row3, row4, row5, row6, row7
            )
            
        if self.title == 'Remark View':
            win = self.window
            frame = self.middle_frame
            row1 = self.element_description_row
            row2 = self.field1_row
            row3 = self.field2_row

            insert_values_to_remark_form(
                self.db, self.element_id, win, frame, row1, row2, row3
            )

        if self.title == 'Event View':
            win = self.window
            frame = self.middle_frame
            row1 = self.element_description_row
            row2 = self.field1_row
            row3 = self.field2_row
            row4 = self.field3_row
            row5 = self.field4_row

            insert_values_to_event_form(
                self.db, self.element_id, win, frame, row1, row2, row3, row4, row5
            )
        