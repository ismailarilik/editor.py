import tkinter as tk
from .file_menu import FileMenu

class MainMenu(tk.Menu):
    def __init__(self, master, main_frame, prefix_app_title):
        super().__init__(master)
        self.main_frame = main_frame
        self.prefix_app_title = prefix_app_title
        # Add file menu
        self.file_menu = FileMenu(self, self.main_frame, self.prefix_app_title)
        self.add_cascade(label='File', menu=self.file_menu)
