import tkinter as tk
import tkinter.font as tk_font
import io
import tokenize
from editor.tokenizer import Tokenizer

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

	def post_init(self):
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

	def clear(self):
		self.delete('1.0', tk.END)

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
			file = self.window.menu.file_menu.file
			if not file.is_modified:
				file.is_modified = True
				title = self.window.get_title()
				title.is_there_unsaved_change = file.is_modified
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
		# Handle open folder event here, too, for this widget and prevent propagation of event
		# Because default behavior of this widget for this event is not wanted here
		self.bind('<Control-KeyPress-d>', self.handle_open_folder_event_and_prevent_propagation)

	def escape(self, event=None):
		# Close find frame
		self.window.main_frame.find_frame.close(event)

	def handle_open_file_event_and_prevent_propagation(self, event=None):
		self.window.menu.file_menu.open_file(event)
		return 'break'

	def handle_open_folder_event_and_prevent_propagation(self, event=None):
		self.window.menu.file_menu.open_folder(event)
		return 'break'
