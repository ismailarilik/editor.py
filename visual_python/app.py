import tkinter as tk
import tkinter.messagebox as tk_messagebox
from .widgets.main_frame import MainFrame
from .menus.main_menu import MainMenu

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set app title
        # Also prefix app title with unsaved file specifier
        self.app_title = 'Visual Python'
        self.title(f'(unsaved_file) - {self.app_title}')
        # Set app icon
        self.iconbitmap('icon.ico')
        # Register delete window protocol to handle things properly on quit
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        # Add main frame
        self.main_frame = MainFrame(self, self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Add main menu
        self.main_menu = MainMenu(self, self)
        self.config(menu=self.main_menu)
        # Set size and center window
        self.set_window_size_and_center_window()

    def set_window_size_and_center_window(self):
        '''
        Set window size as half of screen size
        Also center window
        '''
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        window_x = (screen_width // 2) - (window_width // 2)
        window_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

    def start(self):
        self.mainloop()

    def on_quit(self):
        # If there are unsaved changes, warn user about that
        # Otherwise, destroy the app as usual
        if self.title().startswith('*'):
            reply = tk_messagebox.askyesnocancel(
                'Unsaved Changes',
                'There are unsaved changes, would you like to save them?',
                parent=self
            )
            # If user choose to save, save the file and destroy the app
            # If user choose not to save, just destroy the app
            # If user cancel quitting, do nothing
            if reply:
                self.main_menu.file_menu.save_file()
                self.destroy()
            elif reply == False:
                self.destroy()
            else:
                pass
        else:
            self.destroy()
