import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.font as tk_font
import tkinter.messagebox as tk_messagebox
import io
import keyword
import os
import tokenize

class Token(object):
	def __init__(self, _type, exact_type, name, string, start_row, start_column, end_row, end_column, line):
		self.type = _type
		self.exact_type = exact_type
		self.name = name
		self.string = string
		self.start_row = start_row
		self.start_column = start_column
		self.end_row = end_row
		self.end_column = end_column
		self.line = line

class Tokenizer(object):
	# Initialize keyword token type and name
	KEYWORD = 1000
	_KEYWORD_NAME = 'KEYWORD'

	def __init__(self):
		self._keywords = keyword.kwlist

	def get_token_name(self, token_type):
		if token_type == self.KEYWORD:
			return self._KEYWORD_NAME
		return tokenize.tok_name[token_type]

	def tokenize(self, readline):
		tokens = tokenize.tokenize(readline)
		for token in tokens:
			token2 = Token(token.type, token.exact_type, tokenize.tok_name[token.exact_type], token.string, token.start[0], token.start[1], token.end[0], token.end[1], token.line)
			# Check for keyword token
			if token2.exact_type == tokenize.NAME and token2.string in self._keywords:
				token2.exact_type = token2.type = self.KEYWORD
				token2.name = self._KEYWORD_NAME
			yield token2

class Editor(tk.Text):
	def __init__(self, master, window):
		super().__init__(master, undo=True, wrap=tk.NONE)
		self.window = window
		self.tab_size = 4
		self.tokenizer = Tokenizer()
		self.token_type_color_map = {
			self.tokenizer.KEYWORD: '#FF0000',
			tokenize.STRING: '#00C000',
			tokenize.NUMBER: '#0000FF',
			tokenize.COMMENT: '#808080',
			tokenize.LPAR: '#FFC000',
			tokenize.RPAR: '#FFC000',
			tokenize.LSQB: '#FF00FF',
			tokenize.RSQB: '#FF00FF',
			tokenize.LBRACE: '#00C0C0',
			tokenize.RBRACE: '#00C0C0',
			tokenize.EQUAL: '#800000',
			tokenize.PLUSEQUAL: '#800000',
			tokenize.MINEQUAL: '#800000',
			tokenize.STAREQUAL: '#800000',
			tokenize.DOUBLESTAREQUAL: '#800000',
			tokenize.SLASHEQUAL: '#800000',
			tokenize.DOUBLESLASHEQUAL: '#800000',
			tokenize.PERCENTEQUAL: '#800000',
			tokenize.ATEQUAL: '#800000',
			tokenize.VBAREQUAL: '#800000',
			tokenize.AMPEREQUAL: '#800000',
			tokenize.CIRCUMFLEXEQUAL: '#800000',
			tokenize.LEFTSHIFTEQUAL: '#800000',
			tokenize.RIGHTSHIFTEQUAL: '#800000',
			tokenize.PLUS: '#000080',
			tokenize.MINUS: '#000080',
			tokenize.STAR: '#000080',
			tokenize.DOUBLESTAR: '#000080',
			tokenize.SLASH: '#000080',
			tokenize.DOUBLESLASH: '#000080',
			tokenize.PERCENT: '#000080',
			tokenize.AT: '#000080',
			tokenize.VBAR: '#000080',
			tokenize.AMPER: '#000080',
			tokenize.TILDE: '#000080',
			tokenize.CIRCUMFLEX: '#000080',
			tokenize.LEFTSHIFT: '#000080',
			tokenize.RIGHTSHIFT: '#000080',
			tokenize.LESS: '#808000',
			tokenize.GREATER: '#808000',
			tokenize.EQEQUAL: '#808000',
			tokenize.NOTEQUAL: '#808000',
			tokenize.LESSEQUAL: '#808000',
			tokenize.GREATEREQUAL: '#808000',
			tokenize.DOT: '#800080',
			tokenize.COMMA: '#8000FF',
			tokenize.COLON: '#8080FF',
			tokenize.SEMI: '#FF0080',
			tokenize.RARROW: '#FF8080',
			tokenize.ELLIPSIS: '#FF80FF'
		}
		self.add_scrollbars()
		# Set a flag to ensure modified callback being called only by a change
		self.modified_event_occurred_by_change = True
		# Listen for modified event
		self.bind('<<Modified>>', self.modified)
		# Pack this widget
		self.pack(fill=tk.BOTH, expand=True)

	def post_init(self):
		self.file = self.window.menu.file_menu.file
		self.add_keyboard_bindings()

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

	def modified(self, event):
		if self.modified_event_occurred_by_change:
			self.highlight()
			# File is modified now, so set related flag
			# Also reset title because unsaved changes status has been changed to True
			# Do they only if they were not set before, for a better performance
			if not self.file.is_modified:
				self.file.is_modified = True
				title = self.window.get_title()
				title.is_there_unsaved_change = self.file.is_modified
				self.window.set_title(title)
			# Call this method to set modified flag to False so following modification may cause modified event occurred
			self.edit_modified(False)
		# Switch this flag which is for to ensure modified callback being called only by a change
		# Because changing modified flag above causes modified event occurred
		self.modified_event_occurred_by_change = not self.modified_event_occurred_by_change

	def highlight(self):
		tokens = []
		text = self.get('1.0', tk.END)
		tokens2 = self.tokenizer.tokenize(io.BytesIO(text.encode('UTF-8')).readline)
		try:
			for token in tokens2:
				tokens.append(token)
		except Exception as exception:
			print('An error occurred while tokenizing code for highlighting:')
			print(exception)
		else:
			# Remove previous tags, otherwise they will conflict with new ones
			self.tag_delete(*self.tag_names())
			# Configure tag colors
			for token_type, token_color in self.token_type_color_map.items():
				self.tag_config(self.tokenizer.get_token_name(token_type), foreground=token_color)
			for token in tokens:
				# If there is a configured tag for this token, add it to the token's indices in the editor
				color = self.token_type_color_map.get(token.exact_type)
				if color:
					start_index = f'{token.start_row}.{token.start_column}'
					end_index = f'{token.end_row}.{token.end_column}'
					self.tag_add(token.name, start_index, end_index)

	def add_keyboard_bindings(self):
		# Add keyboard bindings for finding
		self.bind('<Control-KeyPress-f>', self.window.menu.edit_menu.find)
		self.bind('<Control-KeyPress-F>', self.window.menu.edit_menu.find)
		# Add Escape keyboard binding for escaping from things in editor
		self.bind('<Escape>', self.escape)
		# Handle open file event here, too, for this widget and prevent propagation of event
		# Because default behavior of this widget is not wanted here
		self.bind('<Control-KeyPress-o>', self.handle_open_file_event_and_prevent_propagation)

	def escape(self, event=None):
		# Close find frame
		self.window.main_frame.find_frame.close(event)

	def handle_open_file_event_and_prevent_propagation(self, event=None):
		self.window.menu.file_menu.open_file(event)
		return 'break'

