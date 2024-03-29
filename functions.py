import tkinter as tk
import requests

def check_internet(frame1, frame2):
    url = "https://www.google.com"
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        online_frame1 = tk.Frame(
            frame1,
            width = 250,
            height = 5,
            background = "#007606"
        )
        online_frame1.place(x = 8, y = 12)

        online_frame2 = tk.Frame(
            frame2,
            width = 250,
            height = 5,
            background = "#007606"
        )
        online_frame2.place(x = 8, y = 12)
    except requests.ConnectionError:
        offline_frame1 = tk.Frame(
            frame1,
            width = 250,
            height = 5,
        background = "#9B0202"
        )
        offline_frame1.place(x = 8, y = 12)

        offline_frame2 = tk.Frame(
            frame2,
            width = 250,
            height = 5,
            background = "#9B0202"
        )
        offline_frame2.place(x = 8, y = 12)

def exit_window(win_name):
    win_name.destroy()

#def find_task():
#    search_string = find_task_row.get().strip()
#    if len(search_string) != 0:
#        if search_string == "tomorrow":
#            search_string = tomorrow
#        elif search_string == "yesterday":
#            search_string = yesterday
#        else:
#            pass
#
#        clear_treeview()
#        insert_data_into_treeview()
#        items = treeview.get_children()    
#        for item in items:
#            values = treeview.item(item)['values']
#            if search_string in values[1] or search_string in values[2] or search_string in values[4] or search_string in values[6]:
#                treeview.selection_add(item)
#                treeview.focus(item)
#            elif search_string =="previous":
#                for i in range(1,356):
#                    previous_date = (now - timedelta(days=i)).strftime('%d/%m/%Y')
#                    if previous_date in values[1] or previous_date in values[2] or previous_date in values[4] or previous_date in values[6]: 
#                        treeview.selection_add(item)
#                        treeview.focus(item)
#    else:
#        messagebox.showerror("Error", "Insert task or keyword you are willing to find.")
