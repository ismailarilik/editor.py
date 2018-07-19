import tkinter as tk
from .editor.editor_frame import EditorFrame

class MainFrame(tk.Frame):
    def __init__(self, master, prefix_current_title, remove_title_prefix):
        super().__init__(master)
        self.prefix_current_title = prefix_current_title
        self.remove_title_prefix = remove_title_prefix
        # Add editor frame
        self.editor_frame = EditorFrame(self, self.prefix_current_title, self.remove_title_prefix)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)
