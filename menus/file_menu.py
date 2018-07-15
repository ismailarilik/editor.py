import tkinter as tk
import tkinter.filedialog as tk_filedialog

class FileMenu(tk.Menu):
    def __init__(self, master, main_frame):
        super().__init__(master)
        self.main_frame = main_frame
        self.opened_file_path = None
        # Add open file command
        self.add_command(label='Open File', command=self.open_file)

    def open_file(self):
        self.opened_file_path = tk_filedialog.askopenfilename()
        if self.opened_file_path:
            # Set editor text with file content
            with open(self.opened_file_path, encoding='UTF-8') as file:
                self.main_frame.editor_frame.set_text(file.read())
