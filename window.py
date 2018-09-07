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

	def set(self, text):
		self.delete('1.0', tk.END)
		self.insert(tk.END, text)

class File(object):
	def __init__(self, path):
		self.path = path

	@property
	def name(self):
		return os.path.basename(self.path)

class Window(tk.Tk):
	def __init__(self):
		super().__init__()
		self.file = None
		# Create editor
		self.editor = Editor(self)
		self.editor.pack()
		# Add keyboard bindings for opening file
		self.bind('<Control-KeyPress-o>', self.open_file)
		self.bind('<Control-KeyPress-O>', self.open_file)
		# Add keyboard bindings for saving file
		self.bind('<Control-KeyPress-s>', self.save_file)
		self.bind('<Control-KeyPress-S>', self.save_file)
		# Start window
		self.mainloop()

	def open_file(self, event=None):
		file_path = tk_filedialog.askopenfilename(filetypes=[('Python Files', '.py')])
		if file_path:
			self.file = File(file_path)
			# Set editor text with file text
			with tokenize.open(self.file.path) as file:
				self.editor.set(file.read())

	def save_file(self, event=None):
		with open('C:\\Users\\ismail.arilik\\Development\\visual-python\\window.py', 'w', encoding='UTF-8') as file:
			file.write(self.editor.get('1.0', tk.END))

Window()
