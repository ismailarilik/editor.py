import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox
import os
import tokenize
from view.editor.editor import Editor

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        # Initialize opened file path property
        self.opened_file_path = None
        # Set title
        self.title('<unsaved_file> - Visual Python')
        # Set icon
        self.iconbitmap('icon.ico')
        # Create menu
        self.menu = tk.Menu()
        self.config(menu=self.menu)
        # Create file menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open File', accelerator='Ctrl+O', command=self.open_file)
        self.file_menu.add_command(label='Save File', accelerator='Ctrl+S', command=self.save_file)
        self.file_menu.add_command(label='Save File as...', accelerator='Ctrl+Shift+S', command=self.save_file_as)
        # Create editor
        self.editor = Editor(self)
        self.editor.pack(fill=tk.BOTH, expand=True)
        # Set window size as half of screen size
        # Also center window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        window_x = (screen_width // 2) - (window_width // 2)
        window_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
        # Bind keyboard shortcuts
        # For open file
        self.bind('<Control-KeyPress-o>', self.handle_open_file_event)
        self.bind('<Control-KeyPress-O>', self.handle_open_file_event)
        # For save file
        self.bind('<Control-KeyPress-s>', self.handle_save_file_event)
        self.bind('<Control-KeyPress-S>', self.handle_save_file_event)
        # For save file as
        self.bind('<Control-Shift-KeyPress-s>', self.handle_save_file_as_event)
        self.bind('<Control-Shift-KeyPress-S>', self.handle_save_file_as_event)
        # Register delete window protocol to handle things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.on_quit)
        # Start window
        self.mainloop()

    def handle_open_file_event(self, event):
        self.open_file()

    def handle_save_file_event(self, event):
        self.save_file()

    def handle_save_file_as_event(self, event):
        self.save_file_as()

    def open_file(self):
        if self.on_close_file():
            opened_file_path = tk_filedialog.askopenfilename(filetypes=[('Python Files', '.py')])
            if opened_file_path:
                self.opened_file_path = opened_file_path
                # Set editor text with file content
                with tokenize.open(self.opened_file_path) as file:
                    self.editor.set(file.read())
                # Prefix window title with opened file name
                opened_file_name = os.path.basename(self.opened_file_path)
                self.title(f'{opened_file_name} - Visual Python')
                return True
        return False

    def save_file(self):
        # If a file was not opened before, call save_file_as method
        # Else, write editor text to the file
        if not self.opened_file_path:
            return self.save_file_as()
        with open(self.opened_file_path, 'w', encoding='UTF-8') as file:
            file.write(self.editor.get_wo_eol())
        # Prefix window title with opened file name
        opened_file_name = os.path.basename(self.opened_file_path)
        self.title(f'{opened_file_name} - Visual Python')
        return True

    def save_file_as(self):
        opened_file_path = tk_filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python Files', '.py')])
        if opened_file_path:
            self.opened_file_path = opened_file_path
            with open(self.opened_file_path, 'w', encoding='UTF-8') as file:
                file.write(self.editor.get_wo_eol())
            # Prefix window title with opened file name
            opened_file_name = os.path.basename(self.opened_file_path)
            self.title(f'{opened_file_name} - Visual Python')
            return True
        return False

    def on_close_file(self):
        if self.editor.is_modified:
            reply = tk_messagebox.askyesnocancel('Unsaved Changes', 'There are unsaved changes, would you like to save them?')
            if reply:
                return self.save_file()
            elif reply == False:
                return True
            return False
        return True

    def on_quit(self):
        if self.on_close_file():
            self.destroy()
