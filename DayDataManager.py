from tkinter import messagebox
import tkinter as tk
from DBManager import *

db_manager = DBManager()

class DayDataManager:
    def __init__(self):
        if not hasattr(self, 'data_tuple'):
            self.data_tuple = self.make_day_data_tuple()
        else:
            print('Data_tuple already exists')
            pass
    
    def make_day_data_tuple(self):
        self.data_tuple = db_manager.get_day_data_tuple()   # Tuple list stored as a variable - than I can take the data for treeviews 
                                                       # and check them
        print('Creating new data_tuple')
        return self.data_tuple
        # element [2]
        # time [7]
        # delegated [9]
        # category [15]
    
    def insert_data_to_treeview(self, treeview, category): 
        treeview.delete(*treeview.get_children())
        try:
            for data_row in self.data_tuple:
                if category == 'task':
                    if data_row [15] == 'task' and data_row[9] == "":
                        treeview.insert('', 'end', values=(data_row[2], data_row[7]))
                        #treeview.insert('', 'end', text=row[0:], values = row[0:])
                    else:
                        pass
                else:
                    if data_row[15] == category:
                        treeview.insert('', 'end', values=(data_row[2]))
                    else:
                        pass
            #show_number_of_day_element(db, category, date_string)            
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")
    
    def refresh_day_data_to_treeview(self, treeview, category):
        self.data_tuple = self.make_day_data_tuple()
        self.insert_data_to_treeview(treeview, category)

    def count_number_of_day_element(self, category): # no need of today date_string, data_tuple is generated for today
        try:
            number_elements = 0
            for data_row in self.data_tuple:
                if category == 'task' and data_row[15] == 'task' and data_row[9] == "":
                    number_elements += 1
                elif data_row[15] == category and category != 'task':
                    number_elements += 1
                else:
                    pass
            return number_elements
        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")


    # insert_values_to_task_form():

    # insert_values_to_event_form():

    # insert_values_to_remark_form():

#DayDataManager()