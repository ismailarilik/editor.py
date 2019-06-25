import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import tkinter.ttk as ttk
from .editor import Editor
from .file import File
from .tab_title import TabTitle

class EditorGroup(ttk.Notebook):
    def __init__(self, master, set_title, open_folder, search):
        super().__init__(master)
        self.set_title = set_title
        self.open_folder = open_folder
        self.search = search
        self.editors = []

        self.enable_traversal()

        self.add_key_bindings()

        self.bind('<<NotebookTabChanged>>', self.tab_changed)

    def add_editor(self, file):
        # Create an editor with wrapping layout and scrollbars
        editor_layout = ttk.Frame(self)
        self.add(editor_layout, text=file.name)
        editor_title = TabTitle(file.name)
        editor = Editor(editor_layout, file, editor_title, self.open_file, self.open_folder, self.search, self.set_tab_title, self.set_title)
        vertical_scrollbar = ttk.Scrollbar(editor_layout, command=editor.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        horizontal_scrollbar = ttk.Scrollbar(editor_layout, orient=tk.HORIZONTAL, command=editor.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        editor.config(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        editor.pack(fill=tk.BOTH, expand=True)
        self.editors.append(editor)
        # Focus added editor on
        self.select(str(editor_layout))
        editor.focus_set()

    def add_key_bindings(self):
        self.bind('<Button-2>', self.close_editor)

    def close_editor(self, event=None):
        tab_id = f'@{event.x},{event.y}'
        editor_index = None
        try:
            editor_index = self.index(tab_id)
        except tk.TclError as error:
            # There is no tab on coordinates the event came from; do nothing.
            pass
        if editor_index is not None:
            editor = self.editors[editor_index]
            if editor.close(event):
                # Remove related editor from editors list
                del self.editors[editor_index]
                # Remove tab from this notebook
                self.forget(tab_id)

    def close_editor_by_file_path(self, file_path, event=None):
        opened_editors = filter(lambda editor: editor.file.path == file_path, self.editors)
        opened_editor_list = list(opened_editors)
        if opened_editor_list:
            editor = opened_editor_list[0]
            editor_index = self.editors.index(editor)
            # Remove related editor from editors list
            del self.editors[editor_index]
            # Remove tab from this notebook
            tab_id = str(editor.master)
            self.forget(tab_id)

    def find_in_current_editor(self, event=None):
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.find(event)

    def get_current_editor(self):
        '''
        Return current editor if there is one
        Return None otherwise
        '''
        if self.editors:
            current_editor_index = self.index('current')
            current_editor = self.editors[current_editor_index]
            return current_editor
        else:
            return None

    def is_file_open(self, file_path, event=None):
        opened_editors = filter(lambda editor: editor.file.path == file_path, self.editors)
        return list(opened_editors)

    def open_file(self, event=None):
        file_path = tkfiledialog.askopenfilename()
        if file_path:
            self.open_file_by_path(file_path, event)

    def open_file_by_path(self, file_path, event=None):
        file = File(file_path)
        # Add editor to this editor group
        self.add_editor(file)

    def rename_file(self, file_path, new_file_path, event=None):
        opened_editors = filter(lambda editor: editor.file.path == file_path, self.editors)
        opened_editor_list = list(opened_editors)
        if opened_editor_list:
            editor = opened_editor_list[0]
            editor.rename_file(new_file_path, event)

    def save_current_editor(self, event=None):
        # If there is an opened editor, save it
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.save(event)
            # Focus saved editor on
            current_editor.focus_set()
            # Specify that editor is saved, in title and tab_title
            self.set_title(is_there_unsaved_change=False)
            tab_index = str(current_editor.master)
            self.set_tab_title(tab_index, current_editor.title, is_there_unsaved_change=False)

    def save_current_editor_as(self, event=None):
        # If there is an opened editor, save it as...
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.save_as(event)
            # Focus saved editor on
            current_editor.focus_set()
            # Specify that editor's file name was changed and also it was saved, in title
            self.set_title(is_there_unsaved_change=False, file_name=current_editor.file.name)
            # Also update tab title
            tab_index = str(current_editor.master)
            self.set_tab_title(tab_index, current_editor.title, is_there_unsaved_change=False, file_name=current_editor.file.name)

    def save_unsaved_changes(self, event=None):
        '''
        Return True if unsaved changes were saved
        Return False otherwise
        '''
        unsaved_editors = list(filter(lambda editor: editor.is_unsaved, self.editors))
        if unsaved_editors:
            message_box_title = _('Unsaved Changes')
            message_box_description = _('There are unsaved changes, would you like to save them?')
            user_reply = tkmessagebox.askyesnocancel(message_box_title, message_box_description)
            if user_reply:
                # Save unsaved editors
                for unsaved_editor in unsaved_editors:
                    unsaved_editor.save(event)
                return True
            elif user_reply == False:
                return True
            else:
                return False
        else:
            return True

    def set_tab_title(self, tab_index, tab_title, is_there_unsaved_change=None, file_name=None):
        if is_there_unsaved_change is not None:
            tab_title.is_there_unsaved_change = is_there_unsaved_change
        if file_name is not None:
            tab_title.file_name = file_name
        self.tab(tab_index, text=str(tab_title))

    def tab_changed(self, event):
        current_editor = self.get_current_editor()
        if current_editor:
            # Update tab_title
            is_there_unsaved_change = current_editor.is_unsaved
            file_name = current_editor.file.name
            tab_index = str(current_editor.master)
            self.set_tab_title(tab_index, current_editor.title, is_there_unsaved_change=is_there_unsaved_change, file_name=file_name)
        else:
            # If there is no opened editor, it means there is no an unsaved change and file name
            is_there_unsaved_change = False
            file_name = ''
        # Update title
        self.set_title(is_there_unsaved_change=is_there_unsaved_change, file_name=file_name)
