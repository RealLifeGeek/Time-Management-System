from tkinter import messagebox
import tkinter as tk
from DBManager import *
from DataFormObject import *

db_manager = DBManager()
data = DataForm()

class DataStoreManager:
    def __init__(self):
        self.day_data_tuple = ()
        self.list_data_tuple = ()
    
    def make_day_data_tuple(self):
        self.day_data_tuple = db_manager.get_day_data_tuple()   # Tuple for day data on MainScreen
        return self.day_data_tuple

    def make_list_data_tuple(self): # Tuple for ListWindow
        self.list_data_tuple = db_manager.get_list_data_tuple()
        return self.list_data_tuple

    def insert_day_data_to_treeview(self, treeview, category): # Inserting data to treeviews on MainScreen
        treeview.delete(*treeview.get_children())
        try:
            for data_row in self.day_data_tuple:
                if category == 'task':
                    if data_row [15] == 'task' and data_row[9] == "":
                        treeview.insert('', 'end', values=(data_row[2], data_row[7]))
                    else:
                        pass
                else:
                    if data_row[15] == category:
                        treeview.insert('', 'end', values=(data_row[2],))
                    else:
                        pass          
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")

    def insert_list_data_to_treeview(self, treeview, list_category): # Inserting data to treeviews in ListWindow
        treeview.delete(*treeview.get_children())
        try:
            for data_row in self.list_data_tuple:
                if list_category == 'My Tasks':
                    if data_row [15] == 'task' and data_row[9] == "":
                        treeview.insert('', 'end', values=(data_row[2], data_row[3], data_row[4], data_row[9]))
                elif list_category == 'Delegated Tasks':
                    if data_row [15] == 'task' and data_row[9] != "":
                        treeview.insert('', 'end', values=(data_row[2], data_row[3], data_row[4], data_row[9]))
                elif list_category == 'Projects':
                    if data_row [15] == 'project':
                        treeview.insert('', 'end', values=(data_row[2], data_row[3], data_row[4], data_row[9]))
                elif list_category == 'People Cards':
                    if data_row[15] == 'personal card':
                        treeview.insert('', 'end', values=(data_row[12], data_row[2], data_row[3], data_row[4]))
                elif list_category == 'Events':
                    if data_row[15] == 'event':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4]))
                elif list_category == 'Remarks':
                    if data_row[15] == 'remark':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[5]))
                elif list_category == 'Ideas':
                    if data_row[15] == 'idea':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[5]))
                elif list_category == 'Maybe/Sometimes':
                    if data_row[15] == 'maybe/sometimes':
                        treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[5]))
                else:
                    pass
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")

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

    def check_elementid_in_tuple(self, element_id):
        if self.day_data_tuple == () and self.list_data_tuple == ():
            print('Data_tuple empty')
            self.day_data_tuple = self.make_day_data_tuple()
            self.list_data_tuple = self.make_list_data_tuple()
        else:
            print('Data tuple exists')
        for day_data_row in self.day_data_tuple:
            if element_id in day_data_row:
                return day_data_row
        for list_data_row in self.list_data_tuple:
            if element_id in list_data_row:
                print(list_data_row)
                return list_data_row
            
    def get_data_row_from_list_data_tuple(self, element_id):
        for data_row in self.list_data_tuple:
            if element_id in data_row:
                print(data_row)
                return data_row
            else:
                pass

    def insert_values_to_task_form(self, element_id, win, row1, row2, row3, row4, row5, row6, row7, row8, row9):
        data_row = self.check_elementid_in_tuple(element_id)

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
                            if data_row [15] == 'task' and data_row[9] == "":
                                treeview.insert('', 'end', values=(data_row[2], data_row[3], data_row[4], data_row[9]))
                        elif list_category == 'Delegated Tasks':
                            if data_row [15] == 'task' and data_row[9] != "":
                                treeview.insert('', 'end', values=(data_row[2], data_row[3], data_row[4], data_row[9]))
                        elif list_category == 'People Cards':
                            if data_row[15] == 'personal card':
                                treeview.insert('', 'end', values=(data_row[12], data_row[2], data_row[3], data_row[4]))
                        elif list_category == 'Events':
                            if data_row[15] == 'event':
                                treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[4]))
                        elif list_category == 'Remarks':
                            if data_row[15] == 'remark':
                                treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[5]))
                        elif list_category == 'Ideas':
                            if data_row[15] == 'idea':
                                treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[5]))
                        elif list_category == 'Maybe/Sometimes':
                            if data_row[15] == 'maybe/sometimes':
                                treeview.insert('', 'end', values=(data_row[1], data_row[2], data_row[3], data_row[5]))
                        else:
                            pass
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
