from MainScreen import *
from tkinter import Tk

class App:
    def __init__(self):
        self.root = Tk()
        self.main_screen = MainScreen(self.root)

    def run(self):
        self.main_screen.create_window()
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()