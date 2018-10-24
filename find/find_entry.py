import tkinter as tk

class FindEntry(tk.Entry):
	def __init__(self, master, window):
		super().__init__(master)
		self.pack(side=tk.LEFT)
		self.window = window

	def post_init(self):
		self.add_keyboard_bindings()

	def clear(self):
		self.delete(0, tk.END)

	def add_keyboard_bindings(self):
		self.bind('<Return>', self.find_or_see_next_match)
		self.bind('<Shift-Return>', self.window.main_frame.find_frame.see_previous_match)
		# Add Escape keyboard binding for closing find frame
		self.bind('<Escape>', self.window.main_frame.find_frame.close)

	def find_or_see_next_match(self, event=None):
		find_frame = self.window.main_frame.find_frame
		if not find_frame.total_match_variable.get():
			find_frame.find(event)
		else:
			find_frame.see_next_match(event)
