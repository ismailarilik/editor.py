import tkinter as tk
from explorer.explorer import Explorer
from editor.editor import Editor
from find.find_frame import FindFrame

class MainFrame(tk.Frame):
	def __init__(self, master, window):
		super().__init__(master)
		self.pack(fill=tk.BOTH, expand=True)
		self.window = window
		# Create paned window
		paned_window = tk.PanedWindow(self)
		paned_window.pack(fill=tk.BOTH, expand=True)
		# Create explorer frame and add it to paned window
		explorer_frame = tk.Frame(paned_window)
		paned_window.add(explorer_frame)
		# Create explorer inside explorer frame
		self.explorer = Explorer(explorer_frame, self.window)
		self.explorer.pack(fill=tk.BOTH, expand=True)
		# Create editor frame and add it to paned window
		editor_frame = tk.Frame(paned_window)
		paned_window.add(editor_frame)
		# Create editor inside editor frame
		self.editor = Editor(editor_frame, self.window)
		self.editor.pack(fill=tk.BOTH, expand=True)
		# Create find frame inside this frame
		self.find_frame = FindFrame(self, self.window)
