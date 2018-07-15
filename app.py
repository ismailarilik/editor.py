import tkinter as tk
from widgets.main_frame import MainFrame
from menus.main_menu import MainMenu

class App(object):
    def __init__(self):
        self.window = tk.Tk()
        # Set window title
        self.window.title('Visual Python')
        # Set window icon
        self.window.iconbitmap('icon.ico')
        # Add main frame
        self.main_frame = MainFrame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Add main menu
        self.main_menu = MainMenu(self.window, self.main_frame)
        self.window.config(menu=self.main_menu)

    def start(self):
        self.window.mainloop()

if __name__ == '__main__':
    app = App()
    app.start()
