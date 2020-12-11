import gettext
import tkinter as tk
import tkinter.ttk as ttk

from .editor_notebook import EditorNotebook
from .explorer import Explorer
from .search_view import SearchView
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
        # Bind keys for file menu
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
        # Bind keys for edit menu
        self.bind('<Control-f>', self.on_find_in_file)
        self.bind('<Control-F>', self.on_find_in_file)
        self.bind('<Control-Shift-f>', self.on_search)
        self.bind('<Control-Shift-F>', self.on_search)

    def bind_protocols(self):
        # Bind windows manager's delete window protocol to save unsaved changes and handle other things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.on_quit)

    def configure_menu(self):
        self.menu = tk.Menu()
        self.config(menu=self.menu)
        # Configure file menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_('File'), menu=self.file_menu)
        self.file_menu.add_command(label=_('Open File...'), accelerator='Ctrl+O', command=self.on_open_file)
        self.file_menu.add_command(label=_('Open Folder...'), accelerator='Ctrl+Shift+O', command=self.on_open_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=_('Save'), accelerator='Ctrl+S', command=self.on_save)
        self.file_menu.add_command(label=_('Save as...'), accelerator='Ctrl+Shift+S', command=self.on_save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=_('Quit'), accelerator='Ctrl+Q', command=self.on_quit)
        # Configure edit menu
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_('Edit'), menu=self.edit_menu)
        self.edit_menu.add_command(label=_('Find in File...'), accelerator='Ctrl+F', command=self.on_find_in_file)
        self.edit_menu.add_command(label=_('Search...'), accelerator='Ctrl+Shift+F', command=self.on_search)



    def on_find_in_file(self, __=None):
        self.editor_notebook.find_in_current_editor()

    def on_open_file(self, __=None):
        self.editor_notebook.open_file()

    def on_open_folder(self, __=None):
        self.explorer.open_folder()

    def on_quit(self, __=None):
        if self.editor_notebook.save_unsaved_changes():
            self.destroy()

    def on_save(self, __=None):
        self.editor_notebook.save_current_editor()

    def on_save_as(self, __=None):
        self.editor_notebook.save_current_editor_as()

    def on_search(self, __=None):
        self.store.select_search_view()



    def pack_widgets(self):
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.left_notebook = ttk.Notebook(self.paned_window)
        self.paned_window.add(self.left_notebook)

        # Create explorer frame
        explorer_frame = ttk.Frame(self.left_notebook)
        self.left_notebook.add(explorer_frame, text=_('Explorer'))
        # Create explorer inside the explorer frame
        self.explorer = Explorer(
            explorer_frame,
            self.store,
            self.store.close_file_in_editor,
            self.store.is_file_open_in_editor,
            self.store.open_file_by_file,
            self.store.rename_file_in_editor
        )
        # Create vertical scrollbar for explorer
        explorer_vertical_scrollbar = ttk.Scrollbar(explorer_frame, command=self.explorer.yview)
        explorer_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.explorer.config(yscrollcommand=explorer_vertical_scrollbar.set)
        # Pack explorer
        self.explorer.pack(fill=tk.BOTH, expand=True)

        self.search_view = SearchView(self.left_notebook, self.store, self.store.get_folder, self.store.open_file_by_file)
        self.left_notebook.add(self.search_view, text=_('Search'))

        self.right_paned_window = ttk.PanedWindow(self.paned_window)
        self.paned_window.add(self.right_paned_window)

        self.editor_paned_window = ttk.PanedWindow(self.right_paned_window, orient=tk.HORIZONTAL)
        self.right_paned_window.add(self.editor_paned_window)

        self.editor_notebook = EditorNotebook(self.editor_paned_window, self.store, self.on_open_folder, self.on_search)
        self.editor_paned_window.add(self.editor_notebook)

    def resize_and_center(self):
        '''
        Resize window as half of the screen size
        Also center the window
        '''
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        window_x = (screen_width // 2) - (window_width // 2)
        window_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
