import tkinter as tk
import tkinter.ttk as ttk
import gettext
import os.path
from .editor import EditorGroup
from .left_pane import LeftPane
from .title import Title

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_name = 'Visual Python'
        gettext.install('visual_python')
        
        # Set title
        self._title = Title(self.app_name)
        self.set_title()
        
        # Set icon
        current_directory = os.path.dirname(__file__)
        icon_path = os.path.join(current_directory, 'icons/python.png')
        self.icon = tk.PhotoImage(file=icon_path)
        self.iconphoto(True, self.icon)
        
        self.add_menu()
        
        self.create_widgets()
        
        self.add_key_bindings()
        # Register delete window protocol to save unsaved changes and handle other things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.quit)
        
        self.resize_and_center()
    
    def add_key_bindings(self, event=None):
        # Add key bindings for file menu
        self.bind('<Control-o>', self.open_file)
        self.bind('<Control-O>', self.open_file)
        self.bind('<Control-Shift-o>', self.open_folder)
        self.bind('<Control-Shift-O>', self.open_folder)
        self.bind('<Control-s>', self.save_file)
        self.bind('<Control-S>', self.save_file)
        self.bind('<Control-Shift-s>', self.save_file_as)
        self.bind('<Control-Shift-S>', self.save_file_as)
        self.bind('<Control-q>', self.quit)
        self.bind('<Control-Q>', self.quit)
        # Add key bindings for edit menu
        self.bind('<Control-f>', self.find)
        self.bind('<Control-F>', self.find)
        self.bind('<Control-Shift-f>', self.search)
        self.bind('<Control-Shift-F>', self.search)
    
    def add_menu(self, event=None):
        self.menu = tk.Menu()
        self.config(menu=self.menu)
        # Add file menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_('File'), menu=self.file_menu)
        self.file_menu.add_command(label=_('Open File'), accelerator='Ctrl+O', command=self.open_file)
        self.file_menu.add_command(label=_('Open Folder'), accelerator='Ctrl+Shift+O', command=self.open_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=_('Save File'), accelerator='Ctrl+S', command=self.save_file)
        self.file_menu.add_command(label=_('Save File as'), accelerator='Ctrl+Shift+S', command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=_('Quit'), accelerator='Ctrl+Q', command=self.quit)
        # Add edit menu
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_('Edit'), menu=self.edit_menu)
        self.edit_menu.add_command(label=_('Find in File'), accelerator='Ctrl+F', command=self.find)
        self.edit_menu.add_command(label=_('Search'), accelerator='Ctrl+Shift+F', command=self.search)
    
    def close_file_in_editor(self, file, event=None):
        self.editor_group.close_editor_by_file(file, event=event)
    
    def create_widgets(self, event=None):
        # Create paned window
        self.paned_window = ttk.PanedWindow(orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create left pane and add it to the paned window
        self.left_pane = LeftPane(self.paned_window, self.close_file_in_editor, self.is_file_open_in_editor, self.open_file_by_file, self.rename_file_in_editor, self.set_title)
        self.paned_window.add(self.left_pane)
        
        # Create editor group and add it to the paned window
        self.editor_group = EditorGroup(self.paned_window, self.set_title, self.open_folder, self.search)
        self.paned_window.add(self.editor_group)
    
    def find(self, event=None):
        self.editor_group.find_in_current_editor(event=event)
    
    def is_file_open_in_editor(self, file, event=None):
        return self.editor_group.is_file_open(file, event=event)
    
    def open_file(self, event=None):
        self.editor_group.open_file(event=event)
    
    def open_file_by_file(self, file, cursor_index=None, event=None):
        self.editor_group.open_file_by_file(file, cursor_index=cursor_index, event=event)
    
    def open_folder(self, event=None):
        self.left_pane.explorer.open_folder(event=event)
    
    def quit(self, event=None):
        if self.editor_group.save_unsaved_changes(event=event):
            self.destroy()
    
    def rename_file_in_editor(self, old_file, new_file, event=None):
        self.editor_group.rename_file(old_file, new_file, event=event)
    
    def resize_and_center(self, event=None):
        '''
        Set window size as half of the screen size
        Also center window
        '''
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        window_x = (screen_width // 2) - (window_width // 2)
        window_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
    
    def save_file(self, event=None):
        self.editor_group.save_current_editor(event=event)
    
    def save_file_as(self, event=None):
        self.editor_group.save_current_editor_as(event=event)
    
    def search(self, event=None):
        # View search view in the left pane
        self.left_pane.select_search_view()
    
    def set_title(self, is_there_unsaved_change=None, file_name=None, folder_name=None, event=None):
        if is_there_unsaved_change is not None:
            self._title.is_there_unsaved_change = is_there_unsaved_change
        if file_name is not None:
            self._title.file_name = file_name
        if folder_name is not None:
            self._title.folder_name = folder_name
        self.title(str(self._title))
