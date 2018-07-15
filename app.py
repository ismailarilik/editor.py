import tkinter as tk
from main_frame import MainFrame

class App(object):
    def __init__(self):
        self.window = tk.Tk()
        # Set window title
        self.window.title('Visual Python')
        # Set window icon
        self.window.iconbitmap('icon.ico')
        # Add main frame
        self.main_frame = MainFrame(self.window)

    def start(self):
        self.window.mainloop()

app = App()
app.start()
