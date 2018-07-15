import tkinter as tk
from .file_menu import FileMenu

class MainMenu(tk.Menu):
    def __init__(self, master=None):
        super().__init__(master)
        # Add file menu
        self.file_menu = FileMenu(self)
        self.add_cascade(label='File', menu=self.file_menu)
