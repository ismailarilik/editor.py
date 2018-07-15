import tkinter as tk
import tkinter.filedialog as tk_filedialog

class FileMenu(tk.Menu):
    def __init__(self, master, main_frame):
        super().__init__(master)
        self.main_frame = main_frame
        # Add open file command
        self.add_command(label='Open File', command=self.open_file)

    def open_file(self):
        file_name = tk_filedialog.askopenfilename()
        if file_name:
            # Set editor text with file content
            with open(file_name, encoding='UTF-8') as file:
                self.main_frame.editor_frame.set_text(file.read())
