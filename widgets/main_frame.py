import tkinter as tk
from .editor_frame import EditorFrame

class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # Add editor frame
        self.editor_frame = EditorFrame(self)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)
