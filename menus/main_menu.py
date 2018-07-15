import tkinter as tk
from .file_menu import FileMenu

class MainMenu(tk.Menu):
    def __init__(self, master, main_frame):
        super().__init__(master)
        self.main_frame = main_frame
        # Add file menu
        self.file_menu = FileMenu(self, self.main_frame)
        self.add_cascade(label='File', menu=self.file_menu)
