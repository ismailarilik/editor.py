import tkinter as tk
from menu.file_menu.file_menu import FileMenu
from menu.edit_menu.edit_menu import EditMenu

class Menu(tk.Menu):
	def __init__(self, master, window):
		super().__init__(master)
		self.window = window
		# Add file menu
		self.file_menu = FileMenu(self, self.window)
		self.add_cascade(label='File', menu=self.file_menu)
		# Add edit menu
		self.edit_menu = EditMenu(self, self.window)
		self.add_cascade(label='Edit', menu=self.edit_menu)
