import tkinter as tk
from main_frame import MainFrame
from menu.menu import Menu
from title import Title

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		# Set title
		title = Title()
		self.set_title(title)
		# Set icon
		self.iconbitmap('icon.ico')
		# Add menu
		self.menu = Menu(self, self)
		self.config(menu=self.menu)
		# Create main frame
		self.main_frame = MainFrame(self, self)
		# Post initialization
		self._post_init()
		# Resize and center the window
		self._resize_and_center()
		# Add keyboard bindings
		self._add_keyboard_bindings()
		# Register delete window protocol to save unsaved changes and handle other things properly on quit
		self.protocol('WM_DELETE_WINDOW', self.quit)
		# Start window
		self.mainloop()

	def _post_init(self):
		self.main_frame.editor.post_init()
		self.main_frame.find_frame.find_entry.post_init()

	def get_title(self):
		return self._title

	def set_title(self, new_title):
		self._title = new_title
		self.title(self._title)

	def _resize_and_center(self):
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

	def _add_keyboard_bindings(self):
		# Add keyboard bindings for opening file
		self.bind('<Control-KeyPress-o>', self.menu.file_menu.open_file)
		self.bind('<Control-KeyPress-O>', self.menu.file_menu.open_file)
		# Add keyboard bindings for opening folder
		self.bind('<Control-KeyPress-d>', self.menu.file_menu.open_folder)
		self.bind('<Control-KeyPress-D>', self.menu.file_menu.open_folder)
		# Add keyboard bindings for saving file
		self.bind('<Control-KeyPress-s>', self.menu.file_menu.save_file)
		self.bind('<Control-KeyPress-S>', self.menu.file_menu.save_file)
		# Add keyboard bindings for saving file as...
		self.bind('<Control-Shift-KeyPress-s>', self.menu.file_menu.save_file_as)
		self.bind('<Control-Shift-KeyPress-S>', self.menu.file_menu.save_file_as)
		# Add keyboard bindings for quitting
		self.bind('<Control-KeyPress-q>', self.quit)
		self.bind('<Control-KeyPress-Q>', self.quit)

	def quit(self, event=None):
		if self.menu.file_menu.save_unsaved_changes():
			self.destroy()

App()
