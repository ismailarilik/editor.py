import tkinter as tk
import tkinter.ttk as ttk
import mimetypes
import os

class SearchFrame(tk.Frame):
	def __init__(self, master, settings, folder):
		super().__init__(master)
		self.settings = settings
		self.folder = folder
		# Create search bar
		self.search_bar = tk.Frame(self)
		self.search_bar.pack(fill=tk.X)
		self.search_entry = tk.Entry(self.search_bar)
		self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
		self.search_button_image = tk.PhotoImage(file='search.png')
		self.search_button = tk.Button(self.search_bar, image=self.search_button_image, command=self.search)
		self.search_button.pack(side=tk.LEFT)
		# Create search treeview
		self.search_treeview = ttk.Treeview(self, show='tree')
		self.search_treeview.pack(fill=tk.BOTH, expand=True)

	def search(self):
		self.search_treeview.delete(*self.search_treeview.get_children())
		search_text = self.search_entry.get()
		for root, dirs, files in os.walk(self.folder.path):
			# Remove excluded files from the list
			for excluded_file in self.settings['excluded_files']:
				if excluded_file in files:
					files.remove(excluded_file)
			# Search files in the list if it seems like a text file
			for file in files:
				file_path = os.path.join(root, file)
				mime_type = mimetypes.guess_type(file_path)[0]
				is_text_file = mime_type is None or mime_type.startswith('text')
				if is_text_file:
					with open(file_path) as file_object:
						for line in file_object:
							find_index = line.find(search_text)
							while find_index != -1:
								if not self.search_treeview.exists(file_path):
									self.search_treeview.insert('', tk.END, file_path, text=file_path)
								find_index = line.find(search_text, find_index+1)
			# Remove excluded directories from the list
			for excluded_file in self.settings['excluded_files']:
				if excluded_file in dirs:
					dirs.remove(excluded_file)