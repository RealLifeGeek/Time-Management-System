from tkinter import Tk
import bcrypt
from DBManager import *
from DataFormObject import UserForm
from MainScreen import *

db_manager = DBManager()
user = UserForm()

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.password = None
        self.new_password = None
        self.login_window = None
        self.title = 'login'

    def change_title(self):
        if self.title == 'login':
            self.title = 'register'
        else:
            self.title = 'login'

    def get_user_data(self):
        user.user_id = db_manager.generate_element_id('User')
        user.firstName = self.first_name_row.get()
        user.lastName = self.last_name_row.get()
        user.user_email = self.user_email_row.get()
        user.hashed_password = self.hash_password(self.password_row.get())

    def register_new_user(self):
        self.get_user_data()
        db_manager.save_user_to_db(user)

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    def check_password(self, input_password, hashed_password):
        return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

    def exit(self):
        self.root.destroy()

    def authenticate_user(self, user_email, password):
        if len(self.user_email_row.get()) == 0 or len(self.password_row.get()) == 0:
            messagebox.showwarning("UNABLE", "Enter e-mail and password")
        else:
            result = db_manager.get_hashed_password(user_email)
            if result:
                hashed_password = result[0]
                if self.check_password(password, hashed_password):
                    self.create_main_screen()
                else:
                    messagebox.showwarning("UNABLE", "The password or user email are not correct")
            else:
                messagebox.showwarning("UNABLE", "The user is not registered")

    def show_login_window(self):
        self.login_window = self.create_login_window()
    
    def show_register_window(self, event):
        self.change_title()
        self.login_window = self.create_login_window()

    def back_to_login(self):
        self.change_title()
        self.first_name_row.delete(0, 'end')
        self.last_name_row.delete(0, 'end')
        self.user_email_row.delete(0, 'end')
        self.user_email_row.insert(0, '@')
        self.password_row.delete(0, 'end')
        self.first_name_row.place_forget()
        self.last_name_row.place_forget()
        self.first_name_label.place_forget()
        self.last_name_label.place_forget()
        self.back_to_login_text.place_forget()
        self.text1_label.place(relx = 0.5, y = 180, anchor = 'center')
        self.text1_label.configure(text = 'NAVIGATE YOURSELF')
        self.text2_label.place(x = 150, y = 195)
        self.sign_in_text1.place(x = 60, y = 480)
        self.sign_in_text2.place(x = 280, y = 479)
        self.log_in_button.configure(text = 'LOG IN')
        self.log_in_button.configure(command = self.log_in)

    def back_to_login_on_click(self, event):
        self.back_to_login()

    def sign_up(self):
        if len(self.first_name_row.get()) == 0 or len(self.last_name_row.get()) == 0 or len(self.user_email_row.get()) == 0 or len(self.password_row.get()) == 0:
            messagebox.showwarning("ERROR", "Fill the rows")
        else:
            self.get_user_data()
            db_manager.save_user_to_db(user)
            self.back_to_login()
    
    def log_in(self):
        user_email = self.user_email_row.get()
        password = self.password_row.get()
        self.authenticate_user(user_email, password)
            

    def create_login_window(self):
        self.root.geometry ("400x600+300+50")
        self.root.title("TIME MANAGEMENT SYSTEM")
        self.root.resizable(0,0)
        self.root.configure(bg = "#212121")

        if self.title == 'login':

            self.text1_label = tk.Label(
                self.root,
                text = 'NAVIGATE YOURSELF',
                font = ('Montserrat', '20', 'bold'),
                background = "#212121",
                foreground = "#00B0C4"
            )
            self.text1_label.place(relx = 0.5, y = 180, anchor = 'center')

            self.text2_label = tk.Label(
                self.root,
                text = 'Life is a journey',
                font = ('Montserrat', '20'),
                background = "#212121",
                foreground = "#FFFFFF"
            )
            self.text2_label.place(x = 150, y = 195)

            user_email_label = tk.Label(
                self.root,
                text = 'E-mail',
                font = ('Montserrat', '12'),
                background = "#212121",
                foreground = "#FFFFFF"
            )
            user_email_label.place(x = 15, y = 260)

            self.user_email_row = tk.Entry(
                self.root,
                font = ("Open Sans", "15"),
                width = 33,
                insertbackground = "#FFFFFF",
                background = "#212121",
                foreground = "#FFFFFF"
            )
            self.user_email_row.place(x = 15, y = 290)
            self.user_email_row.insert(0, '@')

            password_label = tk.Label(
                self.root,
                text = 'Password',
                font = ('Montserrat', '12'),
                background = "#212121",
                foreground = "#FFFFFF"
            )
            password_label.place(x = 15, y = 330)

            self.password_row = tk.Entry(
                self.root,
                show = '*',
                font = ("Open Sans", "15"),
                width = 33,
                insertbackground = "#FFFFFF",
                background = "#212121",
                foreground = "#FFFFFF"
            )
            self.password_row.place(x = 15, y = 360)

            self.log_in_button = tk.Button(
                self.root,
                text = 'LOG IN',
                font = ('Montserrat', '12'),
                width = 25,
                command = self.log_in,
                background = "#00B0C4",
                foreground = "#FFFFFF"
            )
            self.log_in_button.place(relx = 0.5, y = 440, anchor = 'center')

            self.sign_in_text1 = tk.Label(
                self.root,
                text = 'Don\'t have an accoount yet? Register',
                font = ('Montserrat', '10'),
                background = "#212121",
                foreground = "#FFFFFF"
            )
            self.sign_in_text1.place(x = 60, y = 480)

            self.sign_in_text2 = tk.Label(
                self.root,
                text = 'here',
                font = ('Montserrat', '11', 'bold'),
                background = "#212121",
                foreground = "#0229BB",
            )
            self.sign_in_text2.place(x = 280, y = 479)
            self.sign_in_text2.bind("<Button-1>", self.show_register_window)

            text3_label = tk.Label(
                self.root,
                text = 'Have a plan and stick to it',
                font = ('Montserrat', '12', 'italic'),
                background = "#212121",
                foreground = "#00B0C4"
            )
            text3_label.place(x = 15, y = 570)
        
        else:
            self.text1_label.place(relx = 0.5, y = 70, anchor = 'center')
            self.text1_label.configure(text = 'REGISTER YOURSELF')
            self.text2_label.place_forget()
            self.sign_in_text1.place_forget()
            self.sign_in_text2.place_forget()
            self.log_in_button.configure(text = 'SIGN UP')
            self.log_in_button.configure(command = self.sign_up)

            self.first_name_label = tk.Label(
                self.root,
                text = 'First Name',
                font = ('Montserrat', '12'),
                background = "#212121",
                foreground = "#FFFFFF"
            )
            self.first_name_label.place(x = 15, y = 120)

            self.first_name_row = tk.Entry(
                self.root,
                font = ("Open Sans", "15"),
                width = 33,
                insertbackground = "#FFFFFF",
                background = "#212121",
                foreground = "#FFFFFF"
            )
            self.first_name_row.place(x = 15, y = 150)

            self.last_name_label = tk.Label(
                self.root,
                text = 'Last Name',
                font = ('Montserrat', '12'),
                background = "#212121",
                foreground = "#FFFFFF"
            )
            self.last_name_label.place(x = 15, y = 190)

            self.last_name_row = tk.Entry(
                self.root,
                font = ("Open Sans", "15"),
                width = 33,
                insertbackground = "#FFFFFF",
                background = "#212121",
                foreground = "#FFFFFF"
            )
            self.last_name_row.place(x = 15, y = 220)

            self.back_to_login_text = tk.Label(
                self.root,
                text = 'Back to Login',
                font = ('Montserrat', '11', 'bold'),
                background = "#212121",
                foreground = "#0229BB",
            )
            self.back_to_login_text.place(x = 280, y = 500)
            self.back_to_login_text.bind("<Button-1>", self.back_to_login_on_click)


    def create_main_screen(self):
        main_screen = MainScreen(self.root)
        main_screen.create_window()
        self.login_window.destroy()
    
    def create_main_screen_on_enter_click(self, event):
        self.create_main_screen()
        
