import tkinter as tk
import tkinter.font as tk_font
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox
import keyword
import tokenize
import enum
import io
import os

class Token(object):
	def __init__(self, type, exact_type, name, string, start_row, start_column, end_row, end_column, line):
		self.type = type
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
		for _token in tokens:
			token = Token(_token.type, _token.exact_type, tokenize.tok_name[_token.exact_type], _token.string, _token.start[0], _token.start[1], _token.end[0], _token.end[1], _token.line)
			# Check for keyword token
			if token.exact_type == tokenize.NAME and token.string in self._keywords:
				token.type = self.KEYWORD
				token.exact_type = token.type
				token.name = self._KEYWORD_NAME
			yield token

class Editor(tk.Text):
	def __init__(self, window):
		super().__init__(undo=True, wrap=tk.NONE)
		self.window = window
		self.is_modified = False
		# Initialize tab size property
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
		# Set vertical and horizontal scrollbars
		vertical_scrollbar = tk.Scrollbar(self.master)
		vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		vertical_scrollbar.config(command=self.yview)
		horizontal_scrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
		horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
		horizontal_scrollbar.config(command=self.xview)
		self.config(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
		# Set a flag to ensure modified callback being called only by a change
		self.modified_event_occurred_by_change = True
		# Listen for modified event
		self.bind('<<Modified>>', self.modified)
		# Handle open file event here, too for this widget and prevent propagation of event
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
		tab_width = font.measure(' ' * self.tab_size)
		self.config(tabs=(tab_width,))

	def get_wo_eol(self):
		'''
		Get without (automatically added) final end-of-line character
		'''
		return self.get('1.0', tk.END)[:-1]

	def set(self, text):
		self.delete('1.0', tk.END)
		self.insert(tk.END, text)

	def modified(self, event):
		if self.modified_event_occurred_by_change:
			self.is_modified = True
			self.colorize()
			# Prefix current title with asterisk if it is not exist
			title = self.window.title()
			title = title if title.startswith('*') else f'*{title}'
			self.window.title(title)
			# Call this method to set modified flag to False so following modification may cause modified event occurred
			self.edit_modified(False)
		# Switch this flag, because changing modified flag above causes modified event occurred
		self.modified_event_occurred_by_change = not self.modified_event_occurred_by_change

	def colorize(self):
		# Remove previous tags, otherwise they will conflict with new ones
		self.tag_delete(*self.tag_names())
		# Configure tag colors
		for token_type, token_color in self.token_type_color_map.items():
			self.tag_config(self.tokenizer.get_token_name(token_type), foreground=token_color)
		text = self.get('1.0', tk.END)
		try:
			tokens = self.tokenizer.tokenize(io.BytesIO(text.encode('UTF-8')).readline)
			for token in tokens:
				# If there is a configured tag for this token, add it to the token's indices in the editor
				color = self.token_type_color_map.get(token.exact_type)
				if color:
					start_index = f'{token.start_row}.{token.start_column}'
					end_index = f'{token.end_row}.{token.end_column}'
					self.tag_add(token.name, start_index, end_index)
		except:
			pass

	def handle_open_file_event_and_prevent_propagation(self, event):
		self.window.handle_open_file_event(event)
		return 'break'

class Window(tk.Tk):
	def __init__(self):
		super().__init__()
		# Initialize opened file path property
		self.opened_file_path = None
		# Set title
		self.title('<unsaved_file> - Visual Python')
		# Set icon
		self.iconbitmap('icon.ico')
		# Create menu
		self.menu = tk.Menu()
		self.config(menu=self.menu)
		# Create file menu
		self.file_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label='File', menu=self.file_menu)
		self.file_menu.add_command(label='Open File', accelerator='Ctrl+O', command=self.open_file)
		self.file_menu.add_command(label='Save File', accelerator='Ctrl+S', command=self.save_file)
		self.file_menu.add_command(label='Save File as...', accelerator='Ctrl+Shift+S', command=self.save_file_as)
		# Create edit menu
		self.edit_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label="Edit",menu=self.edit_menu)
		self.edit_menu.add_command(label="Find",command=self.find_gui)
		# Create editor
		self.editor = Editor(self)
		self.editor.pack(fill=tk.BOTH, expand=True)
		# Create a frame for find and replace
		self.find_frame=tk.Frame(self)
		# Set window size as half of screen size
		# Also center window
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		window_width = screen_width // 2
		window_height = screen_height // 2
		window_x = (screen_width // 2) - (window_width // 2)
		window_y = (screen_height // 2) - (window_height // 2)
		self.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
		# Bind keyboard shortcuts
		# For open file
		self.bind('<Control-KeyPress-o>', self.handle_open_file_event)
		self.bind('<Control-KeyPress-O>', self.handle_open_file_event)
		# For save file
		self.bind('<Control-KeyPress-s>', self.handle_save_file_event)
		self.bind('<Control-KeyPress-S>', self.handle_save_file_event)
		# For save file as
		self.bind('<Control-Shift-KeyPress-s>', self.handle_save_file_as_event)
		self.bind('<Control-Shift-KeyPress-S>', self.handle_save_file_as_event)
		# For find
		self.bind('<Control-KeyPress-f>',self.handle_find_event)
		self.bind('<Control-KeyPress-F>',self.handle_find_event)
		self.bind('<F3>',self.handle_find_event)
		# Register delete window protocol to handle things properly on quit
		self.protocol('WM_DELETE_WINDOW', self.on_quit)
		# Start window
		self.mainloop()

	def handle_open_file_event(self, event):
		self.open_file()

	def handle_save_file_event(self, event):
		self.save_file()

	def handle_save_file_as_event(self, event):
		self.save_file_as()

	def handle_find_event(self,event):
		self.find_gui()

	def open_file(self):
		if self.on_close_file():
			opened_file_path = tk_filedialog.askopenfilename(filetypes=[('Python Files', '.py')])
			if opened_file_path:
				self.opened_file_path = opened_file_path
				# Set editor text with file content
				with tokenize.open(self.opened_file_path) as file:
					self.editor.set(file.read())
				# Prefix window title with opened file name
				opened_file_name = os.path.basename(self.opened_file_path)
				self.title(f'{opened_file_name} - Visual Python')
				return True
		return False

	def save_file(self):
		# If a file was not opened before, call save_file_as method
		# Else, write editor text to the file
		if not self.opened_file_path:
			return self.save_file_as()
		with open(self.opened_file_path, 'w', encoding='UTF-8') as file:
			file.write(self.editor.get_wo_eol())
		# Prefix window title with opened file name
		opened_file_name = os.path.basename(self.opened_file_path)
		self.title(f'{opened_file_name} - Visual Python')
		return True

	def save_file_as(self):
		opened_file_path = tk_filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python Files', '.py')])
		if opened_file_path:
			self.opened_file_path = opened_file_path
			with open(self.opened_file_path, 'w', encoding='UTF-8') as file:
				file.write(self.editor.get_wo_eol())
			# Prefix window title with opened file name
			opened_file_name = os.path.basename(self.opened_file_path)
			self.title(f'{opened_file_name} - Visual Python')
			return True
		return False

	def find_gui(self):
		entry=tk.Entry(self.find_frame)
		buton=tk.Button(self.find_frame,text="Find")
		quit_find_frame=tk.Button(self.find_frame,text="X")
		first="1.0"
		def configure(event):
			self.update_idletasks()
			self.find_frame.place_forget()
			self.find_frame.place(x=(self.editor.winfo_width()-self.find_frame.winfo_width()),y=0)
		def nothing(event):
			pass
		def buton_command():
			nonlocal first
			first=self.editor.index(self.find(entry.get(),first))
		def quit_find_frame_command():
			self.bind("<Configure>",nothing)
			self.find_frame.place_forget()
			self.editor.tag_delete("selected")
		buton.config(command=buton_command)
		quit_find_frame.config(command=quit_find_frame_command)
		entry.grid(row=0,column=1)
		buton.grid(row=0,column=2)
		quit_find_frame.grid(row=0,column=3)
		self.update()
		self.find_frame.place(x=(self.editor.winfo_width()-self.find_frame.winfo_width()),y=0)
		self.update_idletasks()
		quit_find_frame_command()
		self.find_frame.place(x=(self.editor.winfo_width()-self.find_frame.winfo_width()),y=0)
		self.bind("<Configure>",configure)

	def find(self,expression,first):
		countVar=tk.StringVar()
		pos=self.editor.search(expression,first,stopindex=tk.END,count=countVar)
		if(pos):
			countVar.get()
			self.editor.tag_delete("selected")
			self.editor.tag_add("selected",pos,f"{pos}+{countVar.get()}c")
			self.editor.tag_configure("selected",background="black",foreground="white")
			self.editor.see(pos)
			return f"{pos}+{countVar.get()}c"
		else:
			return "1.0"

	def on_close_file(self):
		if self.editor.is_modified:
			reply = tk_messagebox.askyesnocancel('Unsaved Changes', 'There are unsaved changes, would you like to save them?')
			if reply:
				return self.save_file()
			elif reply == False:
				return True
			return False
		return True

	def on_quit(self):
		if self.on_close_file():
			self.destroy()

if __name__ == '__main__':
	Window()
