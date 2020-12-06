'''
class Application(tk.Tk)
'''

import tkinter as tk
import tkinter.ttk as ttk
import gettext
import os.path
from .editor import EditorGroup
from .left_pane import LeftPane
from .title import Title

class Application(tk.Tk):
    '''
    class Application(tk.Tk)
    '''
    def __init__(self):
        super().__init__()
        self.__application_name = 'Editor'
        gettext.install('editor')

        # Set title
        self.__title = Title(self.__application_name)
        self.set_title()

        self.add_menu()

        self.create_widgets()

        self.add_key_bindings()
        # Register delete window protocol to save unsaved changes and handle other things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.on_quit)

        self.resize_and_center()

    def add_key_bindings(self):
        '''
        add_key_bindings
        '''
        # Add key bindings for file menu
        self.bind('<Control-o>', self.open_file)
        self.bind('<Control-O>', self.open_file)
        self.bind('<Control-Shift-o>', self.open_folder)
        self.bind('<Control-Shift-O>', self.open_folder)
        self.bind('<Control-s>', self.save_file)
        self.bind('<Control-S>', self.save_file)
        self.bind('<Control-Shift-s>', self.save_file_as)
        self.bind('<Control-Shift-S>', self.save_file_as)
        self.bind('<Control-q>', self.on_quit)
        self.bind('<Control-Q>', self.on_quit)
        # Add key bindings for edit menu
        self.bind('<Control-f>', self.find)
        self.bind('<Control-F>', self.find)
        self.bind('<Control-Shift-f>', self.search)
        self.bind('<Control-Shift-F>', self.search)

    def add_menu(self):
        '''
        add_menu
        '''
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
        self.file_menu.add_command(label=_('Quit'), accelerator='Ctrl+Q', command=self.on_quit)
        # Add edit menu
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_('Edit'), menu=self.edit_menu)
        self.edit_menu.add_command(label=_('Find in File'), accelerator='Ctrl+F', command=self.find)
        self.edit_menu.add_command(label=_('Search'), accelerator='Ctrl+Shift+F', command=self.search)

    @property
    def application_name(self):
        '''
        application_name
        '''
        return self.__application_name

    def close_file_in_editor(self, file):
        '''
        close_file_in_editor
        '''
        self.editor_group.close_editor_by_file(file)

    def create_widgets(self):
        '''
        create_widgets
        '''
        # Create paned window
        self.paned_window = ttk.PanedWindow(orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create left pane and add it to the paned window
        self.left_pane = LeftPane(
            self.paned_window,
            self.close_file_in_editor,
            self.is_file_open_in_editor,
            self.open_file_by_file,
            self.rename_file_in_editor,
            self.set_title
        )
        self.paned_window.add(self.left_pane)

        # Create editor group and add it to the paned window
        self.editor_group = EditorGroup(self.paned_window, self.set_title, self.open_folder, self.search)
        self.paned_window.add(self.editor_group)

    def find(self, __=None):
        '''
        find
        '''
        self.editor_group.find_in_current_editor()

    def is_file_open_in_editor(self, file):
        '''
        is_file_open_in_editor
        '''
        return self.editor_group.is_file_open(file)

    def open_file(self, __=None):
        '''
        open_file
        '''
        self.editor_group.open_file()

    def open_file_by_file(self, file, cursor_index=None):
        '''
        open_file_by_file
        '''
        self.editor_group.open_file_by_file(file, cursor_index=cursor_index)

    def open_folder(self, __=None):
        '''
        open_folder
        '''
        self.left_pane.explorer.open_folder()

    def on_quit(self, __=None):
        '''
        on_quit
        '''
        if self.editor_group.save_unsaved_changes():
            self.destroy()

    def rename_file_in_editor(self, old_file, new_file):
        '''
        rename_file_in_editor
        '''
        self.editor_group.rename_file(old_file, new_file)

    def resize_and_center(self):
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

    def save_file(self, __=None):
        '''
        save_file
        '''
        self.editor_group.save_current_editor()

    def save_file_as(self, __=None):
        '''
        save_file_as
        '''
        self.editor_group.save_current_editor_as()

    def search(self, __=None):
        '''
        search
        '''
        # View search view in the left pane
        self.left_pane.select_search_view()

    def set_title(self, is_there_unsaved_change=None, file_name=None, folder_name=None):
        '''
        set_title
        '''
        if is_there_unsaved_change is not None:
            self.__title.is_there_unsaved_change = is_there_unsaved_change
        if file_name is not None:
            self.__title.file_name = file_name
        if folder_name is not None:
            self.__title.folder_name = folder_name
        self.title(str(self.__title))
