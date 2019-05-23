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
        self.file_menu.add_command(label='New File', accelerator='Ctrl+N', command=self.new_file_command)
        self.file_menu.add_command(label='New Folder', accelerator='Ctrl+Shift+N', command=self.new_folder_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Open File', accelerator='Ctrl+O', command=self.open_file_command)
        self.file_menu.add_command(label='Open Folder', accelerator='Ctrl+Shift+O', command=self.open_folder_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save File', accelerator='Ctrl+S', command=self.save_file_command)
        self.file_menu.add_command(label='Save File as', accelerator='Ctrl+Shift+S', command=self.save_file_as_command)
        self.file_menu.add_command(label='Save All', accelerator='Ctrl+Alt+S', command=self.save_all_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Settings', accelerator='Ctrl+,', command=self.settings_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Close Editor', accelerator='Ctrl+F4', command=self.close_editor_command)
        self.file_menu.add_command(label='Close Folder', accelerator='Ctrl+Shift+F4', command=self.close_folder_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', accelerator='Ctrl+Q', command=self.quit_command)
        # Add edit menu
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Edit', menu=self.edit_menu)
        self.edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', command=self.undo_command)
        self.edit_menu.add_command(label='Redo', accelerator='Ctrl+Shift+Z', command=self.redo_command)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Select All', accelerator='Ctrl+A', command=self.select_all_command)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Cut', accelerator='Ctrl+X', command=self.cut_command)
        self.edit_menu.add_command(label='Copy', accelerator='Ctrl+C', command=self.copy_command)
        self.edit_menu.add_command(label='Paste', accelerator='Ctrl+V', command=self.paste_command)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Find', accelerator='Ctrl+F', command=self.find_command)
        self.edit_menu.add_command(label='Replace', accelerator='Ctrl+R', command=self.replace_command)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Find in Files', accelerator='Ctrl+Shift+F',
            command=self.find_in_files_command)
        self.edit_menu.add_command(label='Replace in Files', accelerator='Ctrl+Shift+R',
            command=self.replace_in_files_command)
        # Add view menu
        self.view_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='View', menu=self.view_menu)
        self.view_menu.add_command(label='Explorer', accelerator='Ctrl+Shift+E', command=self.explorer_command)
        self.view_menu.add_command(label='Search', accelerator='Ctrl+Shift+F', command=self.find_in_files_command)
        self.view_menu.add_command(label='Version Control', accelerator='Ctrl+Shift+V',
            command=self.version_control_command)
        self.view_menu.add_command(label='Debug', accelerator='Ctrl+Shift+D', command=self.debug_command)
        self.view_menu.add_command(label='Extensions', accelerator='Ctrl+Shift+X', command=self.extensions_command)
        self.view_menu.add_separator()
        self.view_menu.add_command(label='Problems', accelerator='Ctrl+Shift+P', command=self.problems_command)
        self.view_menu.add_command(label='Output', accelerator='Ctrl+Shift+U', command=self.output_command)
        self.view_menu.add_command(label='Debug Console', accelerator='Ctrl+Shift+C',
            command=self.debug_console_command)
        self.view_menu.add_command(label='Terminal', accelerator='Ctrl+Shift+T', command=self.terminal_command)
        # Add go menu
        self.go_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Go', menu=self.go_menu)
        self.go_menu.add_command(label='Next Editor', accelerator='Ctrl+PageDown', command=self.next_editor_command)
        self.go_menu.add_command(label='Previous Editor', accelerator='Ctrl+PageUp',
            command=self.previous_editor_command)
        self.go_menu.add_separator()
        self.go_menu.add_command(label='Go to File', accelerator='Ctrl+P', command=self.go_to_file_command)
        self.go_menu.add_separator()
        self.go_menu.add_command(label='Go to Declaration', accelerator='Ctrl+D',
            command=self.go_to_declaration_command)
        self.go_menu.add_separator()
        self.go_menu.add_command(label='Go to Line/Column', accelerator='Ctrl+G',
            command=self.go_to_line_column_command)
        # Add debug menu
        self.debug_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Debug', menu=self.debug_menu)
        self.debug_menu.add_command(label='Start Debugging', accelerator='F5', command=self.start_debugging_command)
        self.debug_menu.add_command(label='Start without Debugging', accelerator='Ctrl+F5',
            command=self.start_without_debugging_command)
        self.debug_menu.add_command(label='Stop Debugging', accelerator='Shift+F5', command=self.stop_debugging_command)
        self.debug_menu.add_command(label='Restart Debugging', accelerator='Ctrl+Shift+F5',
            command=self.restart_debugging_command)
        self.debug_menu.add_separator()
        self.debug_menu.add_command(label='Step Over', accelerator='F10', command=self.step_over_command)
        self.debug_menu.add_command(label='Step Into', accelerator='F11', command=self.step_into_command)
        self.debug_menu.add_command(label='Step Out', accelerator='Shift+F11', command=self.step_out_command)
        self.debug_menu.add_command(label='Continue', accelerator='F5', command=self.continue_command)
        self.debug_menu.add_separator()
        self.debug_menu.add_command(label='Toggle Breakpoint', accelerator='F9', command=self.toggle_breakpoint_command)
        self.debug_menu.add_separator()
        self.debug_menu.add_command(label='Enable All Breakpoints', command=self.enable_all_breakpoints_command)
        self.debug_menu.add_command(label='Disable All Breakpoints', command=self.disable_all_breakpoints_command)
        self.debug_menu.add_command(label='Remove All Breakpoints', command=self.remove_all_breakpoints_command)
        # Add help menu
        self.help_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label='Report Issue', command=self.report_issue_command)
        self.help_menu.add_separator()
        self.help_menu.add_command(label='View License', command=self.view_license_command)
        self.help_menu.add_separator()
        self.help_menu.add_command(label='Check for Updates', command=self.check_for_updates_command)
        self.help_menu.add_separator()
        self.help_menu.add_command(label='About', command=self.about_command)

        # Create keyboard bindings
        self.bind('<Control-n>', self.new_file_command)
        self.bind('<Control-N>', self.new_file_command)
        self.bind('<Control-Shift-n>', self.new_folder_command)
        self.bind('<Control-Shift-N>', self.new_folder_command)
        self.bind('<Control-o>', self.open_file_command)
        self.bind('<Control-O>', self.open_file_command)
        self.bind('<Control-Shift-o>', self.open_folder_command)
        self.bind('<Control-Shift-O>', self.open_folder_command)
        self.bind('<Control-s>', self.save_file_command)
        self.bind('<Control-S>', self.save_file_command)
        self.bind('<Control-Shift-s>', self.save_file_as_command)
        self.bind('<Control-Shift-S>', self.save_file_as_command)
        self.bind('<Control-Alt_L><s>', self.save_all_command)
        self.bind('<Control-,>', self.settings_command)
        self.bind('<Control-F4>', self.close_editor_command)
        self.bind('<Control-Shift-F4>', self.close_folder_command)
        self.bind('<Control-q>', self.quit_command)
        self.bind('<Control-Q>', self.quit_command)
        self.bind('<Control-z>', self.undo_command)
        self.bind('<Control-Z>', self.undo_command)
        self.bind('<Control-Shift-z>', self.redo_command)
        self.bind('<Control-Shift-Z>', self.redo_command)
        self.bind('<Control-a>', self.select_all_command)
        self.bind('<Control-A>', self.select_all_command)
        self.bind('<Control-x>', self.cut_command)
        self.bind('<Control-X>', self.cut_command)
        self.bind('<Control-c>', self.copy_command)
        self.bind('<Control-C>', self.copy_command)
        self.bind('<Control-v>', self.paste_command)
        self.bind('<Control-V>', self.paste_command)
        self.bind('<Control-f>', self.find_command)
        self.bind('<Control-F>', self.find_command)
        self.bind('<Control-r>', self.replace_command)
        self.bind('<Control-R>', self.replace_command)
        self.bind('<Control-Shift-f>', self.find_in_files_command)
        self.bind('<Control-Shift-F>', self.find_in_files_command)
        self.bind('<Control-Shift-r>', self.replace_in_files_command)
        self.bind('<Control-Shift-R>', self.replace_in_files_command)
        self.bind('<Control-Shift-e>', self.explorer_command)
        self.bind('<Control-Shift-E>', self.explorer_command)
        self.bind('<Control-Shift-f>', self.find_in_files_command)
        self.bind('<Control-Shift-F>', self.find_in_files_command)
        self.bind('<Control-Shift-v>', self.version_control_command)
        self.bind('<Control-Shift-V>', self.version_control_command)
        self.bind('<Control-Shift-d>', self.debug_command)
        self.bind('<Control-Shift-D>', self.debug_command)
        self.bind('<Control-Shift-x>', self.extensions_command)
        self.bind('<Control-Shift-X>', self.extensions_command)
        self.bind('<Control-Shift-p>', self.problems_command)
        self.bind('<Control-Shift-P>', self.problems_command)
        self.bind('<Control-Shift-u>', self.output_command)
        self.bind('<Control-Shift-U>', self.output_command)
        self.bind('<Control-Shift-c>', self.debug_console_command)
        self.bind('<Control-Shift-C>', self.debug_console_command)
        self.bind('<Control-Shift-t>', self.terminal_command)
        self.bind('<Control-Shift-T>', self.terminal_command)
        self.bind('<Control-Next>', self.next_editor_command)
        self.bind('<Control-Prior>', self.previous_editor_command)
        self.bind('<Control-p>', self.go_to_file_command)
        self.bind('<Control-P>', self.go_to_file_command)
        self.bind('<Control-d>', self.go_to_declaration_command)
        self.bind('<Control-D>', self.go_to_declaration_command)
        self.bind('<Control-g>', self.go_to_line_column_command)
        self.bind('<Control-G>', self.go_to_line_column_command)
        self.bind('<F5>', self.start_debugging_command)
        self.bind('<Control-F5>', self.start_without_debugging_command)
        self.bind('<Shift-F5>', self.stop_debugging_command)
        self.bind('<Control-Shift-F5>', self.restart_debugging_command)
        self.bind('<F10>', self.step_over_command)
        self.bind('<F11>', self.step_into_command)
        self.bind('<Shift-F11>', self.step_out_command)
        self.bind('<F5>', self.continue_command)
        self.bind('<F9>', self.toggle_breakpoint_command)

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
        self.explorer = Explorer(explorer_frame, self)
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
        self.editor = Editor(editor_frame)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # Create find frame inside this frame
        self.find_frame = FindFrame(self)
        # Post initialization
        self._post_init()
        # Resize and center the window
        self._resize_and_center()
        # Register delete window protocol to save unsaved changes and handle other things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.quit_command)

    def _post_init(self):
        self.explorer.post_init(self.file_component, self.editor.open_file_in_editor, self.editor.close_file_in_editor)
        self.editor.post_init(self.file_component, self.edit_component, self.set_title, self.find_frame.close)
        self.find_frame.post_init(self.editor)

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

    def new_file_command(self, event=None):
        pass

    def new_folder_command(self, event=None):
        pass

    def open_file_command(self, event=None):
        self.file_component.open_file()

    def open_folder_command(self, event=None):
        self.file_component.open_folder()

    def save_file_command(self, event=None):
        self.file_component.save_file()

    def save_file_as_command(self, event=None):
        self.file_component.save_file_as()

    def save_all_command(self, event=None):
        pass

    def settings_command(self, event=None):
        pass

    def close_editor_command(self, event=None):
        pass

    def close_folder_command(self, event=None):
        pass

    def quit_command(self, event=None):
        if self.file_component.save_unsaved_changes():
            self.destroy()

    def undo_command(self, event=None):
        pass

    def redo_command(self, event=None):
        pass

    def select_all_command(self, event=None):
        pass

    def cut_command(self, event=None):
        pass

    def copy_command(self, event=None):
        pass

    def paste_command(self, event=None):
        pass

    def find_command(self, event=None):
        self.edit_component.find()

    def replace_command(self, event=None):
        pass

    def find_in_files_command(self, event=None):
        pass

    def replace_in_files_command(self, event=None):
        pass

    def explorer_command(self, event=None):
        pass

    def version_control_command(self, event=None):
        pass

    def debug_command(self, event=None):
        pass

    def extensions_command(self, event=None):
        pass

    def problems_command(self, event=None):
        pass

    def output_command(self, event=None):
        pass

    def debug_console_command(self, event=None):
        pass

    def terminal_command(self, event=None):
        pass

    def next_editor_command(self, event=None):
        pass

    def previous_editor_command(self, event=None):
        pass

    def go_to_file_command(self, event=None):
        pass

    def go_to_declaration_command(self, event=None):
        pass

    def go_to_line_column_command(self, event=None):
        pass

    def start_debugging_command(self, event=None):
        pass

    def start_without_debugging_command(self, event=None):
        pass

    def stop_debugging_command(self, event=None):
        pass

    def restart_debugging_command(self, event=None):
        pass

    def step_over_command(self, event=None):
        pass

    def step_into_command(self, event=None):
        pass

    def step_out_command(self, event=None):
        pass

    def continue_command(self, event=None):
        pass

    def toggle_breakpoint_command(self, event=None):
        pass

    def enable_all_breakpoints_command(self, event=None):
        pass

    def disable_all_breakpoints_command(self, event=None):
        pass

    def remove_all_breakpoints_command(self, event=None):
        pass

    def report_issue_command(self, event=None):
        pass

    def view_license_command(self, event=None):
        pass

    def check_for_updates_command(self, event=None):
        pass

    def about_command(self, event=None):
        pass

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
