import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.ttk as ttk
import os
import shutil
from ...file import File
from .folder import Folder

class Explorer(ttk.Treeview):
    def __init__(self, master, close_file_in_editor, is_file_open_in_editor, open_file_by_file, rename_file_in_editor, set_title):
        super().__init__(master, show='tree')
        self.close_file_in_editor = close_file_in_editor
        self.is_file_open_in_editor = is_file_open_in_editor
        self.open_file_by_file = open_file_by_file
        self.rename_file_in_editor = rename_file_in_editor
        self.set_title = set_title
        self.folder = None
        
        self.create_context_menu()
        
        self.create_file_icons()
        
        self.add_key_bindings()
    
    def add_key_bindings(self, event=None):
        self.bind('<Return>', self.open_file)
        self.bind('<Double-Button-1>', self.open_file)
        self.bind('<Button-3>', self.open_context_menu)
    
    def clear(self, event=None):
        self.delete(*self.get_children())
    
    def create_context_menu(self, event=None):
        # Create context menu for empty areas
        self.explorer_menu = tk.Menu(self)
        self.explorer_menu.add_command(label='New File', command=self.new_file)
        self.explorer_menu.add_command(label='New Folder', command=self.new_folder)
        # Create context menu for folders
        self.folder_menu = tk.Menu(self)
        self.folder_menu.add_command(label='New File', command=self.new_file)
        self.folder_menu.add_command(label='New Folder', command=self.new_folder)
        self.folder_menu.add_separator()
        self.folder_menu.add_command(label='Rename', command=self.rename_folder)
        self.folder_menu.add_command(label='Delete', command=self.delete_folder)
        # Create context menu for files
        self.file_menu = tk.Menu(self)
        self.file_menu.add_command(label='Rename', command=self.rename_file)
        self.file_menu.add_command(label='Delete', command=self.delete_file)
    
    def create_file_icons(self, event=None):
        current_directory = os.path.dirname(__file__)
        folder_icon_path = os.path.join(current_directory, '../../icons/file_icons/folder.png')
        self.folder_icon = tk.PhotoImage(file=folder_icon_path)
        file_icon_path = os.path.join(current_directory, '../../icons/file_icons/file.png')
        self.file_icon = tk.PhotoImage(file=file_icon_path)
        python_file_icon_path = os.path.join(current_directory, '../../icons/file_icons/python-file.png')
        self.python_file_icon = tk.PhotoImage(file=python_file_icon_path)
    
    def delete_file(self, event=None):
        self.delete_file_or_folder(True, event=event)
    
    def delete_file_or_folder(self, is_file, event=None):
        if is_file:
            file_path = self.menu_target
            file = File(file_path)
            os.remove(file.path)
            is_file_open = self.is_file_open_in_editor(file, event=event)
            if is_file_open:
                self.close_file_in_editor(file, event=event)
        else:
            shutil.rmtree(self.menu_target)
        selection = self.parent(self.menu_target)
        self.refresh(event=event)
        if selection:
            self.see(selection)
            self.selection_set(selection)
            self.item(selection, open=True)
    
    def delete_folder(self, event=None):
        self.delete_file_or_folder(False, event=event)
    
    def new_file(self, event=None):
        self.new_file_or_folder(True, event=event)
    
    def new_file_or_folder(self, is_file, event=None):
        if not self.menu_target:
            parent = ''
        else:
            parent = self.menu_target
        temp_item = self.insert(parent, 0)
        self.see(temp_item)
        bbox = self.bbox(temp_item)
        entry = ttk.Entry(self)
        entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        entry.focus_set()
        
        def create(event=None):
            entry.place_forget()
            self.delete(temp_item)
            file_name = entry.get()
            if file_name:
                if not self.menu_target:
                    root_path = self.folder.path
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
                        pass
                self.refresh(event=event)
                self.focus_set()
                selection = file_path
                self.see(selection)
                self.selection_set(selection)
        def cancel(event=None):
            entry.place_forget()
            self.delete(temp_item)
        entry.bind('<Return>', create)
        entry.bind('<Escape>', cancel)
    
    def new_folder(self, event=None):
        self.new_file_or_folder(False, event=event)
    
    def open_context_menu(self, event=None):
        self.focus_set()
        self.menu_target = self.identify_row(event.y)
        if self.menu_target:
            self.focus(self.menu_target)
            if os.path.isfile(self.menu_target):
                self.file_menu.tk_popup(event.x_root, event.y_root)
            else:
                self.folder_menu.tk_popup(event.x_root, event.y_root)
        else:
            if self.folder:
                self.explorer_menu.tk_popup(event.x_root, event.y_root)
    
    def open_file(self, event=None):
        selections = self.selection()
        for selection in selections:
            if os.path.isfile(selection):
                file_path = selection
                file = File(file_path)
                self.open_file_by_file(file, event=event)
    
    def open_folder(self, event=None):
        folder_path = tkfiledialog.askdirectory(mustexist=True)
        if folder_path:
            folder = Folder(folder_path)
            self.open_folder_by_folder(folder, event=event)
    
    def open_folder_by_folder(self, folder, event=None):
        self.folder = folder
        # Refill explorer with folders and files in the opened folder path
        self.clear()
        for path, folders, files in os.walk(self.folder.path):
            parent = '' if path == self.folder.path else path
            for folder in folders:
                id = os.path.join(path, folder)
                self.insert(parent, tk.END, id, text=folder, image=self.folder_icon)
            for file in files:
                id = os.path.join(path, file)
                # Get file icon depending on the file extension
                file_extension = os.path.splitext(file)[1]
                is_python_file = file_extension == '.py' or file_extension == '.pyw'
                file_icon = self.python_file_icon if is_python_file else self.file_icon
                # Insert file into this treeview
                self.insert(parent, tk.END, id, text=file, image=file_icon)
        # Specify opened folder in title
        self.set_title(folder_name=self.folder.name)
    
    def refresh(self, event=None):
        if self.folder:
            self.open_folder_by_folder(self.folder, event=event)
    
    def rename_file(self, event=None):
        self.rename_file_or_folder(True, event=event)
    
    def rename_file_or_folder(self, is_file, event=None):
        bbox = self.bbox(self.menu_target)
        entry = ttk.Entry(self)
        entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        entry.focus_set()
        old_file_path = self.menu_target
        old_file = File(old_file_path)
        entry.insert(0, old_file.name)
        entry.select_range(0, tk.END)
        def rename(event=None):
            entry.place_forget()
            new_file_name = entry.get()
            if new_file_name:
                new_file_path = os.path.join(old_file.directory_path, new_file_name)
                new_file = File(new_file_path)
                if is_file:
                    is_file_open = self.is_file_open_in_editor(old_file, event=event)
                    if is_file_open:
                        self.rename_file_in_editor(old_file, new_file, event=event)
                os.replace(old_file.path, new_file.path)
                self.refresh(event=event)
                self.focus_set()
                selection = new_file.path
                self.see(selection)
                self.selection_set(selection)
        def cancel(event=None):
            entry.place_forget()
        entry.bind('<Return>', rename)
        entry.bind('<Escape>', cancel)
    
    def rename_folder(self, event=None):
        self.rename_file_or_folder(False, event=event)
