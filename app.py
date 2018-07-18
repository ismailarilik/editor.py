import tkinter as tk
from widgets.main_frame import MainFrame
from menus.main_menu import MainMenu

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set app title
        self.app_title = 'Visual Python'
        self.title(self.app_title)
        # Set app icon
        self.iconbitmap('icon.ico')
        # Add main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Add main menu
        self.main_menu = MainMenu(self, self.main_frame, prefix_app_title=self.prefix_app_title)
        self.config(menu=self.main_menu)

    def start(self):
        self.mainloop()

    def prefix_app_title(self, prefix):
        self.title(f'{prefix} - {self.app_title}')

if __name__ == '__main__':
    app = App()
    app.start()
