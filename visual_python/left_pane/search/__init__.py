import tkinter as tk
import tkinter.ttk as ttk
import os

class SearchView(ttk.Frame):
    def __init__(self, master, get_folder, open_file_by_path):
        super().__init__(master)
        self.get_folder = get_folder
        self.open_file_by_path = open_file_by_path
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

        self.add_key_bindings()

    def add_key_bindings(self):
        # Add key bindings for the Search Explorer
        self.search_explorer.bind('<Double-Button-1>', self.open_file)
        self.search_explorer.bind('<Return>', self.open_file)

    def open_file(self, event=None):
        selections = self.search_explorer.selection()
        for selection in selections:
            parent = self.search_explorer.parent(selection)
            # Open file only if a line view was clicked
            if parent != '':
                path = parent
                cursor_index_as_array = selection.rsplit('-', 2)[-2:]
                cursor_row_index = str(int(cursor_index_as_array[0]) + 1)
                cursor_column_index = cursor_index_as_array[1]
                cursor_index = f'{cursor_row_index}.{cursor_column_index}'
                self.open_file_by_path(path, cursor_index=cursor_index, event=event)

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
                                    while find_index_in_line != -1:
                                        if not self.search_explorer.exists(file_path):
                                            self.search_explorer.insert('', tk.END, file_path, text=file_path)
                                        line_node_id = file_path + '-' + str(line_number) + '-' + str(find_index_in_line)
                                        self.search_explorer.insert(file_path, tk.END, line_node_id, text=line)
                                        find_index_in_line = line.find(search_text, find_index_in_line+1)
                        except UnicodeDecodeError:
                            # It seems that this file is not a text file; ignore it
                            pass
