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
data = DataForm()

class NotificationWindow:

    def __init__(self, parent, user_id):
        self.user_id = user_id
        self.db_manager = DBManager(self.user_id)
        self.data_store_manager = DataStoreManager(self.user_id)

        self.window = tk.Toplevel(parent)
        self.window.geometry('800x600+100+50')
        self.window.title('NOTIFICATIONS')
        self.window.option_add('*Dialog.msg.title.bg', '#000000')
        self.window.configure(bg = "#AFAFAF")
        self.window.resizable(0,0)

    def show_total_number_of_undone_elements(self, category, frame, XX, YY):
        number_elements = self.data_store_manager.count_number_undone_elements(category, frame, XX, YY)
        number_elements_label = tk.Label(
            frame,
            text = f"{number_elements} ",
            font = ('Arial', '12', 'bold'),
            background = "#2D4A54",
            foreground = "#06CA00"
        )
        number_elements_label.place(x = XX, y = YY)
        
        if number_elements != 0:
            number_elements_label.configure(foreground="#FF0018")

    def show_total_number_of_closing_deadlines(self, frame, XX, YY):
        number_elements = self.data_store_manager.count_closing_deadlines(frame, XX, YY)
        number_elements_label = tk.Label(
            frame,
            text = f"{number_elements} ",
            font = ('Arial', '12', 'bold'),
            background = "#2D4A54",
            foreground = "#06CA00"
        )
        number_elements_label.place(x = XX, y = YY)

        if number_elements != 0:
            number_elements_label.configure(foreground="#FF0018")
    
    def show_number_of_pending_ideas(self, frame, XX, YY):
        number_elements = self.data_store_manager.count_pending_ideas(frame, XX, YY)
        number_elements_label = tk.Label(
            frame,
            text = f"{number_elements} ",
            font = ('Arial', '12', 'bold'),
            background = "#2D4A54",
            foreground = "#06CA00"
        )
        number_elements_label.place(x = XX, y = YY)

        if number_elements != 0:
            number_elements_label.configure(foreground="#FF0018")

    def show_undone_tasks_in_treeview(self):
        self.data_store_manager.insert_data_to_notifications_treeview(self.treeview, 'tasks')
        self.treeview_label.configure(text='MY TASKS UNDONE: ')

    def show_undone_delegated_tasks_in_treeview(self):
        self.data_store_manager.insert_data_to_notifications_treeview(self.treeview, 'delegated tasks')
        self.treeview_label.configure(text='DELEGATED TASKS UNDONE: ')

    def show_undone_projects_in_treeview(self):
        self.data_store_manager.insert_data_to_notifications_treeview(self.treeview, 'projects')
        self.treeview_label.configure(text='PROJECTS UNDONE: ')

    def show_closing_deadlines_in_treeview(self):
        self.data_store_manager.insert_data_to_notifications_treeview(self.treeview, 'closing deadlines')
        self.treeview_label.configure(text='CLOSING DEADLINES: ')
    
    def show_pending_ideas_in_treeview(self):
        self.data_store_manager.insert_data_to_notifications_treeview(self.treeview, 'pending ideas')
        self.treeview_label.configure(text = 'PENDING IDEAS: ')

    def show_existing_element_window(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
            data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)
            if data_row[15] == 'task':
                title = 'Task View'
                element_window = element_window_extended(
                    self.window, title, element_id
                )
                element_window.create_window()
                element_window.insert_values()

            elif data_row[15] == 'project':
                project_window = ProjectWindow(
                    self.window, element_id
                )
                project_window.create_window()
                project_window.insert_values()

            elif data_row[15] == 'idea':
                title = 'Idea View'      
                idea_window = element_window_small(
                self.window, title, element_id
                )
                idea_window.create_window()
                idea_window.insert_values()
            else:
                pass
    
    def show_element_window_on_double_click(self, event):
        self.show_existing_element_window()

    def show_existing_personal_card(self):
        selection =  self.birthday_treeview.selection()
        if selection:
            element_id = self.birthday_treeview.item(selection, 'values')[0]
            personal_card_window = PersonalCardWindow(
                self.window, element_id
            )
            personal_card_window.create_window()
            personal_card_window.insert_values()
        else:
            messagebox.showwarning("Error", "Select an element")
    
    def show_personal_card_on_double_click(self, event):
        self.show_existing_personal_card()

    def delete_from_database(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
            data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)
            category = data_row[15]
            delegated = data_row[9]
            if category == 'task' and delegated == "":
                str_category = 'tasks'
            elif category == 'task' and delegated != "":
                str_category = 'delegated tasks'
            elif category == 'project':
                str_category = 'projects'
            self.db_manager.set_element_id(element_id)
            answer = messagebox.askyesno("DELETE", "DELETE from database?")
            if answer:
                self.db_manager.delete_from_db()
                if category == 'project':
                    element_name = self.treeview.item(selection, 'values')[1]
                    rows = self.data_store_manager.get_all_project_tasks_id_from_list_data_tuple(element_name)
                    if rows is not None:
                        for row in rows:
                            self.db_manager.set_element_id(row)
                            messagebox.showwarning("DELETE ASSOCIATED", f"Asscociated task {row} is to be deleted.")
                            self.db_manager.delete_from_db()

                self.data_store_manager.make_list_data_tuple()
                self.data_store_manager.insert_data_to_notifications_treeview(self.treeview, str_category)
                self.show_total_number_of_undone_elements('tasks', self.left_frame, 160, 112)
                self.show_total_number_of_undone_elements('delegated tasks', self.left_frame, 160, 152)
                self.show_total_number_of_undone_elements('projects', self.left_frame, 160, 192)
                self.show_total_number_of_closing_deadlines(self.left_frame, 160, 332)
                self.show_number_of_pending_ideas(self.left_frame, 160, 472)
            else:
                pass
        else:
            messagebox.showwarning("ERROR", "Select an element")

    def exit(self):
        self.window.destroy()

    def create_window(self):
        top_frame = tk.Frame(
            self.window,
            width = 800,
            height = 130,
            background = "#D9D0AF"
        )
        top_frame.place(x = 15, y = 0)

        header_label = tk.Label(
            top_frame,
            text = "NOTIFICATIONS",
            font = ('Montserrat', '25', 'bold'),
            background = "#D9D0AF",
            foreground = "#2D4A54"
        )
        header_label.place(x = 240, y = 45)

        self.left_frame = tk.Frame(
            self.window,
            width = 200,
            height = 585,
            background = "#2D4A54"
        )
        self.left_frame.place(x = 30, y = 0)

        undone_elements_label1 = tk.Label(
            self.left_frame,
            text = "UNDONE",
            font = ('Montserrat', '15'),
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        undone_elements_label1.place(x = 10, y = 30)

        undone_elements_label2 = tk.Label(
            self.left_frame,
            text = "ELEMENTS",
            font = ('Montserrat', '15'),
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        undone_elements_label2.place(x = 55, y = 55)

        my_tasks_button = tk.Button(
            self.left_frame,
            text = "MY TASKS",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.show_undone_tasks_in_treeview,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        my_tasks_button.place(x=15, y=110)

        delegated_tasks_button = tk.Button(
            self.left_frame,
            text = "DELEGATED TASKS",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.show_undone_delegated_tasks_in_treeview,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        delegated_tasks_button.place(x=15, y=150)

        projects_button = tk.Button(
            self.left_frame,
            text = "PROJECTS",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.show_undone_projects_in_treeview,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        projects_button.place(x=15, y=190)

        closing_deadlines_label1 = tk.Label(
            self.left_frame,
            text = "CLOSING",
            font = ('Montserrat', '15'),
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        closing_deadlines_label1.place(x = 10, y = 250)

        closing_deadlines_label2 = tk.Label(
            self.left_frame,
            text = "DEADLINES",
            font = ('Montserrat', '15'),
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        closing_deadlines_label2.place(x = 55, y = 275)

        closing_deadlines_button = tk.Button(
            self.left_frame,
            text = "DEADLINES",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.show_closing_deadlines_in_treeview,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        closing_deadlines_button.place(x=15, y=330)

        pending_ideas_label1 = tk.Label(
            self.left_frame,
            text = "PENDING",
            font = ('Montserrat', '15'),
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        pending_ideas_label1.place(x = 10, y = 390)

        pending_ideas_label2 = tk.Label(
            self.left_frame,
            text = "IDEAS",
            font = ('Montserrat', '15'),
            background = "#2D4A54",
            foreground = "#FFFFFF"
        )
        pending_ideas_label2.place(x = 55, y = 415)

        pending_ideas_button = tk.Button(
            self.left_frame,
            text = "IDEAS",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.show_pending_ideas_in_treeview,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        pending_ideas_button.place(x=15, y=470)

        self.treeview_label = tk.Label(
            self.window,
            text = "MY TASKS UNDONE: ",
            font = ('Montserrat', '12', 'bold'),
            background = "#AFAFAF",
            foreground = "#2D4A54"
        )
        self.treeview_label.place(x = 250, y = 150)


        self.treeview = ttk.Treeview(
            self.window, 
            columns=('#1', '#2', '#3', '#4'),
            height = 6
        )

        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=0, stretch = False)
        self.treeview.heading('#1', text='Element ID')
        self.treeview.column('#1', width=0, stretch = False)
        self.treeview.heading('#2', text='Element')
        self.treeview.column('#2', width=180)
        self.treeview.heading('#3', text='Deadline')
        self.treeview.column('#3', width=80)
        self.treeview.heading('#4', text='Delegated')
        self.treeview.column('#4', width=150)

        self.treeview.place (x = 250, y = 175)
        self.treeview.bind("<Double-1>", self. show_element_window_on_double_click)

        view_button = tk.Button(
            self.window,
            text = "VIEW",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.show_existing_element_window,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        view_button.place(x=680, y=205)

        delete_button = tk.Button(
            self.window,
            text = "DELETE",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.delete_from_database,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        delete_button.place(x=680, y=245)

        birthday_treeview_label = tk.Label(
            self.window,
            text = "BIRTHDAYS AND CLOSING BIRTHDAYS: ",
            font = ('Montserrat', '12', 'bold'),
            background = "#AFAFAF",
            foreground = "#2D4A54"
        )
        birthday_treeview_label.place(x = 250, y = 350)

        self.birthday_treeview = ttk.Treeview(
            self.window, 
            columns=('#1', '#2', '#3', '#4'),
            height = 5
        )

        self.birthday_treeview.heading('#0', text='ID')
        self.birthday_treeview.column('#0', width=0, stretch = False)
        self.birthday_treeview.heading('#1', text='Element ID')
        self.birthday_treeview.column('#1', width=0, stretch = False)
        self.birthday_treeview.heading('#2', text='Name')
        self.birthday_treeview.column('#2', width=180)
        self.birthday_treeview.heading('#3', text='Date of Birth')
        self.birthday_treeview.column('#3', width=80)
        self.birthday_treeview.heading('#4', text='Year of Birth')
        self.birthday_treeview.column('#4', width=150)

        self.birthday_treeview.place (x = 250, y = 375)
        self.birthday_treeview.bind("<Double-1>", self.show_personal_card_on_double_click)

        view_birthday_button = tk.Button(
            self.window,
            text = "VIEW",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.show_existing_personal_card,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        view_birthday_button.place(x=680, y=425)

        exit_button = tk.Button(
            self.window,
            text = "EXIT",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.exit,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        exit_button.place(x = 690, y = 560)

        self.show_total_number_of_undone_elements('tasks', self.left_frame, 160, 112)
        self.show_total_number_of_undone_elements('delegated tasks', self.left_frame, 160, 152)
        self.show_total_number_of_undone_elements('projects', self.left_frame, 160, 192)
        self.show_total_number_of_closing_deadlines(self.left_frame, 160, 332)
        self.show_number_of_pending_ideas(self.left_frame, 160, 472)
        self.data_store_manager.insert_data_to_notifications_treeview(self.treeview, 'tasks')
        self.data_store_manager.insert_data_to_notifications_treeview(self.birthday_treeview, 'birthdays')

