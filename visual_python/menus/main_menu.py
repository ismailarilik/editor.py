import tkinter as tk
from .file_menu import FileMenu

class MainMenu(tk.Menu):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        # Add file menu
        self.file_menu = FileMenu(self, self.app)
        self.add_cascade(label='File', menu=self.file_menu)
