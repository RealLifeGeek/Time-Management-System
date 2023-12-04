from tkinter import messagebox
import tkinter as tk
from DBManager import *
from DataFormObject import *
from datetime import datetime, timedelta

db_manager = DBManager()
data = DataForm()
current_date = datetime.now()
date_string = current_date.strftime("%d/%m/%Y")

class DataStoreManager:
    def __init__(self):
        self.day_data_tuple = []
        self.list_data_tuple = []
    
    def make_list_data_tuple(self): # Tuple for ListWindow
        self.list_data_tuple = db_manager.get_list_data_tuple()
        self.make_day_data_tuple()
        return self.list_data_tuple

    def make_day_data_tuple(self):
        self.day_data_tuple.clear()   
        for data_row in self.list_data_tuple:
            if data_row[15] != 'event' and data_row[3] == date_string or data_row[4] == date_string:
                self.day_data_tuple.append(data_row)
            if data_row[15] == 'event':
                start_date = datetime.strptime(data_row[3], "%d/%m/%Y")
                end_date = datetime.strptime(data_row[4], "%d/%m/%Y")
                date_string_datetime = datetime.strptime(date_string, "%d/%m/%Y")
                if start_date <= date_string_datetime and end_date >= date_string_datetime:
                    self.day_data_tuple.append(data_row)
            else:
                pass
        #print('Creating new day_data_tuple: DataStoreManager')
        return self.day_data_tuple

    def insert_day_data_to_treeview(self, treeview, category): # Inserting data to treeviews on MainScreen
        treeview.delete(*treeview.get_children())
        try:
                for data_row in self.day_data_tuple:
                    if category == 'task':
                        if data_row [15] == 'task' and data_row[9] == "" and data_row[16] == 'No':
                            treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[7]))
                    else:
                        if data_row[15] == category:
                            treeview.insert('', 'end', values=(data_row[1], data_row[2]))
                        else:
                            pass     
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")

    def insert_data_to_project_treeview(self, treeview, project_name):
        treeview.delete(*treeview.get_children())
        for data_row in self.list_data_tuple:
            if data_row[8] == project_name and data_row[15] == 'task' and data_row[16] == 'No':
                treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], 
                                                data_row[4], data_row[9], data_row[10],))
            else:
                pass
    
    def insert_data_to_notifications_treeview(self, treeview, category):
        treeview.delete(*treeview.get_children())
        if category == 'tasks' or category == 'delegated tasks' or category == 'projects':
            for i in range(1,178):
                previous_date = (current_date - timedelta(days=i)).strftime('%d/%m/%Y')
                for data_row in self.list_data_tuple:
                    if category == 'tasks':
                        if data_row[15] == 'task' and data_row[9] == '' and data_row[3] == previous_date and data_row[16] == 'No':
                            treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[4], data_row[9]))
                    elif category == 'delegated tasks':
                        if data_row[15] == 'task' and data_row[9] != '' and data_row[3] == previous_date and data_row[16] == 'No':
                            treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[4], data_row[9]))
                    elif category == 'projects':
                        if data_row[15] == 'project' and data_row[3] == previous_date and data_row[16] == 'No':
                            treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[4], data_row[9]))
                else:
                    pass
        elif category == 'birthdays':
            for i in range(0,7):
                future_date = (current_date + timedelta(days=i)).strftime('%d/%m')
                for data_row in self.list_data_tuple:
                    if data_row[15] == 'personal card' and data_row[3] == future_date:
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4]))
        
        elif category == 'closing deadlines':
            for i in range(0,6):
                future_date = (current_date + timedelta(days=i)).strftime('%d/%m/%Y')
                for data_row in self.list_data_tuple:
                    if data_row[15] == 'task' and data_row[4] == future_date and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[4], data_row[9]))
                    if data_row[15] == 'project' and data_row[4] == future_date and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[4], data_row[9]))
                    else:
                        pass
        elif category == 'pending ideas':
            for i in range (1,178):
                previous_date = (current_date - timedelta(days=i)).strftime('%d/%m/%Y')
                for data_row in self.list_data_tuple:
                    if data_row[15] == 'idea' and data_row[3] == previous_date:
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[4], data_row[9]))
        else:
            print('Wrong category in function: insert_data_to_notifications_treeview.')
    

    def insert_list_data_to_treeview(self, treeview, list_category): # Inserting data to treeviews in ListWindow
        treeview.delete(*treeview.get_children())
        try:
            for data_row in self.list_data_tuple:
                if list_category == 'My Tasks':
                    if data_row [15] == 'task' and data_row[9] == "" and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9]))
                elif list_category == 'Delegated Tasks':
                    if data_row [15] == 'task' and data_row[9] != "" and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9]))
                elif list_category == 'Projects':
                    if data_row [15] == 'project' and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9]))
                elif list_category == 'Personal Cards':
                    if data_row[15] == 'personal card':
                        treeview.insert('', 'end', values=(data_row[1], data_row[11], data_row[2], data_row[3], data_row[4]))
                elif list_category == 'Events':
                    if data_row[15] == 'event':
                        treeview.insert('', 'end', values=(data_row[1], data_row[1], data_row[2], data_row[3], data_row[4]))
                elif list_category == 'Remarks':
                    if data_row[15] == 'remark':
                        treeview.insert('', 'end', values=(data_row[1], data_row[1], data_row[2], data_row[3], data_row[5]))
                elif list_category == 'Ideas':
                    if data_row[15] == 'idea':
                        treeview.insert('', 'end', values=(data_row[1], data_row[1], data_row[2], data_row[3], data_row[5]))
                elif list_category == 'Maybe/Sometimes':
                    if data_row[15] == 'maybe/sometimes':
                        treeview.insert('', 'end', values=(data_row[1], data_row[1], data_row[2], data_row[3], data_row[5]))
                else:
                    pass
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")

    def insert_data_to_personal_card_treeview(self, treeview, category, name):
        self.make_list_data_tuple()
        treeview.delete(*treeview.get_children())
        if name != '':
            for data_row in self.list_data_tuple:
                if category == 'task':
                    if data_row[15] == 'task' and data_row[9] == name and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4]))
                elif category == 'project':
                    if data_row[15] == 'project' and data_row[9] == name and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[4]))
                elif category == 'cooperating':
                    if data_row[15] == 'task' and data_row[10] == name and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4]))
                    if data_row[15] == 'project' and data_row[10] == name and data_row[16] == 'No':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4]))
                else:
                    pass
        else:
            pass

    def count_number_of_day_element(self, category): # no need of today date_string, data_tuple is generated for today
        try:
            number_elements = 0
            for data_row in self.day_data_tuple:
                if category == 'task' and data_row[15] == 'task' and data_row[9] == "" and data_row[16] == 'No':
                    number_elements += 1
                elif data_row[15] == category and category != 'task':
                    number_elements += 1
                else:
                    pass
            return number_elements
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")

    def count_total_number_of_elements(self, category, delegated, done, ProgressBar_bool):
            rows = []
            for data_row in self.list_data_tuple: 
                if category == 'task' and delegated == '':
                    if data_row[15] == 'task' and data_row[9] == '':
                        if done == 'No' and ProgressBar_bool == 'No':
                            if data_row[16] == 'No':
                                rows.append(data_row[2])
                        elif done == 'No' and ProgressBar_bool == 'Yes':
                            if data_row[3] == date_string or data_row[4] == date_string:
                                if data_row[16] == 'No':
                                    rows.append(data_row[2])
                        elif done == 'DONE' and ProgressBar_bool == 'No':
                            if data_row[16] == 'DONE':
                                rows.append(data_row[2])
                        elif done == 'DONE' and ProgressBar_bool == 'Yes':
                            if data_row[3] == date_string or data_row[4] == date_string:
                                if data_row[16] == 'DONE':
                                    rows.append(data_row[2])

                elif category == 'task' and delegated != '':
                    if data_row[15] == 'task' and data_row[9] != '':
                        if done == 'No':
                            if data_row[16] == 'No':
                                rows.append(data_row[2])
                        elif done == 'DONE':
                            if data_row[16] == 'DONE':
                                rows.append(data_row[2])
                
                elif category == 'project':
                    if data_row[15] == 'project':
                        if done == 'No':
                            if data_row[16] == 'No':
                                rows.append(data_row[2])
                        elif done == 'DONE':
                            if data_row[16] == 'DONE':
                                rows.append(data_row[2])
                else:
                    if data_row[15] == category:
                        rows.append(data_row[2])
            number_elements = len(rows)
            return number_elements

    def count_number_undone_elements(self, category, frame, XX, YY):
        self.make_list_data_tuple()
        results = []
        results.clear()
        for i in range(1,178):
            previous_date = (current_date - timedelta(days=i)).strftime('%d/%m/%Y')
            for data_row in self.list_data_tuple:
                if category == 'tasks':
                    if data_row[15] == 'task' and data_row[9] == '' and data_row[3] == previous_date and data_row[16] == 'No':
                        results.append(data_row[1])
                elif category == 'delegated tasks':
                    if data_row[15] == 'task' and data_row[9] != '' and data_row[3] == previous_date and data_row[16] == 'No':
                        results.append(data_row[1])
                elif category == 'projects':
                    if data_row[15] == 'project' and data_row[3] == previous_date and data_row[16] == 'No':
                        results.append(data_row[1])
                else:
                    print('Wrong category given in function: count_number_undone_elements.')
        number_elements = len(results)
        return number_elements

    def count_closing_deadlines(self, frame, XX, YY):
        results = []
        results.clear()
        for i in range(0,6):
            future_date = (current_date + timedelta(days=i)).strftime('%d/%m/%Y')
            for data_row in self.list_data_tuple:
                if data_row[15] == 'task' and data_row[4] == future_date and data_row[16] == 'No':
                    results.append(data_row[1])
                if data_row[15] == 'project' and data_row[4] == future_date and data_row[16] == 'No':
                    results.append(data_row[1])
                else:
                    pass
        number_elements = len(results)
        return number_elements

    def count_pending_ideas(self, frame, XX, YY):
        results = []
        results.clear()
        for i in range(1,178):
            previous_date = (current_date - timedelta(days=i)).strftime('%d/%m/%Y')
            for data_row in self.list_data_tuple:
                if data_row[15] == 'idea' and data_row[3] == previous_date:
                    results.append(data_row[1])
                else:
                    pass
        number_elements = len(results)
        return number_elements

    def count_birthday(self):
        results = []
        results.clear()
        for i in range(0,7):
            future_date = (current_date + timedelta(days=i)).strftime('%d/%m')
            for data_row in self.list_data_tuple:
                if data_row[15] == 'personal card' and data_row[3] == future_date:
                    results.append(data_row[1])
                else:
                    pass
        number_elements = len(results)
        return number_elements

    def count_number_elements_for_project(self, project_name, done):
        rows = []
        for data_row in self.list_data_tuple:
            if done == 'No':
                if data_row[15] == 'task' and data_row[8] == project_name and data_row[16] == 'No':
                    rows.append(data_row[2])
            elif done == 'DONE':
                if data_row[15] == 'task' and data_row[8] == project_name and data_row[16] == 'DONE':
                    rows.append(data_row[2])
        number_elements = len(rows)
        if done == 'No':
            print(f'Tasks to fullfill in project {project_name}: {number_elements}')
        else:
            print(f'Tasks done in project {project_name}: {number_elements}')
        return number_elements

    def check_elementid_in_tuple(self, element_id):
        if self.list_data_tuple == []:
            self.day_data_tuple = self.make_day_data_tuple()
            self.list_data_tuple = self.make_list_data_tuple()
        else:
            pass
        for day_data_row in self.day_data_tuple:
            if element_id in day_data_row:
                return day_data_row
        for list_data_row in self.list_data_tuple:
            if element_id in list_data_row:
                return list_data_row
            
    def get_data_row_from_list_data_tuple(self, element_id):
        for data_row in self.list_data_tuple:
            if element_id in data_row:
                return data_row
            else:
                pass

    def insert_values_to_task_form(self, element_id, win, row1, row2, row3, row4, row5, row6, row7, row8, row9):
        data_row = self.check_elementid_in_tuple(element_id)
        print(data_row)

        element_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 480, y = 5)

        result_element = data_row[2]
        row1.insert(0, result_element)

        chosen_date = data_row[3]
        if chosen_date == None:
            chosen_date = ""
        row2.insert(0, chosen_date)

        chosen_deadline = data_row[4]
        if chosen_deadline == None:
            chosen_deadline = ""
        row3.insert(0, chosen_deadline)

        result_expected_result = data_row[6]
        row4.insert(0, result_expected_result)

        result_time = data_row[7]
        row5.insert(0, result_time)            

        result_project = data_row[8]
        row6.insert(0, result_project)

        result_delegate_to = data_row[9]
        row7.insert(0, result_delegate_to)

        result_cooperate_with = data_row[10]
        row8.insert(0, result_cooperate_with)

        result_keywords = data_row[14]
        row9.insert(0, result_keywords)

    def insert_values_to_event_form(self, element_id, win, row1, row2, row3, row4, row5, row6, row7):
        data_row = self.check_elementid_in_tuple(element_id)
        
        element_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 480, y = 5)

        result_event = data_row[2]
        row1.insert(0, result_event)

        chosen_date = data_row[3]
        if data_row[3] == None:
            chosen_date = data_row[4]
            if data_row[4] == None:
                chosen_date = ""
        row4.insert(0, chosen_date)

        chosen_deadline = data_row[4]
        if data_row[4] == None:
            chosen_date = data_row[3]
            if data_row[3] == None:
                chosen_date = ""
        row5.insert(0, chosen_deadline)
        
        result_field1 = data_row[5]
        row2.insert(0, result_field1)
        
        result_field2 = data_row[6]
        row3.insert(0, result_field2)

        result_start_time = data_row[7]
        row6.insert(0, result_start_time)

        result_end_time = data_row[11]
        row7.insert(0, result_end_time)

    def insert_values_to_remark_form(self, element_id, win, row1, row2, row3, row4):
        data_row = self.check_elementid_in_tuple(element_id)
            
        element_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 480, y = 5)

        result_remark = data_row[2]
        row1.insert(0, result_remark)
        
        result_field1 = data_row[5]
        row2.insert(0, result_field1)
        
        result_field2 = data_row[6]
        row3.insert(0, result_field2)
        
        chosen_date = data_row[3]
        if data_row[3] == None:
            chosen_date = data_row[4]
            if data_row[4] == None:
                chosen_date = ""
            else:
                pass
        row4.insert(0, chosen_date)

    def insert_values_to_idea_form(self, element_id, win, row1, row2, row3):
        data_row = self.check_elementid_in_tuple(element_id)

        idea_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        idea_id_label.place(x = 480, y = 5)

        result_idea = data_row[2]
        row1.insert(0, result_idea)

        result_field1 = data_row[5]
        row2.insert(0, result_field1)

        result_field2 = data_row[6]
        row3.insert(0, result_field2)

        result_date = data_row[3]
        if data_row[3] == None:
            result_date = data_row[4]
            if data_row[4] == None:
                result_date = ""
        date_label = tk.Label(
            win,
            text = result_date,
            font = ('Montserrat', '15'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        date_label.place(x = 480, y = 160)

    def insert_values_to_project_form(self, element_id, win, row1, row2, row3, row4, row5):
        data_row = self.check_elementid_in_tuple(element_id)

        element_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#9C9C9C",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 665, y = 5)

        result_element = data_row[2]
        row1.insert(0, result_element)

        chosen_deadline = data_row[4]
        if chosen_deadline == None:
            chosen_deadline = ""
        row2.insert(0, chosen_deadline)           

        result_delegate_to = data_row[9]
        row3.insert(0, result_delegate_to)

        result_cooperate_with = data_row[10]
        row4.insert(0, result_cooperate_with)

        result_keywords = data_row[14]
        row5.insert(0, result_keywords)

    def insert_values_to_personal_card_form(self, element_id, win, row1, row2, row3, row4, row5, row6, row7,
                                            row8, row9, row10, row11):
        data_row = self.check_elementid_in_tuple(element_id)

        element_id_label = tk.Label(
            win,
            text = element_id,
            font = ("Open Sans", "10"),
            background = "#D9D0AF",
            foreground = "#FFFFFF"
        )
        element_id_label.place(x = 680, y = 5)

        name = data_row[2]
        row1.insert(0, name)

        date_of_birth = data_row[3]
        row2.insert(0, date_of_birth)           

        year_of_birth = data_row[4]
        row3.insert(0, year_of_birth)

        field1 = data_row[5]
        row4.insert(0, field1)

        field2 = data_row[6]
        row5.insert(0, field2)

        field3 = data_row[7]
        row6.insert(0, field3)

        company = data_row[10]
        row7.insert(0, company)

        title_before = data_row[11]
        row8.insert(0, title_before)

        title_after = data_row[12]
        row9.insert(0, title_after)

        email = data_row[13]
        row10.insert(0, email)

        phone_number = data_row[14]
        row11.insert(0, phone_number)


    def get_element_id_from_day_data_tuple(self, element_name):
        for data_row in self.day_data_tuple:
            if element_name in data_row:
                return data_row[1]
            else:
                pass

    def get_element_id_from_list_data_tuple(self, element_name):
        for data_row in self.list_data_tuple:
            if element_name in data_row:
                return data_row[1]
            else:
                pass

    def get_all_project_tasks_id_from_list_data_tuple(self, element_name):
        rows = []
        for data_row in self.list_data_tuple:
            if element_name in data_row[8]:
                rows.append(data_row[1])
            else:
                pass
        return rows
    
    def find_element_in_list_tuple(self, treeview, searched_item, list_category):
        treeview.delete(*treeview.get_children())
        try:
            for data_row in self.list_data_tuple:
                searched_item_str = str(searched_item)
                str_data_row = str(data_row)
                item_pieces = str_data_row.lower().split()
                for item in item_pieces:
                    if searched_item_str.lower() in item:
                        if list_category == 'My Tasks':
                            if data_row [15] == 'task' and data_row[9] == "" and data_row[16] != 'DONE':
                                treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9]))
                        elif list_category == 'Delegated Tasks':
                            if data_row [15] == 'task' and data_row[9] != "" and data_row[16] != 'DONE':
                                treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9]))
                        elif list_category == 'Personal Cards':
                            if data_row[15] == 'personal card':
                                treeview.insert('', 'end', values=(data_row[1], data_row[12], data_row[2], data_row[3], data_row[4]))
                        elif list_category == 'Events':
                            if data_row[15] == 'event':
                                treeview.insert('', 'end', values=(data_row[1], data_row[1], data_row[2], data_row[3], data_row[4]))
                        elif list_category == 'Remarks':
                            if data_row[15] == 'remark':
                                treeview.insert('', 'end', values=(data_row[1], data_row[1], data_row[2], data_row[3], data_row[5]))
                        elif list_category == 'Ideas':
                            if data_row[15] == 'idea':
                                treeview.insert('', 'end', values=(data_row[1], data_row[1], data_row[2], data_row[3], data_row[5]))
                        elif list_category == 'Maybe/Sometimes':
                            if data_row[15] == 'maybe/sometimes':
                                treeview.insert('', 'end', values=(data_row[1], data_row[1], data_row[2], data_row[3], data_row[5]))
                        elif list_category == 'Projects':
                            if data_row[15] == 'project' and data_row[16] != 'DONE':
                                treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4], data_row[9]))
                        else:
                            pass
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")

    def project_name_does_not_exist(self, project_name):
        self.make_list_data_tuple
        rows = []
        for data_row in self.list_data_tuple:
            if data_row[8] == project_name:
                rows.append(data_row[1])
                print(data_row)
            else:
                pass
        if rows == []:
            return True
        else:
            return False