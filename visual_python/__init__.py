import tkinter as tk
import tkinter.ttk as ttk
from .title import Title
from .explorer import Explorer
from .search.search_frame import SearchFrame
from .editor import Editor
from .find.find_frame import FindFrame
from .file_component import FileComponent
from .edit_component import EditComponent
from .settings_component import SettingsComponent

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.app_name = 'Visual Python'
		# Set title
		self._title = None
		self.set_title(False, None, self.app_name)
		# Set icon
		icon_img = tk.PhotoImage(file='./python.png')
		self.iconphoto(True, icon_img)

		# Create settings component
		self.settings_component = SettingsComponent()

		# Add menu
		self.menu = tk.Menu(self)
		self.config(menu=self.menu)
		# Add file menu
		self.file_component = FileComponent()
		self.file_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label='File', menu=self.file_menu)
		self.file_menu.add_command(label='Open File', accelerator='Ctrl+O', command=self.file_component.open_file)
		self.file_menu.add_command(label='Open Folder', accelerator='Ctrl+D', command=self.file_component.open_folder)
		self.file_menu.add_separator()
		self.file_menu.add_command(label='Save File', accelerator='Ctrl+S', command=self.file_component.save_file)
		self.file_menu.add_command(label='Save File as...', accelerator='Ctrl+Shift+S', command=self.file_component.save_file_as)
		self.file_menu.add_separator()
		self.file_menu.add_command(label='Quit', accelerator='Ctrl+Q', command=self.quit)
		# Add edit menu
		self.edit_component = EditComponent()
		self.edit_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label='Edit', menu=self.edit_menu)
		self.edit_menu.add_command(label='Find', accelerator='Ctrl+F', command=self.edit_component.find)
		# Create main frame
		main_frame = tk.Frame(self)
		main_frame.pack(fill=tk.BOTH, expand=True)

		# Create paned window
		paned_window = tk.PanedWindow(main_frame)
		paned_window.pack(fill=tk.BOTH, expand=True)

		# Create explorer notebook and add it to paned window
		self.explorer_notebook = ttk.Notebook(paned_window)
		paned_window.add(self.explorer_notebook)
		# Create explorer frame and add it to explorer notebook
		explorer_frame = tk.Frame(self.explorer_notebook)
		self.explorer_notebook.add(explorer_frame, text='Files')
		# Create explorer inside explorer frame
		self.explorer = Explorer(explorer_frame, self)
		self.explorer.pack(fill=tk.BOTH, expand=True)
		# Create search frame and add it to explorer notebook
		search_settings = self.settings_component.settings['search']
		self.search_frame = SearchFrame(self.explorer_notebook, search_settings, self.file_component.folder)
		self.explorer_notebook.add(self.search_frame, text='Search')

		# Create editor frame and add it to paned window
		editor_frame = tk.Frame(paned_window)
		paned_window.add(editor_frame)
		# Create editor inside editor frame
		self.editor = Editor(editor_frame)
		self.editor.pack(fill=tk.BOTH, expand=True)

		# Create find frame inside this frame
		self.find_frame = FindFrame(self)
		# Post initialization
		self._post_init()
		# Resize and center the window
		self._resize_and_center()
		# Add keyboard bindings
		self._add_keyboard_bindings()
		# Register delete window protocol to save unsaved changes and handle other things properly on quit
		self.protocol('WM_DELETE_WINDOW', self.quit)

	def _post_init(self):
		self.file_component.post_init(self.explorer, self.editor, self.set_title)
		self.edit_component.post_init(self.find_frame)
		self.explorer.post_init(self.file_component, self.editor.open_file_in_editor, self.editor.close_file_in_editor)
		self.editor.post_init(self.file_component, self.edit_component, self.set_title, self.find_frame.close)
		self.find_frame.post_init(self.editor)

	def set_title(self, is_there_unsaved_change=None, file_name=None, app_name=None):
		if not self._title:
			self._title = Title(is_there_unsaved_change, file_name, app_name)
		if is_there_unsaved_change is not None:
			self._title.is_there_unsaved_change = is_there_unsaved_change
		if file_name:
			self._title.file_name = file_name
		elif file_name == '':
			self._title.file_name = self._title.unsaved_file_name
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
		self.bind('<Control-KeyPress-o>', self.file_component.open_file)
		self.bind('<Control-KeyPress-O>', self.file_component.open_file)
		# Add keyboard bindings for opening folder
		self.bind('<Control-KeyPress-d>', self.file_component.open_folder)
		self.bind('<Control-KeyPress-D>', self.file_component.open_folder)
		# Add keyboard bindings for saving file
		self.bind('<Control-KeyPress-s>', self.file_component.save_file)
		self.bind('<Control-KeyPress-S>', self.file_component.save_file)
		# Add keyboard bindings for saving file as...
		self.bind('<Control-Shift-KeyPress-s>', self.file_component.save_file_as)
		self.bind('<Control-Shift-KeyPress-S>', self.file_component.save_file_as)
		# Add keyboard bindings for quitting
		self.bind('<Control-KeyPress-q>', self.quit)
		self.bind('<Control-KeyPress-Q>', self.quit)

	def quit(self, event=None):
		if self.file_component.save_unsaved_changes():
			self.destroy()