class FindEntry(tk.Entry):
	def __init__(self, master, window):
		super().__init__(master)
		self.pack(side=tk.LEFT)
		self.window = window
	
	def post_init(self):
		self.add_keyboard_bindings()

	def add_keyboard_bindings(self):
		# Add Escape keyboard binding for closing find frame
		self.bind('<Escape>', self.window.main_frame.find_frame.close)

class FindFrame(tk.Frame):
	def __init__(self, master, window):
		super().__init__(master)
		self.window = window
		self.create_widgets()

	def create_widgets(self):
		self.find_entry = FindEntry(self, self.window)
		# Create current match label
		self.current_match_label = tk.Label(self, text='0')
		self.current_match_label.pack(side=tk.LEFT)
		# Create separator label
		self.separator_label = tk.Label(self, text='/')
		self.separator_label.pack(side=tk.LEFT)
		# Create total match label
		self.total_match_label = tk.Label(self, text='0')
		self.total_match_label.pack(side=tk.LEFT)
		# Create previous match button
		self.previous_match_button = tk.Button(self, text='<')
		self.previous_match_button.pack(side=tk.LEFT)
		# Create next match button
		self.next_match_button = tk.Button(self, text='>')
		self.next_match_button.pack(side=tk.LEFT)
		# Create close button
		self.close_button = tk.Button(self, text='X', command=self.close)
		self.close_button.pack(side=tk.LEFT)

	def close(self, event=None):
		self.place_forget()
		self.window.main_frame.editor.focus_set()

class MainFrame(tk.Frame):
	def __init__(self, master, window):
		super().__init__(master)
		self.pack(fill=tk.BOTH, expand=True)
		self.window = window
		self.editor = Editor(self, self.window)
		self.find_frame = FindFrame(self, self.window)

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

	def post_init(self):
		self.editor = self.window.main_frame.editor

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
					self.editor.set(file.read())
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
				file.write(self.editor.get_wo_eol())
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
				file.write(self.editor.get_wo_eol())
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

class EditMenu(tk.Menu):
	def __init__(self, master, window):
		super().__init__(master)
		self.window = window
		# Add find command
		self.add_command(label='Find', accelerator='Ctrl+F', command=self.find)

	def find(self, event=None):
		self.window.main_frame.find_frame.place(relx=1.0, anchor=tk.NE)
		self.window.main_frame.find_frame.find_entry.focus_set()

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

class Window(tk.Tk):
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
		self.menu.file_menu.post_init()
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