import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.font as tk_font
import tkinter.messagebox as tk_messagebox
import os
import tokenize

class Editor(tk.Text):
	def __init__(self, master):
		super().__init__(master, undo=True, wrap=tk.NONE)
		self.tab_size = 4
		self.add_scrollbars()
		# Handle open file event here, too, for this widget and prevent propagation of event
		# Because default behavior of this widget is not wanted here
		self.bind('<Control-KeyPress-o>', self.handle_open_file_event_and_prevent_propagation)

	@property
	def tab_size(self):
		return self._tab_size

	@tab_size.setter
	def tab_size(self, new_tab_size):
		self._tab_size = new_tab_size
		# Also configure editor tab stops with specified tab size
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

	def add_scrollbars(self):
		'''
		Add vertical and horizontal scrollbars
		'''
		vertical_scrollbar = tk.Scrollbar(self.master)
		vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		vertical_scrollbar.config(command=self.yview)
		horizontal_scrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
		horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
		horizontal_scrollbar.config(command=self.xview)
		self.config(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

	def handle_open_file_event_and_prevent_propagation(self, event=None):
		self.window.menu.file_menu.open_file(event)
		return 'break'

class File(object):
	def __init__(self, path, is_modified=False):
		self.path = path
		self.is_modified = is_modified

	@property
	def name(self):
		return os.path.basename(self.path)

class Title(object):
	def __init__(self, unsaved_changes_specifier='*', file_name='<unsaved_file>', app_name='Visual Python', is_there_unsaved_change=False):
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
		self.file = File(None)
		self.add_command(label='Open File', accelerator='Ctrl+O', command=self.open_file)
		self.add_command(label='Save File', accelerator='Ctrl+S', command=self.save_file)
		self.add_command(label='Save File as...', accelerator='Ctrl+Shift+S', command=self.save_file_as)
		self.add_separator()
		self.add_command(label='Quit', accelerator='Ctrl+Q', command=self.window.quit)

	def open_file(self, event=None):
		'''
		Return True if a file was opened
		Return False otherwise
		'''
		if self.save_unsaved_changes():
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
				title.is_there_unsaved_change = self.file.is_modified
				self.window.set_title(title)
				# Return that a file was opened
				return True
			else:
				return False
		else:
			return False

	def save_file(self, event=None):
		'''
		Return True if the file was saved
		Return False otherwise
		'''
		# If there is not any opened file, call save_file_as method
		# Else, write editor text to the file
		if not self.file.path:
			return self.save_file_as()
		else:
			with open(self.file.path, 'w', encoding='UTF-8') as file:
				file.write(self.window.editor.get_wo_eol())
			# File is unmodified now
			self.file.is_modified = False
			# Reset title because unsaved changes status has been changed to False
			title = self.window.get_title()
			title.is_there_unsaved_change = self.file.is_modified
			self.window.set_title(title)
			# Return that the file was saved
			return True

	def save_file_as(self, event=None):
		'''
		Return True if the specified file was saved
		Return False otherwise
		'''
		file_path = tk_filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python Files', '.py')])
		if file_path:
			self.file = File(file_path)
			with open(self.file.path, 'w', encoding='UTF-8') as file:
				file.write(self.window.editor.get_wo_eol())
			# Reset title because file name has been changed
			# Also unsaved changes status has been changed to False
			title = self.window.get_title()
			title.file_name = self.file.name
			title.is_there_unsaved_change = self.file.is_modified
			self.window.set_title(title)
			# Return that the specified file was saved
			return True
		else:
			return False

	def save_unsaved_changes(self):
		'''
		Return True if unsaved changes were saved
		Return False otherwise
		'''
		if self.file.is_modified:
			reply = tk_messagebox.askyesnocancel('Unsaved Changes', 'There are unsaved changes, would you like to save them?')
			if reply:
				return self.save_file()
			elif reply == False:
				return True
			else:
				return False
		else:
			return True

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
		title = Title()
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
		# Add keyboard bindings
		self.add_keyboard_bindings()
		# Register delete window protocol to save unsaved changes and handle other things properly on quit
		self.protocol('WM_DELETE_WINDOW', self.quit)
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

	def add_keyboard_bindings(self):
		# Add keyboard bindings for opening file
		self.bind('<Control-KeyPress-o>', self.menu.file_menu.open_file)
		self.bind('<Control-KeyPress-O>', self.menu.file_menu.open_file)
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

Window()