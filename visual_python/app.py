import tkinter as tk
from .widgets.main_frame import MainFrame
from .menus.main_menu import MainMenu

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set app title
        # Also prefix app title with unsaved file specifier
        self.app_title = 'Visual Python'
        self.title(f'(Unsaved File) - {self.app_title}')
        # Set app icon
        self.iconbitmap('icon.ico')
        # Add main frame
        self.main_frame = MainFrame(self, self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Add main menu
        self.main_menu = MainMenu(self, self)
        self.config(menu=self.main_menu)

    def start(self):
        self.mainloop()
