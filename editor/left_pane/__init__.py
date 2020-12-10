import tkinter as tk
import tkinter.ttk as ttk

from .explorer import Explorer
from .search import SearchView

class LeftPane(ttk.Notebook):
    def __init__(self,
        master,
        store,
        close_file_in_editor,
        is_file_open_in_editor,
        open_file_by_file,
        rename_file_in_editor
    ):
        super().__init__(master)
        self.store = store
        self.close_file_in_editor = close_file_in_editor
        self.is_file_open_in_editor = is_file_open_in_editor
        self.open_file_by_file = open_file_by_file
        self.rename_file_in_editor = rename_file_in_editor

        self.explorer = None
        self.search_view = None

        self.create_widgets()

    def create_explorer(self):
        # Create explorer layout and add it to this notebook
        explorer_layout = ttk.Frame(self)
        self.add(explorer_layout, text=_('Explorer'))
        # Create explorer inside the explorer layout
        self.explorer = Explorer(
            explorer_layout,
            self.store,
            self.close_file_in_editor,
            self.is_file_open_in_editor,
            self.open_file_by_file,
            self.rename_file_in_editor
        )
        # Create vertical scrollbar for explorer
        explorer_vertical_scrollbar = ttk.Scrollbar(explorer_layout, command=self.explorer.yview)
        explorer_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.explorer.config(yscrollcommand=explorer_vertical_scrollbar.set)
        # Pack explorer
        self.explorer.pack(fill=tk.BOTH, expand=True)

    def create_search_view(self):
        self.search_view = SearchView(self, self.get_folder, self.open_file_by_file)
        self.add(self.search_view, text=_('Search'))

    def create_widgets(self):
        self.create_explorer()
        self.create_search_view()

    def get_folder(self):
        return self.explorer.folder

    def select_search_view(self):
        self.select(1)
