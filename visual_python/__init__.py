import tkinter as tk
import tkinter.ttk as ttk
import os
from .title import Title
from .explorer import Explorer
from .search.search_frame import SearchFrame
from .editor import Editor
from .find.find_frame import FindFrame
from .file_component import FileComponent
from .edit_component import EditComponent
from .settings_component import SettingsComponent

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_name = 'Editor'
        self.unsaved_changes_specifier = '*'
        self.unsaved_file_name = 'unsaved_file'
        # Set title
        self._title = Title(self.unsaved_changes_specifier, self.unsaved_file_name, self.app_name)
        self.set_title()
        # Set icon
        self.icon_file_name = 'visual_python/icons/python.png'
        self.icon = tk.PhotoImage(file=self.icon_file_name)
        self.iconphoto(True, self.icon)

        # Set menu
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        # Add file menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open File', accelerator='Ctrl+O', command=self.open_file_command)
        self.file_menu.add_command(label='Open Folder', accelerator='Ctrl+Shift+O', command=self.open_folder_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save File', accelerator='Ctrl+S', command=self.save_file_command)
        self.file_menu.add_command(label='Save File as', accelerator='Ctrl+Shift+S', command=self.save_file_as_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', accelerator='Ctrl+Q', command=self.quit_command)
        # Add edit menu
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Edit', menu=self.edit_menu)
        self.edit_menu.add_command(label='Find', accelerator='Ctrl+F', command=self.find_command)

        # Create keyboard bindings
        self.bind('<Control-o>', self.open_file_command)
        self.bind('<Control-O>', self.open_file_command)
        self.bind('<Control-Shift-o>', self.open_folder_command)
        self.bind('<Control-Shift-O>', self.open_folder_command)
        self.bind('<Control-s>', self.save_file_command)
        self.bind('<Control-S>', self.save_file_command)
        self.bind('<Control-Shift-s>', self.save_file_as_command)
        self.bind('<Control-Shift-S>', self.save_file_as_command)
        self.bind('<Control-q>', self.quit_command)
        self.bind('<Control-Q>', self.quit_command)
        self.bind('<Control-f>', self.find_command)
        self.bind('<Control-F>', self.find_command)

        # Create components
        self.file_component = FileComponent(self.__open_file_callback, self.__open_folder_callback, self.__save_file_callback, self.__save_file_as_callback)
        self.edit_component = EditComponent(self.__find_callback)
        self.settings_component = SettingsComponent()

        # Create main frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create paned window
        paned_window = tk.PanedWindow(main_frame)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Create explorer notebook and add it to paned window
        self.explorer_notebook = ttk.Notebook(paned_window)
        paned_window.add(self.explorer_notebook)
        # Create explorer frame and add it to explorer notebook
        explorer_frame = tk.Frame(self.explorer_notebook)
        self.explorer_notebook.add(explorer_frame, text='Explorer')
        # Create explorer inside explorer frame
        self.explorer = Explorer(explorer_frame, self, self.file_component, self.open_file_in_editor, self.close_file_in_editor)
        self.explorer.pack(fill=tk.BOTH, expand=True)
        # Create search frame and add it to explorer notebook
        search_settings = self.settings_component.settings['search']
        self.search_frame = SearchFrame(self.explorer_notebook, search_settings, self.file_component.folder)
        self.explorer_notebook.add(self.search_frame, text='Search')
        # Create version control frame and add it to explorer notebook
        version_control_frame = tk.Frame(self.explorer_notebook)
        self.explorer_notebook.add(version_control_frame, text='Version Control')
        # Create debug frame and add it to explorer notebook
        debug_frame = tk.Frame(self.explorer_notebook)
        self.explorer_notebook.add(debug_frame, text='Debug')
        # Create extensions frame and add it to explorer notebook
        extensions_frame = tk.Frame(self.explorer_notebook)
        self.explorer_notebook.add(extensions_frame, text='Extensions')

        # Create editor frame and add it to paned window
        editor_frame = tk.Frame(paned_window)
        paned_window.add(editor_frame)
        # Create editor inside editor frame
        self.editor = Editor(editor_frame, self.file_component, self.edit_component, self.set_title, self.close_find_frame)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # Create find frame inside this frame
        self.find_frame = FindFrame(self, self.editor)
        # Resize and center the window
        self._resize_and_center()
        # Register delete window protocol to save unsaved changes and handle other things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.quit_command)

    def close_find_frame(self, event=None):
        self.find_frame.close(event)

    def __open_file_callback(self, file_path):
        return self.editor.open_file_in_editor(file_path)

    def __open_folder_callback(self, folder):
        # Refill explorer with folders and files in `folder_path`
        self.explorer.delete(*self.explorer.get_children())
        def on_error(error):
            raise error
        for path, folders, files in os.walk(folder.path, onerror=on_error):
            parent = '' if path == folder.path else path
            for folder_name in folders:
                self.explorer.insert(parent, tk.END, os.path.join(path, folder_name), text=folder_name, image=self.explorer.explorer_folder_image)
            for file in files:
                extension = os.path.splitext(file)[1]
                image = self.explorer.explorer_python_file_image if extension == '.py' or extension == '.pyw' else self.explorer.explorer_file_image
                self.explorer.insert(parent, tk.END, os.path.join(path, file), text=file, image=image)
        # Set title's folder part
        self.set_title(folder_name=folder.name)

    def __save_file_callback(self, file):
        with open(file.path, 'w', encoding='UTF-8') as opened_file:
            opened_file.write(self.editor.get_wo_eol())
        # Focus editor in
        self.editor.focus_set()
        # File is unmodified now
        file.is_modified = False
        # Reset title because unsaved changes status has been changed to False
        self.set_title(is_there_unsaved_change=file.is_modified)
        # Return that the file was saved
        return True

    def __save_file_as_callback(self, file):
        with open(file.path, 'w', encoding='UTF-8') as file_object:
            file_object.write(self.editor.get_wo_eol())
        # Focus editor in
        self.editor.focus_set()
        # Reset title because file name has been changed
        # Also unsaved changes status has been changed to False
        self.set_title(is_there_unsaved_change=file.is_modified, is_file_unsaved=False, file_name=file.name)
        # Return that the specified file was saved
        return True

    def __find_callback(self, event=None):
        self.find_frame.place(relx=1, anchor=tk.NE)
        self.find_frame.find_entry.focus_set()
        self.find_frame.find_entry.select_range(0, tk.END)

    def open_file_in_editor(self, file):
        self.editor.open_file_in_editor(file)

    def close_file_in_editor(self):
        self.editor.close_file_in_editor()

    def set_title(self, is_there_unsaved_change=None, is_file_unsaved=None, file_name=None, folder_name=None):
        if is_there_unsaved_change is not None:
            self._title.is_there_unsaved_change = is_there_unsaved_change
        if is_file_unsaved is not None:
            self._title.is_file_unsaved = is_file_unsaved
        if file_name is not None:
            self._title.file_name = file_name
        if folder_name is not None:
            self._title.folder_name = folder_name
        self.title(str(self._title))

    def open_file_command(self, event=None):
        self.file_component.open_file()

    def open_folder_command(self, event=None):
        self.file_component.open_folder()

    def save_file_command(self, event=None):
        self.file_component.save_file()

    def save_file_as_command(self, event=None):
        self.file_component.save_file_as()

    def quit_command(self, event=None):
        if self.file_component.save_unsaved_changes():
            self.destroy()

    def find_command(self, event=None):
        self.edit_component.find()

    def _resize_and_center(self):
        '''
        Set window size as half of screen size
        Also center window
        '''
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        window_x = (screen_width // 2) - (window_width // 2)
        window_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
