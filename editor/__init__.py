import tkinter as tk
import tkinter.ttk as ttk
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
        self.icon_file_name = 'python.png'
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
        self.view_menu.add_command(label='Search', accelerator='Ctrl+Shift+F', command=self.search_command)
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

        # Create components
        self.file_component = FileComponent()
        self.edit_component = EditComponent()
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
        self.explorer_notebook.add(explorer_frame, text='Files')
        # Create explorer inside explorer frame
        self.explorer = Explorer(explorer_frame, self)
        self.explorer.pack(fill=tk.BOTH, expand=True)
        # Create search frame and add it to explorer notebook
        search_settings = self.settings_component.settings['search']
        self.search_frame = SearchFrame(self.explorer_notebook, search_settings, self.file_component.folder)
        self.explorer_notebook.add(self.search_frame, text='Search')

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
        # Add keyboard bindings
        self._add_keyboard_bindings()
        # Register delete window protocol to save unsaved changes and handle other things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.quit_command)

    def _post_init(self):
        self.file_component.post_init(self.explorer, self.editor, self.set_title)
        self.edit_component.post_init(self.find_frame)
        self.explorer.post_init(self.file_component, self.editor.open_file_in_editor, self.editor.close_file_in_editor)
        self.editor.post_init(self.file_component, self.edit_component, self.set_title, self.find_frame.close)
        self.find_frame.post_init(self.editor)

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

    def new_file_command(self):
        pass

    def new_folder_command(self):
        pass

    def open_file_command(self):
        self.file_component.open_file()

    def open_folder_command(self):
        self.file_component.open_folder()

    def save_file_command(self):
        self.file_component.save_file()

    def save_file_as_command(self):
        self.file_component.save_file_as()

    def save_all_command(self):
        pass

    def settings_command(self):
        pass

    def close_editor_command(self):
        pass

    def close_folder_command(self):
        pass

    def quit_command(self, event=None):
        if self.file_component.save_unsaved_changes():
            self.destroy()

    def undo_command(self):
        pass

    def redo_command(self):
        pass

    def select_all_command(self):
        pass

    def cut_command(self):
        pass

    def copy_command(self):
        pass

    def paste_command(self):
        pass

    def find_command(self):
        self.edit_component.find()

    def replace_command(self):
        pass

    def find_in_files_command(self):
        pass

    def replace_in_files_command(self):
        pass

    def explorer_command(self):
        pass

    def search_command(self):
        pass

    def version_control_command(self):
        pass

    def debug_command(self):
        pass

    def extensions_command(self):
        pass

    def problems_command(self):
        pass

    def output_command(self):
        pass

    def debug_console_command(self):
        pass

    def terminal_command(self):
        pass

    def next_editor_command(self):
        pass

    def previous_editor_command(self):
        pass

    def go_to_file_command(self):
        pass

    def go_to_declaration_command(self):
        pass

    def go_to_line_column_command(self):
        pass

    def start_debugging_command(self):
        pass

    def start_without_debugging_command(self):
        pass

    def stop_debugging_command(self):
        pass

    def restart_debugging_command(self):
        pass

    def step_over_command(self):
        pass

    def step_into_command(self):
        pass

    def step_out_command(self):
        pass

    def continue_command(self):
        pass

    def toggle_breakpoint_command(self):
        pass

    def enable_all_breakpoints_command(self):
        pass

    def disable_all_breakpoints_command(self):
        pass

    def remove_all_breakpoints_command(self):
        pass

    def report_issue_command(self):
        pass

    def view_license_command(self):
        pass

    def check_for_updates_command(self):
        pass

    def about_command(self):
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

    def _add_keyboard_bindings(self):
        # Add keyboard bindings for opening file
        self.bind('<Control-KeyPress-o>', self.file_component.open_file)
        self.bind('<Control-KeyPress-O>', self.file_component.open_file)
        # Add keyboard bindings for opening folder
        self.bind('<Control-KeyPress-d>', self.file_component.open_folder)
        self.bind('<Control-KeyPress-D>', self.file_component.open_folder)
        # Add keyboard bindings for saving file
        self.bind('<Control-KeyPress-s>', self.file_component.save_file)
        self.bind('<Control-KeyPress-S>', self.file_component.save_file)
        # Add keyboard bindings for saving file as...
        self.bind('<Control-Shift-KeyPress-s>', self.file_component.save_file_as)
        self.bind('<Control-Shift-KeyPress-S>', self.file_component.save_file_as)
        # Add keyboard bindings for quitting
        self.bind('<Control-KeyPress-q>', self.quit_command)
        self.bind('<Control-KeyPress-Q>', self.quit_command)
