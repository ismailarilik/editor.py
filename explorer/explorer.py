import tkinter as tk
import tkinter.ttk as ttk
import os
import shutil

class Explorer(ttk.Treeview):
	def __init__(self, master, window):
		super().__init__(master, show='tree')
		self.window = window
		# Create scrollbars for explorer
		vertical_scrollbar = tk.Scrollbar(self.master)
		vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		vertical_scrollbar.config(command=self.yview)
		horizontal_scrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
		horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
		horizontal_scrollbar.config(command=self.xview)
		self.config(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
		# Add keyboard bindings for explorer
		self.bind('<Double-Button-1>', self.open_file_from_explorer)
		self.bind('<Return>', self.open_file_from_explorer)
		self.bind('<Button-3>', self.open_context_menu)
		# Create icons of explorer items
		self.explorer_file_image = tk.PhotoImage(file='file.png')
		self.explorer_python_file_image = tk.PhotoImage(file='python_file.gif')
		self.explorer_folder_image = tk.PhotoImage(file='folder.gif')
		# Create context menu for explorer
		self.folder_menu = tk.Menu(self.window)
		self.folder_menu.add_command(label='New File', command=self.new_file)
		self.folder_menu.add_command(label='New Folder', command=self.new_folder)
		self.folder_menu.add_separator()
		self.folder_menu.add_command(label='Rename', command=self.rename_folder)
		self.folder_menu.add_command(label='Delete', command=self.delete_folder)
		self.file_menu = tk.Menu(self.window)
		self.file_menu.add_command(label='Rename', command=self.rename_file)
		self.file_menu.add_command(label='Delete', command=self.delete_file)
		self.explorer_menu = tk.Menu(self.window)
		self.explorer_menu.add_command(label='New File', command=self.new_root_file)
		self.explorer_menu.add_command(label='New Folder', command=self.new_root_folder)

	def open_file_from_explorer(self, event=None):
		selections = self.selection()
		if len(selections) == 1:
			selection = selections[0]
			if os.path.isfile(selection):
				if self.window.menu.file_menu.save_unsaved_changes():
					self.window.main_frame.editor.open_file_in_editor(selection)

	def open_context_menu(self, event=None):
		self.menu_target = self.identify_row(event.y)
		if self.menu_target:
			self.focus_set()
			self.focus(self.menu_target)
			if os.path.isfile(self.menu_target):
				self.file_menu.tk_popup(event.x_root, event.y_root)
			else:
				self.folder_menu.tk_popup(event.x_root, event.y_root)
		else:
			if self.window.menu.file_menu.folder:
				self.explorer_menu.tk_popup(event.x_root, event.y_root)

	def refresh_explorer(self):
		self.delete(*self.get_children())
		def on_error(error):
			raise error
		folder = self.window.menu.file_menu.folder
		for path, folders, files in os.walk(folder, onerror=on_error):
			parent = '' if path == folder else path
			for folder in folders:
				self.insert(parent, tk.END, os.path.join(path, folder), text=folder, image=self.explorer_folder_image)
			for file in files:
				extension = os.path.splitext(file)[1]
				image = self.explorer_python_file_image if extension == '.py' or extension == '.pyw' else self.explorer_file_image
				self.insert(parent, tk.END, os.path.join(path, file), text=file, image=image)

	def create_file_or_directory(self, is_file, is_root, event=None):
		if is_root:
			parent = ''
		else:
			parent = self.menu_target
		temp_item = self.insert(parent, 0)
		self.see(temp_item)
		bbox = self.bbox(temp_item)
		entry = tk.Entry(self.master)
		entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
		entry.focus_set()
		def create(event=None):
			entry.place_forget()
			self.delete(temp_item)
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
				self.refresh_explorer()
				self.see(selection)
				self.selection_set(selection)
				self.focus_set()
		def cancel(event=None):
			entry.place_forget()
			self.delete(temp_item)
		entry.bind('<Return>', create)
		entry.bind('<Escape>', cancel)

	def new_file(self, event=None):
		self.create_file_or_directory(is_file=True, is_root=False, event=event)

	def new_folder(self, event=None):
		self.create_file_or_directory(is_file=False, is_root=False, event=event)

	def new_root_file(self, event=None):
		self.create_file_or_directory(is_file=True, is_root=True, event=event)

	def new_root_folder(self, event=None):
		self.create_file_or_directory(is_file=False, is_root=True, event=event)

	def rename_file_or_folder(self, is_file, event=None):
		bbox = self.bbox(self.menu_target)
		entry = tk.Entry(self.master)
		entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
		entry.focus_set()
		old_file_name = self.item(self.menu_target, 'text')
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
						self.window.main_frame.editor.close_file_in_editor()
				if not is_cancelled:
					os.replace(self.menu_target, file_path)
					selection = file_path
					self.refresh_explorer()
					self.see(selection)
					self.selection_set(selection)
					self.focus_set()
					if is_file and is_file_open:
						self.open_file_from_explorer(event)
		def cancel(event=None):
			entry.place_forget()
		entry.bind('<Return>', rename)
		entry.bind('<Escape>', cancel)

	def rename_folder(self, event=None):
		self.rename_file_or_folder(is_file=False, event=event)

	def rename_file(self, event=None):
		self.rename_file_or_folder(is_file=True, event=event)

	def delete_file_or_folder(self, is_file, event=None):
		if is_file:
			file_path = self.menu_target
			file_name = os.path.basename(file_path)
			os.remove(file_path)
			is_file_open = self.window.menu.file_menu.file.name == file_name
			if is_file_open:
				self.window.main_frame.editor.close_file_in_editor()
		else:
			shutil.rmtree(self.menu_target)
		selection = self.parent(self.menu_target)
		self.refresh_explorer()
		if selection:
			self.see(selection)
			self.selection_set(selection)
			self.item(selection, open=True)

	def delete_folder(self, event=None):
		self.delete_file_or_folder(is_file=False, event=event)

	def delete_file(self, event=None):
		self.delete_file_or_folder(is_file=True, event=event)
