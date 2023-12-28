import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from functions import exit_window
from DBManager import *
from DataFormObject import *
from DataStoreManager import *
from element_window_extended import *
from element_window_small import *
from ProjectWindow import *
from PersonalCardWindow import *

current_date = datetime.now()
date_string = current_date.strftime("%d/%m/%Y")
tomorrow = datetime.today() + timedelta(days=1)
tomorrow_date = tomorrow.strftime('%d/%m/%Y')
timestamp = current_date.strftime("%d/%m/%Y-%H:%M:%S")
data = DataForm()

class ListWindow:
    def __init__(self, parent, title, user_id):
        self.user_id = user_id
        self.db_manager = DBManager(self.user_id)
        self.data_store_manager = DataStoreManager(self.user_id)

        self.window = tk.Toplevel(parent)
        self.window.geometry("800x550+100+100")
        self.window.configure(bg="#AFAFAF")
        self.window.title(title)
        self.window.resizable(0,0)

        self.title = title
        
        style = ttk.Style()
        style.theme_use('clam')

    def show_existing_element_window(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
        else:
            messagebox.showwarning("ERROR", f"Select an element")

        if self.title == 'Ideas':
            new_title = 'Idea View'
            idea_window = element_window_small(
                self.window, new_title, element_id, self.user_id
            )
            idea_window.create_window()
            idea_window.insert_values()

        elif self.title == 'Projects':
            project_window = ProjectWindow(
                self.window, element_id, self.user_id
            )
            project_window.create_window()
            project_window.insert_values()

        elif self.title == 'Personal Cards':
            personal_card_window = PersonalCardWindow(
                self.window, element_id, self.user_id
            )
            personal_card_window.create_window()
            personal_card_window.insert_values()

        else:
            if self.title == 'My Tasks' or self.title == 'Delegated Tasks':
                new_title = 'Task View'
            elif self.title == 'Remarks':
                new_title = 'Remark View'
            elif self.title == 'Events':
                new_title = 'Event View'
            elif self.title == 'Maybe/Sometimes':
                new_title = 'Maybe/Sometimes View'
                new_title == 'Task View' 
            else:
                pass
            element_window = element_window_extended(
                self.window, new_title, element_id, self.user_id
            )
            element_window.create_window()
            element_window.insert_values()

    def show_element_window_on_double_click(self, event):
        self.show_existing_element_window()

    def show_new_element_window(self):
        if self.title == 'My Tasks' or self.title == 'Delegated Tasks':
            task_window = element_window_extended(
            self.window, 'Task', None, self.user_id
            )
            task_window.create_window()
        elif self.title == 'Remarks':
            remark_window = element_window_extended(
                self.window, "Remark", None, self.user_id
            )
            remark_window.create_window()
        elif self.title == 'Events':
            event_window = element_window_extended(
                self.window, 'Event', None, self.user_id
            )
            event_window.create_window()
        elif self.title == 'Projects':
            project_window = ProjectWindow(
                self.window, None, self.user_id
            )
            project_window.create_window()
        elif self.title == 'Personal Cards':
            personal_card_window = PersonalCardWindow(
                self.window, None, self.user_id
            )
            personal_card_window.create_window()
            personal_card_window.name_row.insert(0, 'FIRST AND LAST NAME')
            personal_card_window.title_before_row.insert(0, 'Title before name')
            personal_card_window.title_after_row.insert(0, 'Title after name')
            personal_card_window.day_month_row.insert(0, 'dd/mm')
            personal_card_window.year_date_row.insert(0, 'yyyy')
            personal_card_window.company_row.insert(0, 'Company name')
            personal_card_window.field1_row.insert(0, 'Field 1')
            personal_card_window.field2_row.insert(0, 'Field 2')
            personal_card_window.field3_row.insert(0, 'Field 3')
            personal_card_window.email_row.insert(0, 'email_adress@default.com')
            personal_card_window.phone_number_row.insert(0, 'Phone number')


        elif self.title == 'Ideas':
            idea_window = element_window_small(
            self.window, 'Idea', None, self.user_id
            )
            idea_window.create_window()
        else:
            print('Not matched in def show_new_elemenet_window in ListWindow')

    def done(self):
        current_date = datetime.now()
        timestamp = current_date.strftime("%d/%m/%Y-%H:%M:%S")
        
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]        
            data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)

            data.element_id = element_id
            data.element = data_row[2]
            data.date = data_row[3]
            data.deadline = ""
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
            data.timestamp_created = data_row[17]
            data.timestamp_finished = timestamp

            self.db_manager.update_db_fields(data)
            self.data_store_manager.make_list_data_tuple()
            self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title)
        else:
            messagebox.showwarning("Error", "Select an element to be done.")
    
    def delete_from_database(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
            #self.db_manager.set_element_id(element_id)
            answer = messagebox.askyesno("DELETE", "DELETE from database?")
            if answer:
                current_date = datetime.now()
                timestamp = current_date.strftime("%d/%m/%Y-%H:%M:%S")
                data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)

                data.element_id = element_id
                data.element = data_row[2]
                data.date = data_row[3]
                data.deadline = ""
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
                data.done = 'DELETED'
                data.timestamp_created = data_row[17]
                data.timestamp_finished = timestamp

                self.db_manager.update_db_fields(data)
                messagebox.showinfo("DELETED", f"Element {data_row[2]} deleted")
                #self.db_manager.delete_from_db()
                if self.title == 'Projects':
                    element_name = self.treeview.item(selection, 'values')[1]
                    rows = self.data_store_manager.get_all_project_tasks_id_from_list_data_tuple(element_name)
                    if rows is not None:
                        for row in rows:
                            data_row = self.data_store_manager.get_data_row_from_list_data_tuple(row)

                            data.element_id = row
                            data.element = data_row[2]
                            data.date = data_row[3]
                            data.deadline = ""
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
                            data.done = 'DELETED'
                            data.timestamp_created = data_row[17]
                            data.timestamp_finished = timestamp
                            #self.db_manager.set_element_id(row)
                            self.db_manager.update_db_fields(data)
                            messagebox.showinfo("DELETE ASSOCIATED", f"Asscociated task {row} deleted.")
                            #self.db_manager.delete_from_db()
                    else:
                        print('No related tasks to the project: ' + element_name)
                
                self.data_store_manager.make_list_data_tuple()
                self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title)
                    
                
            else:
                pass
        else:
            messagebox.showwarning("ERROR", "Select an element")
    
    def find(self):
        if len(self.find_row.get()) != 0:
            searched_item = self.find_row.get()          
            self.data_store_manager.find_element_in_list_tuple(self.treeview, searched_item, self.title)
        else:
            messagebox.showwarning("ERROR", "Find Field is Empty!")
    
    def find_on_enter_click(self, event):
        self.find()
    
    def cancel_find(self):
        self.find_row.delete(0, 'end')
        self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )

    def change_to_task(self):
        try:
            if self.title == 'My Tasks' or self.title == 'Delegated Tasks':
                messagebox.showwarning("ERROR", "Element is aleready task.")
            else:
                selection = self.treeview.selection()
                if selection:
                    element_id = self.treeview.item(selection, 'values')[0]
                    data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)

                    data.element_id = element_id
                    data.element = data_row[2]
                    data.date = data_row[3]  or data_row[4]
                    data.deadline = data_row[4] or data_row[3]
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
                    data.category = 'task'
                    data.done = 'No'
                    data.timestamp_created = data_row[17]
                    data.timestamp_finished = ''

                    self.db_manager.update_db_fields(data)
                    self.data_store_manager.make_list_data_tuple()
                    self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )
                else:
                    messagebox.showwarning("ERROR", "Select an element.")
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 600: {e}")

    def change_to_remark(self):
        try:
            if self.title == 'Remarks':
                messagebox.showwarning("ERROR", "Element is aleready a remark.")
            else:
                selection = self.treeview.selection()
                if selection:
                    element_id = self.treeview.item(selection, 'values')[0]
                    data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)
                
                    data.element_id = element_id
                    data.element = data_row[2]
                    data.date = data_row[3]
                    data.deadline = ""
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
                    data.category = 'remark'
                    data.done = 'No'
                    data.timestamp_created = data_row[17]
                    data.timestamp_finished = ''

                    self.db_manager.update_db_fields(data)
                    self.data_store_manager.make_list_data_tuple()
                    self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )
                else:
                    messagebox.showwarning("ERROR", "Select an element.")
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 601: {e}")

    def change_to_event(self):
        try:
            if self.title == 'Events':
                messagebox.showwarning("ERROR", "Element is aleready an event.")
            else:
                selection = self.treeview.selection()
                if selection:
                    element_id = self.treeview.item(selection, 'values')[0]
                    data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)
                
                    data.element_id = element_id
                    data.element = data_row[2]
                    data.date = data_row[3] or data_row[4]
                    data.deadline = data_row[4] or data_row[3]
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
                    data.category = 'event'
                    data.done = 'No'
                    data.timestamp_created = data_row[17]
                    data.timestamp_finished = ''

                    self.db_manager.update_db_fields(data)
                    self.data_store_manager.make_list_data_tuple()
                    self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )
                else:
                    messagebox.showwarning("ERROR", "Select an element.")
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 602: {e}")

    def change_to_idea(self):
        try:
            if self.title == 'Ideas':
                messagebox.showwarning("ERROR", "Element is aleready an idea.")
            else:
                selection = self.treeview.selection()
                if selection:
                    element_id = self.treeview.item(selection, 'values')[0]
                    data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)
                
                    data.element_id = element_id
                    data.element = data_row[2]
                    data.date = data_row[3]
                    data.deadline = ""
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
                    data.category = 'idea'
                    data.done = 'No'
                    data.timestamp_created = data_row[17]
                    data.timestamp_finished = ''

                    self.db_manager.update_db_fields(data)
                    self.data_store_manager.make_list_data_tuple()
                    self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )
                else:
                    messagebox.showwarning("ERROR", "Select an element.")
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 603: {e}")

    def change_to_maybe_sometimes(self):
        try:
            if self.title == 'Maybe/Sometimes':
                messagebox.showwarning("ERROR", "Element is aleready an idea.")
            else:
                selection = self.treeview.selection()
                if selection:
                    element_id = self.treeview.item(selection, 'values')[0]
                    data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)
                
                    data.element_id = element_id
                    data.element = data_row[2]
                    data.date = ""
                    data.deadline = ""
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
                    data.category = 'maybe/sometimes'
                    data.done = 'No'
                    data.timestamp_created = data_row[17]
                    data.timestamp_finished = ''

                    self.db_manager.update_db_fields(data)
                    self.data_store_manager.make_list_data_tuple()
                    self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )
                else:
                    messagebox.showwarning("ERROR", "Select an element.")
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 604: {e}")

    def change_to_project(self):
        try:
            if self.title == 'Projects':
                messagebox.showwarning("ERROR", "Element is aleready an idea.")
            else:
                selection = self.treeview.selection()
                if selection:
                    element_id = self.treeview.item(selection, 'values')[0]
                    data_row = self.data_store_manager.get_data_row_from_list_data_tuple(element_id)
                
                    data.element_id = element_id
                    data.element = data_row[2]
                    data.date = data_row[3] or data_row[4]
                    data.deadline = data_row[4] or data_row[3]
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
                    data.category = 'project'
                    data.done = 'No'
                    data.timestamp_created = data_row[17]
                    data.timestamp_finished = ''

                    self.db_manager.update_db_fields(data)
                    self.data_store_manager.make_list_data_tuple()
                    self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )
                else:
                    messagebox.showwarning("ERROR", "Select an element.")
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR 605: {e}")                
                  

    def create_window(self):
        self.header_label = tk.Label(
            self.window,
            text = self.title,
            font = ('Montserrat', '22', 'bold'),
            background = "#AFAFAF",
            foreground = "#000000"
        )
        self.header_label.place(relx = 0.5, y = 30, anchor = 'center')

        if self.title == 'My Tasks' or self.title == 'Delegated Tasks' or self.title == 'Projects':
            self.treeview = ttk.Treeview(self.window, columns=('#1', '#2', '#3', '#4', '#5'), height = 13)

            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Element ID')
            self.treeview.column('#1', width=0, stretch = False)
            self.treeview.heading('#2', text='Element Name')
            self.treeview.column('#2', width=210)
            self.treeview.heading('#3', text = 'Date')
            self.treeview.column('#3', width=120)
            self.treeview.heading('#4', text = 'Deadline')
            self.treeview.column('#4', width=120)
            self.treeview.heading('#5', text = 'Delegated')
            self.treeview.column('#5', width=150)
            
            self.treeview.place (x = 15, y = 75)

        elif self.title == 'Personal Cards':
            self.window.geometry('800x450+100+100')

            self.treeview = ttk.Treeview(self.window, columns=('#1', '#2', '#3', '#4', '#5'), height = 13)

            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Element ID')
            self.treeview.column('#1', width=0, stretch = False)
            self.treeview.heading('#2', text='Title before')
            self.treeview.column('#2', width=120)
            self.treeview.heading('#3', text='Name')
            self.treeview.column('#3', width=210)
            self.treeview.heading('#4', text = 'Birthday')
            self.treeview.column('#4', width=150)
            self.treeview.heading('#5', text = 'Year of Birth')
            self.treeview.column('#5', width=120)

            self.treeview.place (x = 15, y = 75)
        
        elif self.title == 'Events':
            self.treeview = ttk.Treeview(self.window, columns=('#1', '#2', '#3', '#4', '#5'), height = 13)

            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Element ID')
            self.treeview.column('#1', width=0, stretch = False)
            self.treeview.heading('#2', text='Element ID')
            self.treeview.column('#2', width=150)
            self.treeview.heading('#3', text='Event')
            self.treeview.column('#3', width=210)
            self.treeview.heading('#4', text = 'Start Date')
            self.treeview.column('#4', width=120)
            self.treeview.heading('#5', text = 'End Date')
            self.treeview.column('#5', width=120)

            self.treeview.place (x = 15, y = 75)

        else: #self.title == 'Remarks' or self.title == 'Ideas' or self.title == 'Maybe/Sometimes'
            self.treeview = ttk.Treeview(self.window, columns=('#1', '#2', '#3', '#4', '#5'), height = 13)

            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Element ID')
            self.treeview.column('#1', width=0, stretch = False)
            self.treeview.heading('#2', text='Element ID')
            self.treeview.column('#2', width=150)
            self.treeview.heading('#3', text='Element Name')
            self.treeview.column('#3', width=210)
            self.treeview.heading('#4', text = 'Date')
            self.treeview.column('#4', width=120)
            self.treeview.heading('#5', text = 'Field 1')
            self.treeview.column('#5', width=120)            

            self.treeview.place (x = 15, y = 75)
        
        self.treeview.bind("<Double-1>", self.show_element_window_on_double_click)
        self.treeview.bind("<Return>", self.show_element_window_on_double_click)

        if self.title == 'Maybe/Sometimes':
            pass
        else:
            new_element_button = tk.Button(
                self.window,
                text = "+",
                font = ('Arial', '15', 'bold'),
                width = 3,
                command = self.show_new_element_window,
                background = '#029F00',
                foreground = '#FFFFFF'
            )
            new_element_button.place(x=740, y=10)

        if self.title == 'My Tasks' or self.title == 'Delegated Tasks':
            done_button = tk.Button(
                self.window,
                text = "DONE",
                font = ('Arial', '12', 'bold'),
                width = 15,
                command = self.done,
                background = '#046702',
                foreground = '#FFFFFF'
            )
            done_button.place(x=630, y=135)

        view_button = tk.Button(
            self.window,
            text = "VIEW",
            font = ('Arial', '12', 'bold'),
            width = 15,
            command = self.show_existing_element_window,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        view_button.place(x=630, y=185)

        delete_button = tk.Button(
            self.window,
            text = "DELETE",
            font = ('Arial', '12', 'bold'),
            width = 15,
            command = self.delete_from_database,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        delete_button.place(x=630, y=235)

        find_label = tk.Label(
            self.window,
            text = "Find:",
            font = ("Open Sans", "13", "bold"),
            background = "#AFAFAF",
            foreground = "#000000"       
        )
        find_label.place(x = 15, y = 380)

        self.find_row = tk.Entry(
            self.window,
            font = ("Open Sans", "11", "bold"),
            width = 30,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        self.find_row.place(x = 65, y = 382)
        self.find_row.bind("<Return>", self.find_on_enter_click)

        find_button = tk.Button(
            self.window,
            text = "FIND",
            font = ('Arial', '11', 'bold'),
            width = 10,
            command = self.find,
            background = '#4F0082',
            foreground = '#FFFFFF'
        )
        find_button.place(x = 320, y = 377)

        cancel_find_button = tk.Button(
            self.window,
            text = "CANCEL FIND",
            font = ('Arial', '11', 'bold'),
            width = 12,
            command = self.cancel_find,
            background = '#A2005D',
            foreground = '#FFFFFF'
        )
        cancel_find_button.place(x = 430, y = 377)

        if self.title == 'Personal Cards':
            pass

        else:
            bottom_line = tk.Frame(
                self.window,
                width = 800,
                height = 10,
                background = "#464646"
            )
            bottom_line.place(x = 0, y = 450)

            bottom_frame = tk.Frame(
                self.window,
                width = 150,
                height = 50,
                background = "#464646"
            )
            bottom_frame.place(relx = 0.5, y = 455, anchor='center')

            change_to_label = tk.Label(
                bottom_frame,
                text = 'Change to:',
                font = ('Montserrat', '15', 'italic'),
                background = "#464646",
                foreground = "#ffffff"
            )
            change_to_label.place(x = 23, y = 8)

            task_button = tk.Button(
                self.window,
                text = "TASK",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = self.change_to_task,
                background = '#004C01',
                foreground = '#FFFFFF'
            )
            task_button.place(x=14, y=500)

            remark_button = tk.Button(
                self.window,
                text = "REMARK",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = self.change_to_remark,
                background = '#9E019A',
                foreground = '#FFFFFF'
            )
            remark_button.place(x=139, y=500)

            event_button = tk.Button(
                self.window,
                text = "EVENT",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = self.change_to_event,
                background = '#A8A803',
                foreground = '#FFFFFF'
            )
            event_button.place(x=269, y=500)

            idea_button = tk.Button(
                self.window,
                text = "IDEA",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = self.change_to_idea,
                background = '#4F0082',
                foreground = '#FFFFFF'
            )
            idea_button.place(x=399, y=500)

            project_button = tk.Button(
                self.window,
                text = "PROJECT",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = self.change_to_project,
                background = '#02266A',
                foreground = '#FFFFFF'
            )
            project_button.place(x=529, y=500)

            maybe_sometimes_button = tk.Button(
                self.window,
                text = "Maybe/Sometimes",
                font = ('Arial', '9', 'bold'),
                width = 16,
                command = self.change_to_maybe_sometimes,
                background = '#A94102',
                foreground = '#FFFFFF'
            )
            maybe_sometimes_button.place(x=660, y=500)

        self.data_store_manager.make_list_data_tuple()
        self.data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )        

