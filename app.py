import tkinter as tk
from widgets.main_frame import MainFrame
from menus.main_menu import MainMenu

class App(object):
    def __init__(self):
        self.window = tk.Tk()
        # Set window title
        self.window_title = 'Visual Python'
        self.window.title(self.window_title)
        # Set window icon
        self.window.iconbitmap('icon.ico')
        # Add main frame
        self.main_frame = MainFrame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Add main menu
        self.main_menu = MainMenu(self.window, self.main_frame, prefix_window_title=self.prefix_window_title)
        self.window.config(menu=self.main_menu)

    def start(self):
        self.window.mainloop()

    def prefix_window_title(self, prefix):
        self.window.title(f'{prefix} - {self.window_title}')

if __name__ == '__main__':
    app = App()
    app.start()
