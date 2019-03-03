import tkinter as tk

class EditComponent(object):
	def __init__(self):
		pass

	def post_init(self, find_frame):
		self.find_frame = find_frame

	def find(self, event=None):
		self.find_frame.place(relx=1, anchor=tk.NE)
		self.find_frame.find_entry.focus_set()
		self.find_frame.find_entry.select_range(0, tk.END)
