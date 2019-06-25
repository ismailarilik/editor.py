import tkinter as tk
import tkinter.ttk as ttk
import mimetypes
import os

class SearchView(ttk.Frame):
    def __init__(self, master, get_folder):
        super().__init__(master)
        self.get_folder = get_folder
		# Create search bar
        self.search_bar = ttk.Frame(self)
        self.search_bar.pack(fill=tk.X)
        self.search_entry = ttk.Entry(self.search_bar)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        current_directory = os.path.dirname(__file__)
        search_button_image_path = os.path.join(current_directory, '../../icons/find_icons/find.png')
        self.search_button_image = tk.PhotoImage(file=search_button_image_path)
        self.search_button = ttk.Button(self.search_bar, image=self.search_button_image, command=self.search)
        self.search_button.pack(side=tk.LEFT)
        # Create search explorer
        self.search_explorer = ttk.Treeview(self, show='tree')
        self.search_explorer.pack(fill=tk.BOTH, expand=True)

    def search(self, event=None):
        folder = self.get_folder()
        if folder:
            folder_path = folder.path
            self.search_explorer.delete(*self.search_explorer.get_children())
            search_text = self.search_entry.get()
            if search_text:
                for root, folders, files in os.walk(folder_path):
                    # Search files in the list, which seem like a text file
                    for file in files:
                        file_path = os.path.join(root, file)
                        mime_type = mimetypes.guess_type(file_path)[0]
                        is_text_file = mime_type is None or mime_type.startswith('text')
                        if is_text_file:
                            with open(file_path) as file_object:
                                file_text = file_object.read()
                            find_index = file_text.find(search_text)
                            if find_index != -1:
                                self.search_explorer.insert('', tk.END, file_path, text=file_path)
