import tkinter as tk

class EditMenu(tk.Menu):
	def __init__(self, master, window):
		super().__init__(master)
		self.window = window
		# Add find command
		self.add_command(label='Find', accelerator='Ctrl+F', command=self.find)

	def find(self, event=None):
		self.window.main_frame.find_frame.place(relx=1, anchor=tk.NE)
		self.window.main_frame.find_frame.find_entry.focus_set()
		self.window.main_frame.find_frame.find_entry.select_range(0, tk.END)
