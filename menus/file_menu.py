import tkinter as tk
import tkinter.filedialog as tk_filedialog

class FileMenu(tk.Menu):
    def __init__(self, master, main_frame):
        super().__init__(master)
        self.main_frame = main_frame
        self.opened_file_path = None
        # Add open file command
        self.add_command(label='Open File', command=self.open_file)
        # Add save file command
        self.add_command(label='Save File', command=self.save_file)

    def open_file(self):
        self.opened_file_path = tk_filedialog.askopenfilename()
        if self.opened_file_path:
            # Set editor text with file content
            with open(self.opened_file_path, encoding='UTF-8') as file:
                self.main_frame.editor_frame.set_text(file.read())

    def save_file(self):
        # If a file is not opened before, open save as dialog
        # Else, save editor text to it
        if not self.opened_file_path:
            self.opened_file_path = tk_filedialog.asksaveasfilename()
        if self.opened_file_path:
            # TODO UTF-8
            with open(self.opened_file_path, 'w', encoding='UTF-8') as file:
                file.write(self.main_frame.editor_frame.get_text())
