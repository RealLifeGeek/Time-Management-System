import tkinter as tk
from RevisionWindow import *

class RevisionChoiceWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.geometry('170x130+600+300')
        self.window.title('REVISION CHOICE')
        self.window.option_add('*Dialog.msg.title.bg', '#000000')
        self.window.configure(bg = "#AFAFAF")
        self.window.resizable(0,0)

    def show_day_revision_window(self):
        title = 'day'
        day_revision_window = RevisionWindow(None, title)
        day_revision_window.create_window()
        self.exit()

    def show_week_revision_window(self):
        title = 'week'
        week_revision_window = RevisionWindow(None, title)
        week_revision_window.create_window()
        self.exit()

    def show_month_revision_window(self):
        title = 'month'
        month_revision_window = RevisionWindow(None, title)
        month_revision_window.create_window()
        self.exit()

    def exit(self):
        self.window.destroy()
    
    def create_window(self):
        day_revision_button = tk.Button(
            self.window,
            text = "DAY REVISION",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.show_day_revision_window,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        day_revision_button.place(x=15, y=10)

        week_revision_button = tk.Button(
            self.window,
            text = "WEEK REVISION",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.show_week_revision_window,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        week_revision_button.place(x=15, y=50)

        month_revision_button = tk.Button(
            self.window,
            text = "MONTH REVISION",
            font = ('Arial', '10', 'bold'),
            width = 16,
            command = self.show_month_revision_window,
            background = '#02266A',
            foreground = '#FFFFFF'
        )
        month_revision_button.place(x=15, y=90)