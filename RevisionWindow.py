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
        self.rows = []

        if self.title == 'day' or self.title == 'week':
            self.current_title = 'MY TASKS'
        elif self.title == 'month':
            self.current_title = 'DEADLINES'
        else:
            print('Wrong self.title in RevisionWindow')

    def insert_data_to_revision_treeview(self):
        self.list_data_tuple = data_store_manager.make_list_data_tuple()
        self.treeview.delete(*self.treeview.get_children())
        self.rows.clear()

        if self.title == 'day': # tasks date +1, deadline + 7 days; projects deadline + 7 days, events +1 day, remarks +1 day, maybe/sometimes all, birthdays + 7 days 
            for data_row in self.list_data_tuple:
                if self.current_title == 'MY TASKS':
                    self.time_interval_label.configure(text = '(for today and tommorow)')
                    if data_row[15] == 'task' and data_row[3] == date_string and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])
                    elif data_row[15] == 'task' and data_row[3] == tomorrow_date and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])
                    for i in range(1,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[3] == data_row[4]:
                            pass
                        else:  
                            if data_row[15] == 'task' and data_row[4] == future_date and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                                self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                                self.rows.append(data_row[2])
                
                elif self.current_title == 'DELEGATED TASKS':
                    self.time_interval_label.configure(text = '(in following 7 days)')
                    if data_row[15] == 'task' and data_row[3] == date_string and data_row[9] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])
                    elif data_row[15] == 'task' and data_row[3] == tomorrow_date and data_row[9] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])
                    for i in range(1,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'task' and data_row[4] == future_date and data_row[9] != "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])
                
                elif self.current_title == 'SHARED TASKS':
                    self.time_interval_label.configure(text = '(in following 7 days)')
                    if data_row[15] == 'task' and data_row[3] == date_string and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])
                    elif data_row[15] == 'task' and data_row[3] == tomorrow_date and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])
                        for i in range(1,7):
                            future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                            if data_row[15] == 'task' and data_row[4] == future_date and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                                self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                                self.rows.append(data_row[2])

                elif self.current_title == 'MY PROJECTS':
                    self.time_interval_label.configure(text = '(in following 7 days)')
                    for i in range(0,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'project' and data_row[4] == future_date and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])

                elif self.current_title == 'DELEGATED PROJECTS':
                    self.time_interval_label.configure(text = '(in following 7 days)')
                    for i in range(0,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'project' and data_row[4] == future_date and data_row[9] != "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])

                elif self.current_title == 'SHARED PROJECTS':
                    self.time_interval_label.configure(text = '(in following 7 days)')
                    for i in range(0,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'project' and data_row[4] == future_date and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])

                elif self.current_title == 'EVENTS':
                    self.time_interval_label.configure(text = '(for tomorrow)')
                    if data_row[15] == 'event':
                        start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                        end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                        future_date = (current_date + timedelta(days=1)).strftime("%d/%m/%Y")
                        future_date_string = datetime.strptime(future_date, "%d/%m/%Y")
                        if start_date <= future_date_string and end_date >= future_date_string:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])

                elif self.current_title == 'REMARKS':
                    self.time_interval_label.configure(text = '(for tomorrow)')
                    if data_row[15] == 'remark' and data_row[3] == tomorrow_date:
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])

                elif self.current_title == 'MAYBE/SOMETIMES':
                    self.time_interval_label.configure(text = '(all)')
                    if data_row[15] == 'maybe/sometimes':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])

                elif self.current_title == 'BIRTHDAYS':
                    self.time_interval_label.configure(text = '(in following 7 days)')
                    for i in range(0,7):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m")
                        if data_row[15] == 'personal card' and data_row[3] == future_date:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])

        elif self.title == 'week':
            for data_row in self.list_data_tuple:
                if self.current_title == 'MY TASKS':
                    self.time_interval_label.configure(text = '(all)')
                    if data_row[15] == 'task'and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])
                
                elif self.current_title == 'DELEGATED TASKS':
                    self.time_interval_label.configure(text = '(all)')
                    if data_row[15] == 'task'and data_row[9] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])

                elif self.current_title == 'SHARED TASKS':
                    self.time_interval_label.configure(text = '(all)')
                    if data_row[15] == 'task'and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])

                elif self.current_title == 'MY PROJECTS':
                    self.time_interval_label.configure(text = '(all)')
                    if data_row[15] == 'project'and data_row[9] == "" and data_row[10] == "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])

                elif self.current_title == 'DELEGATED PROJECTS':
                    self.time_interval_label.configure(text = '(all)')
                    if data_row[15] == 'project'and data_row[9] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])

                elif self.current_title == 'SHARED PROJECTS':
                    self.time_interval_label.configure(text = '(all)')
                    if data_row[15] == 'project'and data_row[9] == "" and data_row[10] != "" and data_row[16] == 'No':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])

                elif self.current_title == 'EVENTS':
                    self.time_interval_label.configure(text = '(in following 30 days)')
                    if data_row[15] == 'event':
                        start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                        end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                        for i in range(0, 30):
                            if data_row[1] not in self.rows:
                                future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                                future_date_string = datetime.strptime(future_date, "%d/%m/%Y")

                                if start_date <= future_date_string and end_date >= future_date_string:
                                    self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                                    self.rows.append(data_row[1])

                elif self.current_title == 'REMARKS':
                    self.time_interval_label.configure(text = '(in following 30 days)')
                    for i in range(0,30):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'remark' and data_row[3] == future_date:
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])

                elif self.current_title == 'MAYBE/SOMETIMES':
                    self.time_interval_label.configure(text = '(all)')
                    if data_row[15] == 'maybe/sometimes':
                        self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                        self.rows.append(data_row[2])

                elif self.current_title == 'BIRTHDAYS':
                    self.time_interval_label.configure(text = '(in following 30 days)')
                    if data_row[15] == 'personal card':
                        for i in range(0,30):
                            future_date = (current_date + timedelta(days=i)).strftime("%d/%m")
                            if data_row[3] == future_date:
                                self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                                self.rows.append(data_row[2])

        elif self.title == 'month':
            for data_row in self.list_data_tuple:
                if self.current_title == 'DEADLINES':
                    self.time_interval_label.configure(text = '(in following 180 days)')
                    for i in range(0,180):
                        future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                        if data_row[15] == 'task' and data_row[4] == future_date and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])
                        if data_row[15] == 'project' and data_row[4] == future_date and data_row[16] == 'No':
                            self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                            self.rows.append(data_row[2])
                elif self.current_title == 'EVENTS':
                    self.time_interval_label.configure(text = '(in following 180 days)')
                    if data_row[15] == 'event':
                        start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                        end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                        for i in range(0, 180):
                            if data_row[1] not in self.rows:
                                future_date = (current_date + timedelta(days=i)).strftime("%d/%m/%Y")
                                future_date_string = datetime.strptime(future_date, "%d/%m/%Y")

                                if start_date <= future_date_string and end_date >= future_date_string:
                                    self.treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9], data_row[10]))
                                    self.rows.append(data_row[1])
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

        self.insert_data_to_revision_treeview()
        total_number_elements = len(self.rows)
        self.treeview_label.configure(text = str(self.current_title) + ': ' + str(total_number_elements))
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
            
            self.insert_data_to_revision_treeview()
            total_number_elements = len(self.rows)
            self.treeview_label.configure(text = str(self.current_title) + ': ' + str(total_number_elements))
            if self.current_title == 'MY TASKS' or self.current_title == 'DELEGATED TASKS' or self.current_title == 'SHARED TASKS' or self.current_title == 'MY PROJECTS' or self.current_title == 'DELEGATED PROJECTS' or self.current_title == 'SHARED PROJECTS' or self.current_title == 'DEADLINES':
                self.done_button.place(x = 15, y = 400)
            else:
                self.done_button.place_forget()
        else:
            self.current_index -= 0

    def done(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
            data_row = data_store_manager.get_data_row_from_list_data_tuple(element_id)
            if self.current_title == 'MY TASKS' or self.current_title == 'DELEGATED TASKS' or self.current_title == 'SHARED TASKS':
                data.element_id = element_id
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

                db_manager.update_db_fields(data)
                self.insert_data_to_revision_treeview()

            elif self.current_title == 'MY PROJECTS' or self.current_title == 'DELEGATED PROJECTS' or self.current_title == 'SHARED PROJECTS':
                data.element_id = element_id
                data.element = data_row[2]
                data.deadline = data_row[4]
                data.project = data_row[8]
                data.delegated = data_row[9]
                data.cooperating = data_row[10]
                data.keywords = data_row[14]
                data.category = data_row[15]
                data.done = 'DONE'
            
                db_manager.update_db_fields(data)
            
                rows = data_store_manager.get_all_project_tasks_id_from_list_data_tuple(data.element)
                if rows is not None:
                    for row in rows:
                        messagebox.showwarning("DONE ASSOCIATED", f"Asscociated task {row} is to be done")
                        db_manager.set_element_id(row)
                        data_row = data_store_manager.get_data_row_from_list_data_tuple(row)

                        data.element_id = row
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

                        db_manager.update_db_fields(data)

            else:
                print('Wrong self.current_title in done function: RevisionWindow')
        else:
            messagebox.showwarning("Error", "Select an element")

    def delete(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
            db_manager.set_element_id(element_id)
            answer = messagebox.askyesno("DELETE", "DELETE from database?")
            if answer:
                db_manager.delete_from_db()
                if self.current_title == 'MY PROJECTS' or self.current_title == 'DELEGATED PROJECTS' or self.current_title == 'SHARED PROJECTS':
                    element_name = self.treeview.item(selection, 'values')[1]
                    rows = data_store_manager.get_all_project_tasks_id_from_list_data_tuple(element_name)
                    if rows is not None:
                        for row in rows:
                            db_manager.set_element_id(row)
                            messagebox.showwarning("DELETE ASSOCIATED", f"Asscociated task {row} is to be deleted.")
                            db_manager.delete_from_db()
                self.insert_data_to_revision_treeview()
            else:
                pass
        else:
            messagebox.showwarning("ERROR", "Select an element")

    def show_existing_element_window(self):
        selection = self.treeview.selection()
        if selection:
            element_id = self.treeview.item(selection, 'values')[0]
        else:
            messagebox.showwarning("ERROR", f"Select an element")

        if self.current_title == 'MY PROJECTS' or self.current_title == 'DELEGATED PROJECTS' or self.current_title == 'SHARED PROJECTS':
            project_window = ProjectWindow(
                self.window, element_id
            )
            project_window.create_window()
            project_window.insert_values()

        elif self.current_title == 'BIRTHDAYS':
            personal_card_window = PersonalCardWindow(
                self.window, element_id
            )
            personal_card_window.create_window()
            personal_card_window.insert_values()

        else:
            if self.current_title == 'MY TASKS' or self.current_title == 'DELEGATED TASKS' or self.current_title == 'SHARED TASKS':
                new_title = 'Task View'
            elif self.current_title == 'REMARKS':
                new_title = 'Remark View'
            elif self.current_title == 'EVENTS':
                new_title = 'Event View'
            elif self.current_title == 'MAYBE/SOMETIMES':
                new_title = 'Maybe/Sometimes View'
                new_title == 'Task View' 
            else:
                pass
            element_window = element_window_extended(
                self.window, new_title, element_id
            )
            element_window.create_window()
            element_window.insert_values()

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

        self.time_interval_label = tk.Label(
            self.window,
            text = "",
            font = ('Montserrat', '12', 'bold'),
            background = "#AFAFAF",
            foreground = "#2D4A54"
        )
        self.time_interval_label.place(x = 570, y = 75)

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
            command = self.done,
            background = '#004C01',
            foreground = '#FFFFFF'
        )
        self.done_button.place(x=15, y=400)

        view_button = tk.Button(
            self.window,
            text = "VIEW",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.show_existing_element_window,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        view_button.place(x=130, y = 400)

        delete_button = tk.Button(
            self.window,
            text = "DELETE",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.delete,
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
        if self.title == 'month':
            self.treeview_label.configure(text = 'DEADLINES: ' + str(len(self.rows)))
        else:
            self.treeview_label.configure(text = 'MY TASKS: ' + str(len(self.rows)))