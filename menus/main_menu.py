import tkinter as tk
from .file_menu import FileMenu

class MainMenu(tk.Menu):
    def __init__(self, master, main_frame, prefix_window_title):
        super().__init__(master)
        self.main_frame = main_frame
        self.prefix_window_title = prefix_window_title
        # Add file menu
        self.file_menu = FileMenu(self, self.main_frame, self.prefix_window_title)
        self.add_cascade(label='File', menu=self.file_menu)
