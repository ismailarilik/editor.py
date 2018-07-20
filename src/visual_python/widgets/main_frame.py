import tkinter as tk
from .editor.editor_frame import EditorFrame

class MainFrame(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        # Add editor frame
        self.editor_frame = EditorFrame(self, app)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)
