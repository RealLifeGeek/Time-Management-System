import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
import datetime
from DBManager import *
from DataStoreManager import *
from DataFormObject import *
from element_window_extended import *

current_date = datetime.now()
timestamp = current_date.strftime("%d/%m/%Y-%H:%M:%S")
date_string = current_date.strftime("%d/%m/%Y")
data = DataForm()


class ProjectWindow:   
    def __init__(self, parent, element_id, user_id):
        self.user_id = user_id
        self.db_manager = DBManager(self.user_id)
        self.data_store_manager = DataStoreManager(self.user_id)

        self.window = tk.Toplevel(parent)
        self.window.geometry('800x600')
        self.window.title('PROJECT')
        self.window.option_add('*Dialog.msg.title.bg', '#000000')
        self.window.configure(bg = "#9C9C9C")
        self.window.resizable(0,0)

        self.calendar = Calendar (
            self.window,
            selectmode = 'day',
            date_pattern = ('dd/mm/yyyy'),
            background = "black")
        self.calendar.place(x= 525, y= 320)

        if element_id == None:
            element_id = self.db_manager.generate_element_id('PR')
        else:
            pass
        
        self.project_name = "Default_Project_StarLord01"
        self.element_id = element_id

    def check_project_name(self):
        if len(self.project_name_row.get()) != 0:
            self.project_name = self.project_name_row.get()
            self.header_label.config(text=self.project_name)
        else:
            self.project_name = "Default_Project_StarLord01"
        self.window.after(10000, self.check_project_name)

    def insert_values_to_treeview(self):
        self.data_store_manager.make_list_data_tuple()
        self.data_store_manager.insert_data_to_project_treeview(self.treeview, self.project_name)
        self.window.after(10000, self.insert_values_to_treeview)

    def insert_values(self):
        win = self.window
        row1 = self.project_name_row 
        row2 = self.deadline_row
        row3 = self.responsible_person_row 
        row4 = self.cooperating_with_row
        row5 = self.keywords_row

        row1.delete(0, tk.END)
        row2.delete(0, tk.END)
        row3.delete(0, tk.END)
        row4.delete(0, tk.END)
        row5.delete(0, tk.END)

        self.data_store_manager.insert_values_to_project_form(
            self.element_id, win, row1, row2, row3, row4, row5
        )
        self.check_project_name()
        self.insert_values_to_treeview()

    def choose_deadline(self):
        chosen_deadline = self.calendar.get_date()
        self.deadline_row.delete(0, "end")
        self.deadline_row.insert(0, chosen_deadline)

    def get_project_data(self):
        current_date = datetime.now()
        timestamp = current_date.strftime("%d/%m/%Y-%H:%M:%S")
        data_row = self.data_store_manager.get_data_row_from_list_data_tuple(self.element_id)
        if data_row == None:
            data.timestamp_created = timestamp
        else:
            data.timestamp_created = data_row[17] 

        data.element_id = self.element_id
        data.element = self.project_name_row.get()
        data.date = ""
        data.deadline = self.deadline_row.get()
        data.project = self.project_name_row.get() 
        data.delegated = self.responsible_person_row.get()
        data.cooperating = self.cooperating_with_row.get()
        data.field4 = ""
        data.field5 = ""
        data.remarks = ""
        data.keywords = self.keywords_row.get()
        data.category = 'project'
        data.done = 'No'
        data.timestamp_finished = ''

    def show_new_task_window(self):
        task_window = element_window_extended(
            self.window, 'Task', None
        )
        task_window.create_window()

    def show_existing_task_window(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
        else:
            messagebox.showwarning("ERROR", f"Select an element")
        task_window = element_window_extended(
            self.window, 'Task View', element_id, self.user_id
        )
        task_window.create_window()
        task_window.insert_values()
    
    def show_task_window_on_double_click(self, event):
        self.show_existing_task_window()

    def save_or_edit_project(self):       
        try:
            self.get_project_data()
            if data.deadline == None or data.deadline == '':
                messagebox.showerror("ERROR", "Deadline is not selected.")
                return
            else:
                if self.db_manager.element_id_already_exists(self.element_id):
                    self.db_manager.update_db_fields(data)
                else:
                    self.db_manager.save_to_db(data)
                self.data_store_manager.make_list_data_tuple()
                self.window.destroy()
        except Exception as e:
                messagebox.showerror("ERROR", f"ERROR 700: {e}")
                self.window.destroy()
    
    def project_done(self):
        current_date = datetime.now()
        timestamp = current_date.strftime("%d/%m/%Y-%H:%M:%S")

        if self.db_manager.element_id_already_exists(self.element_id):
            self.get_project_data()
            if data.done == 'DONE':
                messagebox.showwarning("ALREADY DONE", "This project is already done")
            else:
                data.done = 'DONE'
                self.db_manager.update_db_fields(data)
                print('Project_name for related tasks is: ' + self.project_name)
                rows = self.data_store_manager.get_all_project_tasks_id_from_list_data_tuple(self.project_name)
                if rows is not None:
                    for row in rows:
                        messagebox.showwarning("DONE ASSOCIATED", f"Asscociated task {row} is to be done")
                        self.db_manager.set_element_id(row)
                        data_row = self.data_store_manager.get_data_row_from_list_data_tuple(row)

                        data.element_id = row[1]
                        data.element = data_row[2]
                        data.date = data_row[3]
                        data.deadline = data_row[4]
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
                else:
                    print('No related tasks to the project: ' + self.project_name)
            self.data_store_manager.make_list_data_tuple()
            self.exit()
        else:
            messagebox.showerror("ERROR", "Unable to finish non-existing project")

    def show_new_task_window(self):
        task_window = element_window_extended(
            self.window, 'Task', None, self.user_id
        )
        task_window.create_window()
        task_window.project_row.insert(0, self.project_name)

    def task_done(self):
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
            self.data_store_manager.insert_data_to_project_treeview(self.treeview, self.project_name)
        else:
            messagebox.showwarning("Error", "Select an element")
    
    def delete_task_from_database(self):
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
                self.data_store_manager.make_list_data_tuple()
                self.data_store_manager.insert_data_to_project_treeview(self.treeview, self.project_name)
                #self.exit()
            else:
                pass
        else:
            messagebox.showwarning("ERROR", "Select an element")

    def exit(self):
        self.window.destroy()

    def progress_bar_of_project(self):
        self.insert_values()
        try:
            number_tasks_done = self.data_store_manager.count_number_elements_for_project(self.project_name, 'DONE')
            number_tasks_to_fulfill = self.data_store_manager.count_number_elements_for_project(self.project_name, 'No')
            total_number_tasks = number_tasks_done + number_tasks_to_fulfill
            if total_number_tasks != 0:
                task_value = 100/total_number_tasks
                task_done_value = number_tasks_done * task_value
                value = 0 + task_done_value
            else:
                value = 0

            style_progressbar = ttk.Style()
            style_progressbar.theme_use("clam")
            style_progressbar.configure("green.Horizontal.TProgressbar", background= '#0003C8')

            project_progress_bar = ttk.Progressbar(
                self.window, style = "green.Horizontal.TProgressbar",
                orient="horizontal",
                length=765,
                mode="determinate"
            )
            project_progress_bar.place(x = 15, y = 290)
            project_progress_bar["value"] = value

            if total_number_tasks == 0:
                style_progressbar.configure("green.Horizontal.TProgressbar", background= '#20EE00', troughcolor='#666666')
            else:
                if value == 0:
                    style_progressbar.configure("green.Horizontal.TProgressbar", background= '#970000', troughcolor='#666666')
                elif 1 <= value <= 30:
                    style_progressbar.configure("green.Horizontal.TProgressbar", background= '#970000', troughcolor='#666666')
                elif 31 <= value <= 60:
                    style_progressbar.configure("green.Horizontal.TProgressbar", background= '#F08C05',  troughcolor='#666666')
                elif 61 <= value <= 99:
                    style_progressbar.configure("green.Horizontal.TProgressbar", background= '#BFEE00',  troughcolor='#666666')
                else:
                    style_progressbar.configure("green.Horizontal.TProgressbar", background= '#20EE00',  troughcolor='#666666')
        except Exception as e:
            messagebox.showerror("ERROR", f"Progress bar error 701: {e}")
        self.window.after(10000, self.progress_bar_of_project)


    def create_window(self):
        self.treeview = ttk.Treeview(
            self.window, 
            columns=('Element ID', 'Element', 'Date', 'Deadline', 'Delegated to', 'Cooperating with')
        )

        self.treeview.heading('#0', text='ID')
        self.treeview.column('#0', width=0, stretch = False)
        self.treeview.heading('#1', text='Element ID')
        self.treeview.column('#1', width=100)
        self.treeview.heading('#2', text='Element')
        self.treeview.column('#2', width=170)
        self.treeview.heading('#3', text='Date')
        self.treeview.column('#3', width=80)
        self.treeview.heading('#4', text='Deadline')
        self.treeview.column('#4', width=80)
        self.treeview.heading('#5', text='Delegated to')
        self.treeview.column('#5', width=110)
        self.treeview.heading('#6', text='Cooperating with')
        self.treeview.column('#6', width=110)

        self.treeview.place (x = 15, y = 55)
        self.treeview.bind("<Double-1>", self.show_task_window_on_double_click)
        self.treeview.bind("<Return>", self.show_task_window_on_double_click)

        self.header_label = tk.Label(
            self.window,
            text = str(self.project_name),
            font = ('Montserrat', '15', "bold"),
            background = "#9C9C9C",
            foreground = "#000000"
        )
        self.header_label.place(relx = 0.5, y = 25, anchor = 'center')

        element_id_label = tk.Label(
            self.window,
            text = self.element_id,
            font = ("Open Sans", "10"),
            background = "#9C9C9C",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 665, y = 5)

        new_element_button = tk.Button(
            self.window,
            text = "+",
            font = ('Arial', '15', 'bold'),
            width = 3,
            command = self.show_new_task_window,
            background = '#029F00',
            foreground = '#FFFFFF'
        )
        new_element_button.place(x= 710, y= 55)

        task_done_button = tk.Button(
            self.window,
            text = "DONE",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.task_done,
            background = '#004C01',
            foreground = '#FFFFFF'
        )
        task_done_button.place(x = 680, y = 110)

        task_view_button = tk.Button(
            self.window,
            text = "VIEW",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.show_existing_task_window,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        task_view_button.place(x = 680, y = 150)

        task_delete_button = tk.Button(
            self.window,
            text = "DELETE",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.delete_task_from_database,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        task_delete_button.place(x = 680, y = 190)

        bottom_frame = tk.Frame(
            self.window,
            width = 470,
            height = 185,
            background = "#2F3030"
        )
        bottom_frame.place(x = 15, y = 320)

        project_name_label = tk.Label(
            bottom_frame,
            text = "Project Name",
            font = ("Open Sans", "11", "bold"),
            background = "#2F3030",
            foreground = "#000000"       
        )
        project_name_label.place(x = 10, y = 8)

        self.project_name_row = tk.Entry(
            bottom_frame,
            font = ("Open Sans", "10", "bold"),
            width = 40,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        self.project_name_row.place(x = 170, y = 10)

        keywords_label = tk.Label(
            bottom_frame,
            text = "Keywords",
            font = ("Open Sans", "11", "bold"),
            background = "#2F3030",
            foreground = "#000000"       
        )
        keywords_label.place(x = 10, y = 38)

        self.keywords_row = tk.Entry(
            bottom_frame,
            font = ("Open Sans", "10", "bold"),
            width = 40,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        self.keywords_row.place(x = 170, y = 40)

        responsible_person_label = tk.Label(
            bottom_frame,
            text = "Responsible Person",
            font = ("Open Sans", "11", "bold"),
            background = "#2F3030",
            foreground = "#000000"       
        )
        responsible_person_label.place(x = 10, y = 68)

        self.responsible_person_row = tk.Entry(
            bottom_frame,
            font = ("Open Sans", "10", "bold"),
            width = 40,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        self.responsible_person_row.place(x = 170, y = 70)

        cooperating_with_label = tk.Label(
            bottom_frame,
            text = "Cooperating with",
            font = ("Open Sans", "11", "bold"),
            background = "#2F3030",
            foreground = "#000000"       
        )
        cooperating_with_label.place(x = 10, y = 98)

        self.cooperating_with_row = tk.Entry(
            bottom_frame,
            font = ("Open Sans", "10", "bold"),
            width = 40,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FFFFFF"
        )
        self.cooperating_with_row.place(x = 170, y = 100)

        deadline_button = tk.Button(
            bottom_frame,
            text = "Choose Deadline",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.choose_deadline,
            background = '#464646',
            foreground = '#FFFFFF'
        )
        deadline_button.place(x = 10, y = 138)

        self.deadline_row = tk.Entry(
            bottom_frame,
            font = ("Open Sans", "12", "bold"),
            width = 31,
            insertbackground = "#FFFFFF",
            background = "#000000",
            foreground = "#FF0000"
        )
        self.deadline_row.place(x = 170, y = 140)


        project_done_button = tk.Button(
            self.window,
            text = "PROJECT DONE",
            font = ('Arial', '15', 'bold'),
            width = 15,
            command = self.project_done,
            background = '#029F00',
            foreground = '#FFFFFF'
        )
        project_done_button.place(x = 15, y = 530)

        save_button = tk.Button(
            self.window,
            text = "SAVE",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.save_or_edit_project,
            background = '#004C01',
            foreground = '#FFFFFF'
        )
        save_button.place(x = 570, y = 550)

        exit_button = tk.Button(
            self.window,
            text = "EXIT",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.exit,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        exit_button.place(x = 680, y = 550)

        self.insert_values_to_treeview()
        self.check_project_name()
        self.progress_bar_of_project()
