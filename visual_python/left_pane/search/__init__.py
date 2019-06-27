import tkinter as tk
import tkinter.ttk as ttk
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
                    # Search files in the list
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, encoding='UTF-8') as file_object:
                                for line_number, line in enumerate(file_object, 0):
                                    find_index_in_line = line.find(search_text)
                                    if find_index_in_line != -1:
                                        if not self.search_explorer.exists(file_path):
                                            self.search_explorer.insert('', tk.END, file_path, text=file_path)
                                        self.search_explorer.insert(file_path, tk.END, file_path + str(line_number), text=line)
                        except UnicodeDecodeError:
                            # It seems that this file is not a text file; ignore it
                            pass
