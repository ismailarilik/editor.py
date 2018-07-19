import tkinter as tk
from .text_widget import TextWidget

class EditorFrame(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        # Add text widget
        self.text_widget = TextWidget(self, self.app)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
