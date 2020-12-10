import gettext
import os.path
import tkinter as tk
import tkinter.ttk as ttk

from .editor import EditorGroup
from .left_pane import LeftPane
from .store import Store

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        gettext.install('editor')

        self.store = Store(self)

        self.store.application_name = 'Editor'

        self.configure_menu()

        self.pack_widgets()

        self.resize_and_center()

        self.bind_keys()
        self.bind_protocols()

    def bind_keys(self):
        # Add key bindings for file menu
        self.bind('<Control-o>', self.on_open_file)
        self.bind('<Control-O>', self.on_open_file)
        self.bind('<Control-Shift-o>', self.on_open_folder)
        self.bind('<Control-Shift-O>', self.on_open_folder)
        self.bind('<Control-s>', self.on_save)
        self.bind('<Control-S>', self.on_save)
        self.bind('<Control-Shift-s>', self.on_save_as)
        self.bind('<Control-Shift-S>', self.on_save_as)
        self.bind('<Control-q>', self.on_quit)
        self.bind('<Control-Q>', self.on_quit)
        # Add key bindings for edit menu
        self.bind('<Control-f>', self.on_find_in_file)
        self.bind('<Control-F>', self.on_find_in_file)
        self.bind('<Control-Shift-f>', self.on_search)
        self.bind('<Control-Shift-F>', self.on_search)

    def bind_protocols(self):
        # Register delete window protocol to save unsaved changes and handle other things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.on_quit)

    def configure_menu(self):
        self.menu = tk.Menu()
        self.config(menu=self.menu)
        # Create file menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_('File'), menu=self.file_menu)
        self.file_menu.add_command(label=_('Open File...'), accelerator='Ctrl+O', command=self.on_open_file)
        self.file_menu.add_command(label=_('Open Folder...'), accelerator='Ctrl+Shift+O', command=self.on_open_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=_('Save'), accelerator='Ctrl+S', command=self.on_save)
        self.file_menu.add_command(label=_('Save as...'), accelerator='Ctrl+Shift+S', command=self.on_save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=_('Quit'), accelerator='Ctrl+Q', command=self.on_quit)
        # Create edit menu
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_('Edit'), menu=self.edit_menu)
        self.edit_menu.add_command(label=_('Find in File...'), accelerator='Ctrl+F', command=self.on_find_in_file)
        self.edit_menu.add_command(label=_('Search...'), accelerator='Ctrl+Shift+F', command=self.on_search)

    def on_find_in_file(self, __=None):
        self.editor_group.find_in_current_editor()

    def on_open_file(self, __=None):
        self.editor_group.open_file()

    def on_open_folder(self, __=None):
        self.left_pane.explorer.open_folder()

    def on_quit(self, __=None):
        if self.editor_group.save_unsaved_changes():
            self.destroy()

    def on_save(self, __=None):
        self.editor_group.save_current_editor()

    def on_save_as(self, __=None):
        self.editor_group.save_current_editor_as()

    def on_search(self, __=None):
        # View search view in the left pane
        self.left_pane.select_search_view()

    def pack_widgets(self):
        # Create paned window
        self.paned_window = ttk.PanedWindow(orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create left pane and add it to the paned window
        self.left_pane = LeftPane(
            self.paned_window,
            self.store,
            self.close_file_in_editor,
            self.is_file_open_in_editor,
            self.open_file_by_file,
            self.rename_file_in_editor
        )
        self.paned_window.add(self.left_pane)

        # Create editor group and add it to the paned window
        self.editor_group = EditorGroup(self.paned_window, self.store, self.on_open_folder, self.on_search)
        self.paned_window.add(self.editor_group)

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

    def close_file_in_editor(self, file):
        self.editor_group.close_editor_by_file(file)

    def is_file_open_in_editor(self, file):
        return self.editor_group.is_file_open(file)

    def rename_file_in_editor(self, old_file, new_file):
        self.editor_group.rename_file(old_file, new_file)

    def open_file_by_file(self, file, cursor_index=None):
        self.editor_group.open_file_by_file(file, cursor_index=cursor_index)
