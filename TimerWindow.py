import tkinter as tk
from tkinter import messagebox
import os
import sys
from tkinter import *
import pyglet

class TimerWindow:
    def __init__(self, parent, task_name):
        self.task_name = task_name
        if self.task_name == None:
            self.task_name = ""
        
        self.timer_id = None
        script_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sound_path = os.path.join(script_dir, "Sounds", "timer_alarm.wav")
        self.sound = pyglet.media.load(sound_path)

        self.window = tk.Toplevel(parent)
        self.window.geometry("400x400+300+150")
        self.window.configure(bg="#212121")
        self.window.title('Timer')
        self.window.resizable(0,0)

    def start_timer(self):
        self.times_up_label.place_forget()
        if self.timer_id is not None:
            pass
        else:
            if (not self.required_hours_row.get().isdigit() 
                or not self.required_minutes_row.get().isdigit()
                or not self.required_seconds_row.get().isdigit()):
                messagebox.showwarning("UNABLE", "Time data must be a number")
            else:
                self.required_hours = int(self.required_hours_row.get())
                self.required_minutes = int(self.required_minutes_row.get())
                self.required_seconds = int(self.required_seconds_row.get())
                self.timer_label_hours.config(text = self.required_hours)
                self.timer_label_minutes.config(text = self.required_minutes)
                self.timer_label_seconds.config(text = self.required_seconds)
                self.update_timer()

    def stop_timer(self):
        self.window.after_cancel(self.timer_id)
        self.timer_label_hours.config(text = '00')
        self.timer_label_minutes.config(text = '00')
        self.timer_label_seconds.config(text = '00')
        self.timer_id = None

        self.required_hours_row.delete(0, 'end')
        self.required_minutes_row.delete(0, 'end')
        self.required_seconds_row.delete(0, 'end')
        self.required_hours_row.insert(0, "00")
        self.required_minutes_row.insert(0, "00")
        self.required_seconds_row.insert(0, "00")

    def update_timer(self):
        if self.required_hours > 0 or self.required_minutes > 0 or self.required_seconds > 0:
            if self.required_seconds == 0:
                if self.required_minutes > 0:
                    self.required_minutes -= 1
                    self.required_seconds = 59
                elif self.required_hours > 0:
                    self.required_hours -= 1
                    self.required_minutes = 59
                    self.required_seconds = 59
            else:
                self.required_seconds -= 1

            self.timer_label_hours.config(text=str(self.required_hours).zfill(2))
            self.timer_label_minutes.config(text=str(self.required_minutes).zfill(2))
            self.timer_label_seconds.config(text=str(self.required_seconds).zfill(2))

            self.timer_id = self.window.after(1000, self.update_timer)
        else:
            self.required_seconds = 0
            self.times_up_label.place(relx=0.5, y=275, anchor='center')
            self.timer_label_hours.config(text='00')
            self.timer_label_minutes.config(text='00')
            self.timer_label_seconds.config(text='00')
            self.timer_id = None
            
            player = pyglet.media.Player()
            player.queue(self.sound)
            player.play()

            self.required_hours_row.delete(0, 'end')
            self.required_minutes_row.delete(0, 'end')
            self.required_seconds_row.delete(0, 'end')
            self.required_hours_row.insert(0, "00")
            self.required_minutes_row.insert(0, "00")
            self.required_seconds_row.insert(0, "00")

    def create_window(self):
        header_label = tk.Label(
            self.window,
            text = 'TIMER',
            font = ('Montserrat', '20'),
            background = "#212121",
            foreground = "#00B0C4"
        )
        header_label.place(relx = 0.5, y = 25, anchor = 'center')

        self.timer_label = tk.Label(
            self.window,
            text = self.task_name,
            font = ('Montserrat', '15'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.timer_label.place(relx = 0.5, y = 60, anchor = 'center')

        self.required_time_label = tk.Label(
            self.window,
            text = "Set time: ",
            font = ('Montserrat', '12'),
            background = "#212121",
            foreground = "#00B0C4"
        )
        self.required_time_label.place(x = 20, y = 100)

        self.required_hours_row = tk.Entry(
            self.window,
            width = 4,
            font = ('Montserrat', '12'),
            background = "#212121",
            foreground = "#FFFFFF",
            insertbackground = "#FFFFFF"
        )
        self.required_hours_row.place(x = 110, y = 100)
        self.required_hours_row.insert(0, "00")

        self.time_hours_label = tk.Label(
            self.window,
            text = "hrs",
            font = ('Montserrat', '12'),
            background = "#212121",
            foreground = "#00B0C4"
        )
        self.time_hours_label.place(x = 150, y = 100)

        self.required_minutes_row = tk.Entry(
            self.window,
            width = 4,
            font = ('Montserrat', '12'),
            background = "#212121",
            foreground = "#FFFFFF",
            insertbackground = "#FFFFFF"
        )
        self.required_minutes_row.place(x = 190, y = 100)
        self.required_minutes_row.insert(0, "00")

        self.time_min_label = tk.Label(
            self.window,
            text = "min",
            font = ('Montserrat', '12'),
            background = "#212121",
            foreground = "#00B0C4"
        )
        self.time_min_label.place(x = 230, y = 100)

        self.required_seconds_row = tk.Entry(
            self.window,
            width = 4,
            font = ('Montserrat', '12'),
            background = "#212121",
            foreground = "#FFFFFF",
            insertbackground = "#FFFFFF"
        )
        self.required_seconds_row.place(x = 270, y = 100)
        self.required_seconds_row.insert(0, "00")

        self.time_sec_label = tk.Label(
            self.window,
            text = "sec",
            font = ('Montserrat', '12'),
            background = "#212121",
            foreground = "#00B0C4"
        )
        self.time_sec_label.place(x = 310, y = 100)

        self.timer_label_hours = tk.Label(
            self.window,
            text = "00",
            font = ('Montserrat', '30'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.timer_label_hours.place(relx = 0.3, y = 220, anchor = 'center')

        self.timer_label_sign1 = tk.Label(
            self.window,
            text = ":",
            font = ('Montserrat', '30'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.timer_label_sign1.place(relx = 0.4, y = 220, anchor = 'center')

        self.timer_label_minutes = tk.Label(
            self.window,
            text = "00",
            font = ('Montserrat', '30'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.timer_label_minutes.place(relx = 0.5, y = 220, anchor = 'center')

        self.timer_label_sign2 = tk.Label(
            self.window,
            text = ":",
            font = ('Montserrat', '30'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.timer_label_sign2.place(relx = 0.6, y = 220, anchor = 'center')

        self.timer_label_seconds = tk.Label(
            self.window,
            text = "00",
            font = ('Montserrat', '30'),
            background = "#212121",
            foreground = "#FFFFFF"
        )
        self.timer_label_seconds.place(relx = 0.7, y = 220, anchor = 'center')

        self.times_up_label = tk.Label(
            self.window,
            text = "TIME'S UP",
            font = ('Montserrat', '25', 'bold'),
            background = "#212121",
            foreground = "#FE0712"
        )
        self.times_up_label.place_forget()

        start_button = tk.Button(
            self.window,
            text = "START",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.start_timer,
            background = '#004C01',
            foreground = '#FFFFFF'
        )
        start_button.place(relx = 0.33, y = 360, anchor = 'center')

        stop_button = tk.Button(
            self.window,
            text = "STOP",
            font = ('Arial', '10', 'bold'),
            width = 11,
            command = self.stop_timer,
            background = '#970000',
            foreground = '#FFFFFF'
        )
        stop_button.place(relx = 0.66, y = 360, anchor = 'center')