import tkinter as tk
from tkinter import messagebox
import datetime
from DBManager import *
from DataStoreManager import *
from DataFormObject import *

db_manager = DBManager()
data_store_manager = DataStoreManager()
data = DataForm()



class element_window_small: # Ahoc Task, Idea
    # for new element use title as 'Adhoc Task', 'Idea'
    # for view existing element use title as 'Idea View'
    # for element_id use element_id or None
    def __init__(self, parent, title, element_id):

        self.window = tk.Toplevel(parent)
        self.window.geometry("600x240+100+200")
        self.window.configure(bg="#212121")
        self.window.title(title)

        if element_id == None:
            if title == 'Adhoc Task':
                element_id = db_manager.generate_element_id('AD')
            elif title ==  'Idea':
                element_id = db_manager.generate_element_id('ID')
        else:
            pass
        
        current_date = datetime.datetime.now()
        date_string = current_date.strftime("%d/%m/%Y")

        self.date_string = date_string
        self.element_id = element_id
        self.title = title

    def insert_values(self):
        if self.title == 'Idea View':
            win = self.window
            row1 = self.element_description_row 
            row2 = self.field1_row 
            row3 = self.field2_row

            data_store_manager.insert_values_to_idea_form(
                self.element_id, win, row1, row2, row3
            )

    def get_task_data(self):
        data.element_id = self.element_id
        data.element = self.element_description_row.get()
        data.date = self.date_string
        data.deadline = self.date_string
        data.field2 = self.field2_row.get()
        data.field3 = self.field3_row.get()
        data.project = self.project_row.get()
        data.keywords = self.keywords_row.get()
        data.category = 'task'

    def get_idea_data(self):
        data.element_id = self.element_id
        data.element = self.element_description_row.get()
        data.date = self.date_string
        data.field1 = self.field1_row.get()
        data.field2 = self.field2_row.get()
        data.category = 'idea'      

    def save_or_edit_task(self):
        try:
            self.get_task_data()
            db_manager.save_to_db(data)

            if len(self.project_row.get()) != 0:
                project_name = self.project_row.get()
                if not db_manager.project_name_already_exist(project_name):
                    data.element_id = db_manager.generate_element_id('PR')
                    data.element = self.project_row.get()
                    data.date = self.date_string
                    data.deadline = self.date_string
                    data.keywords = self.keywords_row.get()
                    data.category = 'project'
                    data.done = 'No'

                    db_manager.save_to_db(data)
            else:
                pass
            data_store_manager.make_day_data_tuple()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
            self.window.destroy()

    def save_or_edit_idea(self):
        try:
            self.get_idea_data()    
            if db_manager.element_id_already_exists(self.element_id):
                db_manager.update_db_fields(data)
            else:
                db_manager.save_to_db(data)
            data_store_manager.make_day_data_tuple()
            data_store_manager.make_list_data_tuple()
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

        self.element_id_label = tk.Label(
            self.window,
            text = self.element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.element_id_label.place(x = 480, y = 5)

        self.top_frame = tk.Frame(
            self.window,
            width = 570,
            height = 100,
            background = "#2F3030"
        )
        self.top_frame.place(x = 15, y = 40)

        self.element_description_label = tk.Label(
            self.top_frame,
            text = "Element Name",
            font = ("Open Sans", "10", "bold"),
            background = "#2F3030",
            foreground = "#000000"
        )
        self.element_description_label.place(x = 10, y = 5)

        self.element_description_row = tk.Entry(
            self.top_frame,
            font = ("Open Sans", "10", "bold"),
            width = 56,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        self.element_description_row.place(x = 150, y = 5)

        if self.title == 'Adhoc Task':
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

        else:
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

            self.field2_label = tk.Label(
                self.top_frame,
                text = "Field2",
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

        if self.title == 'Adhoc Task':
            self.bottom_frame = tk.Frame(
                self.window,
                width = 305,
                height = 65,
                background = "#2F3030"
            )
            self.bottom_frame.place(x = 15, y = 160)

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
                text = "Assign to Project",
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
        else:
            pass

        self.date_label = tk.Label(
            self.window,
            text = self.date_string,
            font = ('Montserrat', '15'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.date_label.place(x = 480, y = 160)

        if self.title == 'Adhoc Task':
            self.save_button = tk.Button(
                self.window,
                text = "SAVE",
                font = ('Arial', '10', 'bold'),
                width = 11,
                command = self.save_or_edit_task,
                background = '#A94102',
                foreground = '#FFFFFF'
            )
            self.save_button.place(x = 490, y = 200)
        else:
            self.save_button = tk.Button(
                self.window,
                text = "SAVE",
                font = ('Arial', '10', 'bold'),
                width = 11,
                command = self.save_or_edit_idea,
                background = '#4F0082',
                foreground = '#FFFFFF'
            )
            self.save_button.place(x = 490, y = 200)

        self.exit_button = tk.Button(
            self.window,
            text = "EXIT",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.exit,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        self.exit_button.place(x = 380, y = 200)
        
