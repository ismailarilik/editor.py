import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox
import os

class File(object):
	def __init__(self, path):
		self.path = path
		self.is_modified = False

	@property
	def name(self):
		if self.path:
			return os.path.basename(self.path)

class Folder(object):
	def __init__(self, path):
		self.path = path

class FileComponent(object):
	def __init__(self):
		self.file = File(None)
		self.folder = Folder(None)

	def post_init(self, explorer, editor, get_title, set_title):
		self.explorer = explorer
		self.editor = editor
		self.get_title = get_title
		self.set_title = set_title

	def open_file(self, event=None):
		'''
		Return True if a file was opened
		Return False otherwise
		'''
		if self.save_unsaved_changes():
			file_path = tk_filedialog.askopenfilename(filetypes=[('Python Files', '.py')])
			if file_path:
				return self.editor.open_file_in_editor(file_path)
			else:
				return False
		else:
			return False

	def open_folder(self, event=None):
		self.folder.path = tk_filedialog.askdirectory()
		if self.folder.path:
			self.explorer.delete(*self.explorer.get_children())
			# Create folder
			try:
				os.mkdir(self.folder.path)
			except FileExistsError as error:
				print('An error occurred while opening a folder:')
				print(error)
			def on_error(error):
				raise error
			for path, folders, files in os.walk(self.folder.path, onerror=on_error):
				parent = '' if path == self.folder.path else path
				for folder in folders:
					self.explorer.insert(parent, tk.END, os.path.join(path, folder), text=folder, image=self.explorer.explorer_folder_image)
				for file in files:
					extension = os.path.splitext(file)[1]
					image = self.explorer.explorer_python_file_image if extension == '.py' or extension == '.pyw' else self.explorer.explorer_file_image
					self.explorer.insert(parent, tk.END, os.path.join(path, file), text=file, image=image)

	def save_file(self, event=None):
		'''
		Return True if the file was saved
		Return False otherwise
		'''
		# If there is not any opened file, call save_file_as method
		# Else, write editor text to the file
		if not self.file.path:
			return self.save_file_as(event)
		else:
			with open(self.file.path, 'w', encoding='UTF-8') as file:
				file.write(self.editor.get_wo_eol())
			# Focus editor in
			self.editor.focus_set()
			# File is unmodified now
			self.file.is_modified = False
			# Reset title because unsaved changes status has been changed to False
			title = self.get_title()
			title.is_there_unsaved_change = self.file.is_modified
			self.set_title(title)
			# Return that the file was saved
			return True

	def save_file_as(self, event=None):
		'''
		Return True if the specified file was saved
		Return False otherwise
		'''
		file_path = tk_filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python Files', '.py')])
		if file_path:
			self.file.path = file_path
			self.file.is_modified = False
			with open(self.file.path, 'w', encoding='UTF-8') as file:
				file.write(self.editor.get_wo_eol())
			# Focus editor in
			self.editor.focus_set()
			# Reset title because file name has been changed
			# Also unsaved changes status has been changed to False
			title = self.get_title()
			title.file_name = self.file.name
			title.is_there_unsaved_change = self.file.is_modified
			self.set_title(title)
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
