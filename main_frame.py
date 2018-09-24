import tkinter as tk
import tkinter.ttk as ttk
import os
import shutil
import tokenize
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
		self.explorer = ttk.Treeview(explorer_frame, show='tree')
		# Create scrollbars for explorer
		vertical_scrollbar = tk.Scrollbar(explorer_frame)
		vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		vertical_scrollbar.config(command=self.explorer.yview)
		horizontal_scrollbar = tk.Scrollbar(explorer_frame, orient=tk.HORIZONTAL)
		horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
		horizontal_scrollbar.config(command=self.explorer.xview)
		self.explorer.config(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
		# Pack explorer
		self.explorer.pack(fill=tk.BOTH, expand=True)
		# Add keyboard bindings for explorer
		self.explorer.bind('<Double-Button-1>', self.open_file_from_explorer)
		self.explorer.bind('<Return>', self.open_file_from_explorer)
		self.explorer.bind('<Button-3>', self.open_context_menu)
		# Create icons of explorer items
		self.explorer_file_image = tk.PhotoImage(file='file.png')
		self.explorer_python_file_image = tk.PhotoImage(file='python_file.gif')
		self.explorer_folder_image = tk.PhotoImage(file='folder.gif')
		# Create context menu for explorer
		def refresh_explorer():
			self.explorer.delete(*self.explorer.get_children())
			def on_error(error):
				raise error
			folder = self.window.menu.file_menu.folder
			for path, folders, files in os.walk(folder, onerror=on_error):
				parent = '' if path == folder else path
				for folder in folders:
					self.explorer.insert(parent, tk.END, os.path.join(path, folder), text=folder, image=self.explorer_folder_image)
				for file in files:
					extension = os.path.splitext(file)[1]
					image = self.explorer_python_file_image if extension == '.py' or extension == '.pyw' else self.explorer_file_image
					self.explorer.insert(parent, tk.END, os.path.join(path, file), text=file, image=image)
		def create_file_or_directory(is_file, is_root, event=None):
			if is_root:
				parent = ''
			else:
				parent = self.menu_target
			temp_item = self.explorer.insert(parent, 0)
			self.explorer.see(temp_item)
			bbox = self.explorer.bbox(temp_item)
			entry = tk.Entry(explorer_frame)
			entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
			entry.focus_set()
			def create(event=None):
				entry.place_forget()
				self.explorer.delete(temp_item)
				file_name = entry.get()
				if file_name:
					if is_root:
						root_path = self.window.menu.file_menu.folder
					else:
						root_path = self.menu_target
					file_path = os.path.join(root_path, file_name)
					if is_file:
						with open(file_path, 'w', encoding='UTF-8') as file:
							pass
					else:
						try:
							os.mkdir(file_path)
						except FileExistsError as error:
							print('An error occurred while creating a new folder on explorer:')
							print(error)
					selection = file_path
					refresh_explorer()
					self.explorer.see(selection)
					self.explorer.selection_set(selection)
					self.explorer.focus_set()
			def cancel(event=None):
				entry.place_forget()
				self.explorer.delete(temp_item)
			entry.bind('<Return>', create)
			entry.bind('<Escape>', cancel)
		def new_file(event=None):
			create_file_or_directory(is_file=True, is_root=False, event=event)
		def new_folder(event=None):
			create_file_or_directory(is_file=False, is_root=False, event=event)
		def new_root_file(event=None):
			create_file_or_directory(is_file=True, is_root=True, event=event)
		def new_root_folder(event=None):
			create_file_or_directory(is_file=False, is_root=True, event=event)
		def rename_file_or_folder(is_file, event=None):
			bbox = self.explorer.bbox(self.menu_target)
			entry = tk.Entry(explorer_frame)
			entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
			entry.focus_set()
			old_file_name = self.explorer.item(self.menu_target, 'text')
			entry.insert(0, old_file_name)
			entry.select_range(0, tk.END)
			def rename(event=None):
				entry.place_forget()
				file_name = entry.get()
				if file_name:
					file_path = os.path.join(os.path.dirname(self.menu_target), file_name)
					is_file_open = self.window.menu.file_menu.file.name == old_file_name
					is_cancelled = False
					if is_file and is_file_open:
						is_cancelled = not self.window.menu.file_menu.save_unsaved_changes()
						if not is_cancelled:
							self.close_file_in_editor()
					if not is_cancelled:
						os.replace(self.menu_target, file_path)
						selection = file_path
						refresh_explorer()
						self.explorer.see(selection)
						self.explorer.selection_set(selection)
						self.explorer.focus_set()
						if is_file and is_file_open:
							self.open_file_from_explorer(event)
			def cancel(event=None):
				entry.place_forget()
			entry.bind('<Return>', rename)
			entry.bind('<Escape>', cancel)
		def rename_folder(event=None):
			rename_file_or_folder(is_file=False, event=event)
		def rename_file(event=None):
			rename_file_or_folder(is_file=True, event=event)
		def delete_file_or_folder(is_file, event=None):
			if is_file:
				file_path = self.menu_target
				file_name = os.path.basename(file_path)
				os.remove(file_path)
				is_file_open = self.window.menu.file_menu.file.name == file_name
				if is_file_open:
					self.close_file_in_editor()
			else:
				shutil.rmtree(self.menu_target)
			selection = self.explorer.parent(self.menu_target)
			refresh_explorer()
			if selection:
				self.explorer.see(selection)
				self.explorer.selection_set(selection)
				self.explorer.item(selection, open=True)
		def delete_folder(event=None):
			delete_file_or_folder(is_file=False, event=event)
		def delete_file(event=None):
			delete_file_or_folder(is_file=True, event=event)
		self.folder_menu = tk.Menu(self.window)
		self.folder_menu.add_command(label='New File', command=new_file)
		self.folder_menu.add_command(label='New Folder', command=new_folder)
		self.folder_menu.add_separator()
		self.folder_menu.add_command(label='Rename', command=rename_folder)
		self.folder_menu.add_command(label='Delete', command=delete_folder)
		self.file_menu = tk.Menu(self.window)
		self.file_menu.add_command(label='Rename', command=rename_file)
		self.file_menu.add_command(label='Delete', command=delete_file)
		self.explorer_menu = tk.Menu(self.window)
		self.explorer_menu.add_command(label='New File', command=new_root_file)
		self.explorer_menu.add_command(label='New Folder', command=new_root_folder)
		# Create editor frame and add it to paned window
		editor_frame = tk.Frame(paned_window)
		paned_window.add(editor_frame)
		# Create editor inside editor frame
		self.editor = Editor(editor_frame, self.window)
		self.editor.pack(fill=tk.BOTH, expand=True)
		# Create find frame inside this frame
		self.find_frame = FindFrame(self, self.window)

	def open_file_from_explorer(self, event=None):
		selections = self.explorer.selection()
		if len(selections) == 1:
			selection = selections[0]
			if os.path.isfile(selection):
				if self.window.menu.file_menu.save_unsaved_changes():
					self.open_file_in_editor(selection)

	def open_file_in_editor(self, file_path):
		self.window.menu.file_menu.file.path = file_path
		self.window.menu.file_menu.file.is_modified = False
		# Set editor text with file text
		with tokenize.open(self.window.menu.file_menu.file.path) as file:
			self.window.main_frame.editor.set(file.read())
		# Focus editor in
		self.editor.focus_set()
		# Reset title because file name has been changed
		# Also unsaved changes status has been changed to False
		title = self.window.get_title()
		title.file_name = self.window.menu.file_menu.file.name
		title.is_there_unsaved_change = self.window.menu.file_menu.file.is_modified
		self.window.set_title(title)
		# Return that a file was opened successfully
		return True

	def close_file_in_editor(self):
		self.window.menu.file_menu.file.path = None
		self.window.menu.file_menu.file.is_modified = False
		# Clear editor text
		self.window.main_frame.editor.clear()
		# Reset title because file has been closed
		# Also there is no unsaved change now
		title = self.window.get_title()
		title.file_name = title.unsaved_file_name
		title.is_there_unsaved_change = self.window.menu.file_menu.file.is_modified
		self.window.set_title(title)
		# Return that a file was closed successfully
		return True

	def open_context_menu(self, event=None):
		self.menu_target = self.explorer.identify_row(event.y)
		if self.menu_target:
			self.explorer.focus_set()
			self.explorer.focus(self.menu_target)
			if os.path.isfile(self.menu_target):
				self.file_menu.tk_popup(event.x_root, event.y_root)
			else:
				self.folder_menu.tk_popup(event.x_root, event.y_root)
		else:
			if self.window.menu.file_menu.folder:
				self.explorer_menu.tk_popup(event.x_root, event.y_root)