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

db_manager = DBManager()
data_store_manager = DataStoreManager()
data = DataForm()

class ListWindow:
    def __init__(self, parent, title):
        self.window = tk.Toplevel(parent)
        self.window.geometry("800x550+100+100")
        self.window.configure(bg="#AFAFAF")
        self.window.title(title)
        self.window.resizable(0,0)

        self.title = title
        
        style = ttk.Style()
        style.theme_use('clam')
        data_store_manager.make_list_data_tuple()

    def show_existing_element_window(self):
        selection = self.treeview.selection()
        if selection:
            element_name = self.treeview.item(selection, 'values')[0]
            element_id = data_store_manager.get_element_id_from_list_data_tuple(element_name)
        else:
            messagebox.showwarning("ERROR", f"Select an element")

        if self.title == 'Ideas':
            new_title = 'Idea View'
            idea_window = element_window_small(
                self.window, new_title, element_id
            )
            idea_window.create_window()
            idea_window.insert_values()
            
        else:
            if self.title == 'My Tasks' or self.title == 'Delegated Tasks':
                new_title = 'Task View'
            elif self.title == 'Remarks':
                new_title = 'Remark View'
            elif self.title == 'Events':
                new_title = 'Event View'
            else:
                pass
            element_window = element_window_extended(
                self.window, new_title, element_id
            )
            element_window.create_window()
            element_window.insert_values()

    def show_new_element_window(self):
        if self.title == 'My Tasks' or self.title == 'Delegated Tasks':
            task_window = element_window_extended(
            self.window, 'Task', None
            )
            task_window.create_window()
        elif self.title == 'Remarks':
            remark_window = element_window_extended(
                self.window, "Remark", None
            )
            remark_window.create_window()
        elif self.title == 'Events':
            event_window = element_window_extended(
                self.window, 'Event', None
            )
            event_window.create_window()
        elif self.title == 'Projects':
            pass
        elif self.title == 'People Cards':
            pass
        elif self.title == 'Ideas':
            idea_window = element_window_small(
            self.window, 'Idea', None
            )
            idea_window.create_window()
        else:
            print('Not matched in def show_new_elemenet_window in ListWindow')

    def done(self):
        selection = self.treeview.selection()
        if selection:
            element_name = self.treeview.item(selection, 'values')[0]        
            element_id = data_store_manager.get_element_id_from_list_data_tuple(element_name)
            data.element_id = element_id
            data.element = element_name
            data.done = 'DONE'
            db_manager.update_db_fields(data)
            data_store_manager.make_list_data_tuple()
            data_store_manager.insert_list_data_to_treeview(self.treeview, self.title)
        else:
            messagebox.showwarning("Error", "Select an element to be done.")
    
    def delete_from_database(self):
        selection = self.treeview.selection()
        if selection:
            element_name = self.treeview.item(selection, 'values')[0]
            element_id = data_store_manager.get_element_id_from_list_data_tuple(element_name)
            db_manager.set_element_id(element_id)
            answer = messagebox.askyesno("DELETE", "DELETE from database?")
            if answer:
                db_manager.delete_from_db()
                data_store_manager.make_list_data_tuple()
                data_store_manager.insert_list_data_to_treeview(self.treeview, self.title)
            else:
                pass
        else:
            messagebox.showwarning("ERROR", "Select an element")

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
            self.treeview = ttk.Treeview(self.window, columns=('#1', '#2', '#3', '#4'), height = 13)

            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Element Name')
            self.treeview.column('#1', width=210)
            self.treeview.heading('#2', text = 'Date')
            self.treeview.column('#2', width=120)
            self.treeview.heading('#3', text = 'Deadline')
            self.treeview.column('#3', width=120)
            self.treeview.heading('#4', text = 'Delegated')
            self.treeview.column('#4', width=150)
            
            self.treeview.place (x = 15, y = 75)

        elif self.title == 'People Cards':
            self.window.geometry('800x450+100+100')

            self.treeview = ttk.Treeview(self.window, columns=('#1', '#2', '#3', '#4'), height = 13)

            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Title before')
            self.treeview.column('#1', width=120)
            self.treeview.heading('#2', text='Name')
            self.treeview.column('#2', width=210)
            self.treeview.heading('#3', text = 'Birthday')
            self.treeview.column('#3', width=150)
            self.treeview.heading('#4', text = 'Year of Birth')
            self.treeview.column('#4', width=120)

            self.treeview.place (x = 15, y = 75)
        
        elif self.title == 'Events':
            self.treeview = ttk.Treeview(self.window, columns=('#1', '#2', '#3', '#4'), height = 13)

            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Element ID')
            self.treeview.column('#1', width=150)
            self.treeview.heading('#2', text='Event')
            self.treeview.column('#2', width=210)
            self.treeview.heading('#3', text = 'Start Date')
            self.treeview.column('#3', width=120)
            self.treeview.heading('#4', text = 'End Date')
            self.treeview.column('#4', width=120)

            self.treeview.place (x = 15, y = 75)

        else: #self.title == 'Remarks' or self.title == 'Ideas' or self.title == 'Maybe/Sometimes'
            self.treeview = ttk.Treeview(self.window, columns=('#1', '#2', '#3', '#4'), height = 13)

            self.treeview.heading('#0', text='ID')
            self.treeview.column('#0', width=0, stretch = False)
            self.treeview.heading('#1', text='Element ID')
            self.treeview.column('#1', width=150)
            self.treeview.heading('#2', text='Element Name')
            self.treeview.column('#2', width=210)
            self.treeview.heading('#3', text = 'Date')
            self.treeview.column('#3', width=120)
            self.treeview.heading('#4', text = 'Field 1')
            self.treeview.column('#4', width=120)            

            self.treeview.place (x = 15, y = 75)

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

        find_row = tk.Entry(
            self.window,
            font = ("Open Sans", "11", "bold"),
            width = 30,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        find_row.place(x = 65, y = 382)

        find_button = tk.Button(
            self.window,
            text = "FIND",
            font = ('Arial', '11', 'bold'),
            width = 10,
            command = None,
            background = '#4F0082',
            foreground = '#FFFFFF'
        )
        find_button.place(x = 320, y = 377)

        cancel_find_button = tk.Button(
            self.window,
            text = "CANCEL FIND",
            font = ('Arial', '11', 'bold'),
            width = 12,
            command = None,
            background = '#A2005D',
            foreground = '#FFFFFF'
        )
        cancel_find_button.place(x = 430, y = 377)

        if self.title == 'People Cards':
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
                command = None,
                background = '#004C01',
                foreground = '#FFFFFF'
            )
            task_button.place(x=14, y=500)

            remark_button = tk.Button(
                self.window,
                text = "REMARK",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = None,
                background = '#9E019A',
                foreground = '#FFFFFF'
            )
            remark_button.place(x=139, y=500)

            event_button = tk.Button(
                self.window,
                text = "EVENT",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = None,
                background = '#A8A803',
                foreground = '#FFFFFF'
            )
            event_button.place(x=269, y=500)

            idea_button = tk.Button(
                self.window,
                text = "IDEA",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = None,
                background = '#4F0082',
                foreground = '#FFFFFF'
            )
            idea_button.place(x=399, y=500)

            project_button = tk.Button(
                self.window,
                text = "PROJECT",
                font = ('Arial', '9', 'bold'),
                width = 11,
                command = None,
                background = '#02266A',
                foreground = '#FFFFFF'
            )
            project_button.place(x=529, y=500)

            maybe_sometimes_button = tk.Button(
                self.window,
                text = "Maybe/Sometimes",
                font = ('Arial', '9', 'bold'),
                width = 16,
                command = None,
                background = '#A94102',
                foreground = '#FFFFFF'
            )
            maybe_sometimes_button.place(x=660, y=500)

        data_store_manager.make_list_data_tuple()
        data_store_manager.insert_list_data_to_treeview(self.treeview, self.title )        

