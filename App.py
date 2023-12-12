from tkinter import Tk
from MainScreen import *
from LoginForm import *

class App:
    def __init__(self):
        self.root = Tk()
        self.login_form = LoginForm(self.root)

    def run(self):
        self.login_form.show_login_window()
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()