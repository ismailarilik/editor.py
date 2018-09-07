import tkinter as tk
import tkinter.font as tk_font
import tkinter.filedialog as tk_filedialog
import os
import tokenize

class Editor(tk.Text):
	def __init__(self, master):
		super().__init__(master)
		self.tab_size = 4

	@property
	def tab_size(self):
		return self._tab_size

	@tab_size.setter
	def tab_size(self, new_tab_size):
		self._tab_size = new_tab_size
		font = tk_font.Font(font=self['font'])
		tab_width = font.measure(' ' * self._tab_size)
		self.config(tabs=(tab_width,))

	def get_wo_eol(self):
		'''
		Get without (automatically added) final end-of-line character
		'''
		return self.get('1.0', tk.END)[:-1]

	def set(self, text):
		self.delete('1.0', tk.END)
		self.insert(tk.END, text)

class File(object):
	def __init__(self, path):
		self.path = path

	@property
	def name(self):
		return os.path.basename(self.path)

class Title(object):
	def __init__(self, unsaved_changes_specifier, file_name, app_name, is_there_unsaved_change):
		self.unsaved_changes_specifier = unsaved_changes_specifier
		self.file_name = file_name
		self.app_name = app_name
		self.is_there_unsaved_change = is_there_unsaved_change

	def __str__(self):
		title_string = ''
		if self.is_there_unsaved_change:
			title_string += f'{self.unsaved_changes_specifier}'
		title_string += f'{self.file_name} - {self.app_name}'
		return title_string

class FileMenu(tk.Menu):
	def __init__(self, master, window):
		super().__init__(master)
		self.window = window
		self.file = None
		self.add_command(label='Open File', accelerator='Ctrl+O', command=self.open_file)
		self.add_command(label='Save File', accelerator='Ctrl+S', command=self.save_file)
		self.add_command(label='Save File as...', accelerator='Ctrl+Shift+S', command=self.save_file_as)

	def open_file(self, event=None):
		file_path = tk_filedialog.askopenfilename(filetypes=[('Python Files', '.py')])
		if file_path:
			self.file = File(file_path)
			# Set editor text with file text
			with tokenize.open(self.file.path) as file:
				self.window.editor.set(file.read())
			# Reset title because file name has been changed
			# Also unsaved changes status has been changed to False
			title = self.window.get_title()
			title.file_name = self.file.name
			title.is_there_unsaved_change = False
			self.window.set_title(title)

	def save_file(self, event=None):
		# If there is no an opened file, call save_file_as method
		# Else, write editor text to the file
		if not self.file:
			self.save_file_as()
		else:
			with open(self.file.path, 'w', encoding='UTF-8') as file:
				file.write(self.window.editor.get_wo_eol())
			# Reset title because unsaved changes status has been changed to False
			title = self.window.get_title()
			title.is_there_unsaved_change = False
			self.window.set_title(title)

	def save_file_as(self, event=None):
		file_path = tk_filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python Files', '.py')])
		if file_path:
			self.file = File(file_path)
			with open(self.file.path, 'w', encoding='UTF-8') as file:
				file.write(self.window.editor.get_wo_eol())
			# Reset title because file name has been changed
			# Also unsaved changes status has been changed to False
			title = self.window.get_title()
			title.file_name = self.file.name
			title.is_there_unsaved_change = False
			self.window.set_title(title)

class Menu(tk.Menu):
	def __init__(self, master, window):
		super().__init__(master)
		self.window = window
		# Add file menu
		self.file_menu = FileMenu(self, self.window)
		self.add_cascade(label='File', menu=self.file_menu)

class Window(tk.Tk):
	def __init__(self):
		super().__init__()
		# Set title
		unsaved_changes_specifier = '*'
		unsaved_file_name = '<unsaved_file>'
		app_name = 'Visual Python'
		title = Title(unsaved_changes_specifier, unsaved_file_name, app_name, False)
		self.set_title(title)
		# Set icon
		self.iconbitmap('icon.ico')
		# Create editor
		self.editor = Editor(self)
		self.editor.pack(fill=tk.BOTH, expand=True)
		# Add menu
		self.menu = Menu(self, self)
		self.config(menu=self.menu)
		# Resize and center the window
		self.resize_and_center()
		# Add keyboard bindings for opening file
		self.bind('<Control-KeyPress-o>', self.menu.file_menu.open_file)
		self.bind('<Control-KeyPress-O>', self.menu.file_menu.open_file)
		# Add keyboard bindings for saving file
		self.bind('<Control-KeyPress-s>', self.menu.file_menu.save_file)
		self.bind('<Control-KeyPress-S>', self.menu.file_menu.save_file)
		# Add keyboard bindings for saving file as...
		self.bind('<Control-Shift-KeyPress-s>', self.menu.file_menu.save_file_as)
		self.bind('<Control-Shift-KeyPress-S>', self.menu.file_menu.save_file_as)
		# Start window
		self.mainloop()

	def get_title(self):
		return self._title

	def set_title(self, new_title):
		self._title = new_title
		self.title(self._title)

	def resize_and_center(self):
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

Window()