import tkinter as tk
import tkinter.font as tk_font

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

class Window(tk.Tk):
	def __init__(self):
		super().__init__()
		# Create editor
		self.editor = Editor(self)
		self.editor.pack()
		# Add keyboard bindings for saving file
		self.bind('<Control-KeyPress-s>', self.save_file)
		self.bind('<Control-KeyPress-S>', self.save_file)
		# Start window
		self.mainloop()

	def save_file(self, event=None):
		with open('C:\\Users\\ismail.arilik\\Development\\visual-python\\window.py', 'w', encoding='UTF-8') as file:
			file.write(self.editor.get('1.0', tk.END))

Window()
